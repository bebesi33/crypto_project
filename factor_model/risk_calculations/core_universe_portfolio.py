from typing import Dict
import pandas as pd


def generate_market_portfolio(exposure: pd.DataFrame) -> Dict[str, float]:
    """
    Calculates the market portfolio weights for each symbol based on weighting schema used
    during factor model estimation

    Args:
        exposure (pd.DataFrame): DataFrame containing exposure information.
            Columns required:
            - "core_universe": Indicates whether the symbol is part of the core universe (greater than 0).
            - "symbol": Ticker symbols.
            - "transformed_market_cap": weights used during estimation

    Returns:
        Dict[str, float]: A dictionary where keys are symbol symbols and values are corresponding market portfolio weights.
    """
    universe_info = exposure[exposure["core_universe"] > 0][
        ["symbol", "transformed_market_cap"]
    ].copy()
    universe_info["weight"] = (
        universe_info["transformed_market_cap"]
        / universe_info["transformed_market_cap"].sum()
    )
    return dict(zip(universe_info["symbol"], universe_info["weight"]))
