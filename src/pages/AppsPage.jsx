import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import DataTable from '../components/DataTable';

const InstalledAppsPage = () => {
  const { id } = useParams();
  const [apps, setApps] = useState([]);

  useEffect(() => {
    axios.get(`http://10.100.237.49:5000/api/devices/${id}/installed-apps`)
      .then(res => setApps(res.data.app_data))
      .catch(err => console.error(err));
  }, [id]);

  return (
    <div style={{ backgroundColor: '#6a0dad', minHeight: '100vh', padding: '2rem' }}>
      <h1 style={{ color: '#fff' }}>📦 Installed Applications</h1>
      <DataTable data={apps} />
    </div>
  );
};

export default InstalledAppsPage;
