import pandas as pd
import unittest
from factor_model.risk_calculations.factor_covariance import (
    get_factor_return_standard_deviation,
)


class TestFactorReturnStandardDeviation(unittest.TestCase):
    def test_ewma_standard_deviations(self):
        factor_returns = pd.DataFrame(
            {
                "date": ["2024-03-08", "2024-03-09", "2024-03-10"],
                "factor1": [0.02, 0.03, 0.01],
                "factor2": [0.015, 0.0125, 0.03212],
            }
        )

        parameters = {
            "date": "2024-03-09",
            "variance_half_life": 3,
            "mean_to_zero": False,
        }

        result_no_mean_to_zero = get_factor_return_standard_deviation(
            factor_returns, parameters
        )

        expected_std_factor1 = 0.007071067811865475
        expected_std_factor2 = 0.0017677669529663682

        self.assertTrue(
            abs(result_no_mean_to_zero["factor1"] - expected_std_factor1) < 0.000001
        )
        self.assertTrue(
            abs(result_no_mean_to_zero["factor2"] - expected_std_factor2) < 0.000001
        )

    def test_ewma_standard_deviations_mean_to_zero(self):
        factor_returns = pd.DataFrame(
            {
                "date": ["2024-03-08", "2024-03-09", "2024-03-10"],
                "factor1": [0.12, -0.13, 0.01],
                "factor2": [0.015, -0.65, 0.08762],
            }
        )

        parameters = {
            "date": "2024-03-09",
            "variance_half_life": 3,
            "mean_to_zero": True,
        }

        result_no_mean_to_zero = get_factor_return_standard_deviation(
            factor_returns, parameters
        )

        expected_std_factor1 = 0.12567325357823317
        expected_std_factor2 = 0.48543395778914017

        self.assertTrue(
            abs(result_no_mean_to_zero["factor1"] - expected_std_factor1) < 0.000001
        )
        self.assertTrue(
            abs(result_no_mean_to_zero["factor2"] - expected_std_factor2) < 0.000001
        )


if __name__ == "__main__":
    unittest.main()
