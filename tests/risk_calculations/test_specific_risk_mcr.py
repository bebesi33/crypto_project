import unittest
from factor_model.risk_calculations.risk_attribution import calculate_spec_risk_mctr
import pandas as pd


class TestCalculateSpecRiskMctr(unittest.TestCase):
    def setUp(self):
        # Create sample data for testing
        self.spec_std = {"C1": 0.1, "C2": 0.08, "C3": 0.12}

        self.portfolio_details = {"C1": 0.4, "C2": 0.3, "C3": 0.3}
        self.expected_var_contrib = {"C1": 0.001600, "C2": 0.000576, "C3": 0.001296}
        self.expected_mctr = {"C1": 0.00400, "C2": 0.00192, "C3": 0.00432}

    def test_calculate_spec_risk_mctr(self):
        # Call the function with sample data
        mctr, var_contrib = calculate_spec_risk_mctr(
            self.spec_std, self.portfolio_details
        )

        # Check if the output is a dictionary
        self.assertIsInstance(mctr, pd.Series)
        self.assertIsInstance(var_contrib, pd.Series)

        var_contrib = var_contrib.to_dict()
        mctr = mctr.to_dict()
        # # Check if the keys match the tickers
        self.assertSetEqual(set(mctr.keys()), set(self.spec_std.keys()))
        self.assertSetEqual(set(var_contrib.keys()), set(self.spec_std.keys()))

        # # Check if the values are non-negative
        for ticker in mctr.keys():
            self.assertAlmostEqual(
                var_contrib[ticker], self.expected_var_contrib[ticker], places=6
            )
            self.assertAlmostEqual(mctr[ticker], self.expected_mctr[ticker], places=6)

        # Check if the sum of weights is approximately 1
        total_weight = sum(self.portfolio_details.values())
        self.assertAlmostEqual(total_weight, 1, places=6)


if __name__ == "__main__":
    unittest.main()
