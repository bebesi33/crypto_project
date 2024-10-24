import { BlockMath } from "react-katex";
import "katex/dist/katex.min.css";
import "../assets/css/factor_model_info.css";
import { useEffect, useState } from "react";
import { API } from "../../Api";
import SimpleTable from "../tables/SimpleTable";

const volume_formula = `\\text{VolumeExposure}(t) = \\frac{1}{1,000,000} 
    \\sum_{i=t - TradingDays + 1}^{t} 
    \\text{Volume}(i)`;
const volume_exposure = `\\text{VolumeExposure(t) is the aggregated volume at date \(t\)}`;
const volue_trade_days = `\\text{ TradingDays: is the number of days per month. Default: 30.}`;
const volume_input = `\\text{ Volume(i): is the trade volume at date \(i\)}.`;

const reversal_formula = `\\text{ReversalExposure}(t) = \\frac{\\text{Close}(t) - \\text{Close}(t - LookBack)}{\\text{Close}(t - LookBack)}`;
const reversal_close = `\\text{Close}(t) : \\text{ closing price at date } t `;
const reversal_lookback = `\\text{LookBack} : \\text{ the number of days used to look back. Reversal: 30, Momentum: 180 }`;

const size_formula = `\\text{Size}(t) = \\log{(MarketCap(t)+1)}`;
const size_market_cap = `\\text{MarketCap}(t): \\text{Total supply multiplied by the current market price, expressed in USD}`;

const coin_formula = `\\text{NewCoin} =  0 \\text{ if } \\frac{A(t)}{MarketPresenceMax} > 1 \\text{  ,   }  1 - \\frac{A(t)}{MarketPresenceMax} \\text{  otherwise}`;
const coin_At = `\\text{A}(t) :  \\text{the age of the crypto in days}`;
const coin_P = `\\text{MarketPresenceMax}:  \\text{Represents the maximum number of days to define a new crypto asset. Default: 1095}`;

const excess_return_formula = `\\text{Excess Return}_i(t) = R_i(t) - r_f(t)`;
const excess_return_rf = `\\text{R}_i(t) : \\text{represents the total return between t and t-1}`;
const excess_return_rf2 = `\\text{R}_i(t) : \\ln \\Bigl( 1+\\frac{\\text{Close}_i(t) - \\text{Close}_i(t - 1)}{\\text{Close}_i(t - 1)}\\Bigl) \\text{ where, Close}_i(t)\\text{ is the close price for crypto i at date t}`;
const excess_return_totret = `\\text{r}_f(t) : \\text{represents the daily USD risk free rate.}`;

const wls_formula = `\\text{Excess Return}_i(t) = \\beta_0(t) + \\sum_{k=1}^{K} \\beta_k(t) \\cdot \\text{StyleExposure}_{i,k}(t-1) + \\epsilon_i(t)`;
const wls_market = `\\beta_0(t) : \\text{the market factor's return on date t}`;
const wls_style = `\\beta_k(t) : \\text{ factor return for style k on date t}`;
const wls_style_exp = `\\text{StyleExposure}_{i,k}(t-1) : \\text{exposure to style k at date t-1}`;
const wls_specific = `\\epsilon_i(t) : \\text{ specific return for cryptocurrency i on date t}`;

