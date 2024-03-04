import { useEffect, useState } from 'react';
import axios from 'axios';


function ExplorerPage() {

    const [jsonData, setJsonData] = useState(null);

    useEffect(() => {
        async function fetchData() {
            try {
                const response = await axios.get('/api/get_raw_price_data/');
                setJsonData(response.data);
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        }
        fetchData();
    }, []);


    return (
        <div> 
            <br></br>
            <br></br>
            Explorer Page
            {jsonData && (
                <pre>{JSON.stringify(jsonData, null, 2)}</pre>
            )}
        </div>
    )
}

export default ExplorerPage;