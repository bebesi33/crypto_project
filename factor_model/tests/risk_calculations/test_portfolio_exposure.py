import unittest
import pandas as pd
from risk_calculations.risk_attribution import create_portfolio_exposures  # Replace 'your_module' with the actual module name

class TestCreatePortfolioExposures(unittest.TestCase):
    def setUp(self):
        # Create a sample exposures DataFrame
        self.exposures = pd.DataFrame({
            "ticker": ["C1", "C2", "C3"],
            "momentum": [0.1, 0.2, 0.3],
            "volume": [0.4, 0.5, 0.6]
        })

        # Create a sample portfolio details dictionary
        self.portfolio_details = {
            "C1": 0.4,
            "C2": 0.3,
            "C3": 0.3
        }
        self.non_exposure_fields = [
            "id",
            "ticker",
            "return",
            "core_universe",
            "transformed_market_cap",
            "date",
        ]

    def test_create_portfolio_exposures(self):
        result = create_portfolio_exposures(self.exposures, self.portfolio_details, self.non_exposure_fields)

        self.assertIsInstance(result, pd.DataFrame)

        expected_exposure = {
            "momentum": 0.19,  # (0.4 * 0.1) + (0.3 * 0.2) + (0.3 * 0.3)
            "volume": 0.49,  # (0.4 * 0.4) + (0.3 * 0.5) + (0.3 * 0.6)
            "market": 1.0
        }
        for col in expected_exposure.keys():
            self.assertAlmostEqual(result[result.index==col].values[0][0], expected_exposure[col], places=6)

if __name__ == "__main__":
    unittest.main()

    