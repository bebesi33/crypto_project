import unittest
from factor_model.risk_calculations.parameter_processing import (
    check_input_param_correctness,
)


class TestCheckInputParamCorrectness(unittest.TestCase):
    def test_halflife_positive(self):
        # Test when halflife is a positive value
        all_input = {"halflife": "15"}
        log_elements = []
        processed_input = {}
        override_code = check_input_param_correctness(
            "halflife", 10.0, "half-life", all_input, log_elements, processed_input
        )
        self.assertEqual(override_code, 0)
        self.assertEqual(processed_input["halflife"], 15)
        self.assertIn("input value of 15.0 is correct", log_elements[0])

    def test_halflife_zero(self):
        # Test when halflife is exactly 0
        all_input = {"halflife": "0.0"}
        log_elements = []
        processed_input = {}
        override_code = check_input_param_correctness(
            "halflife", 10.0, "half-life", all_input, log_elements, processed_input
        )
        self.assertEqual(override_code, 1)
        self.assertEqual(processed_input["halflife"], 10.0)
        self.assertIn(
            "If half-life smaller than 0.0001: halflife, half-life set to default 10.0 days.",
            log_elements[0],
        )

    def test_halflife_negative(self):
        # Test when halflife is negative
        all_input = {"halflife": "-0.001"}
        log_elements = []
        processed_input = {}
        override_code = check_input_param_correctness(
            "halflife", 10.0, "half-life", all_input, log_elements, processed_input
        )
        self.assertEqual(override_code, 1)
        self.assertEqual(processed_input["halflife"], 10.0)
        self.assertIn(
            "If half-life smaller than 0.0001: halflife, half-life set to default 10.0 days.",
            log_elements[0],
        )

    def test_no_halflife_input(self):
        # Test when no halflife input is provided
        all_input = {}
        log_elements = []
        processed_input = {}
        override_code = check_input_param_correctness(
            "halflife", 1.0, "half-life", all_input, log_elements, processed_input
        )
        self.assertEqual(override_code, 0)  # No override
        self.assertNotIn("halflife", processed_input)
        self.assertIn("No half-life input!", log_elements[0])


if __name__ == "__main__":
    unittest.main()
