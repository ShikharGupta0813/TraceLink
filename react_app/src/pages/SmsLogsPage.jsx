import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import DataTable from '../components/DataTable';

const SmsLogsPage = () => {
  const { id } = useParams();
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    axios.get(`http://10.100.237.49:5000/api/devices/${id}/sms-logs`)
      .then(res => {
        console.log("SMS Log Response:", res.data);
        setLogs(res.data.sms_data || []); // ✅ Only set the array
      })
      .catch(err => console.error(err));
  }, [id]);
  

  return (
    <div style={{ backgroundColor: '#1e1e2f', minHeight: '100vh', padding: '2rem' }}>
      <h1 style={{ color: '#fff' }}>💬 SMS Logs</h1>
      <DataTable data={logs} />
    </div>
  );
};

export default SmsLogsPage;
