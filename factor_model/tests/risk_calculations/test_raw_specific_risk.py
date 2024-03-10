import unittest
import pandas as pd
from risk_calculations.specific_risk import generate_raw_specific_risk  # Replace with your actual module name


class TestGenerateRawSpecificRisk(unittest.TestCase):

    def setUp(self):
        self.specific_returns_data = {
            "ticker": ["T1", "T1", "T1", "T2", "T2", "T2", "T3", "T3", "T5"],
            "date": [
                "2024-03-01",
                "2024-03-02",
                "2024-03-03",
                "2024-03-01",
                "2024-03-02",
                "2024-03-03",
                "2024-03-02",
                "2024-03-03",
                "2024-03-03",
            ],
            "specific_return": [
                0.02,
                0.0985,
                0.01,
                0.0532,
                -0.015,
                0.053,
                -0.452,
                -0.015,
                0.14
            ],
        }
        self.specific_returns = pd.DataFrame(self.specific_returns_data)

        self.parameters = {
            "date": "2024-03-03",
            "variance_half_life": 10,
        }

        self.portfolio_details = {
            "T1": 0.25,
            "T2": 0.25,
            "T3": 0.40,
            "T4": 0.09,
            "T5": 0.01
        }

    def test_standard_deviations(self):
        standard_deviations, _ = generate_raw_specific_risk(
            self.specific_returns, self.parameters, self.portfolio_details
        )

        self.assertAlmostEqual(standard_deviations["T1"], 0.04868469, places=5)
        self.assertAlmostEqual(standard_deviations["T2"], 0.03932940, places=5)
        self.assertAlmostEqual(standard_deviations["T3"], 0.30900566, places=5)
        self.assertIsNone(standard_deviations["T4"])
        self.assertIsNone(standard_deviations["T5"])


    def test_available_spec_return_history(self):
        _, available_spec_return_history = generate_raw_specific_risk(
            self.specific_returns, self.parameters, self.portfolio_details
        )

        # Check expected results
        self.assertEqual(available_spec_return_history["T1"], 3)
        self.assertEqual(available_spec_return_history["T2"], 3)
        self.assertEqual(available_spec_return_history["T3"], 2)
        self.assertEqual(available_spec_return_history["T4"], 0)
        self.assertEqual(available_spec_return_history["T5"], 1)

if __name__ == "__main__":
    unittest.main()
