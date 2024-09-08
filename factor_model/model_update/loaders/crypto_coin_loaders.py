import pandas as pd
from requests_html import HTMLSession


def grab_yahoo_finance_symbols() -> list[str]:
    """Loads available crypto tickers from Yahoo Finance

    Returns:
        list[str]: list of tickers
    """
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
) -> list[str]:
    """Loads available crypto tickers from Yahoo Finance

    Args:
        max_number_of_crypto (int, optional): maximum nubmer of coins retrieved. Defaults to 3000.

    Returns:
        list[str]: List of tickers
    """
    html_session = HTMLSession()
    currency_increment = 50  # this is the upper limit
    all_tickers = list()
    offset = 0
    for _ in range(0, int(max_number_of_crypto / currency_increment) + 1):

        resp = html_session.get(
            # f"https://finance.yahoo.com/crypto?count={currency_increment}&offset={offset}"
            f"https://finance.yahoo.com/markets/crypto/all/?start={offset}&count={currency_increment}"
        )
        tables = pd.read_html(resp.html.raw_html)
        df = tables[0].copy()
        tickers = df.Symbol.tolist()
        offset += currency_increment
        all_tickers = all_tickers + tickers
    # post processing if ticket contains spaces we use only the first half (true ticker)
    # e.g.: 0X0-USD 0x0.ai USD translates to 0X0-USD
    processed_tickers = []
    for ticker in all_tickers:
        if ticker.find(" ") > -1:
            processed_tickers.append(ticker.split(" ")[0])
        else:
            processed_tickers.append(ticker)
    return processed_tickers


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


def get_ticker_list() -> list[str]:
    """Merges historic ticker list with latest ticker list from Yahoo Finance

    Returns:
        list[str]: ticker list
    """
    return sorted(list(set(TICKER_LIST + grab_yahoo_finance_symbols())))


def get_extended_ticker_list(max_number_of_crypto: int = 3000) -> list[str]:
    """"Merges historic ticker list with latest ticker list from Yahoo Finance

    Args:
        max_number_of_crypto (int, optional): _description_. Defaults to 3000.

    Returns:
        list[str]: list of tickers
    """
    return sorted(
        list(
            set(
                TICKER_LIST
                + grab_all_yahoo_finance_crypto_symbols(max_number_of_crypto)
            )
        )
    )
