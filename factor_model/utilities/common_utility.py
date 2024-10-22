import math


def convert_str_numbs_to_float(v):
    """
    Converts a string representation of a number (with optional suffixes like 'B' for billion or 'M' for million)
    into a floating-point value.

    Args:
        v (str): The input string representing the number.

    Returns:
        float: The converted floating-point value.

    Examples:
        >>> convert_str_numbs_to_float("1.5M")
        1500000.0
        >>> convert_str_numbs_to_float("0.75B")
        750000000.0
    """
    if any(c.isalpha() for c in v):
        temp_values = v.split(".")
        if len(temp_values) == 2 and v[-1].isalpha():
            float_value = float(temp_values[0] + "." + temp_values[1][:-1])
            if temp_values[1][-1] == "B":
                float_value *= 1000000000
            if temp_values[1][-1] == "M":
                float_value *= 1000000
            return float_value
        else:
            return float(v)
    else:
        return float(v)


def compare_dictionaries(dict1: dict, dict2: dict, tolerance = 0.00001) -> bool:
    """Recursively compares two dictionaries

    Args:
        dict1 (dict): dictionary input one
        dict2 (dict): dictionary input two

    Returns:
        bool: returns true if the dictionaries are the same
    """
    if dict1.keys() != dict2.keys():
        return False

    for key in dict1:
        value1 = dict1[key]
        value2 = dict2[key]

        if isinstance(value1, dict) and isinstance(value2, dict):
            if not compare_dictionaries(value1, value2):
                return False
        elif isinstance(value1, float) and isinstance(value2, float):
            if not math.isclose(value1, value2, abs_tol=tolerance):
                return False
        elif value1 != value2:
            return False
    return True
