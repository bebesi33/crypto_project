from typing import Dict
import pandas as pd
import numpy as np

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
               The implementation expects correlation_half_life to be greater than 0
               This condition should be allready handled by logics on higher level

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


def get_factor_return_standard_deviation(
    factor_returns: pd.DataFrame, parameters: Dict
):
    """
    Calculates the exponentially weighted moving average (EWMA) standard deviation
    for factor returns based on specified parameters.

    Args:
        factor_returns (pd.DataFrame): DataFrame containing factor returns.
            Columns should include 'date'
            and the factor returns saved in separate columns by style
        parameters (Dict): A dictionary containing parameters:
            - 'date': The cob date for factor return estimation.
            - 'variance_half_life': Half-life for EWMA variance calculation.

    Returns:
        pd.Series: Series containing EWMA standard deviations for each factor.
    """
    factor_return_estim = factor_returns[
        factor_returns["date"] <= parameters["date"]
    ].copy()
    style_columns = sorted(
        list(set(factor_return_estim.columns) - set(NON_FACTOR_COLUMNS))
    )
    standard_deviations = dict()
    for style_col in style_columns:
        standard_deviations[style_col] = (
            factor_return_estim[style_col]
            .ewm(halflife=parameters["variance_half_life"])
            .std()
            .tail(1)
            .values[0]
        )
    return pd.Series(standard_deviations)


def assemble_factor_covariance_matrix(
    std: pd.Series, correlation: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculates the covariance matrix for factor returns based on standard deviations
    and correlation coefficients.

    Args:
        std (pd.Series): Series containing standard deviations for each factor.
        correlation (pd.DataFrame): DataFrame containing correlation coefficients
            between factors. Rows and columns correspond to factor names.

    Returns:
        pd.DataFrame: Covariance matrix with factor names as row and column indices.
    """
    covariance_matrix = np.matmul(np.matmul(np.diag(std), correlation), np.diag(std))
    covariance_matrix.columns = correlation.columns
    covariance_matrix.index = correlation.columns
    return covariance_matrix


def generate_factor_covariance_matrix(
    factor_returns: pd.DataFrame, parameters: Dict
) -> pd.DataFrame:
    """
    Calculates the covariance matrix of factor returns based on
    separate half lifes for correlation and standard deviation.

    Args:
        factor_returns (pd.DataFrame): A DataFrame containing factor returns.
        parameters (Dict): A dictionary of parameters (e.g., risk model parameters).

    Returns:
        pd.DataFrame: A covariance matrix of factor returns.
    """
    factor_correlation = get_factor_return_correlation(factor_returns, parameters)
    factor_std = get_factor_return_standard_deviation(factor_returns, parameters)
    factor_covariance = assemble_factor_covariance_matrix(
        factor_std, factor_correlation
    )
    return factor_covariance
