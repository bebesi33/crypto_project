import unittest
import pandas as pd
from risk_calculations.factor_covariance import get_factor_return_correlation

class TestFactorReturnCorrelation(unittest.TestCase):
    def setUp(self):
        # Create sample factor returns DataFrame (replace with your actual data)
        self.factor_returns_data = pd.DataFrame({
            "date": ["2024-03-01", "2024-03-02", "2024-03-03"],
            "factor1": [0.01, 0.02, 0.03],
            "factor2": [-0.02, 0.01, 0.02],
            # Add other factor columns...
        })

    def test_no_correlation_id(self):
        # Test when a request is sent without correlation ID
        params = {
            "date": "2024-03-02",
            "correlation_half_life": 10 
        }
        result = get_factor_return_correlation(self.factor_returns_data, params)
        print(result)
        self.assertTrue(result.shape[0] > 0) 

    def test_response_with_correlation_id(self):
        params = {
            "date": "2024-03-03",
            "correlation_half_life": 10  # Adjust as needed
        }
        result = get_factor_return_correlation(self.factor_returns_data, params)
        # Add assertions to check if the result meets your expectations
        self.assertTrue(result.shape[0] > 0)  # Example assertion

if __name__ == "__main__":
    unittest.main()