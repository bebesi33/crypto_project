from typing import Dict, Tuple, List
import pandas as pd
import numpy as np


def generate_raw_specific_risk(
    specific_returns: pd.DataFrame,
    parameters: dict,
    portfolio_details: dict[str, float],
) -> Tuple[dict[str, float], dict[str, float]]:
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
            (specific_returns["symbol"] == symbol)
            & (specific_returns["date"].astype(str) <= parameters["date"])
        ].copy()
        available_spec_return_history[symbol] = len(specific_returns_temp)
        if len(specific_returns_temp) > 1 and not parameters["mean_to_zero"]:
            standard_deviations[symbol] = (
                specific_returns_temp["specific_return"]
                .ewm(halflife=parameters["specific_risk_half_life"])
                .std()
                .tail(1)
                .values[0]
            )
        elif len(specific_returns_temp) > 1 and parameters["mean_to_zero"]:
            standard_deviations[symbol] = (
                specific_returns_temp["specific_return"]
                .pow(2)
                .ewm(halflife=parameters["specific_risk_half_life"])
                .mean()
                .pow(0.5)
                .tail(1)
                .values[0]
            )
        else:
            standard_deviations[symbol] = None
    return standard_deviations, available_spec_return_history


def generate_raw_portfolio_specific_risk(
    spec_std: dict[str, float],
    portfolio_details: dict[str, float],
    is_total_space: bool = True,
) -> float:
    """
    Calculates the raw specific risk (also known as idiosyncratic risk) of a portfolio.

    Args:
        spec_std (Dict[str, float]): A dictionary mapping ticker symbols to their specific standard deviations.
        portfolio_details (Dict[str, float]): A dictionary mapping ticker symbols to their portfolio weights.

    Returns:
        float: The raw specific risk of the portfolio.
    """
    port_total = sum(portfolio_details.values()) if is_total_space else 1
    if abs(port_total) < 10e-10:
        port_total = 1.0  # we want to avoid dividing by zero
    spec_risk_total = 0.0
    weight_coverage = 0.0

    for ticker, weight in portfolio_details.items():
        spec_risk = spec_std.get(ticker)
        if spec_risk is not None:
            current_weight = weight / port_total
            spec_risk_total += (spec_risk * current_weight) ** 2
            weight_coverage += current_weight

    if is_total_space:
        return np.sqrt(spec_risk_total) / weight_coverage if weight_coverage else 0.0
    else:
        return np.sqrt(spec_risk_total)


def closest_halflife_element(lst: List[float], user_halflife: float) -> List[float]:
    """Grabs the closes halflife values

    Args:
        lst (List[float]): List of available halflife in database
        user_halflife (float): user provided halflife

    Returns:
        List[float]: List of closest halflifes
    """
    if user_halflife <= min(lst) or user_halflife >= max(lst):
        idx = (np.abs(np.asarray(lst) - user_halflife)).argmin()
        return [lst[idx]]
    else:
        lst_check = lst.copy()
        element_1 = lst_check[(np.abs(np.asarray(lst_check) - user_halflife)).argmin()]
        lst_check.remove(element_1)
        element_2 = lst_check[(np.abs(np.asarray(lst_check) - user_halflife)).argmin()]
        return sorted([element_1, element_2])


def generate_combined_spec_risk(
    core_spec_risk_df: pd.DataFrame,
    parameters: dict,
    raw_spec_risk: dict[str, float],
    spec_risk_hist: dict[str, int],
) -> dict[str, float]:
    # Step 1: calculate combined core spec risk
    if len(core_spec_risk_df) < 2:
        core_half_life = core_spec_risk_df["specific_risk"].values[0]
    else:
        core_half_life = np.interp(
            parameters["specific_risk_half_life"],
            core_spec_risk_df["half_life"],
            core_spec_risk_df["specific_risk"],
        )
    # Step 2: add the core avg spec risk info if needed
    combined_spec_risk = {}
    for key in raw_spec_risk.keys():
        hist_ratio = max(
            0.0, min(spec_risk_hist[key] / parameters["time_window_len"], 1.0)
        )
        if raw_spec_risk[key] is None:
            raw_spec_risk[key] = 0.0
        combined_spec_risk[key] = (
            hist_ratio * raw_spec_risk[key] + (1 - hist_ratio) * core_half_life
        )
    return combined_spec_risk