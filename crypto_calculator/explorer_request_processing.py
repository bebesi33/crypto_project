import json
from typing import Dict, List, Tuple
from crypto_calculator.models import RawPriceData, Returns
import pandas as pd

from factor_model.risk_calculations import HALF_LIFE_DEFAULT, MIN_OBS_DEFAULT
from factor_model.risk_calculations.parameter_processing import check_input_param_correctness


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
    override_code += check_input_param_correctness(
        parameter_name="halflife",
        parameter_default=HALF_LIFE_DEFAULT,
        parameter_nickname="half-life",
        all_input=all_input,
        log_elements=log_elements,
        processed_input=processed_input,
    )

    override_code += check_input_param_correctness(
        parameter_name="min_obs",
        parameter_default=MIN_OBS_DEFAULT,
        parameter_nickname="minimum number of observations for risk calculation",
        all_input=all_input,
        log_elements=log_elements,
        processed_input=processed_input,
        integer_conversion=True
    )
    return processed_input, log_elements, override_code
