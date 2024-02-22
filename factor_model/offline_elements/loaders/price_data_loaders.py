import yfinance as yf
from typing import List, Dict


def generate_ytickets(ticker_list : List) -> Dict:
    ytickets = dict()
    for ticker in ticker_list:
        ytickets[ticker] = yf.Ticker(ticker)
    return ytickets


def generate_price_data_map(tickers : Dict, horizon: str = "10y"):
    price_data_map = dict()
    for ticker in tickers.keys():
        price_data_map[ticker] = tickers[ticker].history(
            period=horizon).reset_index()
        price_data_map[ticker]["date"] = price_data_map[ticker]["Date"].dt.date
        price_data_map[ticker].drop(columns=["Date"], inplace=True)
    return price_data_map
