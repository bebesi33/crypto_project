import unittest
from factor_model.risk_calculations.portfolio_output import round_float_to_n_decimals_str


class TestRoundingFunction(unittest.TestCase):
    def test_positive_float_to_2_decimals(self):
        result = round_float_to_n_decimals_str(3.14159, 2)
        self.assertEqual(result, "3.14")

    def test_negative_float_to_4_decimals(self):
        result = round_float_to_n_decimals_str(-2.71828, 4)
        self.assertEqual(result, "-2.7183")

    def test_negative_float_to_2_decimals(self):
        result = round_float_to_n_decimals_str(-2.7, 2)
        self.assertEqual(result, "-2.70")

    def test_zero_to_1_decimal(self):
        result = round_float_to_n_decimals_str(0.0, 1)
        self.assertEqual(result, "0.0")

    def test_float_with_no_decimal_places(self):
        result = round_float_to_n_decimals_str(123.456, 1)
        self.assertEqual(result, "123.5")

    def test_float_with_many_zeros(self):
        result = round_float_to_n_decimals_str(123.1, 4)
        self.assertEqual(result, "123.1000")

    def test_float_with_more_decimal_places(self):
        result = round_float_to_n_decimals_str(5.6789, 10)
        self.assertEqual(result, "5.6789000000")

if __name__ == "__main__":
    unittest.main()