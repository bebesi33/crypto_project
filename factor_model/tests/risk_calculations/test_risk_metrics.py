import unittest
import numpy as np
from scipy.stats import norm, lognorm
from risk_calculations.risk_metrics import (
    calculate_lognormal_es_var,
)


class TestCalculateLognormalESVar(unittest.TestCase):
    def test_calculate_lognormal_es_var(self):
        portfolio_std = 0.02
        confidence_level = 0.95
        expected_es = 0.04038847797307765
        expected_var = 0.03236184899838068
        es, var = calculate_lognormal_es_var(portfolio_std, confidence_level)
        self.assertAlmostEqual(es, expected_es, places=6)
        self.assertAlmostEqual(var, expected_var, places=6)

        portfolio_std = 0.01
        confidence_level = 0.99
        expected_es = 0.0262954009615457
        expected_var = 0.022994970196682618
        es, var = calculate_lognormal_es_var(portfolio_std, confidence_level)
        self.assertAlmostEqual(es, expected_es, places=6)
        self.assertAlmostEqual(var, expected_var, places=6)


if __name__ == "__main__":
    unittest.main()

