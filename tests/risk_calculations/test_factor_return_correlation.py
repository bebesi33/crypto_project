import unittest
import pandas as pd
from factor_model.risk_calculations.factor_covariance import get_factor_return_correlation


class TestFactorReturnCorrelation(unittest.TestCase):
    def setUp(self):
        self.factor_returns_data = pd.DataFrame(
            {
                "date": ["2024-03-01", "2024-03-02", "2024-03-03"],
                "factor1": [0.01, 0.02, 0.03],
                "factor2": [-0.02, 0.01, 0.02],
            }
        )

    def factor_return_correlation_test_1(self):
        params = {"date": "2024-03-03", "correlation_half_life": 10}
        result = get_factor_return_correlation(self.factor_returns_data, params)
        self.assertTrue(abs(result["factor2"].values[0] - 0.95990131006) < 0.000001)
        self.assertTrue(result.shape[0] > 0)

    def tesfactor_return_correlation_test_2(self):
        params = {"date": "2024-03-03", "correlation_half_life": 1}
        result = get_factor_return_correlation(self.factor_returns_data, params)
        self.assertTrue(abs(result["factor2"].values[0] - 0.950933) < 0.000001)
        self.assertTrue(result.shape[0] > 0)


if __name__ == "__main__":
    unittest.main()
