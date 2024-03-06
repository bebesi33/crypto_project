import pandas as pd
from typing import Dict, Any


def generate_x_month_aggregate_volume(
    price_data_map: Dict[str, pd.DataFrame], x_len: int = 12, month_len: int = 30
) -> Dict[str, pd.DataFrame]:
    return_map: Dict[str, pd.DataFrame] = {}
    for key in price_data_map.keys():
        volume_rolling = (
            price_data_map[key]["Volume"].rolling(x_len * month_len).sum() / 1000000
        )
        df_temp = pd.DataFrame(
            {
                "date": price_data_map[key]["date"].tail(-x_len * month_len),
                "exposure": volume_rolling,
            }
        )
        df_temp.fillna(0, inplace=True)
        return_map[key] = df_temp.tail(-x_len * month_len)
    return return_map
