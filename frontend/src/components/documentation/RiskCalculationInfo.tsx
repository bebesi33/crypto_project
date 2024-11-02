import { BlockMath } from "react-katex";
import "katex/dist/katex.min.css";

const ewma_std = `\\sigma_{ExplorerTool,i,t}(\\lambda) = \\sqrt{\\frac{(1 - \\lambda)}{1 - \\lambda^t} \\sum_{i=1}^{t} \\lambda^{t-i} (r_i - \\xi\\mu_t)^2}`;
const ewma_std_risk_calc = `\\sigma_{i,t}(\\lambda) = \\sqrt{\\frac{(1 - \\lambda)}{1 - \\lambda^{L}} \\sum_{i=t-L+1}^{t} \\lambda^{t-i} (r_i - \\xi\\mu_t)^2}`;

const ewma_lambda = `\\lambda = 2^{-\\frac{1}{\\text{HalfLife}}} \\text{ or } \\text{HalfLife} = \\frac{\\ln(2)}{\\ln\\left(\\frac{1}{\\lambda}\\right)}`;
const ewma_r =
  "r_i : \\text{represents excess returns for a cryptocurrency or factor returns for date i}";
const ewma_mu =
  "\\mu_t : \\text{represents the average of } r_i \\text{ over the time period between 1 and t}";
const ewma_xi =
  '\\xi: \\text{represents the "Mean to Zero" flag, can have value 0 or 1. 0 representing the zero mean setting.}';
const ewma_corr = `\\rho_{j,i,t}(\\lambda_c) =\\frac{1}{\\sigma_{i,t}(\\lambda_c)\\sigma_{j,t}(\\lambda_c)} \\frac{(1 - \\lambda_c)}{1 - \\lambda_c^L} \\sum_{i=t-L+1}^{t} \\lambda_c^{t-i} (r_i - \\xi\\mu_{i,t})(r_j - \\xi\\mu_{j,t})`;
const ewma_l = "L : \\text{ represents the time window length in days}";

const port_risk_cov =
  "\\kappa_{i,j,t} = \\rho_{j,i,t}(\\lambda_c)\\sigma_{j,t}(\\lambda)\\sigma_{i,t}(\\lambda)";
const port_risk_sig =
  "\\rho_{j,i,t}(\\lambda_c): \\text{correlation between factor i and j}";
const port_risk_corr =
  "\\sigma_{i,t}(\\lambda): \\text{standard deviation estimate for factor i}";
const port_risk_fac_matrix =
  "\\Kappa_t: \\text{factor covariance matrix for k number of factors having } \\kappa_{i,j,t} \\text{ elements}";

const port_risk_exp =
  '\\delta_{i,j}: \\text{the "i"th cryptocurrencies exposure to factor j}';
const port_risk_exp_m =
  "\\Epsilon_{t,P}: \\text{the exposure matrix for n number of portfolio elements and k factors, having } \\delta_{i,j} \\text{ elements}";

const port_sigma_elem =
  "\\nu_{i,j}(\\lambda_s): \\text{0 if i!=j, }  \\sigma_{i}(\\lambda_s)^2 \\text{ if i=j}";
const port_sigma_lambda =
  "\\lambda_s: \\text{half-life parameter specified by the user for specific risk half-life}";

const port_variance =
  "\\sigma_{P,t, FactorModel}^2 = w_P\\Epsilon_{t,P}\\Kappa_t\\Epsilon_{t,P}^Tw_P^T+w_P\\Nu_tw_P^T";

const port_factor_risk =
  "\\text{Factor risk: } \\sqrt{w_P\\Epsilon_{t,P}\\Kappa_t\\Epsilon_{t,P}^Tw_P^T}";
const port_specific_risk = "\\text{Specific risk: } \\sqrt{w_P\\Nu_tw_P^T}";

const port_variance_no_factor =
  "\\sigma_{P,t, NoFactorModel}^2 = w_P\\Kappa_{t,NoFactorModel}w_P^T";

const port_beta_theory = "Beta(P,B) = \\frac{cov(r_P, r_B)}{variance(r_B)}";
const port_beta_factor =
  "Beta_{t,FactorModel}(P,B) = \\frac{w_P\\Epsilon_{t,P}\\Kappa_t\\Epsilon_{t,B}^Tw_B^T+w_P\\Nu_tw_B^T}{w_B\\Epsilon_{t,B}\\Kappa_t\\Epsilon_{t,B}^Tw_B^T+w_B\\Nu_tw_B^T}";

