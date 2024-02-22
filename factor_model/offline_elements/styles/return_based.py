import numpy as np
import pandas as pd


def generate_x_month_price_change(price_data_map, x_len=12, month_len=30):
    return_map = dict()
    for key in price_data_map.keys():
        gg = np.matrix(
            price_data_map[key]["Close"]
            .diff(periods=x_len * month_len)
            .tail(-x_len * month_len)
        ) / np.matrix(price_data_map[key]["Close"].head(-x_len * month_len))
        df_temp = pd.DataFrame(
            {
                "date": price_data_map[key]["date"].tail(-x_len * month_len),
                "exposure": gg.tolist()[0],
            }
        )
        df_temp["exposure"] = np.where(
            df_temp["exposure"] > 10, 10, df_temp["exposure"]
        )
        df_temp.fillna(0, inplace=True)
        return_map[key] = df_temp.tail(-x_len * month_len)
    return return_map
