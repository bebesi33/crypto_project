import { useState, useEffect, useRef } from "react";
import "./assets/css/explorer_page.css";
import { API } from "../Api";
import LineChart from "./charts/LineChart";
import ReturnChart from "./charts/ReturnChart";
import { errorStyles } from "./Colors";
import csrftoken from "./token/Token";
import html2pdf from "html2pdf.js";
import axios from "axios";

// https://dev.to/deboragaleano/how-to-handle-multiple-inputs-in-react-55el

function ExplorerPage() {
  const [jsonData, setJsonData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isContentReady, setIsContentReady] = useState(true);
  const [isUnderExport, setIsUnderExport] = useState(false);
  const contentRef = useRef<HTMLDivElement>(null);
  //  https://www.nutrient.io/blog/how-to-convert-html-to-pdf-using-html2df-and-react/

  const initialValues = {
    symbol: "BTC-USD",
    halflife: "30",
    min_obs: "30",
    mean_to_zero: false,
  };
  const [values, setValues] = useState(initialValues);

  const handleExport = (event: { preventDefault: () => void }) => {
    event.preventDefault();
    setIsLoading(true);
    setIsUnderExport(true);
  }; // end handleExport

  const generateFileName = (): string => {
    const now = new Date();
    const timeStamp = now.toISOString().replace(/[:.]/g, "-");
    const filename = values.symbol.concat("-", timeStamp.toString());
    return filename;
  }; // end generateFileName

  useEffect(() => {
    if (isUnderExport) {
      const filename = generateFileName();
      const contentReference = contentRef.current;
      console.log(contentReference);
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
            setIsLoading(false);
            setIsUnderExport(false);
            document.body.classList.remove("exclude-from-pdf");
          });
      } else {
        console.error("Element not found");
        setIsLoading(false);
        setIsUnderExport(false);
      }
    }
  }, [isUnderExport]); // end useEffect

  const handleInputChange =
    (property: string) => (event: React.ChangeEvent<HTMLInputElement>) => {
      if (property == "mean_to_zero") {
        setValues({
          ...values,
          ["mean_to_zero"]: !values.mean_to_zero,
        });
      } else {
        setValues({
          ...values,
          [property]: event.target.value,
        });
      }
    };

  const handleSubmit = async (event: { preventDefault: () => void }) => {
    event.preventDefault();
    try {
      setIsLoading(true);
      const response = await axios.post(
        API + "crypto/api/get_raw_price_data",
        {
          symbol: values["symbol"],
          halflife: values["halflife"],
          min_obs: values["min_obs"],
          mean_to_zero: values["mean_to_zero"],
        },
        {
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
          },
          withCredentials: true,
          responseType: 'json',
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
  }; // end handleSubmit

  return (
    <div
      className="parent-container"
      id="main-exploler-page-container"
      ref={contentRef}
    >
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label
            htmlFor="ticker-input"
            className="ticker-input-label"
            style={{ textAlign: "left" }}
          >
            Enter a crypto symbol
          </label>
          <input
            type="text"
            className="form-control"
            id="ticker-input"
            value={values.symbol}
            onChange={handleInputChange("symbol")}
          ></input>
          <label
            htmlFor="half-life-input"
            className="half-life-label"
            style={{ textAlign: "left" }}
          >
            Specify half-life parameter (in days)
          </label>
          <input
            type="number"
            className="form-control"
            id="half-life-input"
            value={values.halflife}
            onChange={handleInputChange("halflife")}
            title="This should be a number greater than 0"
          ></input>
          <label
            htmlFor="obs-number-input"
            className="obs-number-label"
            style={{ textAlign: "left" }}
          >
            Minimum number of observations for risk calculation (in days)
          </label>
          <input
            type="number"
            className="form-control"
            id="obs-number-input"
            value={values.min_obs}
            onChange={handleInputChange("min_obs")}
            title="This should be a number greater than 1"
          ></input>

          <label
            htmlFor="exp-mean-to-zero-box"
            className="exp-mean-to-zero-box-label"
            title="No demeaning in risk calculation"
          >
            <span>Set mean to zero</span>
          </label>
          <input
            type="checkbox"
            id="exp-mean-to-zero-box"
            checked={values.mean_to_zero}
            onChange={handleInputChange("mean_to_zero")}
          />

          <button
            type="submit"
            className="btn btn-primary exclude-from-pdf"
            id="explore-btn"
            onClick={handleSubmit}
            disabled={isLoading}
          >
            {isLoading && (
              <span
                className="spinner-border spinner-border-sm"
                role="status"
                aria-hidden="true"
              ></span>
            )}
            Explore
          </button>
        </div>
      </form>
      <button
        type="submit"
        className="btn btn-primary exclude-from-pdf"
        id="export-btn"
        onClick={handleExport}
        disabled={isLoading || !isContentReady || isUnderExport}
      >
        {isUnderExport && (
          <span
            className="spinner-border spinner-border-sm"
            role="status"
            aria-hidden="true"
          ></span>
        )}
        Export to PDF
      </button>
      <div className="chart-container" ref={contentRef}>
        {jsonData !== null && (
          <p
            className={errorStyles[jsonData["ERROR_CODE"]]}
            role="alert"
            style={{ textAlign: "left" }}
          >
            {jsonData["log"]}
          </p>
        )}
        {jsonData !== null &&
          "raw_price" in jsonData &&
          jsonData["ERROR_CODE"] != "404" && (
            <LineChart
              primaryData={jsonData["raw_price"]["close"]}
              titleText={"Price data for " + jsonData["symbol"]}
              primaryDataLabel={jsonData["symbol"]}
              xAxisTitle="Date"
              yAxisTitle="Close Price (USD)"
            />
          )}
        {jsonData !== null &&
          "return_data" in jsonData &&
          "ewma" in jsonData && (
            <ReturnChart
              primaryData={jsonData["return_data"]["total_return"]}
              primaryDataLabel="Returns"
              titleText={"Risk estimates and returns for " + jsonData["symbol"]}
              xAxisTitle="Date"
              yAxisTitle="Return and Std. dev. (0.01 = 1 pct)"
              secondaryData={jsonData["ewma"]["ewma_std"]}
              secondaryDataLabel="EWMA Std. Dev. Estimates"
            />
          )}
      </div>
    </div>
  );
}

export default ExplorerPage;
