import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import DataTable from '../components/DataTable';  // Importing the DataTable component

const SmsDetails = () => {
  const { caseId } = useParams();  // Extract caseId from URL
  const [smsData, setSmsData] = useState(null);  // State to store the fetched data

  useEffect(() => {
    // Fetching data for SMS logs
    const fetchSmsData = async () => {
      try {
        const response = await axios.get(`http://10.100.237.49:5000/api/cases/${caseId}/evaluate/sms`);
        setSmsData(response.data);  // Storing the fetched data
      } catch (error) {
        console.error("Error fetching SMS data:", error);
        alert("Failed to load SMS data");
      }
    };

    fetchSmsData();  // Calling the function to fetch SMS data
  }, [caseId]);  // Effect runs when the caseId changes

  if (!smsData) {
    return <div>Loading SMS data...</div>;
  }

  return (
    <div style={{ backgroundColor: '##1e1e2f', minHeight: '100vh', padding: '2rem' }}>
      <h1 style={{ color: '#fff', fontSize: '2.5rem', fontWeight: 'bold' }}>
        💬 SMS Logs Details
      </h1>

      <div style={{ marginTop: '3rem', color: '#fff' }}>
        {/* Log 1: SMS Counts */}
        <h2>Log 1: Frequent SMS </h2>
        <DataTable 
          data={smsData.log} 
          columns={[
            { name: 'SMS Count', field: 'sms_count' },
            { name: 'Phone Number', field: 'number' }
          ]}
        />

        {/* Log 2: SMS Duration (if available) */}
        <h2>Log 2: Duplicate SMS</h2>
        <DataTable 
          data={smsData.log1} 
          columns={[
            { name: 'Phone Number', field: 'number' },
            { name: 'Total SMS Duration', field: 'total_sms_duration' }
          ]}
        />

        {/* Log 3: SMS Using Multiple Devices */}
        <h2>Log 3: Excessive SMS</h2>
        <DataTable 
          data={smsData.log3} 
          columns={[
            { name: 'SMS Count', field: 'sms_count' },
            { name: 'Phone Number', field: 'number' }
          ]}
        />
      </div>
    </div>
  );
};

export default SmsDetails;
