import { BlockMath } from "react-katex";
import "katex/dist/katex.min.css";

const ewma_std = `\\sigma_t = \\sqrt{\\frac{(1 - \\lambda)}{1 - \\lambda^t} \\sum_{i=1}^{t} \\lambda^{t-i} (r_i - \\mu_t)^2}`;
const ewma_lambda = `\\lambda = 2^{-\\frac{1}{\\text{HalfLife}}} \\text{ or } \\text{HalfLife} = \\frac{\\ln(2)}{\\ln\\left(\\frac{1}{\\lambda}\\right)}`;
const ewma_r =
  "r_i : \\text{represents excess returns or factor returns for date i}";
const ewma_mu =
  "\\mu_t : \\text{represents the average of } r_i \\text{ over the time period between 1 and t}";

const var_formula = `\\text{VaR}_\\alpha = 1 - F^{-1}(1 - \\alpha)`;
const es_formula = `\\text{ES}_\\alpha = 1 - e^{0.5 \\cdot \\sigma^2} \\cdot \\frac{\\Phi\\left(\\Phi^{-1}(1 - \\alpha) - \\sigma\\right)}{1 - \\alpha}`;
const var_f = 'F^{-1} \\text{ : is the inverse of the cumulative density function of the lognormal distribution, with zero mean and } \\sigma \\text{ standard deviation parameter}' 
const var_a = '\\alpha \\text{: confidence level, e.g.: 95\\% or 99\\%}';
const var_sigma = '\\sigma \\text{: standard deviation calculated for a given portfolio on daily frequency}';
const es_cdf = '\\Phi \\text{ : represents the cumulative distribution function of the normal distribution with zero mean and } \\sigma \\text{ standard deviation parameter}';

function RiskCalculationInfo() {
  return (
    <div className="container">
      {" "}
      <br></br>
      <div className="content-text">
        <h2> 1. Overview</h2>
        <p>
          {" "}
          This section details the risk calculation logic found in the risk
          calculation and in the explorer tools. Most of the risk calculation
          methodology relies heavily on the exponentially weighted moving
          average (EWMA) processes, both on single time series and on portfolio
          level. The user has the option to remove the average term from the
          risk calculation and hence introduce extra convervativism. To enhance
          the user experience instead of specifying the so called &lambda;
          parameters, the half-life parameters can be supplied to the
          calculations.
        </p>
        <p>
          Portfolio-level risk calculations involve computing the covariance
          matrix using EWMA-based weighting. Factor covariance matrices are
          calculated on the fly. If the user chooses not to use style factors,
          then each portfolio element is treated as its own factor. Specific
          risk contribution is only relevant when the factor model is chosen. In
          this case, the specific risk covariance matrix is calculated, with
          non-zero elements only on its diagonal (assuming that specific returns
          are independent of each other).
        </p>
        <p>
          Portfolio level Value-at-Risk (VaR) and Expected shortfall (ES)
          estimates are calculated using the normality assumption. Their
          calculationa are perfomed at both the 95 percent and 99 percent
          confidence levels.
        </p>
        <h2> 2. Exponentially weighted risk calculation </h2>
        <p>
          The EWMA is a useful tool when calculating risk. This model is capable
          to given different weights for newer and older observations. In
          general more recent observations are given higher weights, while older
          observations given lower weights. The higher the lambda parameter (or
          larger half-life), the bigger the weight for more recent observations.
          This allows investors to match the risk calculation to their specified
          investment horizon. (e.g.: a long term investor may choose 365
          half-life, while a short term investor choose only 30 day half-life.)
          The standard deviation formula (or in this context the risk) for time
          period "t" with a user defined half-life can be given as:
        </p>
        <BlockMath math={ewma_std} />
        <p>Where: </p>
        <BlockMath math={ewma_lambda} />
        <BlockMath math={ewma_r} />
        <BlockMath math={ewma_mu} />
        <h2> 3. Portfolio level risk calculation </h2>
        <h2> 4. Marginal contribution to risk calculation </h2>
        <h2> 5. VaR and ES calculation </h2>
        <p>
          For a fixed condifence level (&alpha;) over a given time period (1
          day), Value-at-Risk (VaR) is defined as the maximum loss that can
          occur with a confidence level of &alpha;. ES is the expected value of
          the losses, which are greater than VaR. The risk calculator tool
          presents the VaR and ES on 95 and 99 percent confidence levels. By
          concention both ES and VaR are positive numbers and represent a loss.
          In the case of the risk calculator tool a value of 4 tells the user
          that the VaR of the porfolio is 4 percent of the total
          portfolio value.
        </p>
        <BlockMath math={var_formula} />
        <BlockMath math={es_formula} />
        <BlockMath math={var_sigma} />
        <BlockMath math={var_a} />
        <BlockMath math={var_f} />
        <BlockMath math={es_cdf} />
      </div>
    </div>
  );
}

export default RiskCalculationInfo;
