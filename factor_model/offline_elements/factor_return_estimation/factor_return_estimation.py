import numpy as np
from datetime import timedelta


def create_expo_from_daily_data(date, daily_expo_map, variable_name="exposure"):
    expo_map = dict()
    for key in daily_expo_map.keys():
        v = daily_expo_map[key][daily_expo_map[key]["date"] == date][variable_name]
        if len(v) > 0:
            expo_map[key] = v.values[0]
        else:
            expo_map[key] = None
    return expo_map


def create_factor_return_data(estimation_basis, parameters, date, daily_data_maps):
    estimation_basis_current = estimation_basis.copy()

    estimation_basis_current["reversal"] = estimation_basis_current["ticker"].map(
        create_expo_from_daily_data(date + timedelta(-1), daily_data_maps["reversal"])
    )
    estimation_basis_current["momentum"] = estimation_basis_current["ticker"].map(
        create_expo_from_daily_data(date + timedelta(-1), daily_data_maps["momentum"])
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

    estimation_basis_final["return"] = (
        estimation_basis_final["return"]
        .replace(np.inf, np.nan)
        .replace(-np.inf, np.nan)
    )
    estimation_basis_final["return"] = np.where(
        estimation_basis_final["return"] > 1, 1, estimation_basis_final["return"]
    )
    estimation_basis_final["return"] = np.where(
        estimation_basis_final["return"] < -1, -1, estimation_basis_final["return"]
    )
    return estimation_basis_final.dropna()
