from typing import Dict
import pandas as pd
NON_FACTOR_COLUMNS = ["id", "date", "version_date"]


def get_factor_return_correlation(
    factor_returns: pd.DataFrame, parameters: Dict
) -> pd.DataFrame:
    """
    Calculates the exponentially weighted moving average (EWMA) correlation matrix
    for factor returns based on specified parameters.
    The correlation matrix is only reported for the specified date

    Args:
        factor_returns (pd.DataFrame): DataFrame containing factor returns.
            Columns should include 'date' and the factor returns for each style.
        parameters (Dict): A dictionary containing parameters:
            - 'date': The cob date for factor return estimation.
            - 'correlation_half_life': Half-life for EWMA correlation calculation.

    Returns:
        pd.DataFrame: EWMA correlation matrix for factor returns.
    """
    factor_return_estim = factor_returns[
        factor_returns["date"] <= parameters["date"]
    ].copy()
    style_columns = sorted(
        list(set(factor_return_estim.columns) - set(NON_FACTOR_COLUMNS))
    )
    return (
        factor_return_estim[style_columns]
        .ewm(halflife=parameters["correlation_half_life"])
        .corr()
        .tail(len(style_columns))
    )
