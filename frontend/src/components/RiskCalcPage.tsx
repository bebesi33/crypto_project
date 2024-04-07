import { useState } from "react";
import { API } from "../Api";
import "./RiskCalcPage.css";
import SimpleTable from "./tables/SimpleTable";

function RiskCalcPage() {
  const [jsonData, setJsonData] = useState(null);

  const initialValues = {
    cob_date: "2024-03-03",
    correlation_hl: "60",
    factor_risk_hl: "30",
    specific_risk_hl: "30",
    min_ret_hist: "20",
  };
  const [values, setValues] = useState(initialValues);

  const handleInputChange =
    (property: string) => (event: React.ChangeEvent<HTMLInputElement>) => {
      setValues({
        ...values,
        [property]: event.target.value,
      });
    };

  const handleSubmit = async (event: { preventDefault: () => void }) => {
    event.preventDefault();
    try {
      const response = await fetch(
        API + "crypto/api/get_risk_calculation_output",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
          body: JSON.stringify({
            cob_date: values["cob_date"],
          }),
        }
      );
      if (response.ok) {
        const jsonData = await response.json();
        console.log("Data received successfully!");
        console.log(jsonData);
        setJsonData(jsonData);
      } else {
        console.error("Error sending data to the backend.");
      }
    } catch (error) {
      console.error("An error occurred:", error);
    }
  };

  return (
    <div className="parent-container">
      <link href="/RiskCalcPage.css"></link>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <strong>
            <label
              htmlFor="cob-input"
              className="cob-input-label"
              style={{ textAlign: "left" }}
            >
              Enter calculation date
            </label>
          </strong>
          <input
            type="cob-input"
            className="form-control"
            id="cob-input"
            value={values.cob_date}
            onChange={handleInputChange("cob_date")}
          ></input>
          <strong>
            <label
              htmlFor="portfolio-input"
              className="portfolio-input-label"
              style={{ textAlign: "left" }}
            >
              Upload portfolio input
            </label>
          </strong>
          <input
            className="form-control"
            id="portfolio-input"
            type="file"
          ></input>

          <strong>
            <label
              htmlFor="market-input"
              className="market-input-label"
              style={{ textAlign: "left" }}
            >
              Upload benchmark (portfolio) input
            </label>
          </strong>
          <input className="form-control" id="market-input" type="file"></input>

          <strong>
            <label
              htmlFor="parameters"
              className="parameters"
              style={{ textAlign: "left" }}
            >
              Risk calculation parameters (all in days)
            </label>
          </strong>

          <label
            htmlFor="hl-corr-input"
            className="hl-corr-input-label"
            style={{ textAlign: "left" }}
          >
            Factor correlation half-life
          </label>
          <input
            type="hl-corr-input"
            className="form-control"
            id="hl-corr-input"
            value={values.correlation_hl}
            onChange={handleInputChange("correlation_hl")}
            style={{ direction: "rtl" }}
          ></input>

          <label
            htmlFor="hl-risk-input"
            className="hl-risk-input-label"
            style={{ textAlign: "left" }}
          >
            Factor risk half-life
          </label>
          <input
            type="hl-risk-input"
            className="form-control"
            id="hl-risk-input"
            value={values.factor_risk_hl}
            onChange={handleInputChange("factor_risk_hl")}
            style={{ direction: "rtl" }}
          ></input>

          <label
            htmlFor="min-ret-hist-input"
            className="min-ret-hist-input-label"
            style={{ textAlign: "left" }}
          >
            Min. return history length
          </label>
          <input
            type="min-ret-hist-input"
            className="form-control"
            id="min-ret-hist-input"
            value={values.min_ret_hist}
            onChange={handleInputChange("min_ret_hist")}
            style={{ direction: "rtl" }}
          ></input>

          <label
            htmlFor="spec-hl-risk-input"
            className="spec-hl-risk-input-label"
            style={{ textAlign: "left" }}
          >
            Specific risk half-life
          </label>
          <input
            type="spec-hl-risk-input"
            className="form-control"
            id="spec-hl-risk-input"
            value={values.specific_risk_hl}
            onChange={handleInputChange("specific_risk_hl")}
            style={{ direction: "rtl" }}
          ></input>

          <button
            type="submit"
            className="btn btn-primary"
            id="calc-btn"
            onClick={handleSubmit}
          >
            Calculate
          </button>
        </div>
      </form>
      <div className="table-container">
        {jsonData !== null && "risk_metrics" in jsonData && (
          <SimpleTable
            primary_data={jsonData["risk_metrics"]}
            metric_column="Risk Measure"
            value_column="Value in pct"
            table_title="High level risk summary"
          />
        )}
      </div>
      <div className="chart-container" id="top-right-chart-container">
        {jsonData !== null && "exposures" in jsonData && (
            <div/>
        )}
      </div>
    </div>
  );
}

export default RiskCalcPage;