const port_beta_no_factor =
  "Beta_{t,NoFactorModel}(P,B) = \\frac{w_P\\Kappa_{t,NoFactorModel}w_B^T}{w_B\\Kappa_{t,NoFactorModel}w_B^T}";

const mcv_factor = "MCV_{t,P,Factor}= 2(w_P\\Epsilon_{t,P})\\Kappa_t";
const mcv_no_factor = "MCV_{t,P,NoFactorModel}= 2w_P\\Kappa_t";

const mcv_spec_risk = "MCV_{t,P,Specific}= 2w_P\\Nu_t";

const var_formula = `\\text{VaR}_\\alpha = 1 - F^{-1}(1 - \\alpha)`;
const es_formula = `\\text{ES}_\\alpha = 1 - e^{0.5 \\cdot \\sigma^2} \\cdot \\frac{\\Phi\\left(\\Phi^{-1}(1 - \\alpha) - \\sigma\\right)}{1 - \\alpha}`;
const var_f =
  "F^{-1} \\text{ : is the inverse of the cumulative density function of the lognormal distribution, with zero mean and } \\sigma \\text{ standard deviation parameter}";
const var_a = "\\alpha \\text{: confidence level, e.g.: 95\\% or 99\\%}";
const var_sigma =
  "\\sigma \\text{: standard deviation calculated for a given portfolio on daily frequency}";
