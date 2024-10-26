import { useState, useEffect, useRef } from "react";
import { API } from "../Api";
import "./assets/css/risk_calc_page.css";
import SimpleTable from "./tables/SimpleTable";
import ExposureChart from "./charts/ExposureChart";
import MarginalContribChart from "./charts/MarginalContribChart";
import { errorStyles } from "./Colors";
import PortfolioTable from "./tables/PortfolioTable";
import RiskDecompositionChart from "./charts/RiskDecomposition";
import csrftoken from "./token/Token";
import html2pdf from "html2pdf.js";
import axios from "axios";

function RiskCalcPage() {
  const [jsonData, setJsonData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const initialInputValues = {
    cob_date: "2023-12-31",
    correlation_hl: "60",
    factor_risk_hl: "30",
    specific_risk_hl: "30",
    min_ret_hist: "20",
    portfolio: null,
    benchmark: null,
    mean_to_zero: false,
    use_factors: true,
  };
  const [inputValues, setInputValues] = useState(initialInputValues);
  const [isUnderExport, setIsUnderExport] = useState(false);
  const contentRef = useRef<HTMLDivElement>(null);
  const [isContentReady, setIsContentReady] = useState(false);

  const handleExport = (event: { preventDefault: () => void }) => {
    event.preventDefault();
    setIsUnderExport(true);
  }; // end handleExport

  const generateFileName = (): string => {
    const now = new Date();
    const timeStamp = now.toISOString().replace(/[:.]/g, "-");
    const filename = inputValues.cob_date.concat("-", timeStamp.toString());
    return filename;
  }; // end generateFileName

  useEffect(() => {
    if (isUnderExport) {
      const filename = generateFileName();
      const contentReference = contentRef.current;
      if (contentReference) {
        const options = {
          margin: 1,
          filename: filename,
          image: { type: "jpeg", quality: 0.98 },
          html2canvas: {
            scale: 3,
            scrollY: 0,
            useCORS: true,
            width: contentReference.scrollWidth,
            height: contentReference.scrollHeight,
            onclone: (documentClone: {
              querySelectorAll: (arg0: string) => any[];
            }) => {
              documentClone
                .querySelectorAll(".exclude-from-pdf")
                .forEach((element) => {
                  element.style.display = "none";
                });
            }, // very crude solution to drop the buttons
          },
          jsPDF: { unit: "in", format: "letter", orientation: "portrait" },
        };
        html2pdf()
          .from(contentReference)
          .set(options)
          .save()
          .then(() => {
            setIsUnderExport(false);
            document.body.classList.remove("exclude-from-pdf");
          });
      } else {
        console.error("Element not found");
        setIsUnderExport(false);
      }
    }
  }, [isUnderExport]); // end useEffect

  const handleInputChange =
    (property: string) => (event: React.ChangeEvent<HTMLInputElement>) => {
      if (property == "mean_to_zero" || property == "use_factors") {
        setInputValues({
          ...inputValues,
          [property]: !inputValues[property],
        });
      } else {
        setInputValues({
          ...inputValues,
          [property]: event.target.value,
        });
      }
    };

  const handleFileInputChange =
    (property: string) => (event: React.ChangeEvent<HTMLInputElement>) => {
      if (event.target.files) {
        const file = event.target.files[0];
        const reader = new FileReader();

        reader.addEventListener(
          "load",
          () => {
            const file_content = reader.result;
            setInputValues({
              ...inputValues,
              [property]: file_content,
            });
          },
          false
        );
        reader.readAsText(file);
      }
    };

  const handleSubmit = async (event: { preventDefault: () => void }) => {
    event.preventDefault();
    try {
      setIsLoading(true);
      const response = await axios.post(
        API + "crypto/api/get_risk_calculation_output",
        {
          cob_date: inputValues["cob_date"],
          correlation_hl: inputValues["correlation_hl"],
          factor_risk_hl: inputValues["factor_risk_hl"],
          specific_risk_hl: inputValues["specific_risk_hl"],
          min_ret_hist: inputValues["min_ret_hist"],
          portfolio: inputValues["portfolio"],
          benchmark: inputValues["benchmark"],
          mean_to_zero: inputValues["mean_to_zero"],
          use_factors: inputValues["use_factors"],
        },
        {
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
          },
          withCredentials: true,
          responseType: "json",
        }
      );
      if (response.status == 200) {
        const jsonData = await response.data;
        console.log("Data received successfully!");
        setJsonData(jsonData);
        setIsLoading(false);
        setIsContentReady(true);
      } else {
        console.error("Error sending data to the backend.");
        setIsLoading(false);
        setIsContentReady(false);
      }
    } catch (error) {
      console.error("An error occurred:", error);
      setIsLoading(false);
      setIsContentReady(false);
    }
  };

  return (
    <div className="parent-container" ref={contentRef}>
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
            type="date"
            className="form-control"
            id="cob-input"
            value={inputValues.cob_date}
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
            accept=".csv"
            onChange={handleFileInputChange("portfolio")}
            title="Only .csv input , with ',' and ';' separation is allowed. Each row should contain one symbol and its weight."
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

          <input
            className="form-control"
            id="market-input"
            type="file"
            accept=".csv"
            onChange={handleFileInputChange("benchmark")}
            title="Only .csv input , with ',' and ';' separation is allowed. Each row should contain one symbol and its weight."
          ></input>

          <strong>
            <h6 className="parameters" style={{ textAlign: "left" }}>
              Risk calculation parameters (all in days)
            </h6>
          </strong>

          <label
            htmlFor="hl-risk-input"
            className="hl-risk-input-label"
            style={{ textAlign: "left" }}
            title="This should be a number greater than 0"
          >
            Factor risk half-life
          </label>
          <input
            type="number"
            className="form-control"
            id="hl-risk-input"
            value={inputValues.factor_risk_hl}
            onChange={handleInputChange("factor_risk_hl")}
            style={{ direction: "rtl" }}
            title="This should be a number greater than 0"
          ></input>

          <label
            htmlFor="hl-corr-input"
            className="hl-corr-input-label"
            style={{ textAlign: "left" }}
          >
            Factor correlation half-life
          </label>
          <input
            type="number"
            className="form-control"
            id="hl-corr-input"
            value={inputValues.correlation_hl}
            onChange={handleInputChange("correlation_hl")}
            style={{ direction: "rtl" }}
            title="This should be a number greater than 0"
          ></input>

          <label
            htmlFor="min-ret-hist-input"
            className="min-ret-hist-input-label"
            style={{ textAlign: "left" }}
          >
            Min. return history length
          </label>
          <input
            type="number"
            className="form-control"
            id="min-ret-hist-input"
            value={inputValues.min_ret_hist}
            onChange={handleInputChange("min_ret_hist")}
            style={{ direction: "rtl" }}
            title="This should be a number greater than 1"
          ></input>

          <label
            htmlFor="spec-hl-risk-input"
            className="spec-hl-risk-input-label"
            style={{ textAlign: "left" }}
          >
            Specific risk half-life
          </label>
          <input
            type="number"
            className="form-control"
            id="spec-hl-risk-input"
            value={inputValues.specific_risk_hl}
            onChange={handleInputChange("specific_risk_hl")}
            style={{ direction: "rtl" }}
            title="This should be a number greater than 0"
          ></input>

          <label
            htmlFor="mean-to-zero-box"
            className="mean-to-zero-box-label"
            title="No demeaning in risk calculation"
          >
            <span>Set mean to zero</span>
          </label>
          <input
            type="checkbox"
            id="mean-to-zero-box"
            checked={inputValues.mean_to_zero}
            onChange={handleInputChange("mean_to_zero")}
          />

          <label
            htmlFor="use-factors-box"
            className="use-factors-box-label"
            title="Abandon the usage of style factors and treat all symbols as a single factor"
          >
            <span>Use factors</span>
          </label>
          <input
            type="checkbox"
            id="use-factors-box"
            checked={inputValues.use_factors}
            onChange={handleInputChange("use_factors")}
          />

          <span
            className="tool-tip"
            data-toggle="tooltip"
            data-placement="top"
            title="Please provide portfolio input to start the calculation"
          >
            <button
              type="submit"
              className="btn btn-primary exclude-from-pdf"
              id="calc-btn"
              onClick={handleSubmit}
              disabled={isLoading || isUnderExport || inputValues["portfolio"] == null}
            >
              {isLoading && (
                <span
                  className="spinner-border spinner-border-sm"
                  role="status"
                  aria-hidden="true"
                ></span>
              )}
              Calculate
            </button>
          </span>
        </div>
      </form>

      <button
        type="submit"
        className="btn btn-primary exclude-from-pdf"
        id="export-rc-btn"
        onClick={handleExport}
        disabled={isLoading || !isContentReady || isUnderExport}
      >
        {isUnderExport && (
          <span
            className="spinner-border spinner-border-sm"
            role="status"
            aria-hidden="true"
            title="Only available if risk calculation output is rendered on the screen"
          ></span>
        )}
        Export to PDF
      </button>

      <div className="log-container">
        {jsonData !== null && (
          <div
            className={errorStyles[jsonData["ERROR_CODE"]]}
            role="alert"
            style={{ textAlign: "left" }}
          >
            {jsonData["log"]}
          </div>
        )}
      </div>
      <div className="chart-container" id="top-right-chart-container">
        {jsonData !== null && "decomposition" in jsonData && (
          <RiskDecompositionChart
            primaryData={jsonData["decomposition"]}
            titleText="Risk decomposition"
          />
        )}
      </div>
      <div className="table-container">
        {jsonData !== null && "risk_metrics" in jsonData && (
          <SimpleTable
            primaryData={jsonData["risk_metrics"]}
            metricColumn="Risk Measure"
            valueColumn="Value in pct"
            tableTitle="High level risk summary"
          />
        )}
      </div>
      {jsonData !== null && (
        <div
          className="chart-container"
          id="bot-first-chart-container"
          style={{ top: jsonData["model"] === "factor" ? 635 : 465 }}
        >
          {"mctr" in jsonData && (
            <MarginalContribChart
              primaryData={jsonData["mctr"]}
              titleText="Marginal contribution to variance breakdown"
            />
          )}
        </div>
      )}

      {jsonData !== null && (
        <div
          className="portfolio-table-container"
          id="portfolio-table-container"
          style={{ top: jsonData["model"] === "factor" ? 1050 : 880 }}
        >
          {"all_portfolios" in jsonData && (
            <PortfolioTable
              primaryData={jsonData["all_portfolios"]}
              tableTitle="Portfolio compositon by symbols"
            />
          )}
        </div>
      )}
      {jsonData !== null && (
        <div
          className="chart-container"
          id="bottom-right-chart-container"
          style={{ top: jsonData["model"] === "factor" ? 1050 : 880 }}
        >
          {"exposures" in jsonData && (
            <ExposureChart
              primaryData={jsonData["exposures"]}
              titleText={
                jsonData["model"] === "factor"
                  ? "Factor exposure breakdown"
                  : "Exposure breakdown (top 10 only)"
              }
            />
          )}
        </div>
      )}
    </div>
  );
}

export default RiskCalcPage;
