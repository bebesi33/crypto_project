import { useEffect, useState } from 'react';
import { API } from '../Api';


function ExplorerPage() {

    const [jsonData, setJsonData] = useState(null);

    useEffect(() => {
        // Simple data fetch
        fetch(API + 'crypto/api/get_raw_price_data')  // fetch json value from url
            .then(response => response.json())
            .then(data => setJsonData(data))
            .catch(error => console.error('Error fetching data:', error));
    }, []);


    return (
        <div> 
            <br></br>
            <br></br>
            Explorer Page
            The json content should be here
            <br></br>
            {jsonData && (
                <pre>{JSON.stringify(jsonData, null, 2)}</pre>
            )}
        </div>
    )
}

export default ExplorerPage;