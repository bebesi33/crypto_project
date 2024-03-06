import requests
import pandas as pd
from requests_html import HTMLSession
from typing import List


def grab_yahoo_finance_symbols() -> List[str]:
    html_session = HTMLSession()
    currency_limit = 100  # this is the upper limit

    resp = html_session.get(
        f"https://finance.yahoo.com/crypto?offset=0&count={currency_limit}"
    )
    tables = pd.read_html(resp.html.raw_html)
    df = tables[0].copy()
    tickers = df.Symbol.tolist()
    return tickers


def grab_all_yahoo_finance_crypto_symbols(
    max_number_of_crypto: int = 3000,
) -> List[str]:
    html_session = HTMLSession()
    currency_increment = 100  # this is the upper limit
    all_tickers = list()
    offset = 0
    for i in range(0, int(max_number_of_crypto / 100) + 1):

        resp = html_session.get(
            f"https://finance.yahoo.com/crypto?count={currency_increment}&offset={offset}"
        )
        tables = pd.read_html(resp.html.raw_html)
        df = tables[0].copy()
        tickers = df.Symbol.tolist()
        offset += 100
        all_tickers = all_tickers + tickers
    return all_tickers


# to be kept for historical reason
TICKER_LIST = [
    "BTC-USD",
    "ETH-USD",
    "USDT-USD",
    "BNB-USD",
    "XRP-USD",
    "USDC-USD",
    "STETH-USD",
    "ADA-USD",
    "DOGE-USD",
    "SOL-USD",
    "WTRX-USD",
    "WKAVA-USD",
    "TRX-USD",
    "DOT-USD",
    "TON11419-USD",
    "MATIC-USD",
    "DAI-USD",
    "LTC-USD",
    "SHIB-USD",
    "WBTC-USD",
    "BCH-USD",
    "AVAX-USD",
    "LEO-USD",
    "XLM-USD",
    "LINK-USD",
    "BUSD-USD",
    "TUSD-USD",
    "UNI7083-USD",
    "XMR-USD",
    "OKB-USD",
    "ATOM-USD",
    "ETC-USD",
    "HBAR-USD",
    "WHBAR-USD",
    "ICP-USD",
    "FIL-USD",
    "BTCB-USD",
    "LDO-USD",
    "MNT27075-USD",
    "APT21794-USD",
    "CRO-USD",
    "ARB11841-USD",
    "QNT-USD",
    "VET-USD",
    "NEAR-USD",
    "OP-USD",
    "MKR-USD",
    "WEOS-USD",
    "AAVE-USD",
    "GRT6719-USD",
]


def get_ticker_list() -> List[str]:
    return sorted(list(set(TICKER_LIST + grab_yahoo_finance_symbols())))


def get_extended_ticker_list(max_number_of_crypto: int = 3000) -> List[str]:
    return sorted(
        list(
            set(
                TICKER_LIST
                + grab_all_yahoo_finance_crypto_symbols(max_number_of_crypto)
            )
        )
    )
