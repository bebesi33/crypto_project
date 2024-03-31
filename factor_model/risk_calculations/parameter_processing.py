from typing import Dict, List


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
                    f"If {parameter_nickname} smaller than 0.0001: {parameter_name}, {parameter_nickname} set to default {parameter_default} days."
                )
                halflife = parameter_default
                override_code = 1
                log_elements.append(
                    f"The {parameter_nickname} should be a positive number."
                )
            elif halflife < 2 and integer_conversion == True:
                log_elements.append(
                    f"If {parameter_nickname} smaller than 2: {parameter_name}, {parameter_nickname} set to default {parameter_default} days."
                )
                halflife = parameter_default
                override_code = 1
                log_elements.append(
                    f"The {parameter_nickname} should be a positive number, at least 2"
                )
            else:
                log_elements.append(
                    f"The {parameter_nickname} input value of {halflife} is correct."
                )
        except ValueError:
            log_elements.append(
                f"Incorrect {parameter_nickname} value: {halflife}, {parameter_nickname} is set to default {parameter_default} days."
            )
            halflife = parameter_default
            override_code = 1
        processed_input[parameter_name] = halflife
        if integer_conversion:
            processed_input[parameter_name] = int(processed_input[parameter_name])
    else:
        log_elements.append(f"No {parameter_nickname} input!")
    return override_code