function FactorModelInfo() {
  const [factor_stats, setJsonData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(
          API + "crypto/api/get_factor_return_stats"
        );
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        if (response.ok) {
          const factor_stats = await response.json();
          console.log("Data received successfully!");
          setJsonData(factor_stats);
        } else {
          console.error("Error recievig data from the backend.");
        }
      } catch (err) {
        console.error("An error occurred:", err);
      }
    };

    fetchData();
  }, []); // Empty dependency array means this runs once when the component mounts

  return (
    <div className="container">
      {" "}
      <br></br>
      <div className="content-text">
        <h2> 1. Overview</h2>
        <p>
          The model presented on this webpage is a fundamental factor model. This
          means that the factor returns are generated using a sequence of
          cross-sectional regressions and are the result of regression
          estimations (estimated coefficients). The style exposures (or
          regressors in the regressions) are calculated based on asset
          characteristics for each time period.
        </p>
        <h2> 2. Style factors</h2>
        <p>
          The following section explain the calculation of "raw" style
          exposures. These exposure values are considered "raw", as they are not
          directly fed into the risk factor return regressions. All of the "raw"
          exposures below are subject to standardization on the estimation
          universe, the standardized version of these style exposures is used to
          estimate factor returns.
        </p>
        <h4> 2.1. Volume style</h4>
        <p>
          The rolling volume exposure is calculated by summing the volume over a
          specified number of days, corresponding to a certain number of months,
          and then scaling the result by dividing by 1,000,000 to convert the
          units into USD millions. Currently the calculation uses 30 trading
          days as a default.
        </p>
        <BlockMath math={volume_formula} />
        <BlockMath math={volume_exposure} />
        <BlockMath math={volue_trade_days} />
        <BlockMath math={volume_input} />
        <h4> 2.2. Reversal and Momentum styles</h4>
        <p>
          Both style exposures rely on the same formula, albeit they use
          different lookback time horizons: Reversal uses a 30 day lookback
          horizon, while Momentum uses a 180 day lookback. Reversal style and
          reversal strategies are based on the principle of mean reversion,
          ideally reversal investors take advantage of short-term price
          fluctuations due to market overreactions. Momentum style tries to
          capitalize on the tendency of securities to continue moving in the
          same direction (upward or downward) for a certain period. This style
          is based on the belief that stocks or in this case crypto assets that
          performed well in the past will continue to perform well in the near
          future, while the worst performers will continue to underperform.
        </p>
        <BlockMath math={reversal_formula} />
        <BlockMath math={reversal_close} />
        <BlockMath math={reversal_lookback} />
        <h4> 2.3. Size style</h4>
        <p>
          Size style tries to capture price movement differences between high
          market cap and low market cap cryptocurrencies. Market capitalization
          (or market cap) for cryptocurrencies is calculated by multiplying the
          total supply of a cryptocurrency by its current market price.
          Typically cryptocurrencies with more than 10 billion USD market cap
          are considered Large-cap. Some examples are Bitcoin (BTC) amd Ethereum
          (ETH).
        </p>
        <BlockMath math={size_formula} />
        <BlockMath math={size_market_cap} />
        <h4> 2.3. New Coin style</h4>
        <p>
          The New Coin style calculates an exposure variable ranging from 0 to
          1. For cryptocurrencies that have been in the market for a long time,
          such as Bitcoin (BTC), the exposure will be 0. In contrast, a recently
          introduced coin will have an exposure value closer to 1.
        </p>
        <BlockMath math={coin_formula} />
        <BlockMath math={coin_At} />
        <BlockMath math={coin_P} />
        <h4> 2.4. Market</h4>
        <p>
          Market "style" represents the cryptocurrency market and serves as the
          constant in the regressions. Therefore, all records in the regression
          have an exposure value of 1 with respect to the market.
        </p>
        <h2> 3. Factor return estimation</h2>
        <h4> 3.1 Estimation universe generation</h4>
        <p>
          For each time period a reduced set of crypto is defined as the
          estimation universe. The regression estimation is performed on these
          selected assets. There are two conditions that should be met:
          <ul>
            <li>
              {" "}
              Square root of market cap coverage: The cryptocurrencies are
              ordered from highest to lowest by market capitalization. Based on
              the square root of their market cap, assets are selected to cover
              80 percent of the total square root of the market cap. This
              approach ensures two things: 1{")"} the smallest coins are
              excluded from the estimation, preventing additional noise in the
              model, and 2{")"} the weighting reduces the impact of the largest
              cryptocurrencies while still gives more weight to larger ones than
              smaller ones.
            </li>
            <li>
              New coin inclusion: The newest coins are not immidiately included
              into the estimation universe. These should present in the market
              for at least 14 days.
            </li>
          </ul>
        </p>
        <h4> 3.2 Factor return estimation technical details</h4>
        <p>
          {" "}
          For each trading day, the factor returns are calculated by estimating
          a cross-sectional weighted least squares (WLS) regression on the
          elements of the estimation universe. The weighting is based on the
          square root of market capitalization (as described in 3.1). The
          regressors are the standardized style exposures, including the market
          exposure (the latter serving as the constant in the regression). The
          explanatory variable is the daily excess return of each
          cryptocurrency, which is calculated by subtracting the risk-free rate
          from the total returns.
        </p>
        <p>Excess returns can be specified using the following formula:</p>
        <BlockMath math={excess_return_formula} />
        <BlockMath math={excess_return_rf} />
        <BlockMath math={excess_return_rf2} />
        <BlockMath math={excess_return_totret} />
        <p>
          In this model, 1/365th of the relevant SOFR (Secured overnight
          Financing Rate) is used for all dates as a risk free rate.
        </p>
        <p>
          The daily crosssectional regressions can be specfied with the
          following formula:
        </p>
        <BlockMath math={wls_formula} />
        <BlockMath math={wls_market} />
        <BlockMath math={wls_style} />
        <BlockMath math={wls_style_exp} />
        <BlockMath math={wls_specific} />
        <p>
          It must be noted that for each day, the WLS regression uses the
          previous day's style exposures. This is important, as the aim of this
          regression is to explain the next day's returns (e.g., returns between
          t and t-1) by using the available information on day t-1. The
          residuals of the regression can be interpreted as specific returns. By
          applying the estimated regression coefficients, the specific returns
          for non-estimation universe elements are calculated. As the specific
          returns are derived from the error terms of the estimated regressions,
          they are assumed to be independent of each other.
        </p>
        <h2> 4. Factor return related statistics</h2>
      </div>
      {factor_stats !== null && (
        <>
          <div>
            <p>
              The average estimated R-squared in the estimation universe is{" "}
              {Math.round(factor_stats["rsquares"]["avg_core_r2"] * 1000) /
                1000}{" "}
              percent, while the average number of observations is{" "}
              {Math.round(factor_stats["rsquares"]["avg_nobs"])} under{" "}
              {factor_stats["rsquares"]["len"]} time periods (days).
            </p>
            <p>
              For each daily regression, the T-statistics of the estimated
              coefficients can be calculated. If the absolute value of a
              T-statistic is greater than 1.96, it indicates that the estimated
              coefficient is significantly non-zero. These cases are referred to
              as active T-statistics. Ideally, an active T-statistic ratio is
              considered favorable when the proportion of active T-statistics
              exceeds 20 percent within a given time frame. The results below
              cover {factor_stats["rsquares"]["len"]} estimation dates between:{" "}
              {factor_stats["tstats"]["first_date"]} and{" "}
              {factor_stats["tstats"]["last_date"]}.
            </p>
          </div>
          <div className="stats-table-container">
            <SimpleTable
              primaryData={factor_stats["tstats"]["active_tstat_ratio"]}
              metricColumn="Style"
              valueColumn="Active T-statistics ratio"
              tableTitle="Active T-statistics ratio by styles in percentage points"
              headerLevel="h5"
            />
          </div>
          <p>
            The Variance Inflation Factor (VIF) is a useful tool in regression
            analysis to observe multicollinearity among independent variables.
            The higher the value the VIF the bigger the multicollinearity
            problem. Ideally VIF between 1 and 5 shows moderate correlation,
            which is generally acceptable. Problematic level of
            multicollinearity is the case when VIF {">"} 5. Since this model
            have hundreds of regressions for all trading days and all the
            regressors have a VIF estimate for all trading days, only the
            proportion of problematic VIF is shown.
          </p>
          <div className="stats-table-container">
            <SimpleTable
              primaryData={factor_stats["vifs"]["problematic_ratio"]}
              metricColumn="Style"
              valueColumn="Proportion of VIF over 5"
              tableTitle="Proportion of VIF metrics over 5 in percentage points"
              headerLevel="h5"
            />
          </div>
        </>
      )}
      {factor_stats == null && (
        <p>
          Unfortunately some technical error occured, the factor return related
          statistics are not available.
        </p>
      )}
    </div>
  );
}

export default FactorModelInfo;
