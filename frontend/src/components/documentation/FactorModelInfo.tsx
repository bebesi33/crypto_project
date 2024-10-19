import { BlockMath } from "react-katex";
import "katex/dist/katex.min.css";
import "./FactorModelInfo.css";

const volume_formula = `\\text{VolumeExposure}(t) = \\frac{1}{1,000,000} 
    \\sum_{i=t - TradingDays + 1}^{t} 
    \\text{Volume}(i)`;
const volume_exposure = `\\text{VolumeExposure(t) is the aggregated volume at date \(t\)}`;
const volue_trade_days = `\\text{ TradingDays: is the number of days per month. Default: 30.}`;
const volume_input = `\\text{ Volume(i): is the trade volume at date \(i\)}.`;

const reversal_formula = `\\text{Exposure}(t) = \\frac{\\text{Close}(t) - \\text{Close}(t - LookBack)}{\\text{Close}(t - LookBack)}`;
const reversal_close = `\\text{Close}(t) : \\text{ closing price at date } t `;
const reversal_lookback = `\\text{LookBack} : \\text{ the number of days used to look back. Reversal: 30, Momentum: 180 }`;

const size_formula = `\\text{Size}(t) = \\log{(MarketCap(t)+1)}`;
const size_market_cap = `\\text{MarketCap}(t): \\text{Total supply multiplied by the current market price, expressed in USD}`;


function FactorModelInfo() {
  return (
    <div>
      {" "}
      <br></br>
      <h2> 1. Overview</h2>
      <p>The model presented in this webpage is a fundamental factor model.</p>
      <h2> 2. Style factors</h2>
      <p>
        The following section explain the calculation of "raw" style exposures.
        These exposure values are considered "raw", as they are not directly fed
        into the risk factor return regressions. All of the "raw" exposures
        below are subject to standardization on the estimation universe, the
        standardized version of these style exposures is used to estimate factor
        returns.
      </p>
      <h4> 2.1. Volume style</h4>
      <p>
        The rolling volume exposure is calculated by summing the volume over a
        specified number of days, corresponding to a certain number of months,
        and then scaling the result by dividing by 1,000,000 to convert the
        units into USD millions. Currently the calculation uses 30 trading days
        as a default.
      </p>
      <BlockMath math={volume_formula} />
      <BlockMath math={volume_exposure} />
      <BlockMath math={volue_trade_days} />
      <BlockMath math={volume_input} />
      <h4> 2.2. Reversal and Momentum styles</h4>
      <p>
        Both style exposures rely on the same formula, albeit they use different
        lookback time horizons: Reversal uses a 30 day lookback horizon, while Momentum
        uses a 180 day lookback. Reversal style and reversal strategies are
        based on the principle of mean reversion, ideally reversal investors
        take advantage of short-term price fluctuations due to market
        overreactions. Momentum style tries to capitalize on the tendency of
        securities to continue moving in the same direction (upward or downward)
        for a certain period. This style is based on the belief that stocks or
        in this case crypto assets that performed well in the past will continue
        to perform well in the near future, while the worst performers will
        continue to underperform.
      </p>
      <BlockMath math={reversal_formula} />
      <BlockMath math={reversal_close} />
      <BlockMath math={reversal_lookback} />
      <h4> 2.3. Size style</h4>
      <p>
        Size style tries to capture price movement differences between high
        market cap and low market cap cryptocurrencies. Market capitalization
        (or market cap) for cryptocurrencies is calculated by multiplying the
        total supply of a cryptocurrency by its current market price. Typically
        cryptocurrencies with more than 10 billion USD market cap are considered
        Large-cap. Some examples are Bitcoin (BTC) amd Ethereum (ETH).
      </p>
      <BlockMath math={size_formula} />
      <BlockMath math={size_market_cap} />
    </div>
  );
}

export default FactorModelInfo;
