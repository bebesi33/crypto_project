import requests
import pandas as pd
from requests_html import HTMLSession
from typing import List


def grab_yahoo_finance_symbols() -> List[str]:
    html_session = HTMLSession()
    currency_limit = 250  # this is the upper limit
    resp = html_session.get(
        f"https://finance.yahoo.com/crypto?offset=0&count={currency_limit}"
    )
    tables = pd.read_html(resp.html.raw_html)
    df = tables[0].copy()
    tickers = df.Symbol.tolist()
    return tickers


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


def get_ticker_list():
    return sorted(list(set(TICKER_LIST + grab_yahoo_finance_symbols())))
