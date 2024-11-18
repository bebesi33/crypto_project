from json import JSONDecodeError
from factor_model.utilities.common_utility import convert_str_numbs_to_float
import logging
import pandas as pd
import yfinance as yf
import time
logger = logging.getLogger(__name__)


def generate_market_cap_only(ticker_map: dict):
    market_caps = list()
    for ticker in ticker_map.keys():
        try:
            crypto_info = yf.Ticker(ticker).info
            market_caps.append(
                pd.DataFrame({"ticker": [ticker], "market_cap": [crypto_info["marketCap"]]})
            )
        except KeyError:
            logger.info(f"No data for ticker: {ticker}")
        except JSONDecodeError:
            logger.info(f"No data for ticker: {ticker}. JsonDecoder problems...")
        time.sleep(1)
    return pd.concat(market_caps)


def generate_market_cap_data(ticker_map: dict):
    col_name_map = {
        "Market Cap": "market_cap",
        "Circulating Supply": "in_circulation",
        "Max Supply": "max_supply",
        "Volume": "volume",
        "Volume (24hr)": "volume_24h",
        "Volume (24hr) All Currencies": "volume_24h_all_ccy",
    }
    market_caps = list()
    for ticker in ticker_map.keys():
        try:
            temp_df = (
                ticker_map[ticker]
                .get_institutional_holders()
                .set_index(0)
                .T.rename(columns=col_name_map)
            )
            temp_df["ticker"] = ticker
            market_caps.append(temp_df)
        except (AttributeError, KeyError):
            logger.info(f"No data for ticker: {ticker}")
    market_cap_df = pd.concat(market_caps)
    market_cap_df.drop(columns=["max_supply"], inplace=True)
    for col in market_cap_df.columns[:-1]:
        market_cap_df[col + "_t"] = market_cap_df[col].apply(
            lambda x: convert_str_numbs_to_float(x)
        )
        market_cap_df.drop(columns=[col], inplace=True)
        market_cap_df.rename(columns={col + "_t": col}, inplace=True)
    return market_cap_df
