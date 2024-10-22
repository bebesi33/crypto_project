import pandas as pd
import numpy as np
import unittest

from factor_model.risk_calculations.excess_return_manipulation import (
    generate_processed_excess_returns,
)


class TestGenerateProcessedExcessReturns(unittest.TestCase):
    def test_generate_processed_excess_returns(self):
        # Create sample dataframes
        return_data = pd.DataFrame(
            {
                "date": ["2022-01-01", "2022-01-02", "2022-01-01", "2022-01-02"],
                "symbol": ["A1", "A1", "A2", "A2"],
                "excess_return": [0.02, np.nan, 0.01, np.nan],
            }
        )

        fill_miss_data = pd.DataFrame(
            {"date": ["2022-01-01", "2022-01-02"], "proxy_return": [0.015, 0.03]}
        )

        # Call the function
        result_df = generate_processed_excess_returns(return_data, fill_miss_data)
        # Assert that the result dataframe has the expected columns
        expected_columns = ["date", "A1", "A2"]
        self.assertListEqual(list(result_df.columns), expected_columns)
        self.assertListEqual(list(result_df["A1"]), [0.02, 0.03])
        self.assertListEqual(list(result_df["A2"]), [0.01, 0.03])


if __name__ == "__main__":
    unittest.main()
