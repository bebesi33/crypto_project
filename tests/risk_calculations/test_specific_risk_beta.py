import unittest
import pandas as pd
from factor_model.risk_calculations.risk_attribution import get_specific_risk_beta

class TestGetSpecificRiskBeta(unittest.TestCase):
    def setUp(self):
        self.portfolio_details = {
            "BTC-USD": 0.4,
            "ETH-USD": 0.3,
            "LNC-USD": 0.2
        }

        self.market_portfolio = {
            "BTC-USD": 0.2,
            "ETH-USD": 0.5,
            "LNC-USD": 0.3
        }

        self.spec_risk = {
            "BTC-USD": 0.02,
            "ETH-USD": 0.015,
            "LNC-USD": 0.018
        }

    def test_get_specific_risk_beta(self):
        result = get_specific_risk_beta(self.portfolio_details, self.market_portfolio, self.spec_risk)
        self.assertIsInstance(result, float)
        self.assertAlmostEqual(result, 9.465555555555556e-05, places=6)

if __name__ == "__main__":
    unittest.main()