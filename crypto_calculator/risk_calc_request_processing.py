import json
from typing import List, Dict, Set, Tuple
from crypto_calculator.models import (
    CoreSpecificRisk,
    Exposures,
    FactorReturns,
    RawPriceData,
    Returns,
    SpecificReturns,
)
import pandas as pd
import numpy as np
from factor_model.risk_calculations import HALF_LIFE_DEFAULT, MIN_OBS_DEFAULT
from factor_model.risk_calculations.core_universe_portfolio import (
    generate_market_portfolio,
)
from factor_model.risk_calculations.excess_return_manipulation import (
    generate_processed_excess_returns,
)
from factor_model.risk_calculations.factor_covariance import (
    generate_factor_covariance_matrix,
)
from factor_model.risk_calculations.parameter_processing import (
    check_input_param_correctness,
    parse_file_input_into_portfolio,
)
from factor_model.risk_calculations.portfolio_output import assemble_portfolios_into_df, parse_portfolio_input
from factor_model.risk_calculations.risk_attribution import (
    generate_active_space_portfolio,
    generate_mctr_chart_input,
    generate_mctr_chart_input_reduced,
)
from factor_model.risk_calculations.risk_attribution import (
    calculate_spec_risk_mctr,
    create_portfolio_exposures,
    generate_factor_covariance_attribution,
    generate_factor_covariance_table,
    get_specific_risk_beta,
)
from factor_model.risk_calculations.risk_metrics import calculate_lognormal_es_var
from factor_model.risk_calculations.specific_risk import (
    closest_halflife_element,
    generate_combined_spec_risk,
    generate_raw_portfolio_specific_risk,
    generate_raw_specific_risk,
)
from factor_model.model_update.database_generators import (
    EXPOSURE_NON_STYLE_FIELDS,
    FIX_SET_OF_HALF_LIFES,
)
import logging

logger = logging.getLogger("risk calc")

FRONTEND_TO_BACKEND = {
    "correlation_hl": "correlation_half_life",
    "factor_risk_hl": "variance_half_life",
    "specific_risk_hl": "specific_risk_half_life",
    "min_ret_hist": "minimum_history_spec_ret",
    "cob_date": "date",
}


def get_available_estimation_dates() -> List[str]:
    dates = FactorReturns.objects.using("factor_model_estimates").values("date")
    df = pd.DataFrame(list(dates))
    return [str(date_value) for date_value in set(df["date"])]


def get_coverage_for_date(cob_date: str) -> Set[str]:
    symbols = (
        RawPriceData.objects.using("default").filter(date=cob_date).values("symbol")
    )
    df = pd.DataFrame(list(symbols))
    return set(df["symbol"])


def get_core_avg_spec_risk(cob_date: str, halflife: int) -> pd.DataFrame:
    closest_hls = closest_halflife_element(FIX_SET_OF_HALF_LIFES, halflife)
    spec_risks = (
        CoreSpecificRisk.objects.using("specific_risk_estimates")
        .filter(date=cob_date)
        .filter(half_life__in=closest_hls)
        .values("date", "half_life", "specific_risk")
    )
    df = pd.DataFrame(list(spec_risks))
    return df


def check_missing_coverage(
    symbols: Set[str],
    processed_input: Dict[str, Dict[str, float]],
    portfolio_name: str,
    log_elements: List[str],
) -> int:
    """Enriches log elements with the name of missing coins
    and redefines input portfolios with respect to coverage

    Args:
        symbols (Set[str]): set of available symbols
        processed_input (Dict[str, Dict[str, float]]): processed input containing input portfolios
        portfolio_name (str): name of the portfolio (the portfolio or the market)
        log_elements (List[str]): log elements

    Returns:
        int: 0 if coverage is not missing, 1 if there is a caveat in coverage
    """
    missing_coverage = sorted(list(set(processed_input[portfolio_name]) - symbols))
    if len(missing_coverage) > 0:
        log_elements.append(
            f"No coverage for {portfolio_name} input: {str(missing_coverage)}. "
        )
        # redefine portfolio with respect to missing symbols
        for symbol in missing_coverage:
            del processed_input[portfolio_name][symbol]
        total_weight = sum(processed_input[portfolio_name].values())
        processed_input[portfolio_name] = {
            key: value / total_weight
            for (key, value) in processed_input[portfolio_name].items()
        }
        return 1
    return 0


