import {useEffect, SetStateAction, useState } from "react";
import "./ExplorerPage.css";
import { API } from "../Api";

function ExplorerPage() {

    const [jsonData, setJsonData] = useState(null);
    const [inputValue, setInputValue] = useState('');

    const makeRequest = () => {
        console.log('Input value:', inputValue);
    };

    const handleInputChange = (event: { target: { value: SetStateAction<string>; }; }) => {
        setInputValue(event.target.value);
    };

    const handleSubmit = async (event: { preventDefault: () => void; }) => {
        event.preventDefault();

        try {
        // Make a POST request to your backend
        const response = await fetch(API + 'crypto/api/get_raw_price_data', {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({ inputString: inputValue }), // Send the input value
        });
        console.log(response);
        if (response.ok) {
            // Handle success (e.g., show a success message)
            useEffect(() => {
                // Simple data fetch
                fetch(API + 'crypto/api/get_raw_price_data')  // fetch json value from url
                    .then(response => response.json())
                    .then(data => setJsonData(data))
                    .catch(error => console.error('Error fetching data:', error));
            }, []);
            console.log('Data sent successfully!');
        } else {
            console.error('Error sending data to the backend.');
        }
        } catch (error) {
        console.error('An error occurred:', error);
        }
    };


  return (
    <div className="parent-container">
      <link href="/ExplorerPage.css"></link>
      <form  onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="ticker_input" className='ticker_input-label'>Choose a ticker</label>
          <input
            type="ticker_input"
            className="form-control"
            id="ticker_input"
            placeholder="BTC-USD"
            value={inputValue}
            onChange={handleInputChange}
          ></input>
          <button type="submit" className="btn btn-primary" onClick={makeRequest}>
            Explore
          </button>
        </div>
        {jsonData && (
                <pre>{JSON.stringify(jsonData, null, 2)}</pre>
        )}
      </form>
    </div>
  );
}

export default ExplorerPage;
