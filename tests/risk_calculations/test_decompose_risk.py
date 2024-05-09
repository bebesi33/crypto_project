import unittest
import pandas as pd
import numpy as np
from factor_model.risk_calculations.risk_attribution import decompose_risk


class TestDecomposeRisk(unittest.TestCase):
    def test_specific_risk(self):
        # Test with specific risk provided
        total_risk = 10.7703296143
        factor_covar = pd.DataFrame({
            'Factor1': [11, -5],
            'Factor2': [-5, 15]
        }, index=['Factor1', 'Factor2'])
        spec_risk = 10.0
        expected = {'specific_risk': 9.284766908825876,
                    'Factor2': 1.3927150363238816,
                    'Factor1': 1.0213243599708464,
                    'diversification': -0.9284766908825876
                    }
        result_dict = decompose_risk(total_risk, factor_covar, spec_risk)
        for key in expected.keys():
            self.assertAlmostEqual(
                result_dict[key], expected.get(key, 0.0), places=5)
        self.assertAlmostEqual(
            sum(result_dict.values()),
            total_risk,
            places=7
        )

    def test_no_specific_risk(self):
        # Test with specific risk provided
        factor_covar = pd.DataFrame({
            'Factor1': [1, -0.5],
            'Factor2': [-0.5, 2]
        }, index=['Factor1', 'Factor2'])
        total_risk = factor_covar.sum().sum() ** 0.5
        expected = {'Factor2': 1.414213562373095,
                    'Factor1': 0.7071067811865475,
                    'diversification': -0.7071067811865475}
        result_dict = decompose_risk(total_risk, factor_covar)
        for key in expected.keys():
            self.assertAlmostEqual(
                result_dict[key], expected.get(key, 0.0), places=5)
        self.assertAlmostEqual(
            sum(result_dict.values()),
            total_risk,
            places=7
        )

    def test_more_than_10_factors(self):
        # Test with more than 10 factors
        factor_covar = pd.DataFrame(data=np.diag(range(15)),
                                    index=['Factor{}'.format(i) for i in range(15)],
                                    columns=['Factor{}'.format(i) for i in range(15)])
        total_risk = factor_covar.sum().sum() ** 0.5
        result_dict = decompose_risk(total_risk, factor_covar)
        self.assertAlmostEqual(result_dict['other'], 0.9759000729485332, places=5)
        self.assertAlmostEqual(result_dict['Factor14'], 1.3662601021279466, places=5)
        self.assertAlmostEqual(result_dict['diversification'], 0.0, places=5)
        self.assertAlmostEqual(result_dict.get("Factor1", -10), -10, places=5)

if __name__ == '__main__':
    unittest.main()