def query_factor_return_data(cob_date: str) -> pd.DataFrame:
    """
    Queries factor return data from a database for the specified close of business date.

    Args:
        cob_date (str): The close of business date in the format "YYYY-MM-DD".

    Returns:
        pd.DataFrame: A DataFrame with factor return data.
    """
    factor_return_data = (
        FactorReturns.objects.using("factor_model_estimates")
        .filter(date__lte=cob_date)  # date less than equal to cob_date input...
        .values()
    )
    df = pd.DataFrame(list(factor_return_data))
    df["date"] = df["date"].apply(lambda x: x.strftime("%Y-%m-%d"))
    return df


def query_fillmiss_returns(cob_date: str) -> pd.DataFrame:
    """
    Queries market factor return from a database for the specified close of business date.
    This will be used for fill miss purposes

    Args:
        cob_date (str): The close of business date in the format "YYYY-MM-DD".

    Returns:
        pd.DataFrame: A DataFrame with factor return data.
    """
    factor_return_data = (
        FactorReturns.objects.using("factor_model_estimates")
        .filter(date__lte=cob_date)  # date less than equal to cob_date input...
        .values("date", "market")
    )
    fill_miss_returns = pd.DataFrame(list(factor_return_data))
    fill_miss_returns["date"] = fill_miss_returns["date"].apply(
        lambda x: x.strftime("%Y-%m-%d")
    )
    fill_miss_returns.drop_duplicates(inplace=True)
    return fill_miss_returns.rename(columns={"market": "proxy_return"})


def query_exposures(cob_date: str) -> pd.DataFrame:
    """
    Queries exposures data from a database for the specified close of business date.

    Args:
        cob_date (str): The close of business date in the format "YYYY-MM-DD".

    Returns:
        pd.DataFrame: A DataFrame with exposures data.
    """
    exposures = (
        Exposures.objects.using("factor_model_estimates").filter(date=cob_date).values()
    )
    return pd.DataFrame(list(exposures))


def query_exposures_for_market_portfolio_data(cob_date: str) -> pd.DataFrame:
    """
    Queries exposures data for market portfolio data from a database for the specified close of business date.

    Args:
        cob_date (str): The close of business date in the format "YYYY-MM-DD".

    Returns:
        pd.DataFrame: A DataFrame with ticker and transformed market cap data.
    """
    exposures = (
        Exposures.objects.using("factor_model_estimates")
        .filter(date=cob_date)
        .values("ticker", "transformed_market_cap")
    )
    return pd.DataFrame(list(exposures))


def query_specific_returns(cob_date: str, symbols: List[str]) -> pd.DataFrame:
    """Executes a query to get specific returns for a set of symbols

    Args:
        cob_date (str): date in yyyy-mm-dd format
        symbols (List[str]): symbols to be queried

    Returns:
        pd.DataFrame: df containing the specific returns
    """
    specific_returns = (
        SpecificReturns.objects.using("factor_model_estimates")
        .filter(date__lte=cob_date)
        .filter(ticker__in=symbols)
        .values()
    )
    df = pd.DataFrame(list(specific_returns))
    return df


def query_excess_returns(cob_date: str, symbols: List[str]) -> pd.DataFrame:
    """Executes a query to get excess returns for a set of symbols

    Args:
        cob_date (str): date in yyyy-mm-dd format
        symbols (List[str]): symbols to be queried

    Returns:
        pd.DataFrame: df containing the specific returns
    """
    excess_returns = (
        Returns.objects.using("returns")
        .filter(date__lte=cob_date)
        .filter(symbol__in=symbols)
        .values("date", "return_field", "symbol")
    )
    df = pd.DataFrame(list(excess_returns))

    return df.rename(columns={"return_field": "excess_return"})


