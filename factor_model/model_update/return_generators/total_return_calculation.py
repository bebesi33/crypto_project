import numpy as np
import pandas as pd
from typing import Dict


def generate_return_data(price_data_map: Dict):
    return_map = dict()
    for key in price_data_map.keys():
        gg = np.matrix(price_data_map[key]["Close"].diff().tail(-1)) / np.matrix(
            price_data_map[key]["Close"].head(-1)
        )
        df_temp = pd.DataFrame(
            {"date": price_data_map[key]["date"].tail(-1), "return": gg.tolist()[0]}
        )
        df_temp.fillna(0, inplace=True)
        return_map[key] = df_temp.tail(-1)
    return return_map
