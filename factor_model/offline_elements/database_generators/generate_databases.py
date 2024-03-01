import sqlite3
import os
from typing import Dict

RAW_DATA_DB = "raw_price_data.db"


def refresh_raw_price_database(price_data_map: Dict, database_location: str):
    try:
        os.remove(os.path.join(database_location, RAW_DATA_DB))
    except Exception:
        pass
    with sqlite3.connect(os.path.join(database_location, RAW_DATA_DB)) as conn:
        for key in price_data_map:
            df_temp = price_data_map[key].copy()
            df_temp["symbol"] = key
            df_temp.columns = [col.lower().replace(" ","_") for col in df_temp.columns]
            df_temp.to_sql(
                "raw_price_data", conn, if_exists="append", index=False
            )