def risk_calc_request_full(
    portfolio_details: Dict[str, float],
    market_portfolio: Dict[str, float],
    risk_calculation_parameters: Dict,
):
    # Step 1: cob_date and basic queries
    cob_date = risk_calculation_parameters["date"]
    exposures = query_exposures(cob_date=cob_date)
    if market_portfolio is None:
        market_portfolio = generate_market_portfolio(exposures)

    all_tickers = list(
        set(market_portfolio.keys()).union(set(portfolio_details.keys()))
    )
    full_specific_returns = query_specific_returns(
        cob_date=cob_date, symbols=all_tickers
    )
    factor_returns = query_factor_return_data(cob_date=cob_date)

    # Step 2: calculate risk
    factor_covariance = generate_factor_covariance_matrix(
        factor_returns, risk_calculation_parameters
    )
    active_space_port = generate_active_space_portfolio(
        portfolio_details, market_portfolio
    )

    portfolios = {
        "portfolio": portfolio_details,
        "market": market_portfolio,
        "active": active_space_port,
    }

    port_exposures = {}
    factor_risks = {}
    factor_attributions = {}
    factor_covars = {}
    raw_specific_risks = {}
    spec_risk_availabilities = {}
    spec_risks = {}
    total_risks = {}
    factor_mctrs = {}
    spec_risk_attributions = {}
    spec_risk_var_decomps = {}
    spec_risk_mctrs = {}
    combined_spec_risk = {}
    for port in portfolios.keys():
        # 2.1. exposure calc
        port_exposures[port] = create_portfolio_exposures(
            exposures=exposures,
            portfolio_details=portfolios[port],
            non_style_fields=EXPOSURE_NON_STYLE_FIELDS,
            is_total_space=True if port != "active" else False,
        )
        port_exposures[port] = port_exposures[port].reindex(factor_covariance.index)
        # 2.2. factor risk related
        (
            factor_risks[port],
            factor_attributions[port],
        ) = generate_factor_covariance_attribution(
            port_exposures[port], factor_covariance
        )
        factor_covars[port] = generate_factor_covariance_table(
            port_exposures[port], factor_covariance
        )
        # 2.3. spec risk related
        (
            raw_specific_risks[port],
            spec_risk_availabilities[port],
        ) = generate_raw_specific_risk(
            full_specific_returns, risk_calculation_parameters, portfolios[port]
        )

        core_spec_risk_df = get_core_avg_spec_risk(
            cob_date, risk_calculation_parameters["specific_risk_half_life"]
        )
        combined_spec_risk[port] = generate_combined_spec_risk(
            core_spec_risk_df,
            risk_calculation_parameters,
            raw_specific_risks[port],
            spec_risk_availabilities[port],
        )
        spec_risks[port] = generate_raw_portfolio_specific_risk(
            combined_spec_risk[port],
            portfolios[port],
            is_total_space=True if port != "active" else False,
        )

        # 2.4 other risk calcs
        total_risks[port] = np.sqrt(factor_risks[port] ** 2 + spec_risks[port] ** 2)
        factor_mctrs[port] = factor_attributions[port] / total_risks[port]
        spec_risk_attributions[port], spec_risk_var_decomps[port] = (
            calculate_spec_risk_mctr(
                combined_spec_risk[port],
                portfolios[port],
                True if port != "active" else False,
            )
        )
        spec_risk_mctrs[port] = spec_risk_attributions[port] / total_risks[port]

    # 3. beta calculation...
    factor_beta_covar, _ = generate_factor_covariance_attribution(
        port_exposures["portfolio"], factor_covariance, port_exposures["market"]
    )
    spec_risk_covar = get_specific_risk_beta(
        portfolios["portfolio"],
        market_portfolio=portfolios["market"],
        spec_risk=combined_spec_risk["active"],
    )
    portfolio_beta = (factor_beta_covar**2 + spec_risk_covar) / (
        total_risks["market"] ** 2
    )

    # 4. expected shortfall calculation assuming normality, 1 Day
    es95, var95 = calculate_lognormal_es_var(total_risks["portfolio"], 0.95)
    es99, var99 = calculate_lognormal_es_var(total_risks["portfolio"], 0.99)

    # 5. assemble output
    risk_categories = [
        "Total Risk (portfolio)",
        "Total Risk (benchmark)",
        "Total Risk (active)",
        "Factor Risk (portfolio)",
        "Factor Risk (active)",
        "Specific Risk (portfolio)",
        "Specific Risk (active)",
    ]
    risk_values = [
        total_risks["portfolio"] * 100,
        total_risks["market"] * 100,
        total_risks["active"] * 100,
        factor_risks["portfolio"] * 100,
        factor_risks["active"] * 100,
        spec_risks["portfolio"] * 100,
        spec_risks["active"] * 100,
    ]
    risk_metrics = dict(zip(risk_categories, risk_values))

    risk_metrics_extended = risk_metrics.copy()
    risk_metrics_extended["Portfolio Beta (vs benchmark)"] = portfolio_beta * 100
    risk_metrics_extended["Portfolio VaR (1-day, 95%, total space)"] = var95 * 100
    risk_metrics_extended["Portfolio ES (1-day, 95%, total space)"] = es95 * 100
    risk_metrics_extended["Portfolio VaR (1-day, 99%, total space)"] = var99 * 100
    risk_metrics_extended["Portfolio ES (1-day, 99%, total space)"] = es99 * 100
    for key in risk_metrics_extended.keys():
        risk_metrics_extended[key] = np.round(risk_metrics_extended[key], decimals=3)

    exposures = {}
    for portfolio in portfolios.keys():
        exposures[portfolio] = port_exposures[portfolio].to_dict()

    mctr_output = generate_mctr_chart_input(portfolios, factor_mctrs, spec_risk_mctrs)

    portfolio_df = assemble_portfolios_into_df(portfolios)
    parsed_port_data = parse_portfolio_input(portfolio_df)

    return {
        "risk_metrics": risk_metrics_extended,
        "exposures": exposures,
        "mctr": mctr_output,
        "all_portfolios": parsed_port_data,
        "model": "factor",
    }


