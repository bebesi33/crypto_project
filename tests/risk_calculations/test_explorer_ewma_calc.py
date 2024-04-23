import unittest
import pandas as pd
from factor_model.risk_calculations.simple_risk_calculation import (
    create_ewma_std_estimates,
)
from pandas.testing import assert_frame_equal


class TestCreateEwmaStdEstimates(unittest.TestCase):
    def test_mean_to_zero(self):
        data = {"A": list(range(0, 30))}
        expected = {
            "A": [
                11.166972202893326,
                11.7499438402762,
                12.33318424192119,
                12.916693945917327,
                13.500473389208722,
                14.08452292842172,
                14.668842855742053,
                15.253433411162273,
                15.838294792032048,
                16.423427160579777,
                17.008830649891113,
            ]
        }
        df = pd.DataFrame(data)
        expected_df = pd.DataFrame(expected)
        result_df = create_ewma_std_estimates(
            df, halflife=365, min_periods=20, mean_to_zero=True
        )
        result_df.reset_index(drop=True, inplace=True)
        expected_df.reset_index(drop=True, inplace=True)
        assert_frame_equal(result_df, expected_df)

    def test_mean_to_zero_false(self):
        data = {"A": list(range(0, 30))}
        expected = {
            "A": [
                5.915885,
                6.204610,
                6.493325,
                6.782030,
                7.070727,
                7.359414,
                7.648093,
                7.936765,
                8.225429,
                8.514085,
                8.802734,
            ]
        }
        df = pd.DataFrame(data)
        expected_df = pd.DataFrame(expected)
        result_df = create_ewma_std_estimates(
            df, halflife=365, min_periods=20, mean_to_zero=False
        )
        result_df.reset_index(drop=True, inplace=True)
        expected_df.reset_index(drop=True, inplace=True)
        assert_frame_equal(result_df, expected_df)


if __name__ == "__main__":
    unittest.main()
