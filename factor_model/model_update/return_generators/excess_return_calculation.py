import pandas as pd


DAYCOUNT_NOMINATOR = 360


def generate_excess_returns(
    total_return_data_map: dict[str, pd.DataFrame], risk_free_rate_data: pd.DataFrame
) -> dict[str, pd.DataFrame]:
    excess_return_data_map = dict()
    for key in total_return_data_map.keys():
        excess_return_data_map[key] = total_return_data_map[key].merge(
            risk_free_rate_data[["date", "risk_free_rate"]], how="left", on="date"
        )
        excess_return_data_map[key]["total_return"] = excess_return_data_map[key][
            "return"
        ].copy()
        excess_return_data_map[key]["return"] = excess_return_data_map[key][
            "return"
        ] - excess_return_data_map[key]["risk_free_rate"] / (100 * DAYCOUNT_NOMINATOR)
    return excess_return_data_map
