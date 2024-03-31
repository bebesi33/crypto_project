import json
from typing import Dict, Tuple
from crypto_calculator.models import RawPriceData, Returns
import pandas as pd

from factor_model.risk_calculations import HALF_LIFE_DEFAULT, MIN_OBS_DEFAULT


def get_close_data(symbol: str) -> pd.DataFrame:
    raw_price_data = RawPriceData.objects.filter(symbol=symbol).values("close", "date")
    df = pd.DataFrame(list(raw_price_data))
    if len(list(raw_price_data)) > 0:
        df["date"] = df["date"].apply(lambda x: x.strftime("%Y-%m-%d"))
        df.set_index("date", inplace=True, drop=True)
    return df


def get_return_data(symbol: str) -> pd.DataFrame:
    return_data = (
        Returns.objects.using("returns")
        .filter(symbol=symbol)
        .values("total_return", "date")
    )
    df = pd.DataFrame(list(return_data))
    df["date"] = df["date"].apply(lambda x: x.strftime("%Y-%m-%d"))
    df.set_index("date", inplace=True, drop=True)
    return df


def decode_explorer_input(request) -> Tuple[Dict, str, int]:
    all_input = json.loads(request.body.decode("utf-8"))
    log_elements = list()
    processed_input = {}

    # symbol checks
    symbol = all_input.get("symbol")
    if symbol is not None and len(symbol) > 0:
        processed_input["symbol"] = symbol
        log_elements.append(f"The input '{symbol}' is parsed as a smybol.")
    else:
        log_elements.append(f"No Symbol input!")

    override_code = 0  # we set it to one if any override occurs

    # half life checks
    halflife = all_input.get("halflife")
    if halflife is not None:
        try:
            halflife = float(halflife)
            if halflife < 0.0001:
                log_elements.append(
                    f"In half-life smaller than 0.01: {halflife}, half-life set to default {HALF_LIFE_DEFAULT} days."
                )
                halflife = HALF_LIFE_DEFAULT
                override_code = 1
                log_elements.append("The half-life should be a positive number.")
            else:
                log_elements.append(f"The half-life input {halflife} is correct.")
        except ValueError:
            log_elements.append(
                f"Incorrect half-life value: {halflife}, half-life is set to default {HALF_LIFE_DEFAULT} days."
            )
            halflife = HALF_LIFE_DEFAULT
            override_code = 1
        processed_input["halflife"] = halflife
    else:
        log_elements.append(f"No half-life input!")

    min_obs = all_input.get("min_obs")
    if min_obs is not None:
        try:
            min_obs = float(min_obs)
            if min_obs < 0.0001:
                log_elements.append(
                    f"In minimum observation number is smaller than 0.0001: {min_obs}, minimum observation number is set to default {MIN_OBS_DEFAULT} days."
                )
                min_obs = MIN_OBS_DEFAULT
                log_elements.append(
                    "The minimum observation number should be a positive integer number."
                )
                override_code = 1
            else:
                log_elements.append(
                    f"The minimum observation number input {min_obs} is correct."
                )
        except ValueError:
            log_elements.append(
                f"Incorrect minimum observation number value: {min_obs}, minimum observation number is set to default {MIN_OBS_DEFAULT} days."
            )
            min_obs = MIN_OBS_DEFAULT
            override_code = 1

        processed_input["min_obs"] = min_obs
    else:
        log_elements.append(f"No minimum number of observations input!")
    return processed_input, log_elements, override_code
