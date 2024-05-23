from typing import Dict
import pandas as pd
import numpy as np


def assemble_portfolios_into_df(
    portfolios: Dict[str, Dict[str, float]]
) -> pd.DataFrame:
    """Assebmles a dataframe that contains portfolio weights

    Args:
        portfolios (Dict[str, Dict[str, float]]): portfolios in dictionaries

    Returns:
        pd.DataFrame: all 3 portfolios in 1 dataframe
    """
    port_df = None
    for key in portfolios.keys():
        if port_df is None:
            port_df = pd.Series(portfolios[key]).to_frame(key)
        else:
            port_df = port_df.merge(
                pd.Series(portfolios[key]).to_frame(key),
                how="outer",
                left_index=True,
                right_index=True,
            )
    if port_df is None:
        return pd.DataFrame(columns=["symbol", "portfolio", "benchmark", "active"])
    port_df.fillna(0, inplace=True)
    port_df.reset_index(inplace=True)
    port_df.rename(columns={"index": "symbol", "market": "benchmark"}, inplace=True)
    port_df.sort_values(
        by=["portfolio", "benchmark", "active"],
        ascending=[False, False, False],
        inplace=True,
    )
    return port_df


def parse_portfolio_input(portfolio_df: pd.DataFrame) -> Dict:
    """Return a dictionary based dataframe input

    Args:
        portfolio_df (pd.DataFrame): dataframe containing portfolios details

    Returns:
        Dict: dictionary to be used by frontend
    """
    portfolio_df.set_index("symbol", inplace=True)
    frontend_port_input = portfolio_df[["portfolio", "benchmark", "active"]].apply(
        lambda x: {
            key: np.round(val, 3)
            for (key, val) in x[["portfolio", "benchmark", "active"]].items()
        },
        axis=1,
    )
    return frontend_port_input.to_dict()


def round_float_to_n_decimals_str(val: float, decimals: int = 3) -> str:
    val = np.round(val, decimals)
    return str(val) + "".rjust(max(decimals - str(val)[::-1].find("."), 0), "0")
