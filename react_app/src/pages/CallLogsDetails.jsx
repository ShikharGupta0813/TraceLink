import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import DataTable from '../components/DataTable';  // Importing the DataTable component

const CallLogsDetails = () => {
  const { caseId } = useParams();  // Extract caseId from URL
  const [callLogData, setCallLogData] = useState(null);  // State to store the fetched data

  useEffect(() => {
    // Fetching data for call logs
    const fetchCallLogsData = async () => {
      try {
        const response = await axios.get(`http://10.100.237.49:5000/api/cases/${caseId}/evaluate/calllogs`);
        setCallLogData(response.data);  // Storing the fetched data
      } catch (error) {
        console.error("Error fetching call logs data:", error);
        alert("Failed to load call logs data");
      }
    };

    fetchCallLogsData();  // Calling the function to fetch data
  }, [caseId]);  // Effect runs when the caseId changes

  if (!callLogData) {
    return <div>Loading call logs data...</div>;
  }

  return (
    <div style={{ backgroundColor: '##1e1e2f', minHeight: '100vh', padding: '2rem' }}>
      <h1 style={{ color: '#fff', fontSize: '2.5rem', fontWeight: 'bold' }}>
        📞 Call Logs Details
      </h1>

      <div style={{ marginTop: '3rem', color: '#fff' }}>
        {/* Log 1: Repeated Calls */}
        <h2>Log 1: Repeated Calls</h2>
        <DataTable 
          data={callLogData.log} 
          columns={[
            { name: 'Call Count', field: 'call_count' },
            { name: 'Phone Number', field: 'number' }
          ]}
        />

        {/* Log 2: Call Durations */}
        <h2>Log 2: Call Durations</h2>
        <DataTable 
          data={callLogData.log1} 
          columns={[
            { name: 'Phone Number', field: 'number' },
            { name: 'Total Duration', field: 'total_duration' }
          ]}
        />

        {/* Log 3: Call Using Multiple Devices */}
        <h2>Log 3: Call Using Multiple Devices</h2>
        <DataTable 
          data={callLogData.log3} 
          columns={[
            { name: 'Call Count', field: 'call_count' },
            { name: 'Phone Number', field: 'number' }
          ]}
        />
      </div>
    </div>
  );
};

export default CallLogsDetails;
