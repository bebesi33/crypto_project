import unittest
import pandas as pd
import numpy as np
from factor_model.risk_calculations.factor_covariance import assemble_factor_covariance_matrix

class TestFactorCovarianceMatrix(unittest.TestCase):
    def test_covariance_matrix(self):
        std = pd.Series({
            "factor1": 0.02,
            "factor2": 0.015
        })

        correlation = pd.DataFrame({
            "factor1": [1.0, 0.7],
            "factor2": [0.7, 1.0]
        })

        result = assemble_factor_covariance_matrix(std, correlation)

        expected_cov_factor1_factor1 = 0.0004
        expected_cov_factor1_factor2 = 0.00021
        expected_cov_factor2_factor2 = 0.000225

        self.assertAlmostEqual(result.loc["factor1", "factor1"], expected_cov_factor1_factor1, places=6)
        self.assertAlmostEqual(result.loc["factor1", "factor2"], expected_cov_factor1_factor2, places=6)
        self.assertAlmostEqual(result.loc["factor2", "factor2"], expected_cov_factor2_factor2, places=6)

if __name__ == "__main__":
    unittest.main()