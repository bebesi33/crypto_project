from typing import List
import pandas_datareader as pdr
import logging
from pandas.tseries.offsets import BDay
from datetime import timedelta
import datetime
import pandas as pd
import yfinance as yf

logger = logging.getLogger(__name__)


def get_risk_free_rate_history(estimation_dates: List[datetime.date]) -> pd.DataFrame:
    """_summary_

    Args:
        estimation_dates (List[datetime.date]): _description_

    Returns:
        pd.DataFrame: _description_
    """

    # first get SOFR from FED through pandas_datareader
    sofr_symbol = "SOFR"
    data_source = "fred"
    risk_free_rate_data = pdr.DataReader(
        sofr_symbol, data_source, str(min(estimation_dates) - timedelta(10))
    ).reset_index()
    risk_free_rate_data.rename(
        columns={"DATE": "date", "SOFR": "risk_free_rate"}, inplace=True
    )
    # second get 3M treasury rate for ealier time periods
    # Note: SOFR start date was in April 2018, hence for longer horizon we need another close to risk free rate
    treasury_3m_symbol = "^IRX"
    treasury_data = yf.download(
        tickers=treasury_3m_symbol,
        start=str(min(estimation_dates) - timedelta(100)),
        end=str(max(estimation_dates)),
        interval="1d",
    )
    treasury_data = treasury_data.reset_index()[["Date", "Close"]].rename(
        columns={"Date": "date", "Close": "risk_free_rate"}
    )
    first_sofr_date = min(risk_free_rate_data["date"])
    logger.info(
        f"First SOFR date is {first_sofr_date}, before this date, the 3M US Treasury rate is used as risk free rate."
    )
    treasury_data = treasury_data[
        treasury_data["date"] <= min(risk_free_rate_data["date"])
    ].copy()
    logger.info(f"3M US Treasury rate is used for {len(treasury_data)} trading days.")

    # third: crypto trades on weekends, while ON rates and treasury do not
    # this means that Friday's ON data should be applicable between Friday and Modnay for Treasury
    # and Monday's SOFR should be applciable for the preceeding weekend
    risk_free_rate_data = risk_free_rate_data.set_index("date").reindex(
        pd.date_range(
            start=risk_free_rate_data["date"].min(),
            end=max(estimation_dates),
        )
    )
    risk_free_rate_data["risk_free_rate"] = risk_free_rate_data[
        "risk_free_rate"
    ].fillna(method="backfill")
    risk_free_rate_data["date"] = risk_free_rate_data.index
    risk_free_rate_data.reset_index(inplace=True, drop=True)

    treasury_data = (
        treasury_data.set_index("date")
        .reindex(
            pd.date_range(
                start=treasury_data["date"].min(), end=treasury_data["date"].max()
            )
        )
        .copy()
    )
    treasury_data["risk_free_rate"] = treasury_data["risk_free_rate"].fillna(
        method="ffill"
    )
    treasury_data["date"] = list(treasury_data.index)
    treasury_data.reset_index(inplace=True, drop=True)

    # four: these ON rates are between T and T+1. or in case of treasury between T and T+90 or so...
    # This means that we need to adjust day T's crypto currency return by day T-1's risk free rate.
    # E.g. a BTC total return presented for 2023.03.04 is calcualted using close price in 2023.03.04 - 2023.03.03.
    # Hence for 2023.03.04 total returns the preceeding day's ON return should be used
    # so for treasury data we need to bring the rate forward 1 day
    treasury_data["date"] = treasury_data["date"] + timedelta(1)

    risk_free_rate_data = pd.concat(
        [
            treasury_data[
                treasury_data["date"] < risk_free_rate_data["date"].min()
            ].copy(),
            risk_free_rate_data,
        ]
    )
    # finally if for the last estim days SOFR is not available, we ffwd the lates
    risk_free_rate_data["risk_free_rate"].fillna(method="ffill", inplace=True)
    return risk_free_rate_data
