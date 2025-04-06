import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import DataTable from '../components/DataTable';

const OsDetailsPage = () => {
  const { id } = useParams();
  const [osDetails, setOsDetails] = useState(null);

  useEffect(() => {
    axios.get(`http://10.100.237.49:5000/api/os-details`)
      .then(res => setOsDetails(res.data))
      .catch(err => console.error(err));
  }, [id]);

  return (
    <div style={{ backgroundColor: '#6a0dad', minHeight: '100vh', padding: '2rem' }}>
      <h1 style={{ color: '#fff' }}>🖥️ Operating System Details</h1>

      {osDetails ? (
        Object.entries(osDetails).map(([section, output]) => (
          <div key={section} style={{ marginBottom: '2rem', background: '#4a0072', padding: '1rem', borderRadius: '12px' }}>
            <h2 style={{ color: '#fff', marginBottom: '0.5rem' }}>{section.replace(/_/g, ' ').toUpperCase()}</h2>
            <pre style={{ color: '#fff', whiteSpace: 'pre-wrap' }}>{output}</pre>
          </div>
        ))
      ) : (
        <p style={{ color: '#fff' }}>Loading...</p>
      )}
    </div>
  );
};

export default OsDetailsPage;
