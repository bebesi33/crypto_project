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
