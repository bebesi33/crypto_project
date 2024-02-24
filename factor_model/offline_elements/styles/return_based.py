import numpy as np
import pandas as pd
from typing import Dict, List


def generate_x_month_price_change(
    price_data_map: Dict[str, pd.DataFrame], 
    x_len: int = 12, month_len: int = 30
) -> Dict[str, pd.DataFrame]:
    """
    Analyzes price data to generate momentum and reversal like exposure values.

    Args:
        price_data_map (Dict[str, pd.DataFrame]): A dictionary mapping crypto tickers to price data.
        x_len (int, optional): Number of months for analysis. Defaults to 12.
        month_len (int, optional): Number of days in a month. Defaults to 30.

    Returns:
        Dict[str, pd.DataFrame]: A dictionary containing exposure values for each stock.
    """
    return_map: Dict[str, pd.DataFrame] = {}
    for key in price_data_map.keys():
        close_price_changes = np.matrix(
            price_data_map[key]["Close"]
            .diff(periods=x_len * month_len)
            .tail(-x_len * month_len)
        ) / np.matrix(price_data_map[key]["Close"].head(-x_len * month_len))
        df_temp = pd.DataFrame(
            {
                "date": price_data_map[key]["date"].tail(-x_len * month_len),
                "exposure": close_price_changes.tolist()[0],
            }
        )
        df_temp["exposure"] = np.where(
            df_temp["exposure"] > 10, 10, df_temp["exposure"]
        )
        df_temp.fillna(0, inplace=True)
        return_map[key] = df_temp
    return return_map
