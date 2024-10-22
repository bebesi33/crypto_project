import json
import sqlite3
from django.test import RequestFactory, TestCase
import pandas as pd
from crypto_calculator.models import Returns
from crypto_calculator.views import get_raw_price_data
from database_server.settings import BASE_DIR
from factor_model.utilities.common_utility import compare_dictionaries


# notes:
# https://dev.to/vergeev/testing-against-unmanaged-models-in-django


class FactorStatModelTest(TestCase):
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
        # setup t_statistics table on the fly, by hand...
        total_returns = pd.read_csv(
            cls.test_location
            / "resources"
            / "test_input"
            / "test_coin_total_returns.csv",
            sep=";",
        )
        with sqlite3.connect(BASE_DIR / "test_returns") as conn:
            total_returns.to_sql("returns", conn, if_exists="replace", index=False)

        price_history = pd.read_csv(
            cls.test_location / "resources" / "test_input" / "test_raw_price_data.csv",
            sep=";",
        )
        with sqlite3.connect(BASE_DIR / "test_raw_price_data") as conn:
            price_history.to_sql(
                "raw_price_data", conn, if_exists="replace", index=False
            )

    def test_explorer_with_symbol(self):
        request = self.factory.post(
            "api/get_raw_price_data",
            json.dumps(self.default_params),
            content_type="application/json",
        )
        json_response = get_raw_price_data(request)
        result_struct = json.loads(json_response.content)
        with open(
            self.test_location
            / "resources"
            / "test_expected_output"
            / "test_explorer_with_symbol.json",
            "r",
        ) as json_file:
            expected_struct = json.load(json_file)
        self.assertTrue(compare_dictionaries(expected_struct, result_struct))

    def test_explorer_with_symbol_no_mean(self):
        params = self.default_params.copy()
        params["mean_to_zero"] = True
        request = self.factory.post(
            "api/get_raw_price_data",
            json.dumps(params),
            content_type="application/json",
        )
        json_response = get_raw_price_data(request)
        result_struct = json.loads(json_response.content)

        with open(
            self.test_location
            / "resources"
            / "test_expected_output"
            / "test_explorer_with_symbol_no_mean.json",
            "r",
        ) as json_file:
            expected_struct = json.load(json_file)
        self.assertTrue(compare_dictionaries(expected_struct, result_struct))

    def test_explorer_with_symbol_problematic_output(self):
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

        # with open(
        #     self.test_location
        #     / "resources"
        #     / "test_expected_output"
        #     / "test_explorer_with_symbol_problematic_output.json",
        #     "w",
        # ) as json_file:
        #     json.dump(result_struct, json_file, indent=4)
        with open(
            self.test_location
            / "resources"
            / "test_expected_output"
            / "test_explorer_with_symbol_problematic_output.json",
            "r",
        ) as json_file:
            expected_struct = json.load(json_file)
        self.assertTrue(compare_dictionaries(expected_struct, result_struct))
