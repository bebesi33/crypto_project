from datetime import timedelta
import numpy as np


def generate_estimation_basis(
    return_data_map, market_cap_df, market_cap_date, parameters
):
    # 1. universe element is present in the last X years...
    core_univ_by_age = {}
    univ_first_appearence = {}
    for key in return_data_map.keys():
        core_univ_by_age[key] = max(
            0,
            (market_cap_date - min(return_data_map[key]["date"])).days,
        )
        univ_first_appearence[key] = min(return_data_map[key]["date"])
    # 1.1 generate the new coin style
    market_cap_df["new_coin"] = (
        market_cap_df["ticker"].map(core_univ_by_age) / parameters["PRESENT_IN_MARKET"]
    )
    market_cap_df["new_coin"] = np.where(
        market_cap_df["new_coin"] > 1, 0, 1 - market_cap_df["new_coin"]
    )

    filtered_cap_data = market_cap_df[
        market_cap_df["new_coin"]
        < (1 - parameters["NEW_COIN_INCLUSION"] / parameters["PRESENT_IN_MARKET"])
    ].copy()

    filtered_cap_data["cumsum"] = (
        filtered_cap_data["transformed_market_cap"].cumsum()
        / filtered_cap_data["transformed_market_cap"].sum()
    )

    in_universe = list(
        filtered_cap_data[
            filtered_cap_data["cumsum"] < parameters["MARKET_CAP_COVERAGE"]
        ]["ticker"]
    )

    # 3. assemble final data

    estimation_basis = market_cap_df[
        ["ticker", "market_cap", "transformed_market_cap", "new_coin"]
    ].copy()
    estimation_basis["core_universe"] = np.where(
        estimation_basis["ticker"].isin(in_universe), 1, 0
    )
    return estimation_basis, univ_first_appearence
