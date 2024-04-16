import json
from typing import List, Dict, Tuple
from crypto_calculator.models import Exposures, FactorReturns, SpecificReturns
import pandas as pd
import numpy as np
from factor_model.risk_calculations import HALF_LIFE_DEFAULT, MIN_OBS_DEFAULT
from factor_model.risk_calculations.core_universe_portfolio import (
    generate_market_portfolio,
)
from factor_model.risk_calculations.factor_covariance import (
    generate_factor_covariance_matrix,
)
from factor_model.risk_calculations.parameter_processing import (
    check_input_param_correctness,
)
from factor_model.risk_calculations.risk_attribution import (
    generate_active_space_portfolio,
    generate_mctr_chart_input,
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
    generate_raw_portfolio_specific_risk,
    generate_raw_specific_risk,
)
from factor_model.model_update.database_generators import EXPOSURE_NON_STYLE_FIELDS
import logging

logger = logging.getLogger("risk calc")


def query_factor_return_data(cob_date: str) -> pd.DataFrame:
    factor_return_data = (
        FactorReturns.objects.using("factor_model_estimates")
        .filter(date__lte=cob_date)  # date less than equal to cob_date input...
        .values()
    )
    df = pd.DataFrame(list(factor_return_data))
    df["date"] = df["date"].apply(lambda x: x.strftime("%Y-%m-%d"))
    return df


def query_exposures(cob_date: str) -> pd.DataFrame:
    exposures = (
        Exposures.objects.using("factor_model_estimates").filter(date=cob_date).values()
    )
    return pd.DataFrame(list(exposures))


def query_specific_returns(cob_date: str, symbols: List[str]) -> pd.DataFrame:
    specific_returns = (
        SpecificReturns.objects.using("factor_model_estimates")
        .filter(date__lte=cob_date)
        .filter(ticker__in=symbols)
        .values()
    )
    df = pd.DataFrame(list(specific_returns))
    return df


def risk_calc_request_full(
    portfolio_details: Dict[str, float],
    market_portfolio: Dict[str, float],
    risk_calculation_parameters: Dict,
):
    # Step 1: cob_date and basic queries
    print("risk_calc_request_full - STARTED")
    cob_date = risk_calculation_parameters["date"]
    exposures = query_exposures(cob_date=cob_date)
    print("Step 1: exposure query - READY")
    if market_portfolio is None:
        market_portfolio = generate_market_portfolio(exposures)

    all_tickers = list(
        set(market_portfolio.keys()).union(set(portfolio_details.keys()))
    )
    full_specific_returns = query_specific_returns(
        cob_date=cob_date, symbols=all_tickers
    )
    print("Step 1: specific return query - READY")
    factor_returns = query_factor_return_data(cob_date=cob_date)
    print("Step 1: factor return query - READY")
    print("Step 1: all query input - READY")

    # Step 2: calculate risk
    factor_covariance = generate_factor_covariance_matrix(
        factor_returns, risk_calculation_parameters
    )
    active_space_port = generate_active_space_portfolio(
        portfolio_details, market_portfolio
    )

    portolios = {
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
    for port in portolios.keys():
        # 2.1. exposure calc
        port_exposures[port] = create_portfolio_exposures(
            exposures=exposures,
            portfolio_details=portolios[port],
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
            full_specific_returns, risk_calculation_parameters, portolios[port]
        )
        spec_risks[port] = generate_raw_portfolio_specific_risk(
            raw_specific_risks[port],
            portolios[port],
            is_total_space=True if port != "active" else False,
        )
        total_risks[port] = np.sqrt(factor_risks[port] ** 2 + spec_risks[port] ** 2)

        factor_mctrs[port] = factor_attributions[port] / total_risks[port]
        spec_risk_attributions[port], spec_risk_var_decomps[port] = (
            calculate_spec_risk_mctr(
                raw_specific_risks[port],
                portolios[port],
                True if port != "active" else False,
            )
        )
        spec_risk_mctrs[port] = spec_risk_attributions[port] / total_risks[port]
    print("Step 2: calculate risk - READY")

    # 3. beta calculation...
    factor_beta_covar, _ = generate_factor_covariance_attribution(
        port_exposures["portfolio"], factor_covariance, port_exposures["market"]
    )
    spec_risk_covar = get_specific_risk_beta(
        portolios["portfolio"],
        market_portfolio=portolios["market"],
        spec_risk=raw_specific_risks["active"],
    )
    portfolio_beta = (factor_beta_covar**2 + spec_risk_covar) / (
        total_risks["market"] ** 2
    )
    print("Step 3: calculate beta - READY")

    # 4. expected shortfall calculation assuming normality, 1 Day
    es95, var95 = calculate_lognormal_es_var(total_risks["portfolio"], 0.95)
    es99, var99 = calculate_lognormal_es_var(total_risks["portfolio"], 0.99)
    print("Step 4: calculate ES/VaR - READY")

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
    for portfolio in portolios.keys():
        exposures[portfolio] = port_exposures[portfolio].to_dict()

    mctr_output = generate_mctr_chart_input(portolios, factor_mctrs, spec_risk_mctrs)

    print("Step 5: output assembly - READY")

    return {
        "risk_metrics": risk_metrics_extended,
        "exposures": exposures,
        "mctr": mctr_output,
    }


def decode_risk_calc_input(request) -> Tuple[Dict, str, int]:
    all_input = json.loads(request.body.decode("utf-8"))
    print(all_input)
    log_elements = list()
    processed_input = {}

    override_code = 0  # we set it to one if any override occurs
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
    )

    return processed_input, log_elements, override_code
