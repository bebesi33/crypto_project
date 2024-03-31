import unittest
import pandas as pd
import numpy as np
from factor_model.risk_calculations.risk_attribution import generate_factor_covariance_attribution

class TestGenerateFactorCovarianceAttribution(unittest.TestCase):
    def test_no_market_exposure(self):
        # Create sample data
        port_exposure = pd.DataFrame({
            "exposure": [0.5, 0.3, 0.2],
        }, index=["A", "B", "C"])
        factor_covariance = pd.DataFrame({
            "A": [0.1, 0.2, 0.3],
            "B": [0.2, 0.4, 0.5],
            "C": [0.3, 0.5, 0.7],
        }, index=["A", "B", "C"])

        # Call the function
        factor_std, factor_attribution = generate_factor_covariance_attribution(
            port_exposure, factor_covariance
        )

        # Assertions
        self.assertAlmostEqual(factor_std, 0.51865209919, places=6)
        #self.assertEqual(factor_attribution, 3)