def generate_market_portfolio(cob_date: str):
    df = query_exposures_for_market_portfolio_data(cob_date)
    df = df.head(20).copy()
    df["weight"] = df["transformed_market_cap"] / sum(df["transformed_market_cap"])
    return {
        list(df["ticker"])[idx]: list(df["weight"])[idx]
        for idx in range(len(list(df["ticker"])))
    }


def decode_risk_calc_input(request) -> Tuple[Dict, str, int]:
    # parse request body and check whether correct date input is provided
    all_input = json.loads(request.body.decode("utf-8"))
    log_elements = list()
    processed_input = {}
    override_code = 0  # we set it to one if any override occurs

    processed_input["cob_date"] = all_input["cob_date"]
    available_dates = get_available_estimation_dates()
    if processed_input["cob_date"] not in available_dates:
        log_elements.append(
            "The calculation date ({date}) is not covered by the model! ".format(
                date=processed_input["cob_date"]
            )
        )

    processed_input["mean_to_zero"] = all_input["mean_to_zero"]
    date = processed_input["cob_date"]
    # process parameter imput
    for parameter_name, parameter_nickname in zip(
        ["correlation_hl", "factor_risk_hl", "specific_risk_hl"],
        ["correlation half-life", "factor risk half-life", "specific risk half-life"],
    ):
        override_code += check_input_param_correctness(
            parameter_name=parameter_name,
            parameter_default=HALF_LIFE_DEFAULT,
            parameter_nickname=parameter_nickname,
            all_input=all_input,
            log_elements=log_elements,
            processed_input=processed_input,
        )

    override_code += check_input_param_correctness(
        parameter_name="min_ret_hist",
        parameter_default=MIN_OBS_DEFAULT,
        parameter_nickname="minimum number of observations for risk calculation",
        all_input=all_input,
        log_elements=log_elements,
        processed_input=processed_input,
        integer_conversion=True,
    )

    # process portfolio file input
    processed_input["portfolio"], port_log_messages, port_error_code = (
        parse_file_input_into_portfolio(all_input["portfolio"])
    )
    log_elements = log_elements + port_log_messages

    # process benchmark data
    if all_input["benchmark"]:
        processed_input["market"], bmrk_log_messages, bmrk_error_code = (
            parse_file_input_into_portfolio(all_input["benchmark"])
        )
        log_elements = log_elements + bmrk_log_messages
        bmrk_error_code = 0
    elif (
        all_input["benchmark"] is None
        and processed_input["cob_date"] in available_dates
    ):
        log_elements.append(
            "No benchmark was provided, hence the model universe based benchmark is loaded! "
        )
        override_code += 1
        bmrk_error_code = 1
        processed_input["market"] = generate_market_portfolio(date)
    else:
        bmrk_error_code = 404

    # check coverage
    if processed_input["cob_date"] in available_dates:
        symbol_coverage = get_coverage_for_date(date)
        for portfolio in ["market", "portfolio"]:
            override_code += check_missing_coverage(
                symbols=symbol_coverage,
                processed_input=processed_input,
                portfolio_name=portfolio,
                log_elements=log_elements,
            )
        if len(processed_input["market"].keys()) < 1:
            log_elements.append(f"No benchmark coverage for date : {date}! ")
        if len(processed_input["portfolio"].keys()) < 1:
            log_elements.append(f"No portfolio coverage for date : {date}! ")
    else:
        processed_input["market"] = {}
        processed_input["portfolio"] = {}
        log_elements.append(
            "The symbol coverage was not evaluated as the provided calculation date is outside model estimation range! "
        )

    if (
        bmrk_error_code == 404
        or port_error_code == 404
        or processed_input["cob_date"] not in available_dates
        or len(processed_input["market"].keys()) < 1
        or len(processed_input["portfolio"].keys()) < 1
    ):
        override_code = 404
    else:
        override_code = 1 if override_code > 0 else 0

    # finally renameing the risk param elements is needed
    # frontend has shorter names for these, hence we do the translation here
    for key in FRONTEND_TO_BACKEND.keys():
        processed_input[FRONTEND_TO_BACKEND[key]] = processed_input[key]

    processed_input["mean_to_zero"] = all_input["mean_to_zero"]
    if processed_input["mean_to_zero"]:
        log_elements.append(
            "The demeaned returns are used for the calculation of risk. "
        )
    processed_input["use_factors"] = all_input["use_factors"]
    if not processed_input["use_factors"]:
        log_elements.append("All cryptocurrency is treated as a single factor. ")

    return processed_input, log_elements, override_code


