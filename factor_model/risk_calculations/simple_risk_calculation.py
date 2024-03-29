import pandas as pd


def create_ewma_std_estimates(
    df: pd.DataFrame, halflife: float = 365, min_periods: int = 20
) -> pd.DataFrame:
    return df.ewm(halflife=halflife, min_periods=min_periods).std().dropna()
