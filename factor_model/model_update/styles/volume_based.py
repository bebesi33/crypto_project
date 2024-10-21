import pandas as pd


def generate_x_month_aggregate_volume(
    price_data_map: dict[str, pd.DataFrame], x_len: int = 12, month_len: int = 30
) -> dict[str, pd.DataFrame]:
    """
    Volume style calculation logic
    Generates an aggregate volume for each item in the price data map over a rolling window of x months.

    Args:
        price_data_map (dict[str, pd.DataFrame]): A dictionary where keys are strings representing assets or categories,
            and values are pandas DataFrames containing the columns 'date' and 'Volume'.
        x_len (int, optional): The number of months for the rolling aggregation. Defaults to 12.
        month_len (int, optional): The number of days representing one month. Defaults to 30.

    Returns:
        dict[str, pd.DataFrame]: A dictionary where keys are the same as in the input map, and values are DataFrames
            containing the 'date' and 'exposure' (aggregated volume) columns. The 'exposure' represents the rolling
            sum of the 'Volume' column divided by 1,000,000 to scale the values.
    """
    return_map = {}
    for key in price_data_map.keys():
        volume_rolling = (
            price_data_map[key]["Volume"].rolling(x_len * month_len).sum() / 1000000
        )
        df_temp = pd.DataFrame(
            {
                "date": price_data_map[key]["date"].tail(-x_len * month_len),
                "exposure": volume_rolling,
            }
        )
        df_temp["exposure"] = df_temp["exposure"].fillna(0.0)
        return_map[key] = df_temp.tail(-x_len * month_len)
    return return_map
