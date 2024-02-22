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
            price_data_map[key].to_sql(
                "raw_price_data", conn, if_exists="append", index=False
            )
