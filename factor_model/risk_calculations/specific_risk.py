from typing import Dict
import pandas as pd


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
                .ewm(halflife=parameters["variance_half_life"])
                .std()
                .tail(1)
                .values[0]
            )
        else:
            standard_deviations[symbol] = None
    return standard_deviations, available_spec_return_history
