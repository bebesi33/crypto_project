import numpy as np
import datetime
from typing import Dict, Union


def create_expo_from_daily_data(
    date: str, daily_expo_map: Dict[str, np.ndarray], variable_name: str = "exposure"
) -> Dict[str, Union[float, None]]:
    """
    Creates a dictionary mapping keys to exposure values for a specific date.

    Args:
        date (str): The target date in the format "YYYY-MM-DD".
        daily_expo_map (Dict[str, np.ndarray]): A dictionary where keys represent data sources and values are NumPy arrays.
            Each array should have a "date" column and a column corresponding to the specified variable_name.
        variable_name (str, optional): The name of the exposure variable. Defaults to "exposure".

    Returns:
        Dict[str, Union[float, None]]: A dictionary mapping keys to exposure values. If no value is found for a key, the value is None.
    """
    expo_map = dict()
    for key in daily_expo_map.keys():
        temp_mask = daily_expo_map[key]["date"] == date
        if np.any(temp_mask):
            expo_map[key] = daily_expo_map[key][temp_mask][variable_name].values[0]
        else:
            expo_map[key] = None
    return expo_map


def create_factor_return_data(
    estimation_basis, parameters: Dict, date: datetime.date, daily_data_maps: Dict
):
    estimation_basis_current = estimation_basis.copy()

    for style in list(set(parameters["REGRESSORS_SET1"]) - set(["market", "size", "new_coin"])):
        estimation_basis_current[style] = estimation_basis_current["ticker"].map(
            create_expo_from_daily_data(
                date + datetime.timedelta(-1), daily_data_maps[style]
            )
        )

    estimation_basis_current["market"] = 1
    estimation_basis_current["size"] = np.log1p(estimation_basis_current["market_cap"])
    estimation_basis_current.fillna(0, inplace=True)

    estimation_basis_current["return"] = estimation_basis_current["ticker"].map(
        create_expo_from_daily_data(date, daily_data_maps["return"], "return")
    )
    estimation_basis_final = estimation_basis_current[
        ["ticker", "return", "core_universe", "market", "transformed_market_cap"]
    ].copy()

    for style in list(
        set(parameters["REGRESSORS_SET1"] + parameters["REGRESSORS_SET2"]) - {"market"}
    ):
        if style in parameters["REGRESSORS_SET2"]:
            filtered = estimation_basis_current
        else:
            filtered = estimation_basis_current[
                estimation_basis_current["core_universe"] > 0
            ]

        calc_mean = np.average(
            filtered[style], weights=filtered["transformed_market_cap"]
        )
        calc_sd = np.sqrt(
            np.average(
                (filtered[style] - calc_mean) ** 2,
                weights=filtered["transformed_market_cap"],
            )
        )
        estimation_basis_final[style] = (
            estimation_basis_current[style].copy() - calc_mean
        ) / calc_sd

    estimation_basis_final["return"] = estimation_basis_final["return"].replace([np.inf, -np.inf], np.nan)

    estimation_basis_final["return"] = estimation_basis_final["return"].clip(-1, 1)

    return estimation_basis_final.dropna()
