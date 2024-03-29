import { SetStateAction, useState } from "react";
import "./ExplorerPage.css";
import { API } from "../Api";
import LineChart from "./charts/LineChart";
import ReturnChart from "./charts/ReturnChart";
import { getTextAlign } from "./Utilities";
// https://dev.to/deboragaleano/how-to-handle-multiple-inputs-in-react-55el

function ExplorerPage() {
  const [jsonData, setJsonData] = useState(null);
  // const [hlInputValue, setHlInputValue] = useState("30");
  // const [obsInputValue, setObsInputValue] = useState("30");
  // const [inputValue, setInputValue] = useState("BTC-USD");

  const initialValues = {
    symbol: "BTC-USD",
    halflife: "30",
    min_obs: "30",
  };
  const [values, setValues] = useState(initialValues);

  const handleInputChange = (event: {
    target: {
      name: string;
      value: SetStateAction<string>;
    };
  }) => {
    //const name = e.target.name
    //const value = e.target.value
    const name = event.target.name;
    const value = event.target.value;

    setValues({
      ...values,
      [name]: value,
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
      console.log(response);
      if (response.ok) {
        const jsonData = await response.json();
        console.log("Data received successfully!");
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
            className="ticker_input-label"
            style={{ textAlign: getTextAlign("left") }}
          >
            Enter a crypto symbol
          </label>
          <input
            type="ticker_input"
            className="form-control"
            id="ticker_input"
            placeholder="BTC-USD"
            value={values.symbol}
            onChange={handleInputChange}
          ></input>
          <label
            htmlFor="half-life"
            className="half-life-label"
            style={{ textAlign: getTextAlign("left") }}
          >
            Specify half life parameter (in days)
          </label>
          <input
            type="halflife_input"
            className="half-life-input"
            id="half_life_input"
            placeholder="30"
            value={values.halflife}
            onChange={handleInputChange}
          ></input>
          <label
            htmlFor="obs-number"
            className="obs-number-label"
            style={{ textAlign: getTextAlign("left") }}
          >
            Minimum number of observations for risk calculation (in days)
          </label>
          <input
            type="obs_number_input"
            className="obs-number-input"
            id="obs_number_input"
            placeholder="30"
            value={values.min_obs}
            onChange={handleInputChange}
          ></input>
          <button
            type="submit"
            className="btn btn-primary"
            onClick={handleSubmit}
          >
            Explore
          </button>
        </div>
      </form>
      <div className="chart-container">
        {jsonData !== null && (
          <LineChart
            primary_data={jsonData["raw_price"]["close"]}
            title_text={"Price data for " + jsonData["symbol"]}
            primary_data_label={jsonData["symbol"]}
            x_axis_title="Date"
            y_axis_title="Close Price (USD)"
          />
        )}
        {jsonData !== null && (
          <ReturnChart
            primary_data={jsonData["return_data"]["total_return"]}
            primary_data_label="Total returns"
            title_text={
              "Risk estimates and total returns for " + jsonData["symbol"]
            }
            x_axis_title="Date"
            y_axis_title="Return and Std. dev. (0.01 = 1 pct)"
            secondary_data={jsonData["ewma"]["ewma_std"]}
            secondary_data_label="EWMA Std. Dev. Estimates"
          />
        )}
      </div>
    </div>
  );
}

export default ExplorerPage;
