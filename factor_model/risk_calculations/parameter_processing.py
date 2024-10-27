from typing import Dict, List, Tuple


def check_input_param_correctness(
    parameter_name: str,
    parameter_default: float,
    parameter_nickname: str,
    all_input: Dict,
    log_elements: List[str],
    processed_input: Dict,
    integer_conversion: bool = False,
):
    halflife = all_input.get(parameter_name)
    override_code = 0
    if halflife is not None:
        try:
            halflife = float(halflife)
            if halflife < 0.0001 and integer_conversion == False:
                log_elements.append(
                    f"If {parameter_nickname} smaller than 0.0001: {parameter_name}, {parameter_nickname} set to default {parameter_default} days. "
                )
                halflife = parameter_default
                override_code = 1
                log_elements.append(
                    f"The {parameter_nickname} should be a positive number. "
                )
            elif halflife < 2 and integer_conversion == True:
                log_elements.append(
                    f"If {parameter_nickname} smaller than 2: {parameter_name}, {parameter_nickname} set to default {parameter_default} days. "
                )
                halflife = parameter_default
                override_code = 1
                log_elements.append(
                    f"The {parameter_nickname} should be a positive number, at least 2. "
                )
            else:
                log_elements.append(
                    f"The {parameter_nickname} input value of {halflife} is correct. "
                )
        except ValueError:
            log_elements.append(
                f"Incorrect {parameter_nickname} value: {halflife}, {parameter_nickname} is set to default {parameter_default} days. "
            )
            halflife = parameter_default
            override_code = 1
        processed_input[parameter_name] = halflife
        if integer_conversion:
            processed_input[parameter_name] = int(processed_input[parameter_name])
    else:
        log_elements.append(f"No {parameter_nickname} input! ")
    return override_code


def parse_file_input_into_portfolio(
    input_stream: str,
) -> Tuple[Dict[str, float], List[str], int]:
    lines = input_stream.split("\r\n")

    # Only two separators are accepted: "," and ";"
    separator = ","
    if separator not in input_stream and ";" in input_stream:
        separator = ";"

    # Initialize empty lists for index and values
    port_weights = {}
    log_messages = list()
    error_code = 0
    # Parse each line
    for line in lines:
        if line:
            try:
                symbol, value = line.split(separator)
                try:
                    if symbol in port_weights.keys():
                        log_messages.append(
                            f"There are multiple instances for {symbol} in the input data. ({symbol}, {value}) "
                        )
                        error_code = 1
                    else:
                        port_weights[symbol] = float(value)
                except ValueError:
                    log_message = f"Symbol: {symbol} cannot be parsed with value: {value}."
                    log_messages.append(log_message)
                    error_code = 1
            except ValueError:
                log_message = f"Line: {str(line)} cannot be parsed. "
                log_messages.append(log_message)
    # Normalize portfolio
    total_weight = abs(sum(port_weights.values()))
    if abs(total_weight) > 0.000000001:
        for key in port_weights.keys():
            port_weights[key] = port_weights[key] / total_weight
    if sum(port_weights.values()) < 0:
        log_messages.append(
            "The total portfolio weights are less then 0! Are you sure, that this can be shorted?"
        )
        error_code = 1
    if len(port_weights.keys()) < 1:
        log_messages.append("The portfolio input is empty!")
        error_code = 404

    return port_weights, log_messages, error_code