def risk_calc_request_reduced(
    portfolio_details: Dict[str, float],
    market_portfolio: Dict[str, float],
    risk_calculation_parameters: Dict,
):
    # Step 1: cob_date and portfolio related
    cob_date = risk_calculation_parameters["date"]
    if market_portfolio is None:
        exposures = query_exposures(cob_date=cob_date)
        market_portfolio = generate_market_portfolio(exposures)
    all_tickers = list(
        set(market_portfolio.keys()).union(set(portfolio_details.keys()))
    )
    active_space_port = generate_active_space_portfolio(
        portfolio_details, market_portfolio
    )

    # Step 2: query and manipulate returns
    return_df = query_excess_returns(cob_date=cob_date, symbols=all_tickers)
    fill_miss_returns = query_fillmiss_returns(cob_date=cob_date)
    factor_return_formatted_df = generate_processed_excess_returns(
        return_df, fill_miss_returns
    )

    # Step 3: risk calculation
    portfolios = {
        "portfolio": portfolio_details,
        "market": market_portfolio,
        "active": active_space_port,
    }
    covariance_matrixes = {}
    relevant_keys = {}
    port_exposures = {}
    total_risks = {}
    total_attributions = {}
    mctrs = {}
    factor_covars = {}
    for portfolio in portfolios.keys():
        # 3.1. exposure calc
        port_exposures[portfolio] = pd.Series(portfolios[portfolio]).sort_values(
            ascending=False
        )
        relevant_keys[portfolio] = list(port_exposures[portfolio].index)
        covariance_matrixes[portfolio] = generate_factor_covariance_matrix(
            factor_return_formatted_df[["date"] + relevant_keys[portfolio]],
            risk_calculation_parameters,
        )

        # 3.2. risk calculation without factors
        (
            total_risks[portfolio],
            total_attributions[portfolio],
        ) = generate_factor_covariance_attribution(
            port_exposures[portfolio].to_frame("exposure"),
            covariance_matrixes[portfolio],
        )
        mctrs[portfolio] = total_attributions[portfolio] / total_risks[portfolio]

        factor_covars[portfolio] = generate_factor_covariance_table(
            port_exposures[portfolio].to_frame("exposure"),
            covariance_matrixes[portfolio],
        )

    # Step 4: beta and ES calculation
    all_exposure = pd.concat(
        [port_exposures["portfolio"], port_exposures["market"]], axis=1
    ).fillna(0)
    cov_for_beta = generate_factor_covariance_matrix(
        factor_return_formatted_df[["date"] + list(all_exposure.index)],
        risk_calculation_parameters,
    )

    factor_beta_covar, _ = generate_factor_covariance_attribution(
        all_exposure[[0]].rename(columns={0: "exposure"}),
        cov_for_beta,
        all_exposure[[1]].rename(columns={1: "exposure"}),
    )

    portfolio_beta = (factor_beta_covar**2) / (total_risks["market"] ** 2)

    es95, var95 = calculate_lognormal_es_var(total_risks["portfolio"], 0.95)
    es99, var99 = calculate_lognormal_es_var(total_risks["portfolio"], 0.99)
    # 5. assemble output
    risk_categories = [
        "Total Risk (portfolio)",
        "Total Risk (benchmark)",
        "Total Risk (active)",
    ]
    risk_values = [
        total_risks["portfolio"] * 100,
        total_risks["market"] * 100,
        total_risks["active"] * 100,
    ]
    risk_metrics = dict(zip(risk_categories, risk_values))

    risk_metrics_extended = risk_metrics.copy()
    risk_metrics_extended["Portfolio Beta (vs benchmark)"] = portfolio_beta * 100
    risk_metrics_extended["Portfolio VaR (1-day, 95%, total space)"] = var95 * 100
    risk_metrics_extended["Portfolio ES (1-day, 95%, total space)"] = es95 * 100
    risk_metrics_extended["Portfolio VaR (1-day, 99%, total space)"] = var99 * 100
    risk_metrics_extended["Portfolio ES (1-day, 99%, total space)"] = es99 * 100
    for key in risk_metrics_extended.keys():
        risk_metrics_extended[key] = np.round(risk_metrics_extended[key], decimals=3)

    mctr_output = generate_mctr_chart_input_reduced(portfolios, mctrs)

    portfolio_df = assemble_portfolios_into_df(portfolios)
    parsed_port_data = parse_portfolio_input(portfolio_df)

    port_weights = {}
    for portfolio in portfolios.keys():
        if portfolio == "market":
            port_weights["market"] = {"exposure": portfolio_df["benchmark"].to_dict()}
        else:
            port_weights[portfolio] = {"exposure": portfolio_df[portfolio].to_dict()}

    return {
        "risk_metrics": risk_metrics_extended,
        "exposures": port_weights,
        "mctr": mctr_output,
        "all_portfolios": parsed_port_data,
        "model": "no-factor",
    }
