RAW_DATA_DB = "raw_price_data.sqlite3"
RETURN_DB = "returns.sqlite3"
FACTOR_MODEL_ESTIMATES = "factor_model_estimates.sqlite3"
SPECIFIC_RISK = "specific_risk_estimates.sqlite3"
FIX_SET_OF_HALF_LIFES = sorted(list(range(10, 3 * 365, 30)) + [365])
EXPOSURE_NON_STYLE_FIELDS = [
    "id",
    "ticker",
    "return",
    "core_universe",
    "transformed_market_cap",
    "date"
]
RECOGNIZED_STYLES = [
    "market",
    "momentum",
    "new_coin",
    "reversal",
    "size",
    "volume"
]