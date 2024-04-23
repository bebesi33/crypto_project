import pandas as pd


def create_ewma_std_estimates(
    df: pd.DataFrame, halflife: float = 365, min_periods: int = 20, mean_to_zero: bool=False
) -> pd.DataFrame:
    if mean_to_zero:
        return df.pow(2).ewm(halflife=halflife, min_periods=min_periods).mean().pow(0.5).dropna()
    else:
        return df.ewm(halflife=halflife, min_periods=min_periods).std().dropna()
