import unittest
from factor_model.risk_calculations.specific_risk import closest_halflife_element


class TestClosestHalflifeElement(unittest.TestCase):
    def test_single_halflife(self):
        # Test when user_halflife is equal to the only available halflife
        lst = [10.0]
        user_halflife = 10.0
        result = closest_halflife_element(lst, user_halflife)
        self.assertEqual(result, [10.0])

    def test_closest_halflife(self):
        # Test when user_halflife is between two available halflifes
        lst = [5.0, 10.0, 15.0]
        user_halflife = 8.0
        result = closest_halflife_element(lst, user_halflife)
        self.assertEqual(result, [5.0, 10.0])

    def test_outside_range(self):
        # Test when user_halflife is outside the available halflife range
        lst = [5.0, 10.0, 15.0]
        user_halflife = 20.0
        result = closest_halflife_element(lst, user_halflife)
        self.assertEqual(result, [15.0])


if __name__ == "__main__":
    unittest.main()
