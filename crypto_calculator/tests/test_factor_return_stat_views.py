import json
import sqlite3
from django.test import RequestFactory, TestCase
import pandas as pd
from crypto_calculator.factor_return_stats_requests import (
    get_rsquares,
    get_tstats_stats,
    get_vif_stats,
)
from crypto_calculator.models import TStatistics
from crypto_calculator.tests.resources.conftest import (
    REFRESH_TEST_DB,
    REFRESH_TESTS,
    get_expected_output,
    update_expected_output,
)
from crypto_calculator.views import get_factor_return_stats
from database_server.settings import BASE_DIR, TEST_DATABASE_LOCATION
from factor_model.utilities.common_utility import compare_dictionaries
import logging


logger = logging.getLogger(__file__)

# notes:
# https://dev.to/vergeev/testing-against-unmanaged-models-in-django


class FactorStatModelTest(TestCase):
    databases = {"factor_model_estimates"}

    def setUp(self):
        self.factory = RequestFactory()

    @classmethod
    def setUpTestData(cls):
        # setup t_statistics table on the fly, by hand...
        if REFRESH_TEST_DB:
            df = pd.DataFrame(
                {
                    "id": [0, 1, 2],
                    "market": [0.1, 1.1, 2.2],
                    "size": [-1.1, -1, 2],
                    "momentum": [0.5, -1.99, -2.0],
                    "reversal": [0.5, 1.99, 2.0],
                    "volume": [0.5, 1.99, 2.0],
                    "new_coin": [0.5, 1.99, 2.0],
                    "date": ["2024-10-17", "2024-10-18", "2024-10-19"],
                    "version_date": ["2024-10-20", "2024-10-20", "2024-10-20"],
                }
            )
            with sqlite3.connect(
                TEST_DATABASE_LOCATION / "test_factor_model_estimates.sqlite3"
            ) as conn:
                df.to_sql("t_statistics", conn, if_exists="replace", index=False)
            # setup t_statistics table on the fly, by hand...
            vifs = pd.DataFrame(
                {
                    "id": [0, 1, 2],
                    "market": [0.1, 1.1, 2.2],
                    "size": [1.1, 1, 2],
                    "momentum": [0.5, 1.99, 2.0],
                    "reversal": [0.5, 1.99, 2.0],
                    "volume": [0.5, 11.99, 51.0],
                    "new_coin": [0.5, 11.99, 20.0],
                    "date": ["2024-10-17", "2024-10-18", "2024-10-19"],
                    "version_date": ["2024-10-20", "2024-10-20", "2024-10-20"],
                }
            )
            with sqlite3.connect(
                TEST_DATABASE_LOCATION / "test_factor_model_estimates.sqlite3"
            ) as conn:
                vifs.to_sql("vifs", conn, if_exists="replace", index=False)
            r_sq = pd.DataFrame(
                {
                    "id": [0, 1, 2],
                    "r2_core": [0.15, 0.25, 0.4],
                    "r2_adj": [0.1, 0.1, 0.3],
                    "nobs": [100, 300, 400],
                    "date": ["2024-10-17", "2024-10-18", "2024-10-19"],
                    "version_date": ["2024-10-20", "2024-10-20", "2024-10-20"],
                }
            )
            with sqlite3.connect(
                TEST_DATABASE_LOCATION / "test_factor_model_estimates.sqlite3"
            ) as conn:
                r_sq.to_sql("r_squares", conn, if_exists="replace", index=False)
        TStatistics.objects.using("factor_model_estimates").create(
            market=2.0,
            size=1.0,
            momentum=2.4,
            reversal=0.5,
            volume=1.9,
            new_coin=1.6,
            date="2024-10-20",
            version_date="2024-10-20",
        )

    def perform_get_stat_routine(self, test_case_name: str):
        request = self.factory.get("api/get_factor_return_stats")
        stat_response = get_factor_return_stats(request)
        result_struct = json.loads(stat_response.content)
        if REFRESH_TESTS:
            update_expected_output(test_case_name, result_struct)
        expected_struct = get_expected_output(test_case_name)
        test_result = compare_dictionaries(expected_struct, result_struct)
        if not test_result:
            logger.error(f"test case: {test_case_name} failed!")
        self.assertTrue(test_result)

    def test_tstatistics(self):
        result_struct = get_tstats_stats()
        self.assertEqual(result_struct.get("len"), 4)
        self.assertAlmostEqual(
            result_struct.get("active_tstat_ratio").get("market"), 50.0, places=5
        )
        self.assertAlmostEqual(
            result_struct.get("active_tstat_ratio").get("momentum"), 75.0, places=5
        )
        self.assertAlmostEqual(
            result_struct.get("active_tstat_ratio").get("reversal"), 50.0, places=5
        )
        self.assertAlmostEqual(
            result_struct.get("active_tstat_ratio").get("size"), 25.0, places=5
        )
        self.assertAlmostEqual(
            result_struct.get("active_tstat_ratio").get("volume"), 50.0, places=5
        )
        self.assertEqual(str(result_struct.get("last_date")), "2024-10-20")
        self.assertEqual(str(result_struct.get("first_date")), "2024-10-17")

    def test_vif_stats(self):
        result_struct = get_vif_stats()
        self.assertEqual(result_struct.get("len"), 3)
        self.assertAlmostEqual(
            result_struct.get("problematic_ratio").get("new_coin"), 66.7, places=5
        )
        self.assertAlmostEqual(
            result_struct.get("problematic_ratio").get("market", 0.0), 0.0, places=5
        )
        self.assertAlmostEqual(
            result_struct.get("problematic_ratio").get("momentum"), 00.0, places=5
        )
        self.assertAlmostEqual(
            result_struct.get("problematic_ratio").get("reversal"), 0.0, places=5
        )
        self.assertAlmostEqual(
            result_struct.get("problematic_ratio").get("size"), 0.0, places=5
        )
        self.assertAlmostEqual(
            result_struct.get("problematic_ratio").get("volume"), 66.7, places=5
        )
        self.assertEqual(str(result_struct.get("last_date")), "2024-10-19")
        self.assertEqual(str(result_struct.get("first_date")), "2024-10-17")

    def test_rquares(self):
        result_struct = get_rsquares()
        self.assertEqual(result_struct.get("len"), 3)
        self.assertAlmostEqual(result_struct.get("avg_core_r2"), 26.666666, places=5)
        self.assertAlmostEqual(result_struct.get("avg_nobs"), 266.666666, places=5)

    def test_stat_request(self):
        test_case_name = "test_stat_request"
        self.perform_get_stat_routine(test_case_name)
