import unittest
import pandas as pd
from factor_model.offline_elements.styles.return_based import (
    generate_x_month_price_change,
)


class TestGenerateVolume(unittest.TestCase):
    def setUp(self):
        # Initialize sample price data map for testing
        self.price_data_map = {
            "BTC-USD": pd.DataFrame(
                {
                    "date": pd.date_range(start="2022-01-01", periods=100),
                    "Close": [100.0 + i for i in range(100)],
                }
            )
        }

    def test_generate_x_month_price_change(self):
        result = generate_x_month_price_change(
            self.price_data_map, x_len=6, month_len=20
        )
        self.assertEqual(len(result["BTC-USD"]), 80)


if __name__ == "__main__":
    unittest.main()
