import pandas as pd
import unittest
from risk_calculations.factor_covariance import get_factor_return_standard_deviation

class TestFactorReturnStandardDeviation(unittest.TestCase):
    def test_ewma_standard_deviations(self):
        factor_returns = pd.DataFrame({
            "date": ["2024-03-08", "2024-03-09", "2024-03-10"],
            "factor1": [0.02, 0.03, 0.01],
            "factor2": [0.015, 0.0125, 0.03212]
        })

        parameters = {
            "date": "2024-03-09",
            "variance_half_life": 3
        }

        result = get_factor_return_standard_deviation(factor_returns, parameters)

        expected_std_factor1 = 0.007071067811865475
        expected_std_factor2 = 0.0017677669529663682

        self.assertTrue(abs(result["factor1"]-expected_std_factor1) < 0.000001)
        self.assertTrue(abs(result["factor2"]-expected_std_factor2) < 0.000001)

if __name__ == "__main__":
    unittest.main()
