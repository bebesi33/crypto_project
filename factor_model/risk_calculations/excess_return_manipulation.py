import numpy as np
import pandas as pd


def generate_processed_excess_returns(
    return_df: pd.DataFrame, fill_miss_returns: pd.DataFrame
) -> pd.DataFrame:
    """Generates the excess return history for the non factor model

    Args:
        return_df (pd.DataFrame): contains date, excess_return and symbol columns
        fill_miss_returns (pd.DataFrame): contains date and proxiy return columns

    Returns:
        pd.DataFrame: excess returns in a factor return data like format
    """
    symbols = sorted(list(set(return_df["symbol"])))
    factor_return_formatted_df = None

    for symbol in symbols:
        if factor_return_formatted_df is None:
            factor_return_formatted_df = return_df[return_df["symbol"] == symbol][
                ["date", "excess_return"]
            ].rename(columns={"excess_return": symbol})

        else:
            temp_df = return_df[return_df["symbol"] == symbol][
                ["date", "excess_return"]
            ].rename(columns={"excess_return": symbol})
            factor_return_formatted_df = factor_return_formatted_df.merge(
                temp_df, how="outer", on="date"
            )

    factor_return_formatted_df.sort_values(by="date", inplace=True)
    factor_return_formatted_df["date"] = factor_return_formatted_df["date"].astype(str)
    fill_miss_returns["date"] = fill_miss_returns["date"].astype(str)

    # deploy the fill miss procedure and filter to relevant time horizons

    factor_return_formatted_df = factor_return_formatted_df.merge(
        fill_miss_returns, how="left", on="date"
    )

    first_market_return_date = min(fill_miss_returns["date"])
    factor_return_formatted_df = factor_return_formatted_df[
        factor_return_formatted_df["date"] >= first_market_return_date
    ]

    for symbol in symbols:
        factor_return_formatted_df[symbol] = np.where(
            factor_return_formatted_df[symbol].isnull(),
            factor_return_formatted_df["proxy_return"],
            factor_return_formatted_df[symbol],
        )

    factor_return_formatted_df.drop(columns=["proxy_return"], inplace=True)
    return factor_return_formatted_df
