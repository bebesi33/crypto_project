import json
from database_server.settings import BASE_DIR


REFRESH_TESTS = True
REFRESH_TEST_DB = False
TEST_LOCATION = BASE_DIR / "crypto_calculator" / "tests"


def get_expected_output(test_case: str) -> dict:
    """Loads the expected output from the resources/test_expected_output folder

    Args:
        test_case (str): name of the test case

    Returns:
        dict: dictionary containing the test result content
    """
    with open(
        TEST_LOCATION / "resources" / "test_expected_output" / f"{test_case}.json",
        "r",
    ) as json_file:
        expected_struct = json.load(json_file)
    return expected_struct


def update_expected_output(test_case: str, result_struct):
    """Updates the expected test output

    Args:
        test_case (str): name of the test case
        result_struct (_type_): dictionary containing test output
    """
    with open(
        TEST_LOCATION / "resources" / "test_expected_output" / f"{test_case}.json",
        "w",
    ) as json_file:
        json.dump(result_struct, json_file, indent=4)
