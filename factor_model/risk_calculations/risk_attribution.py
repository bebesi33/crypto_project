from typing import Dict, Tuple, List
import pandas as pd
import numpy as np


def create_portfolio_exposures(
    exposures: pd.DataFrame,
    portfolio_details: Dict[str, float],
    non_style_fields: List[str] = [],
    is_total_space: bool = True,
) -> pd.DataFrame:
    available_styles = sorted(list(set(exposures.columns) - set(non_style_fields)))
    expo_selected = exposures[exposures["ticker"].isin(portfolio_details.keys())][
        ["ticker"] + available_styles
    ].copy()
    expo_selected["portfolio_weight"] = expo_selected["ticker"].map(portfolio_details)
    if is_total_space:
        expo_selected["portfolio_weight"] = expo_selected["portfolio_weight"] / sum(
            expo_selected["portfolio_weight"]
        )
    weighted_port_exposure = dict()
    for col in available_styles:
        weighted_port_exposure[col] = sum(
            expo_selected["portfolio_weight"] * expo_selected[col]
        )
    if is_total_space:
        weighted_port_exposure["market"] = 1.0
    else:
        weighted_port_exposure["market"] = 0.0

    port_exposure = pd.Series(weighted_port_exposure).to_frame().reset_index()
    port_exposure.columns = ["factor", "exposure"]
    return port_exposure.set_index("factor").fillna(0)


def generate_factor_covariance_attribution(
    port_exposure: pd.DataFrame,
    factor_covariance: pd.DataFrame,
    market_exposure: pd.DataFrame = None,
):
    if market_exposure is None:
        market_exposure = port_exposure

    port_exposure = port_exposure.reindex(factor_covariance.index)
    market_exposure = market_exposure.reindex(factor_covariance.index)

    factor_attribution = np.matmul(port_exposure["exposure"].T, factor_covariance)

    factor_std = np.sqrt(
        np.matmul(
            factor_attribution,
            market_exposure["exposure"],
        )
    )
    return factor_std, factor_attribution


def generate_factor_covariance_table(
    port_exposure: pd.DataFrame, factor_covariance: pd.DataFrame
) -> pd.DataFrame:
    port_exposure = port_exposure.reindex(factor_covariance.index)
    diag_port_exposure = np.diag(port_exposure["exposure"])
    covar = np.matmul(
        np.matmul(diag_port_exposure, factor_covariance), diag_port_exposure
    )
    covar.columns = factor_covariance.columns
    covar.set_index(factor_covariance.index, inplace=True)
    return covar


def calculate_spec_risk_mctr(
    spec_std: Dict[str, float],
    portfolio_details: Dict[str, float],
    is_total_space: bool = True,
) -> Tuple[pd.Series, pd.Series]:
    """
    Calculates the specific risk marginal contribution to risk

    Args:
        spec_std (Dict[str, float]): A dictionary mapping ticker symbols to their specific standard deviations.
        portfolio_details (Dict[str, float]): A dictionary mapping ticker symbols to their portfolio weights.

    Returns:
        Dict: The marginal contribution to risk of the portfolio
        Dict: The variance decomposition for specific risk
    """
    weight_coverage = 0
    if is_total_space:
        port_total = sum(portfolio_details.values())
    else:
        port_total = 1

    spec_risk_mctr = {}
    spec_risk_var_contrib = {}
    for ticker in portfolio_details.keys():
        spec_risk = spec_std.get(ticker)
        if spec_risk:
            current_weight = portfolio_details.get(ticker) / port_total
            spec_risk_mctr[ticker] = current_weight * spec_risk**2
            spec_risk_var_contrib[ticker] = spec_risk_mctr[ticker] * current_weight
            weight_coverage += current_weight

    spec_risk_mctr = pd.Series(spec_risk_mctr)
    spec_risk_var_contrib = pd.Series(spec_risk_var_contrib)
    if is_total_space:
        spec_risk_mctr = spec_risk_mctr / weight_coverage
        spec_risk_var_contrib = spec_risk_var_contrib / (weight_coverage**2)
    else:
        spec_risk_var_contrib = spec_risk_var_contrib
        spec_risk_mctr = spec_risk_mctr

    return spec_risk_mctr, spec_risk_var_contrib


def generate_active_space_portfolio(
    portfolio_details: Dict[str, float], market_portfolio: Dict[str, float]
) -> Dict[str, float]:
    """
    Calculates the portfolio  weights in active space
    based on the difference between the portfolio weights and market portfolio weights.

    Args:
        portfolio_details (Dict[str, float]): A dictionary containing ticker symbols as keys
        and corresponding portfolio weights.
        market_portfolio (Dict[str, float]): A dictionary containing ticker symbols as keys
        and corresponding market weights.

    Returns:
        Dict[str, float]: A dictionary with ticker symbols as keys and active space values as float.
            The active space value represents the difference between portfolio weight and market weight.
    """
    active_space_portfolio = {}
    total_port_w = sum(portfolio_details.values())
    total_market_w = sum(market_portfolio.values())

    for ticker in set(portfolio_details.keys()).union(market_portfolio.keys()):
        port_w = portfolio_details.get(ticker, 0)
        market_w = market_portfolio.get(ticker, 0)
        active_space_portfolio[ticker] = (port_w / total_port_w) - (
            market_w / total_market_w
        )
    return active_space_portfolio


