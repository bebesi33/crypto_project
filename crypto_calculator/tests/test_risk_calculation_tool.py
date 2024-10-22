import json
import sqlite3
from django.test import RequestFactory, TestCase
import pandas as pd
from crypto_calculator.tests.resources.conftest import (
    REFRESH_TESTS,
    get_expected_output,
    update_expected_output,
)
from crypto_calculator.views import get_risk_calculation_output
from database_server.settings import BASE_DIR, TEST_DATABASE_LOCATION
from factor_model.utilities.common_utility import compare_dictionaries


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
            "min_ret_hist": 5,
            "mean_to_zero": False,
            "use_factors": True,
        }

    @classmethod
    def setUpTestData(cls):
        if REFRESH_TESTS:
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

    def test_risk_calc_tool_default(self):
        test_case_name = "test_risk_calc_tool_default"
        request = self.factory.post(
            "api/get_risk_calculation_output",
            json.dumps(self.default_params),
            content_type="application/json",
        )
        json_response = get_risk_calculation_output(request)
        result_struct = json.loads(json_response.content)
        if REFRESH_TESTS:
            update_expected_output(test_case_name, result_struct)
        expected_struct = get_expected_output(test_case_name)
        self.assertTrue(compare_dictionaries(expected_struct, result_struct))

    def test_risk_calc_tool_no_factor_no_mean(self):
        test_case_name = "test_risk_calc_tool_no_factor_no_mean"
        params = self.default_params.copy()
        params["use_factors"] = False
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
        self.assertTrue(compare_dictionaries(expected_struct, result_struct))

    def test_risk_calc_tool_no_factor_w_mean_hl_problem(self):
        test_case_name = "test_risk_calc_tool_no_factor_w_mean_hl_problem"
        params = self.default_params.copy()
        params["use_factors"] = False
        params["mean_to_zero"] = True
        params["factor_risk_hl"] = 0
        params["specific_risk_hl"] = "-2"
        params["correlation_hl"] = -20
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
        self.assertTrue(compare_dictionaries(expected_struct, result_struct))

    def test_risk_calc_tool_uncovered_element(self):
        test_case_name = "test_risk_calc_tool_uncovered_element"
        params = self.default_params.copy()
        params["portfolio"] = (
            "EXAMPLE-USD;0.250\r\nTEST-USD;0.250\r\nTEST99-USD;0.50\r\nTEST22-USD;0.50"
        )
        params["benchmark"] = (
            "EXAMPLE-USD;0.150\r\nTEST-USD;0.650\r\nTEST99-USD;0.650\r\nTEST22-USD;0.750"
        )
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
        self.assertTrue(compare_dictionaries(expected_struct, result_struct))

    def test_risk_calc_tool_no_input(self):
        test_case_name = "test_risk_calc_tool_no_input"
        params = self.default_params.copy()
        params["portfolio"] = ""
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
        self.assertTrue(compare_dictionaries(expected_struct, result_struct))

    def test_risk_calc_tool_default_benchmark(self):
        test_case_name = "test_risk_calc_tool_default_benchmark"
        params = self.default_params.copy()
        params["portfolio"] = (
            "EXAMPLE-USD;0.250\r\nTEST-USD;0.250\r\nTEST99-USD;0.50\r\nTEST22-USD;0.50"
        )
        params["benchmark"] = None
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
        self.assertTrue(compare_dictionaries(expected_struct, result_struct))

    def test_risk_calc_tool_default_benchmark_no_factor(self):
        test_case_name = "test_risk_calc_tool_default_benchmark_no_factor"
        params = self.default_params.copy()
        params["portfolio"] = (
            "EXAMPLE-USD;0.250\r\nTEST-USD;0.250\r\nTEST99-USD;0.50\r\nTEST22-USD;0.50"
        )
        params["use_factors"] = False
        params["benchmark"] = None
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
        self.assertTrue(compare_dictionaries(expected_struct, result_struct))

    def test_risk_calc_tool_no_input_at_all(self):
        test_case_name = "test_risk_calc_tool_no_input_at_all"
        params = self.default_params.copy()
        params["portfolio"] = ""
        params["use_factors"] = False
        params["benchmark"] = None
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
        self.assertTrue(compare_dictionaries(expected_struct, result_struct))

    def test_risk_calc_tool_cob_date_incorrect(self):
        test_case_name = "test_risk_calc_tool_cob_date_incorrect"
        params = self.default_params.copy()
        params["cob_date"] = "2024-01-01"
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
        self.assertTrue(compare_dictionaries(expected_struct, result_struct))
