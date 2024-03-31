import { useState } from "react";
import { API } from "../Api";
import { getTextAlign } from "./Utilities";

function RiskCalcPage() {
  const [jsonData, setJsonData] = useState(null);

  const initialValues = {
    cob_date: "2024-03-03",
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
    <div>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label
            htmlFor="ticker_input"
            className="ticker_input-label"
            style={{ textAlign: getTextAlign("left") }}
          >
            Enter the date of calculation
          </label>
          <input
            type="ticker_input"
            className="form-control"
            id="ticker_input"
            value={values.cob_date}
            onChange={handleInputChange("cob_date")}
          ></input>
          <button
            type="submit"
            className="btn btn-primary"
            onClick={handleSubmit}
          >
            Calculate
          </button>
        </div>
      </form>
      {jsonData !== null && (
        <div>
          {Object.keys(jsonData["risk_metrics"]).map((key) => (
            <div key={key}>{jsonData["risk_metrics"][key]}</div>
          ))}
        </div>
      )}
    </div>
  );
}

export default RiskCalcPage;
