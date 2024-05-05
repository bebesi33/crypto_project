import unittest
import pandas as pd
import numpy as np
from factor_model.risk_calculations.portfolio_output import assemble_portfolios_into_df


class TestAssemblePortfoliosIntoDF(unittest.TestCase):
    def test_empty_portfolios(self):
        portfolios = {}
        result_df = assemble_portfolios_into_df(portfolios)
        expected_df = pd.DataFrame(columns=["symbol", "portfolio", "benchmark", "active"])
        self.assertTrue(result_df.equals(expected_df))

    def test_multiple_portfolios(self):
        portfolios = {
            "portfolio": {"A1": 0.5, "B2": 0.3, "C1": 0.2},
            "market": {"A1": 0.4, "B2": 0.4, "C1": 0.2},
            "active": {"A1": 0.1, "B2": -0.1, "C1": 0.0}
        }
        result_df = assemble_portfolios_into_df(portfolios)
        expected_df = pd.DataFrame({
            "symbol": ["A1", "B2", "C1"],
            "portfolio": [0.5, 0.3, 0.2],
            "benchmark": [0.4, 0.4, 0.2],
            "active": [0.1, -0.1, 0.0]
        })
        self.assertTrue(result_df.equals(expected_df))

if __name__ == "__main__":
    unittest.main()