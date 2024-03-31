import unittest
import pandas as pd
from factor_model.risk_calculations.core_universe_portfolio import generate_market_portfolio  # Replace with the actual module name

class TestGenerateMarketPortfolio(unittest.TestCase):
    def test_market_portfolio_calculation(self):
        # Create a sample exposure DataFrame
        exposure_data = {
            "core_universe": [1, 0, 1, 1],
            "ticker": ["C1", "C2", "C3", "C4"],
            "transformed_market_cap": [1000, 2000, 1500, 1800],
        }
        exposure_df = pd.DataFrame(exposure_data)

        # Calculate the market portfolio
        result = generate_market_portfolio(exposure_df)

        # Expected weights based on the sample data
        expected_weights = {
            "C1": 0.2325581395,
            "C3": 0.3488372093,
            "C4": 0.4186046511,
        }

        # Check if the calculated weights match the expected weights
        for ticker, expected_weight in expected_weights.items():
            self.assertAlmostEqual(result[ticker], expected_weight, places=6)

if __name__ == "__main__":
    unittest.main()