import { BlockMath } from "react-katex";
import "katex/dist/katex.min.css";
import "./FactorModelInfo.css";
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

function FactorModelInfo() {
  const [jsonData, setJsonData] = useState(null);

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
          const jsonData = await response.json();
          console.log("Data received successfully!");
          console.log(jsonData);
          setJsonData(jsonData);
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
          The model presented in this webpage is a fundamental factor model.
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
          The Market ("style") represents the cryptocurrency market and serves
          as the constant in the regressions. Therefore, all records in the
          regression have an exposure value of 1 with respect to the market.
        </p>
        <h2> 3. Factor return estimation</h2>
        <h2> 4. Factor return related statistics</h2>
      </div>
      {jsonData !== null && (
        <>
          <div>
            <p>
              The average estimated R-squared in the estimation universe is{" "}
              {Math.round(jsonData["rsquares"]["avg_core_r2"] * 1000) / 1000}{" "}
              percent, while the average number of observations is{" "}
              {Math.round(jsonData["rsquares"]["avg_nobs"])} under{" "}
              {jsonData["rsquares"]["len"]} time periods (days).
            </p>
            <p>
              For each daily regression, the T-statistics of the estimated
              coefficients can be calculated. If the absolute value of a
              T-statistic is greater than 1.96, it indicates that the estimated
              coefficient is significantly non-zero. These cases are referred to
              as active T-statistics. Ideally, an active T-statistic ratio is
              considered favorable when the proportion of active T-statistics
              exceeds 20 percent within a given time frame. The results below
              cover {jsonData["rsquares"]["len"]} estimation dates between:{" "}
              {jsonData["tstats"]["first_date"]} and{" "}
              {jsonData["tstats"]["last_date"]}.
            </p>
          </div>
          <div className="stats-table-container">
            <SimpleTable
              primaryData={jsonData["tstats"]["active_tstat_ratio"]}
              metricColumn="Style"
              valueColumn="Active T-statistics ratio"
              tableTitle="Active T-statistics ratio by styles in percentage points"
              headerLevel="h5"
            />
          </div>
          <p>VIF related...</p>
          <div className="stats-table-container">
          <SimpleTable
            primaryData={jsonData["vifs"]["problematic_ratio"]}
            metricColumn="Style"
            valueColumn="Proportion of VIF over 5"
            tableTitle="Proportion of VIF metrics over 5 in percentage points"
            headerLevel="h5"
          />
          </div>
        </>
      )}
    </div>
  );
}

export default FactorModelInfo;