def get_specific_risk_beta(
    portfolio_details: Dict[str, float],
    market_portfolio: Dict[str, float],
    spec_risk: Dict[str, float],
) -> float:
    """
    Calculates the specific risk beta for a given portfolio.

    Args:
        portfolio_details (Dict[str, float]): A dictionary containing ticker symbols as keys
            and corresponding portfolio weights (as floats).
        market_portfolio (Dict[str, float]): A dictionary representing the market portfolio,
            with ticker symbols as keys and their respective weights (as floats).
        spec_risk (Dict[str, float]): A dictionary containing ticker symbols as keys
            and their specific risk (as floats).

    Returns:
        float: The total specific risk beta for the portfolio.

    Example:
        portfolio_details = {'BTC-USD': 0.4, 'ETH-USD': 0.3, 'LNC-USD': 0.2}
        market_portfolio = {'BTC-USD': 0.2, 'ETH-USD': 0.5, 'LNC-USD': 0.3}
        spec_risk = {'BTC-USD': 0.02, 'ETH-USD': 0.015, 'LNC-USD': 0.018}
        result = get_specific_risk_beta(portfolio_details, market_portfolio, spec_risk)
        # Returns the specific risk beta for the given portfolio.
    """
    spec_risk_beta = 0
    port_total = sum(portfolio_details.values())
    market_total = sum(market_portfolio.values())
    for ticker in set(portfolio_details.keys()).union(market_portfolio.keys()):
        spec_risk_temp = spec_risk.get(ticker)
        if spec_risk_temp:
            port_w = portfolio_details.get(ticker, 0)
            market_w = market_portfolio.get(ticker, 0)
            spec_risk_beta += (
                (port_w / port_total) * (spec_risk_temp**2) * (market_w / market_total)
            )
    return spec_risk_beta


def generate_mctr_chart_input(
    portolios: Dict[str, Dict[str, float]],
    factor_mctrs: Dict[str, pd.Series],
    spec_risk_mctrs: Dict[str, pd.Series],
) -> Dict[str, Dict[str, float]]:
    """
    Assembles and orders risk metrics (MCTRs) for different portfolios.

    Args:
        portolios (Dict[str, Dict[str, float]]): A dictionary containing portfolio names as keys
            and corresponding factor weights as inner dictionaries.
        factor_mctrs (Dict[str, pd.Series]): A dictionary with portfolio names as keys
            and factor MCTRs (risk metrics) as inner pandas Series.
        spec_risk_mctrs (Dict[str, pd.Series]): A dictionary with portfolio names as keys
            and specific risk MCTRs as inner pandas Series.

    Returns:
        Dict[str, Dict[str, float]]: A dictionary containing ordered MCTRs for each portfolio,
        including relevant factors and zero values for missing factors.
    """
    # assemble mctr_data, first all keys
    all_mctr = {}
    for portfolio in portolios.keys():
        all_mctr[portfolio] = factor_mctrs[portfolio].append(spec_risk_mctrs[portfolio])

    # top 5 spec risk mctr (for portfolio) and if exists active risk are presented
    port_largest_contrib = set(spec_risk_mctrs["portfolio"].abs().nlargest(5).index)
    if "active" in portolios.keys():
        active_largest_contrib = set(spec_risk_mctrs["active"].abs().nlargest(5).index)
        port_largest_contrib = port_largest_contrib.union(active_largest_contrib)
    relevant_mctr_keys = list(factor_mctrs["portfolio"].keys()) + list(
        port_largest_contrib
    )

    all_mctr_ordered = {}
    for portfolio in portolios.keys():
        all_mctr[portfolio] = {
            key: value
            for key, value in all_mctr[portfolio].items()
            if key in relevant_mctr_keys
        }

    main_port = "active" if "active" in portolios.keys() else "portfolio"
    for portfolio in portolios.keys():
        all_mctr_ordered[portfolio] = {}
        for key in all_mctr[main_port].keys():
            all_mctr_ordered[portfolio][key] = (
                all_mctr[portfolio][key] if key in all_mctr[portfolio].keys() else 0
            )
            all_mctr_ordered[portfolio][key] = (
                all_mctr_ordered[portfolio][key]
                if pd.notna(all_mctr_ordered[portfolio][key])
                else 0
            )
    if "active" in portolios.keys() and "market" in all_mctr_ordered["active"].keys():
        all_mctr_ordered["active"]["market"] = 0
    return all_mctr_ordered
