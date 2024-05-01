import unittest
import pandas as pd
from factor_model.risk_calculations.risk_attribution import (
    generate_mctr_chart_input,
    generate_mctr_chart_input_reduced,
)


class TestGenerateMctrChartInput(unittest.TestCase):
    def test_generate_mctr_chart_input(self):
        portfolios = {
            "portfolio": {"factor1": 0.1, "factor2": 0.2},
            "active": {"factor1": 0.15, "factor3": 0.3},
        }
        factor_mctrs = {
            "portfolio": pd.Series({"factor1": 0.1, "factor2": 0.2, "factor3": 0.3}),
            "active": pd.Series({"factor1": 0.15, "factor3": 0.3}),
        }
        spec_risk_mctrs = {
            "portfolio": pd.Series({"factor2": 0.2, "factor4": 0.4}),
            "active": pd.Series({"factor3": 0.3, "factor5": 0.5}),
        }

        expected_result = {
            "portfolio": {"factor1": 0.1, "factor3": 0.3, "factor5": 0},
            "active": {"factor1": 0.15, "factor3": 0.3, "factor5": 0.5},
        }

        reduced_expected_result = {
            "portfolio": {"factor1": 0.1, "factor3": 0.3},
            "active": {"factor1": 0.15, "factor3": 0.3},
        }

        result_mctr = generate_mctr_chart_input(
            portfolios, factor_mctrs, spec_risk_mctrs
        )

        reduced_result_mctr = generate_mctr_chart_input_reduced(
            portfolios, factor_mctrs
        )
        self.assertEqual(str(result_mctr.keys()), str(expected_result.keys()))
        for port in result_mctr.keys():
            for factor in result_mctr[port]:
                self.assertEqual(
                    result_mctr[port][factor], expected_result[port][factor]
                )
        self.assertEqual(
            str(reduced_result_mctr.keys()), str(reduced_expected_result.keys())
        )
        for port in reduced_result_mctr.keys():
            for factor in reduced_result_mctr[port]:
                self.assertEqual(
                    reduced_result_mctr[port][factor],
                    reduced_expected_result[port][factor],
                )


if __name__ == "__main__":
    unittest.main()
