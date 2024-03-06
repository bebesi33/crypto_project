import sqlite3
import os
from typing import Dict
import pandas as pd
from factor_model.model_update.database_generators import RAW_DATA_DB


def refresh_database(
    symbol_level_data: Dict[str, pd.DataFrame],
    database_location: str,
    database_name: str = RAW_DATA_DB,
    database_table_name: str = "raw_price_data",
    key_field_name: str = "symbol",
    update_mode: str = "append",
    delete_database: bool = True,
):
    """
    Refreshes the database with new data.

    Args:
        symbol_level_data (Dict): A dictionary containing pd.DataFrames as values.
        database_location (str): The location where the database file will be stored.
        database_name (str, optional): Name of the database file. Defaults to RAW_DATA_DB.
        database_table_name (str, optional): Name of the database table. Defaults to "raw_price_data".
        key_field_name (str, optional): Name of the key field in the data. Defaults to "symbol".
        update_mode (str, optional): Update mode for existing data. Defaults to "append".
        delete_database (bool, optional): Whether to delete the existing database file. Defaults to True.
    """
    if delete_database:
        try:
            os.remove(os.path.join(database_location, database_name))
        except Exception:
            pass
    with sqlite3.connect(os.path.join(database_location, database_name)) as conn:
        for key in symbol_level_data:
            df_temp = symbol_level_data[key].copy()
            df_temp[key_field_name] = key
            df_temp.columns = [col.lower().replace(" ", "_") for col in df_temp.columns]
            df_temp.reset_index(inplace=True)
            df_temp.rename(
                columns={"index": "id"}, inplace=True
            )  # for some reason django needs an id col
            df_temp.to_sql(
                database_table_name, conn, if_exists=update_mode, index=False
            )
