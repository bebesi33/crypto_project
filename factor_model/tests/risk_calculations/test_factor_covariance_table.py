import unittest
import pandas as pd
import numpy as np
from risk_calculations.risk_attribution import generate_factor_covariance_table

class TestGenerateFactorCovarianceTable(unittest.TestCase):
    def setUp(self):
        self.port_exposure = pd.DataFrame({
            "exposure": [0.5, 0.8, 1.2]
        }, index=["A", "B", "C"])

        self.factor_covariance = pd.DataFrame({
            "A": [0.01, 0.02, 0.03],
            "B": [0.02, 0.04, 0.05],
            "C": [0.03, 0.05, 0.06]
        }, index=["A", "B", "C"])

    def test_generate_factor_covariance_table(self):
        result = generate_factor_covariance_table(self.port_exposure, self.factor_covariance)

        self.assertIsInstance(result, pd.DataFrame)

        self.assertListEqual(result.columns.tolist(), self.factor_covariance.columns.tolist())
        self.assertListEqual(result.index.tolist(), self.factor_covariance.index.tolist())

        expected_covar = np.diag(self.port_exposure["exposure"]).dot(self.factor_covariance).dot(np.diag(self.port_exposure["exposure"]))
        np.testing.assert_array_almost_equal(result.values, expected_covar, decimal=6)

if __name__ == "__main__":
    unittest.main()
