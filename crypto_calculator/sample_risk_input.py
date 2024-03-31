# This is a temporary file, for sample input
# A sample portfolio to test calculations and restrict query...
portfolio_details = {
    "BCUBE-USD": 0.17,
    "LNC-USD": 0.05,
    "PMG24050-USD": 0.2,
    "ZNN-USD": 0.04,
    "EFI-USD": 0.03,
    "BTC-USD": 0.32,
    "ETH-USD": 0.19,
}

market_portfolio = {
    "BTC-USD": 0.31574372070244366,
    "ETH-USD": 0.18711055133973806,
    "USDT-USD": 0.08725061854643708,
    "BNB-USD": 0.06932395681724883,
    "SOL-USD": 0.06602083999170749,
    "STETH-USD": 0.0534749145676961,
    "XRP-USD": 0.05020181639431607,
    "USDC-USD": 0.046874562996328084,
    "ADA-USD": 0.04406750903164565,
    "DOGE-USD": 0.041257706928259585,
    "SHIB-USD": 0.03867380268417949,
}

# risk calculation
risk_calculation_parameters = {
    "correlation_half_life": 730,  # days
    "variance_half_life": 365,  # days
    "specific_risk_half_life": 365,
    "date": "2023-03-01",
    "minimum_history_spec_ret": 730,
}