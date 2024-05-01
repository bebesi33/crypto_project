import json
from typing import Dict, List, Tuple
from crypto_calculator.models import FactorReturns, RawPriceData, Returns
import pandas as pd

from factor_model.model_update.database_generators import RECOGNIZED_STYLES
from factor_model.risk_calculations import HALF_LIFE_DEFAULT, MIN_OBS_DEFAULT
from factor_model.risk_calculations.parameter_processing import (
    check_input_param_correctness,
)
from factor_model.risk_calculations.simple_risk_calculation import (
    create_ewma_std_estimates,
)


def get_close_data(symbol: str) -> pd.DataFrame:
    raw_price_data = RawPriceData.objects.filter(symbol=symbol).values("close", "date")
    df = pd.DataFrame(list(raw_price_data))
    if len(list(raw_price_data)) > 0:
        df["date"] = df["date"].apply(lambda x: x.strftime("%Y-%m-%d"))
        df.set_index("date", inplace=True, drop=True)
    return df


def get_total_return(
    symbol: str, close_price: pd.DataFrame = None, is_factor: bool = False
) -> pd.DataFrame:
    if is_factor:
        return close_price[["total_return"]]
    else:
        # total returns on symbols were subject to cleaning,
        # hence an additional query is needed
        return_data = (
            Returns.objects.using("returns")
            .filter(symbol=symbol)
            .values("total_return", "date")
        )
        df = pd.DataFrame(list(return_data))
        df["date"] = df["date"].apply(lambda x: x.strftime("%Y-%m-%d"))
        df.set_index("date", inplace=True, drop=True)
        return df


def assemble_price_data(
    symbol: str, is_factor: bool, log_elements: List[str]
) -> Tuple[pd.DataFrame, str]:
    if symbol is not None and not is_factor:
        close_price = get_close_data(symbol=symbol)
        log_elements.append(
            "Please note that for symbols (coins) the total return is presented. "
        )
    elif symbol is not None and is_factor:
        close_price = query_explorer_factor_return_data(style_name=symbol.lower())
        log_elements.append(
            "Please note that for style factors a cumulative return time series is presented as price data. "
            "This time series starts from 1 USD at the start of the estimation horizon. "
        )
    else:
        close_price = pd.DataFrame()
        symbol = "EMPTY INPUT"
        log_elements.append(
            "The symbol is not recognized, no data is queried from the database! "
        )
    return close_price, symbol


def query_explorer_factor_return_data(style_name: str) -> pd.DataFrame:
    factor_return_data = FactorReturns.objects.using("factor_model_estimates").values(
        style_name, "date"
    )
    df = pd.DataFrame(list(factor_return_data))
    df["date"] = df["date"].apply(lambda x: x.strftime("%Y-%m-%d"))
    df["close"] = (df[style_name] + 1).cumprod()
    df.rename(columns={style_name: "total_return"}, inplace=True)
    df.set_index("date", inplace=True, drop=True)
    return df[["total_return", "close"]]


def decode_explorer_input(request) -> Tuple[Dict, str, int, bool]:
    all_input = json.loads(request.body.decode("utf-8"))
    log_elements = list()
    processed_input = {}

    # symbol checks
    is_factor = False
    symbol = all_input.get("symbol")
    if symbol is not None and len(symbol) > 0 and symbol.lower() in RECOGNIZED_STYLES:
        processed_input["symbol"] = symbol
        log_elements.append(f"The input '{symbol}' is parsed as a style factor. ")
        is_factor = True
    elif (
        symbol is not None
        and len(symbol) > 0
        and symbol.lower() not in RECOGNIZED_STYLES
    ):
        processed_input["symbol"] = symbol
        log_elements.append(f"The input '{symbol}' is parsed as a symbol. ")
    else:
        log_elements.append(f"No Symbol input! ")

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
        integer_conversion=True,
    )
    processed_input["mean_to_zero"] = all_input["mean_to_zero"]
    if processed_input["mean_to_zero"]:
        log_elements.append("The demeaned returns are used for the calculation of risk. ")

    return processed_input, log_elements, override_code, is_factor


def get_ewma_estimates(
    halflife: float,
    min_periods: float,
    override_code: float,
    json_data: Dict,
    log_elements: Dict,
    returns: pd.DataFrame,
    mean_to_zero: bool = False,
):
    if halflife is not None and min_periods is not None:
        ewma_std = create_ewma_std_estimates(
            returns, halflife=halflife, min_periods=min_periods, mean_to_zero=mean_to_zero
        )
        ewma_std.rename(columns={"total_return": "ewma_std"}, inplace=True)
        # align ouput length
        returns = returns[returns.index.isin(ewma_std.index)].copy()
        json_data["return_data"] = returns.to_dict()
        json_data["ewma"] = ewma_std.to_dict()
        json_data["ERROR_CODE"] = 1 if override_code > 0 else 0
    else:
        log_elements.append(
            "Either the halflife or the minimum number of observations is incorrect, no risk estimate calculated! "
        )
        json_data["ERROR_CODE"] = 1
