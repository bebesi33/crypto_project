import pandas as pd
import unittest
from model_update.styles.volume_based import generate_x_month_aggregate_volume

class TestGenerateVolume(unittest.TestCase):
    def test_generate_volume(self):
        # Create sample price data map
        price_data_map = {
            "BTC-USD": pd.DataFrame({
                "date": pd.date_range(start="2022-01-01", periods=100),
                "Volume": [1000] * 100
            })
        }

        # Call the function
        result = generate_x_month_aggregate_volume(price_data_map, x_len=3, month_len=20)

        # Assert expected output
        self.assertTrue(abs(sum(result["BTC-USD"]["exposure"]) - 2.400000)<0.000001)
        self.assertEqual(len(result["BTC-USD"]), 40)  # Check the length of the resulting DataFrame

if __name__ == "__main__":
    unittest.main()