const es_cdf =
  "\\Phi \\text{ : represents the cumulative distribution function of the normal distribution with zero mean and } \\sigma \\text{ standard deviation parameter}";

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
          risk calculation and hence introduce extra conservativism. To enhance
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
          calculation is performed at both the 95 percent and 99 percent
          confidence levels.
        </p>
        <h2> 2. Exponentially weighted risk calculation </h2>
        <p>
          The EWMA is a useful tool when calculating risk. This model is capable
          to give different weights for newer and older observations. In
          general, more recent observations are given higher weights, while
          older observations given lower weights. The higher the lambda
          parameter (or the larger the half-life), the bigger the weight for
          more recent observations. This allows investors to match the risk
          calculation to their specified investment horizon. (e.g.: a long-term
          investor may choose 365 half-life, while a short term investor choose
          only 30 day half-life.) A key difference between the Explorer tool and
          Risk calculator tool is that the former uses a continuously expanding
          window, while the latter uses a time period window. If a time period
          window is specified only, the last L days are used for the risk
          calculation. The standard deviation formula (or in this context the
          risk) for time period "t" for a given crypto ("i") excess return time
          series with a user defined half-life can be given as:
        </p>
        <BlockMath math={ewma_std} />
        <BlockMath math={ewma_std_risk_calc} />
        <p>Where: </p>
        <BlockMath math={ewma_lambda} />
        <BlockMath math={ewma_r} />
        <BlockMath math={ewma_mu} />
        <BlockMath math={ewma_xi} />
        <BlockMath math={ewma_l} />
        <p>
          The formula for standard deviation can be extended to cover
          correlation estimates as well:
        </p>
        <BlockMath math={ewma_corr} />
        <p>
          The user has the option to specify different half-life for standard
          deviation (risk) estimation and correlation estimates. (Standard
          deviation estimation: &lambda;, while for correlation: &lambda;
          <sub>c</sub>) This coincides with financial industry standards, as it
          is allows the user to calculate the correlation with a longer memory,
          than the memory used for standard deviation estimations. Notice that
          the L parameter (look back time horizon) is not used for Explorer tool
          standard deviation calculation (marked by ExplorerTool suffix) as it
          is using a continuously expanding window.
        </p>
        <h2> 3. Portfolio level risk calculation </h2>
        <p>
          The elements of the factor covariance matrix (
          <b>
            &Kappa;<sub>t</sub>
          </b>
          ) are specified using the following formulas:
        </p>
        <BlockMath math={port_risk_cov} />
        <BlockMath math={port_risk_sig} />
        <BlockMath math={port_risk_corr} />
        <BlockMath math={port_risk_fac_matrix} />
        <p>
          A user defined portfolio can be represented by a 1 x n vector (
          <b>
            w<sub>P</sub>
          </b>
          ), each element can represent one cryptocurrency and its weight by
          market value in a given portfolio.
        </p>
        <p>
          The elements of the exposure matrix (
          <b>
            E<sub>t,P</sub>
          </b>
          ) for time period "t" can be specified:
        </p>
        <BlockMath math={port_risk_exp} />
        <BlockMath math={port_risk_exp_m} />
        <p>
          The specific risk covariance matrix is a diagonal matrix, meaning that
          all off-diagonal elements are zero. Its elements are calculated using
          specific returns isntead of excess returns. Let's denote the specific
          risk covariance matrix for n number of assets for time period t with:{" "}
          <b>
            &Nu;
            <sub>t</sub>
          </b>
          . The elements of this matrix can be specified:
        </p>
        <BlockMath math={port_sigma_elem} />
        <BlockMath math={port_sigma_lambda} />
        <p>
          {" "}
          Using the notations specified above, the variance for a portfolio
          represented by{" "}
          <b>
            w<sub>P</sub>
          </b>{" "}
          can be calculated (the final risk is still given as a standard
          deviation estimate):
        </p>
        <BlockMath math={port_variance} />
        <p>
          The Factor model's total variance can be decomposed to factor and
          specific risk components:
        </p>
        <BlockMath math={port_factor_risk} />
        <BlockMath math={port_specific_risk} />
        <p>
          If the user turns off the "Use factors" flag, each cryptocurrency
          excess return time series are treated as a separate factor. (Hence a
          covariance matrix is calculated for elements in the portfolio.) The
          user can govern the half-life of this covariance matrix with the
          factor related half-life parameters. The variance for portfolio P can
          be specified:
        </p>
        <BlockMath math={port_variance_no_factor} />
        <p>
          By specifying a 1 x n vector (
          <b>
            w<sub>B</sub>
          </b>
          ), the benchmark portfolio can be introduced to the calculations. The
          active space portfolio (
          <b>
            w<sub>A</sub>
          </b>
          ) can be given by subtracting the benchmark weights from the portfolio
          weights.
        </p>
        <p>
          The Beta estimate for portfolio P with respect to the benchmark B can
          be specified:
        </p>
        <BlockMath math={port_beta_theory} />
        <p>In the Factor model this translates to: </p>
        <BlockMath math={port_beta_factor} />
        <p>The NoFactor model equivalent is: </p>
        <BlockMath math={port_beta_no_factor} />
        <h2> 4. Marginal contribution to variance calculation </h2>
        <p>
          {" "}
          Marginal contribution to variance (MCV) is a derivative, that shows
          how 1 unit of additional exposure can impact the total portfolio
          variance. For the Factor model the MCV contribution of the factors and
          the specific risks are presented, while for the No Factor model the
          individual cryptocurrencies contribution are presented.
        </p>
        <p>The MCV values for the Factor model are the following:</p>
        <BlockMath math={mcv_factor} />
        <BlockMath math={mcv_spec_risk} />
        <p>
          The MCV for factors is basically the derivative of the portfolio
          variance with respect to factor exposures. The specific risk related
          MCV is the derivative of the variance's specific risk part with
          respect to portfolio weight vector. In the Risk calculator output,
          only those specific risk related MCV values are presented, which have
          the larges impact.
        </p>
        <p>The MCV values for the No Factor model are the following:</p>
        <BlockMath math={mcv_no_factor} />

        <h2> 5. VaR and ES calculation </h2>
        <p>
          For a fixed confidence level ( &alpha;) over a given time horizon (1
          day), Value-at-Risk (VaR) represent the maximum expected loss not to
          be exceeded with a confidence level of  &alpha; percent. Expected Shortfall
          (ES) with confidence level ( &alpha;) is the expected value of the
          losses exceeding the VaR(&alpha;) threshold. The risk calculator tool
          presents the VaR and ES on 95 and 99 percent confidence levels. By
          construction, both ES and VaR are positive numbers. The risk measures represent a
          percentage loss in this project. In the case of the risk calculator tool
          a value of 4 tells the user that the VaR of the portfolio is 4 percent
          of the total portfolio value. This 4 percent means that, with a
          confidence level of  &alpha;, the portfolio’s losses are not expected
          to exceed 4 percent of its value in a single day. A 4 percent results
          on ES means, the portfolios average losses on its (1- &alpha;) worst
          trading days.
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
