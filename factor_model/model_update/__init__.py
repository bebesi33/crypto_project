import numpy as np
from datetime import date


UPDATE_PARAMS = {
    "HORIZON": "15y",
    "ESTIMATION_HORIZON": int(7.5 * 365),
    "WEIGHT_FUNCTION": np.sqrt,
    "PRESENT_IN_MARKET": 3 * 365,  # trade days, 3 years approx
    "ESTIMATION_DAY": date.today(),
    "MARKET_CAP_COVERAGE": 0.90,
    "NEW_COIN_INCLUSION": 120,  # after X days
    "REGRESSORS_SET1": ["market", "size", "momentum", "reversal", "volume", "new_coin"],
    "REGRESSORS_SET2": [],
    "MONTH_LENGTH": 30,
    "NOBS": 3000,
    "GENERATE_DATABASE": True,
}

RISK_CALCULATION_PARAMETERS = {
    "correlation_half_life": 730,  # days
    "variance_half_life": 365,  # days
    "specific_risk_half_life": 365,
    "date": "2023-03-04",
    "minimum_history_spec_ret": 730
}