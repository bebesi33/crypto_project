import numpy as np
from scipy.stats import norm
from scipy.stats import lognorm


def calculate_lognormal_es_var(
    portfolio_std: float, confidence_level: float, portfolio_value: float = 1.00
) -> tuple:
    """
    Calculates 1-Day Expected Shortfall (ES) and 1-Day VaR assuming lognormality.

    Args:
        portfolio_std (float): Standard deviation of the log returns of the portfolio.
        confidence_level (float): Confidence level (e.g., 0.95 for 95% confidence).
        portfolio_value (float): Total value of the portfolio.

    Returns:
        tuple: (1-Day ES, 1-Day VaR)
    """
    var = 1-lognorm.ppf(1 - confidence_level, portfolio_std, scale=1)

    es = (
        1
        - np.exp(0.5 * portfolio_std**2)
        * norm.cdf(norm.ppf(1-confidence_level) - portfolio_std)
        / (1-confidence_level)
    )

    return es, var
