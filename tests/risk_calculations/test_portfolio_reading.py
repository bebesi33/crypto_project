import unittest
from factor_model.risk_calculations.parameter_processing import (
    parse_file_input_into_portfolio,
)


class TestPortfolioParser(unittest.TestCase):
    def test_valid_input_1(self):
        input_stream = "BTC-USD,0.50\r\nETH-USD,0.45\r\nXRP-USD,0.05\r\n\r\n"
        port_weights, _, _ = parse_file_input_into_portfolio(input_stream)
        expected_result = {"BTC-USD": 0.5, "ETH-USD": 0.45, "XRP-USD": 0.05}
        self.assertEqual(port_weights, expected_result)

    def test_valid_input_2(self):
        input_stream = "BTC-USD,0.50\r\nETH-USD,0.50"
        port_weights, _, _ = parse_file_input_into_portfolio(input_stream)
        expected_result = {"BTC-USD": 0.5, "ETH-USD": 0.5}
        self.assertEqual(port_weights, expected_result)

    def test_invalid_port_weigth(self):
        input_stream = "BTC-USD;herh0.50\r\nETH-USD;0.50"
        port_weights, log_messages, error_code = parse_file_input_into_portfolio(
            input_stream
        )
        expected_result = {"ETH-USD": 1.0}
        self.assertEqual(port_weights, expected_result)
        self.assertEqual(error_code, 1)
        self.assertIn(
            "Symbol: BTC-USD cannot be parsed with value: herh0.50\r.", log_messages
        )

    def test_duplicate_input(self):
        input_stream = "BTC-USD;0.50\r\nBTC-USD;0.50"
        port_weights, log_messages, error_code = parse_file_input_into_portfolio(
            input_stream
        )
        expected_result = {"BTC-USD": 1.00}
        self.assertEqual(port_weights, expected_result)
        self.assertEqual(error_code, 1)
        self.assertIn(
            'There are multiple instances for BTC-USD in the input data. (BTC-USD, 0.50) ', log_messages
        )

    def test_empty_input(self):
        input_stream = ""
        _, _, error_code = parse_file_input_into_portfolio(input_stream)
        self.assertEqual(error_code, 404)

    def test_negative_weights(self):
        input_stream = "BTC-USD,-0.50\r\nETH-USD,-0.50"
        port_weights, log_messages, error_code = parse_file_input_into_portfolio(
            input_stream
        )
        expected_result = {"BTC-USD": -0.5, "ETH-USD": -0.5}
        self.assertEqual(port_weights, expected_result)
        self.assertEqual(error_code, 1)
        self.assertIn(
            "The total portfolio weights are less then 0! Are you sure, that this can be shorted?",
            log_messages,
        )

    def test_invalid_value_with_negative_port_value(self):
        input_stream = "BTC-USD,-0.50\r\nETH-USD,egewgew"
        port_weights, log_messages, error_code = parse_file_input_into_portfolio(
            input_stream
        )
        expected_result = {"BTC-USD": -1.0}
        self.assertEqual(port_weights, expected_result)
        self.assertEqual(error_code, 1)
        self.assertIn(
            "Symbol: ETH-USD cannot be parsed with value: egewgew.", log_messages
        )
        self.assertIn(
            "The total portfolio weights are less then 0! Are you sure, that this can be shorted?",
            log_messages,
        )


if __name__ == "__main__":
    unittest.main()
