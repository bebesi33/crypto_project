from typing import Dict, Tuple, List
import pandas as pd
import numpy as np


def create_portfolio_exposures(
    exposures: pd.DataFrame,
    portfolio_details: Dict[str, float],
    non_style_fields : List[str] = [] 
) -> pd.DataFrame:
    available_styles = sorted(
        list(set(exposures.columns) - set(non_style_fields))
    )
    expo_selected = exposures[exposures["ticker"].isin(portfolio_details.keys())][
        ["ticker"] + available_styles
    ]
    expo_selected["portfolio_weight"] = expo_selected["ticker"].map(portfolio_details)
    expo_selected["portfolio_weight"] = expo_selected["portfolio_weight"] / sum(
        expo_selected["portfolio_weight"]
    )
    weighted_port_exposure = dict()
    for col in available_styles:
        weighted_port_exposure[col] = sum(
            expo_selected["portfolio_weight"] * expo_selected[col]
        )
    weighted_port_exposure["market"] = 1  # set market to 1

    port_exposure = pd.Series(weighted_port_exposure).to_frame().reset_index()
    port_exposure.columns = ["factor", "exposure"]
    return port_exposure.set_index("factor")


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
    spec_std: Dict[str, float], portfolio_details: Dict[str, float]
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
    port_total = sum(portfolio_details.values())
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
    spec_risk_mctr = spec_risk_mctr / weight_coverage
    spec_risk_var_contrib = pd.Series(spec_risk_var_contrib)
    spec_risk_var_contrib = spec_risk_var_contrib / (weight_coverage**2)
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
