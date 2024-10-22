import unittest

from factor_model.utilities.common_utility import compare_dictionaries, convert_str_numbs_to_float


class TestCommonUtilities(unittest.TestCase):

    def test_convert_str_numbs_to_float(self):
        self.assertEqual(convert_str_numbs_to_float("1.5M"), 1500000.0)
        self.assertEqual(convert_str_numbs_to_float("0.75B"), 750000000.0)
        self.assertEqual(convert_str_numbs_to_float("100"), 100.0)
        self.assertEqual(convert_str_numbs_to_float("100.5"), 100.5)
        self.assertEqual(convert_str_numbs_to_float("1.5"), 1.5)
        self.assertEqual(convert_str_numbs_to_float("1.5K"), 1.5)

    def test_compare_dictionaries(self):
        dict1 = {'a': 1, 'b': {'c': 2, 'd': 3.0}}
        dict2 = {'a': 1, 'b': {'c': 2, 'd': 3}}
        dict3 = {'a': 1, 'b': {'c': 2, 'd': 4}}
        dict4 = {'a': 1, 'b': {'c': 2}}
        dict5 = {'a': 1, 'b': {'c': 2, 'd': 3, 'e': 4}}
        dict6 = {'a': 1, 'b': {'c': 2, 'd': 3.00001}}
        dict7 = {'a': 1, 'b': {'c': 2, 'd': 3.000001}}

        self.assertTrue(compare_dictionaries(dict1, dict2))
        self.assertFalse(compare_dictionaries(dict1, dict3))
        self.assertFalse(compare_dictionaries(dict1, dict4))
        self.assertFalse(compare_dictionaries(dict1, dict5))
        self.assertFalse(compare_dictionaries(dict1, dict6, tolerance=0.00001))
        self.assertTrue(compare_dictionaries(dict1, dict7, tolerance=0.00001))

if __name__ == '__main__':
    unittest.main()