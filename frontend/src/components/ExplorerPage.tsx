import { useState } from "react";
import "./ExplorerPage.css";
import { API } from "../Api";
import LineChart from "./charts/LineChart";
import ReturnChart from "./charts/ReturnChart";
// https://dev.to/deboragaleano/how-to-handle-multiple-inputs-in-react-55el

function ExplorerPage() {
  const [jsonData, setJsonData] = useState(null);

  const errorStyles = {
    "0": "alert alert-info",
    "1": "alert alert-warning",
    "404": "alert alert-danger",
  };

  const initialValues = {
    symbol: "BTC-USD",
    halflife: "30",
    min_obs: "30",
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
      const response = await fetch(API + "crypto/api/get_raw_price_data", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({
          symbol: values["symbol"],
          halflife: values["halflife"],
          min_obs: values["min_obs"],
        }),
      });
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
      <link href="/ExplorerPage.css"></link>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label
            htmlFor="ticker_input"
            className="ticker-input-label"
            style={{ textAlign: "left" }}
          >
            Enter a crypto symbol
          </label>
          <input
            type="ticker_input"
            className="form-control"
            id="ticker-input"
            // placeholder="BTC-USD"
            value={values.symbol}
            onChange={handleInputChange("symbol")}
          ></input>
          <label
            htmlFor="half-life-label"
            className="half-life-label"
            style={{ textAlign: "left" }}
          >
            Specify half-life parameter (in days)
          </label>
          <input
            type="ticker_input"
            className="form-control"
            id="half-life-input"
            // placeholder="30"
            value={values.halflife}
            onChange={handleInputChange("halflife")}
          ></input>
          <label
            htmlFor="obs-number"
            className="obs-number-label"
            style={{ textAlign: "left" }}
          >
            Minimum number of observations for risk calculation (in days)
          </label>
          <input
            type="ticker_input"
            className="form-control"
            id="obs-number-input"
            // placeholder="30"
            value={values.min_obs}
            onChange={handleInputChange("min_obs")}
          ></input>
          <button
            type="submit"
            className="btn btn-primary"
            id="explore-btn"
            onClick={handleSubmit}
          >
            Explore
          </button>
        </div>
      </form>
      <div className="chart-container">
        {jsonData !== null && "raw_price" in jsonData && jsonData["ERROR_CODE"]!= "404" && (
          <LineChart
            primaryData={jsonData["raw_price"]["close"]}
            titleText={"Price data for " + jsonData["symbol"]}
            primaryDataLabel={jsonData["symbol"]}
            xAxisTitle="Date"
            yAxisTitle="Close Price (USD)"
          />
        )}
        {jsonData !== null && "return_data" in jsonData && "ewma" in jsonData && (
          <ReturnChart
            primaryData={jsonData["return_data"]["total_return"]}
            primaryDataLabel="Total returns"
            titleText={
              "Risk estimates and total returns for " + jsonData["symbol"]
            }
            xAxisTitle="Date"
            yAxisTitle="Return and Std. dev. (0.01 = 1 pct)"
            secondaryData={jsonData["ewma"]["ewma_std"]}
            secondaryDataLabel="EWMA Std. Dev. Estimates"
          />
        )}
        {jsonData !== null && (
          <div className={errorStyles[jsonData["ERROR_CODE"]]} role="alert" style={{ textAlign: "left" }}>
            {jsonData["log"]}
          </div>
        )}
      </div>
    </div>
  );
}

export default ExplorerPage;
