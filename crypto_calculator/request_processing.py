from crypto_calculator.models import RawPriceData, Returns
import pandas as pd

def get_close_data(symbol : str) -> pd.DataFrame:
    raw_price_data = RawPriceData.objects.filter(symbol=symbol).values("close", "date")
    df = pd.DataFrame(list(raw_price_data))
    df["date"] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
    df.set_index("date", inplace=True, drop=True)
    return df


def get_return_data(symbol : str) -> pd.DataFrame:
    return_data = Returns.objects.using("returns").filter(symbol=symbol).values("total_return", "date")
    df = pd.DataFrame(list(return_data))
    df["date"] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
    df.set_index("date", inplace=True, drop=True)
    return df