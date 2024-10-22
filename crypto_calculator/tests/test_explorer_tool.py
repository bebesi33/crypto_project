import json
import sqlite3
from django.test import RequestFactory, TestCase
import pandas as pd
from crypto_calculator.tests.resources.conftest import (
    REFRESH_TESTS,
    get_expected_output,
    update_expected_output,
)
from crypto_calculator.views import get_raw_price_data
from database_server.settings import BASE_DIR, TEST_DATABASE_LOCATION
from factor_model.utilities.common_utility import compare_dictionaries


# notes:
# https://dev.to/vergeev/testing-against-unmanaged-models-in-django


class FactorExplorerToolTest(TestCase):
    databases = {"factor_model_estimates", "returns", "raw_price_data"}
    test_location = BASE_DIR / "crypto_calculator" / "tests"

    def setUp(self):
        self.factory = RequestFactory()
        self.default_params = {
            "symbol": "TEST-USD",
            "cob_date": "2023-01-23",
            "halflife": 10,
            "min_obs": 5,
            "mean_to_zero": False,
        }

    @classmethod
    def setUpTestData(cls):
        if REFRESH_TESTS:
            for test_db, table, test_input in zip(
                ["test_returns.sqlite3", "test_raw_price_data.sqlite3", "test_factor_model_estimates.sqlite3"],
                ["returns", "raw_price_data", "factor_returns"],
                [
                    "test_coin_total_returns.csv",
                    "test_raw_price_data.csv",
                    "test_factor_returns.csv",
                ],
            ):
                df = pd.read_csv(
                    cls.test_location / "resources" / "test_input" / test_input,
                    sep=";",
                )
                with sqlite3.connect(TEST_DATABASE_LOCATION / test_db) as conn:
                    df.to_sql(table, conn, if_exists="replace", index=False)

    def test_explorer_with_symbol(self):
        test_case_name = "test_explorer_with_symbol"
        request = self.factory.post(
            "api/get_raw_price_data",
            json.dumps(self.default_params),
            content_type="application/json",
        )
        json_response = get_raw_price_data(request)
        result_struct = json.loads(json_response.content)

        if REFRESH_TESTS:
            update_expected_output(test_case_name, result_struct)
        expected_struct = get_expected_output(test_case_name)
        self.assertTrue(compare_dictionaries(expected_struct, result_struct))

    def test_explorer_with_symbol_no_mean(self):
        test_case_name = "test_explorer_with_symbol_no_mean"
        params = self.default_params.copy()
        params["mean_to_zero"] = True
        request = self.factory.post(
            "api/get_raw_price_data",
            json.dumps(params),
            content_type="application/json",
        )
        json_response = get_raw_price_data(request)
        result_struct = json.loads(json_response.content)

        json_response = get_raw_price_data(request)
        result_struct = json.loads(json_response.content)
        if REFRESH_TESTS:
            update_expected_output(test_case_name, result_struct)
        expected_struct = get_expected_output(test_case_name)
        self.assertTrue(compare_dictionaries(expected_struct, result_struct))

    def test_explorer_with_symbol_problematic_output(self):
        test_case_name = "test_explorer_with_symbol_problematic_output"
        params = self.default_params.copy()
        params["halflife"] = -1
        params["min_obs"] = -1
        request = self.factory.post(
            "api/get_raw_price_data",
            json.dumps(params),
            content_type="application/json",
        )

        json_response = get_raw_price_data(request)
        result_struct = json.loads(json_response.content)
        if REFRESH_TESTS:
            update_expected_output(test_case_name, result_struct)
        expected_struct = get_expected_output(test_case_name)
        self.assertTrue(compare_dictionaries(expected_struct, result_struct))

    def test_explorer_with_factor(self):
        test_case_name = "test_explorer_with_factor"
        params = self.default_params.copy()
        params["symbol"] = "market"
        request = self.factory.post(
            "api/get_raw_price_data",
            json.dumps(params),
            content_type="application/json",
        )

        json_response = get_raw_price_data(request)
        result_struct = json.loads(json_response.content)
        if REFRESH_TESTS:
            update_expected_output(test_case_name, result_struct)
        expected_struct = get_expected_output(test_case_name)
        self.assertTrue(compare_dictionaries(expected_struct, result_struct))

    def test_explorer_with_factor_incorrect_hl(self):
        test_case_name = "test_explorer_with_factor_incorrect_hl"
        params = self.default_params.copy()
        params["symbol"] = "size"
        params["halflife"] = -1000
        request = self.factory.post(
            "api/get_raw_price_data",
            json.dumps(params),
            content_type="application/json",
        )

        json_response = get_raw_price_data(request)
        result_struct = json.loads(json_response.content)
        if REFRESH_TESTS:
            update_expected_output(test_case_name, result_struct)
        expected_struct = get_expected_output(test_case_name)
        self.assertTrue(compare_dictionaries(expected_struct, result_struct))

    def test_explorer_with_factor_incorrect_min_obs(self):
        test_case_name = "test_explorer_with_factor_incorrect_min_obs"
        params = self.default_params.copy()
        params["symbol"] = "size"
        params["min_obs"] = "-1000"
        request = self.factory.post(
            "api/get_raw_price_data",
            json.dumps(params),
            content_type="application/json",
        )

        json_response = get_raw_price_data(request)
        result_struct = json.loads(json_response.content)
        if REFRESH_TESTS:
            update_expected_output(test_case_name, result_struct)
        expected_struct = get_expected_output(test_case_name)
        self.assertTrue(compare_dictionaries(expected_struct, result_struct))

    def test_explorer_symbol_no_coverage(self):
        test_case_name = "test_explorer_symbol_no_coverage"
        params = self.default_params.copy()
        params["symbol"] = "NOT-COVERED-USD"
        params["min_obs"] = "-1000"
        request = self.factory.post(
            "api/get_raw_price_data",
            json.dumps(params),
            content_type="application/json",
        )

        json_response = get_raw_price_data(request)
        result_struct = json.loads(json_response.content)
        if REFRESH_TESTS:
            update_expected_output(test_case_name, result_struct)
        expected_struct = get_expected_output(test_case_name)
        self.assertTrue(compare_dictionaries(expected_struct, result_struct))

    def test_explorer_min_obs_too_large(self):
        test_case_name = "test_explorer_min_obs_too_large"  # larger then the available history
        params = self.default_params.copy()
        params["min_obs"] = 1000
        request = self.factory.post(
            "api/get_raw_price_data",
            json.dumps(params),
            content_type="application/json",
        )

        json_response = get_raw_price_data(request)
        result_struct = json.loads(json_response.content)
        if REFRESH_TESTS:
            update_expected_output(test_case_name, result_struct)
        expected_struct = get_expected_output(test_case_name)
        self.assertTrue(compare_dictionaries(expected_struct, result_struct))
