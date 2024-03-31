import unittest
from factor_model.risk_calculations.specific_risk import (
    generate_raw_portfolio_specific_risk,
)


class TestGenerateRawPortfolioSpecificRisk(unittest.TestCase):
    def test_portfolio_specific_risk(self):
        spec_std = {"T1": 0.15, "T2": 0.12, "T3": 0.18, "T4": None}
        portfolio_details = {"T1": 0.4, "T2": 0.3, "T3": 0.2, "T4": 0.1}

        actual_result = generate_raw_portfolio_specific_risk(
            spec_std, portfolio_details
        )

        self.assertAlmostEqual(actual_result, 0.0874325136, places=6)


if __name__ == "__main__":
    unittest.main()
