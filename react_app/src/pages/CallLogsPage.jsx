import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import DataTable from '../components/DataTable';

const CallLogsPage = () => {
  const { id } = useParams();
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    axios
      .get(`http://10.100.237.49:5000/api/devices/${id}/call-logs`)
      .then(res => {
        console.log('API response:', res.data);
        setLogs(res.data.call_log || []);
      })
      .catch(err => console.error(err));
  }, [id]);


  return (
    <div style={{ backgroundColor: '#1e1e2f', minHeight: '100vh', padding: '2rem' }}>
      <h1 style={{ color: '#fff' }}>📞 Call Logs</h1>
      <DataTable data={logs} />
    </div>
  );
};

export default CallLogsPage;
