import { SetStateAction, useState } from "react";
import "./ExplorerPage.css";
import { API } from "../Api";
import LineChart from "./charts/LineChart";


function ExplorerPage() {
  const [jsonData, setJsonData] = useState(null);
  const [inputValue, setInputValue] = useState("");

  const makeRequest = () => {
    console.log("Input value:", inputValue);
  };

  const handleInputChange = (event: {
    target: { value: SetStateAction<string> };
  }) => {
    setInputValue(event.target.value);
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
        body: JSON.stringify({ symbol: inputValue }),
      });
      console.log(response);
      if (response.ok) {
        const jsonData = await response.json();
        console.log("Data received successfully!");
        console.log(jsonData["symbol"])
        console.log(jsonData["symbol"])        
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
          <label htmlFor="ticker_input" className="ticker_input-label">
            Enter a crypto symbol
          </label>
          <input
            type="ticker_input"
            className="form-control"
            id="ticker_input"
            placeholder="BTC-USD"
            value={inputValue}
            onChange={handleInputChange}
          ></input>
          <button
            type="submit"
            className="btn btn-primary"
            onClick={makeRequest}
          >
            Explore
          </button>
        </div>
      </form>
      {jsonData !== null && (<LineChart
        input_values={jsonData["raw_price"]["close"]}
        title= {jsonData["symbol"]}
        x_axis_title="Date"
        y_axis_title="Close Price (USD)"
      />)}
      {/* {jsonData && <pre>{JSON.stringify(jsonData, null, 2)}</pre>} */}
    </div>
  );
}

export default ExplorerPage;
