from typing import Dict
import pandas as pd
import numpy as np


def generate_raw_specific_risk(
    specific_returns: pd.DataFrame,
    parameters: Dict,
    portfolio_details: Dict[str, float],
) -> tuple[Dict[str, float], Dict[str, float]]:
    """
    Calculates raw specific risk for each symbol in a portfolio.

    Args:
        specific_returns (pd.DataFrame): DataFrame containing specific returns data.
        parameters (Dict): A dictionary of parameters including:
            - "date": The reference date for calculating specific risk.
            - "variance_half_life": The half-life for exponential moving average (EMA) calculation.

    Returns:
        tuple[Dict[str,float], Dict[str,float]]: A tuple containing two dictionaries:
            - First dictionary (standard_deviations): Symbol-wise specific risk standard deviations.
            - Second dictionary (available_spec_return_history): Number of available specific return data points for each symbol.
    """
    standard_deviations = dict()
    available_spec_return_history = dict()
    for symbol in portfolio_details.keys():
        specific_returns_temp = specific_returns[
            (specific_returns["ticker"] == symbol)
            & (specific_returns["date"] <= parameters["date"])
        ].copy()
        available_spec_return_history[symbol] = len(specific_returns_temp)
        if len(specific_returns_temp) > 1:
            standard_deviations[symbol] = (
                specific_returns_temp["specific_return"]
                .ewm(halflife=parameters["specific_risk_half_life"])
                .std()
                .tail(1)
                .values[0]
            )
        else:
            standard_deviations[symbol] = None
    return standard_deviations, available_spec_return_history


def generate_raw_portfolio_specific_risk(
    spec_std: Dict[str, float], portfolio_details: Dict[str, float]
) -> float:
    """
    Calculates the raw specific risk (also known as idiosyncratic risk) of a portfolio.

    Args:
        spec_std (Dict[str, float]): A dictionary mapping ticker symbols to their specific standard deviations.
        portfolio_details (Dict[str, float]): A dictionary mapping ticker symbols to their portfolio weights.

    Returns:
        float: The raw specific risk of the portfolio.
    """
    spec_risk_total = 0
    weight_coverage = 0
    port_total = sum(portfolio_details.values())
    for ticker in spec_std.keys():
        spec_risk = spec_std.get(ticker)
        if spec_risk:
            current_weight = portfolio_details.get(ticker) / port_total
            spec_risk_total += spec_risk**2 * current_weight**2
            weight_coverage += current_weight

    spec_risk_total = np.sqrt(spec_risk_total / (weight_coverage**2))
    return spec_risk_total
