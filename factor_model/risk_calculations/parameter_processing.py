from typing import Dict, List


def check_input_param_correctness(
    parameter_name: str,
    parameter_default: float,
    parameter_nickname: str,
    all_input: Dict,
    log_elements: List[str],
    processed_input: Dict,
):
    halflife = all_input.get(parameter_name)
    override_code = 0
    if halflife is not None:
        try:
            halflife = float(halflife)
            if halflife < 0.0001:
                log_elements.append(
                    f"If {parameter_nickname} smaller than 0.0001: {parameter_name}, half-life set to default {parameter_default} days."
                )
                halflife = parameter_default
                override_code = 1
                log_elements.append(
                    f"The {parameter_nickname} should be a positive number."
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
    else:
        log_elements.append(f"No {parameter_nickname} input!")
    return override_code