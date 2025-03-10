import json
import sqlite3
import logging
from django.test import RequestFactory, TestCase
import pandas as pd
from crypto_calculator.tests.resources.conftest import (
    REFRESH_TEST_DB,
    REFRESH_TESTS,
    get_expected_output,
    update_expected_output,
)
from crypto_calculator.views import get_risk_calculation_output
from database_server.settings import BASE_DIR, TEST_DATABASE_LOCATION
from factor_model.utilities.common_utility import compare_dictionaries


logger = logging.getLogger(__file__)


class FactorRiskCalcToolTest(TestCase):
    databases = {
        "factor_model_estimates",
        "returns",
        "raw_price_data",
        "specific_risk_estimates",
    }
    test_location = BASE_DIR / "crypto_calculator" / "tests"

    def setUp(self):
        self.factory = RequestFactory()
        self.default_params = {
            "portfolio": "EXAMPLE-USD;0.50\r\nTEST-USD;0.50",
            "benchmark": "EXAMPLE-USD;0.40\r\nTEST-USD;0.60",
            "cob_date": "2023-01-23",
            "correlation_hl": 10,
            "factor_risk_hl": 5,
            "specific_risk_hl": 5,
            "time_window_len": 30,
            "mean_to_zero": False,
            "use_factors": True,
        }

    @classmethod
    def setUpTestData(cls):
        if REFRESH_TEST_DB:
            for test_db, table, test_input in zip(
                [
                    "test_returns.sqlite3",
                    "test_raw_price_data.sqlite3",
                    "test_factor_model_estimates.sqlite3",
                    "test_factor_model_estimates.sqlite3",
                    "test_factor_model_estimates.sqlite3",
                    "test_specific_risk_estimates.sqlite3",
                ],
                [
                    "returns",
                    "raw_price_data",
                    "factor_returns",
                    "exposures",
                    "specific_returns",
                    "core_specific_risk",
                ],
                [
                    "test_coin_total_returns.csv",
                    "test_raw_price_data.csv",
                    "test_factor_returns.csv",
                    "test_exposures.csv",
                    "test_specific_returns.csv",
                    "test_core_specific_risk.csv",
                ],
            ):
                df = pd.read_csv(
                    cls.test_location / "resources" / "test_input" / test_input,
                    sep=";",
                )
                with sqlite3.connect(TEST_DATABASE_LOCATION / test_db) as conn:
                    df.to_sql(table, conn, if_exists="replace", index=False)

    def perform_risk_calc_test_routine(self, test_case_name: str, params: dict = None):
        if params is None:
            params = self.default_params
        request = self.factory.post(
            "api/get_risk_calculation_output",
            json.dumps(params),
            content_type="application/json",
        )
        json_response = get_risk_calculation_output(request)
        result_struct = json.loads(json_response.content)
        if REFRESH_TESTS:
            update_expected_output(test_case_name, result_struct)
        expected_struct = get_expected_output(test_case_name)
        test_result = compare_dictionaries(expected_struct, result_struct)
        if not test_result:
            logger.error(f"test case: {test_case_name} failed!")
        self.assertTrue(test_result)

    def test_risk_calc_tool_default(self):
        test_case_name = "test_risk_calc_tool_default"
        self.perform_risk_calc_test_routine(test_case_name)

    def test_risk_calc_tool_no_factor_no_mean(self):
        test_case_name = "test_risk_calc_tool_no_factor_no_mean"
        params = self.default_params.copy()
        params["use_factors"] = False
        self.perform_risk_calc_test_routine(test_case_name, params)

    def test_risk_calc_tool_no_factor_w_mean_hl_problem(self):
        test_case_name = "test_risk_calc_tool_no_factor_w_mean_hl_problem"
        params = self.default_params.copy()
        params["use_factors"] = False
        params["mean_to_zero"] = True
        params["factor_risk_hl"] = 0
        params["specific_risk_hl"] = "-2"
        params["correlation_hl"] = -20
        self.perform_risk_calc_test_routine(test_case_name, params)

    def test_risk_calc_tool_uncovered_element(self):
        test_case_name = "test_risk_calc_tool_uncovered_element"
        params = self.default_params.copy()
        params["portfolio"] = (
            "EXAMPLE-USD;0.250\r\nTEST-USD;0.250\r\nTEST99-USD;0.50\r\nTEST22-USD;0.50"
        )
        params["benchmark"] = (
            "EXAMPLE-USD;0.150\r\nTEST-USD;0.650\r\nTEST99-USD;0.650\r\nTEST22-USD;0.750"
        )
        self.perform_risk_calc_test_routine(test_case_name, params)

    def test_risk_calc_tool_no_input(self):
        test_case_name = "test_risk_calc_tool_no_input"
        params = self.default_params.copy()
        params["portfolio"] = ""
        self.perform_risk_calc_test_routine(test_case_name, params)

    def test_risk_calc_tool_default_benchmark(self):
        test_case_name = "test_risk_calc_tool_default_benchmark"
        params = self.default_params.copy()
        params["portfolio"] = (
            "EXAMPLE-USD;0.250\r\nTEST-USD;0.250\r\nTEST99-USD;0.50\r\nTEST22-USD;0.50"
        )
        params["benchmark"] = None
        self.perform_risk_calc_test_routine(test_case_name, params)

    def test_risk_calc_tool_default_benchmark_no_factor(self):
        test_case_name = "test_risk_calc_tool_default_benchmark_no_factor"
        params = self.default_params.copy()
        params["portfolio"] = (
            "EXAMPLE-USD;0.250\r\nTEST-USD;0.250\r\nTEST99-USD;0.50\r\nTEST22-USD;0.50"
        )
        params["use_factors"] = False
        params["benchmark"] = None
        self.perform_risk_calc_test_routine(test_case_name, params)

    def test_risk_calc_tool_no_input_at_all(self):
        test_case_name = "test_risk_calc_tool_no_input_at_all"
        params = self.default_params.copy()
        params["portfolio"] = ""
        params["use_factors"] = False
        params["benchmark"] = None
        self.perform_risk_calc_test_routine(test_case_name, params)

    def test_risk_calc_tool_cob_date_incorrect(self):
        test_case_name = "test_risk_calc_tool_cob_date_incorrect"
        params = self.default_params.copy()
        params["cob_date"] = "2024-01-01"
        self.perform_risk_calc_test_routine(test_case_name, params)

    def test_risk_calc_tool_default_benchmark_with_factor(self):
        test_case_name = "test_risk_calc_tool_default_benchmark_with_factor"
        params = self.default_params.copy()
        params["portfolio"] = (
            "EXAMPLE-USD;0.250\r\nTEST-USD;0.250\r\nTEST99-USD;0.50\r\nTEST22-USD;0.50"
        )
        params["use_factors"] = True
        params["benchmark"] = None
        self.perform_risk_calc_test_routine(test_case_name, params)

    def test_risk_calc_tool_no_active_risk_with_factor(self):
        test_case_name = "test_risk_calc_tool_no_active_risk_with_factor"
        params = self.default_params.copy()
        params["portfolio"] = (
            "EXAMPLE-USD;0.250\r\nTEST-USD;0.250\r\nTEST99-USD;0.50\r\nTEST22-USD;0.50"
        )
        params["use_factors"] = True
        params["benchmark"] = (
            "EXAMPLE-USD;0.250\r\nTEST-USD;0.250\r\nTEST99-USD;0.50\r\nTEST22-USD;0.50"
        )
        self.perform_risk_calc_test_routine(test_case_name, params)

    def test_risk_calc_tool_no_active_risk_no_factor(self):
        test_case_name = "test_risk_calc_tool_no_active_risk_no_factor"
        params = self.default_params.copy()
        params["portfolio"] = (
            "EXAMPLE-USD;0.250\r\nTEST-USD;0.250\r\nTEST99-USD;0.50\r\nTEST22-USD;0.50"
        )
        params["use_factors"] = True
        params["benchmark"] = (
            "EXAMPLE-USD;0.250\r\nTEST-USD;0.250\r\nTEST99-USD;0.50\r\nTEST22-USD;0.50"
        )
        self.perform_risk_calc_test_routine(test_case_name, params)

    def test_risk_calc_tool_long_short_no_factor(self):
        test_case_name = "test_risk_calc_tool_long_short_no_factor"
        params = self.default_params.copy()
        params["portfolio"] = (
            "EXAMPLE-USD;-0.250\r\nTEST-USD;0.250\r\nTEST99-USD;0.50\r\nTEST22-USD;0.50"
        )
        params["use_factors"] = False
        params["benchmark"] = (
            "EXAMPLE-USD;0.250\r\nTEST-USD;0.250\r\nTEST99-USD;0.50\r\nTEST22-USD;0.50"
        )
        self.perform_risk_calc_test_routine(test_case_name, params)

    def test_risk_calc_tool_long_short_with_factor(self):
        test_case_name = "test_risk_calc_tool_long_short_with_factor"
        params = self.default_params.copy()
        params["portfolio"] = (
            "EXAMPLE-USD;-0.250\r\nTEST-USD;0.250\r\nTEST99-USD;0.50\r\nTEST22-USD;0.50"
        )
        params["use_factors"] = True
        params["benchmark"] = (
            "EXAMPLE-USD;0.250\r\nTEST-USD;0.250\r\nTEST99-USD;0.50\r\nTEST22-USD;0.50"
        )
        self.perform_risk_calc_test_routine(test_case_name, params)

    def test_risk_calc_tool_long_short_with_factor_no_active(self):
        test_case_name = "test_risk_calc_tool_long_short_with_factor_no_active"
        params = self.default_params.copy()
        params["portfolio"] = (
            "EXAMPLE-USD;-0.250\r\nTEST-USD;0.250\r\nTEST99-USD;0.50\r\nTEST22-USD;0.50"
        )
        params["use_factors"] = True
        params["benchmark"] = (
            "EXAMPLE-USD;-0.250\r\nTEST-USD;0.250\r\nTEST99-USD;0.50\r\nTEST22-USD;0.50"
        )
        self.perform_risk_calc_test_routine(test_case_name, params)

    def test_risk_calc_tool_long_short_no_factor_no_active(self):
        test_case_name = "test_risk_calc_tool_long_short_no_factor_no_active"
        params = self.default_params.copy()
        params["portfolio"] = (
            "EXAMPLE-USD;-0.250\r\nTEST-USD;0.250\r\nTEST99-USD;0.50\r\nTEST22-USD;0.50"
        )
        params["use_factors"] = False
        params["benchmark"] = (
            "EXAMPLE-USD;-0.250\r\nTEST-USD;0.250\r\nTEST99-USD;0.50\r\nTEST22-USD;0.50"
        )
        self.perform_risk_calc_test_routine(test_case_name, params)

    def test_risk_calc_tool_double_entry_with_factor(self):
        test_case_name = "test_risk_calc_tool_double_entry_with_factor"
        params = self.default_params.copy()
        params["portfolio"] = (
            "EXAMPLE-USD;-0.250\r\nEXAMPLE-USD;0.250\r\nTEST99-USD;0.50\r\nTEST22-USD;0.50"
        )
        params["use_factors"] = True
        params["benchmark"] = (
            "EXAMPLE-USD;0.250\r\nTEST-USD;0.250\r\nTEST99-USD;0.50\r\nTEST22-USD;0.50"
        )
        self.perform_risk_calc_test_routine(test_case_name, params)

    def test_risk_calc_tool_double_entry_no_factor(self):
        test_case_name = "test_risk_calc_tool_double_entry_no_factor"
        params = self.default_params.copy()
        params["portfolio"] = (
            "EXAMPLE-USD;-0.250\r\nEXAMPLE-USD;0.250\r\nTEST99-USD;0.50\r\nTEST22-USD;0.50"
        )
        params["use_factors"] = False
        params["benchmark"] = (
            "EXAMPLE-USD;0.250\r\nTEST-USD;0.250\r\nTEST99-USD;0.50\r\nTEST22-USD;0.50"
        )
        self.perform_risk_calc_test_routine(test_case_name, params)

    def test_risk_calc_tool_port_long_bmrk_short_factor(self):
        test_case_name = "test_risk_calc_tool_port_long_bmrk_short_factor"
        params = self.default_params.copy()
        params["portfolio"] = "EXAMPLE-USD;0.250\r\nEXAMPLE-USD;0.250"
        params["use_factors"] = True
        params["benchmark"] = "EXAMPLE-USD;-0.250\r\nEXAMPLE-USD;-0.250"
        self.perform_risk_calc_test_routine(test_case_name, params)

    def test_risk_calc_tool_port_long_bmrk_short_no_factor(self):
        test_case_name = "test_risk_calc_tool_port_long_bmrk_short_no_factor"
        params = self.default_params.copy()
        params["portfolio"] = "EXAMPLE-USD;0.250\r\nEXAMPLE-USD;0.250"
        params["use_factors"] = False
        params["benchmark"] = "EXAMPLE-USD;-0.250\r\nEXAMPLE-USD;-0.250"
        self.perform_risk_calc_test_routine(test_case_name, params)

    def test_risk_calc_tool_wrong_number_format(self):
        test_case_name = "test_risk_calc_tool_wrong_number_format"
        params = self.default_params.copy()
        params["portfolio"] = "EXAMPLE-USD,0,250\r\nEXAMPLE-USD;0.250"
        params["use_factors"] = False
        params["benchmark"] = "EXAMPLE-USD;-0;250\r\nEXAMPLE-USD;-0.250"
        self.perform_risk_calc_test_routine(test_case_name, params)

    def test_risk_calc_tool_hacky_input(self):
        test_case_name = "test_risk_calc_tool_hacky_input"
        params = self.default_params.copy()
        params["portfolio"] = "<script>alert('Hacked!')</script>;0.250"
        params["use_factors"] = False
        params["benchmark"] = (
            "Some <b>bold</b> description with <i>HTML</i> tags.;-0.250"
        )
        self.perform_risk_calc_test_routine(test_case_name, params)

    def test_risk_calc_tool_too_short_horizon_no_factor(self):
        test_case_name = "test_risk_calc_tool_too_short_horizon_no_factor"
        params = self.default_params.copy()
        params["cob_date"] = "2023-01-01"
        params["use_factors"] = False
        self.perform_risk_calc_test_routine(test_case_name, params)

    def test_risk_calc_tool_too_short_horizon_factor(self):
        test_case_name = "test_risk_calc_tool_too_short_horizon_factor"
        params = self.default_params.copy()
        params["cob_date"] = "2023-01-01"
        params["use_factors"] = True
        self.perform_risk_calc_test_routine(test_case_name, params)

    def test_risk_calc_tool_2_day_horizon_no_factor(self):
        test_case_name = "test_risk_calc_tool_2_day_horizon_no_factor"
        params = self.default_params.copy()
        params["cob_date"] = "2023-01-02"
        params["use_factors"] = False
        self.perform_risk_calc_test_routine(test_case_name, params)

    def test_risk_calc_tool_2_day_horizon_factor(self):
        test_case_name = "test_risk_calc_tool_2_day_horizon_factor"
        params = self.default_params.copy()
        params["cob_date"] = "2023-01-02"
        params["use_factors"] = True
        self.perform_risk_calc_test_routine(test_case_name, params)

    def test_risk_calc_tool_short_w_horizon_no_factor(self):
        test_case_name = "test_risk_calc_tool_short_w_horizon_no_factor"
        params = self.default_params.copy()
        params["time_window_len"] = 10
        params["use_factors"] = False
        self.perform_risk_calc_test_routine(test_case_name, params)

    def test_risk_calc_tool_short_w_horizon_factor(self):
        test_case_name = "test_risk_calc_tool_short_w_horizon_factor"
        params = self.default_params.copy()
        params["time_window_len"] = 10
        params["use_factors"] = True
        self.perform_risk_calc_test_routine(test_case_name, params)
