import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import '../index.css';
import { useNavigate } from 'react-router-dom';


function Home() {
  const navigate = useNavigate();
  const [cases, setCases] = useState([]);

  const [showingCases, setShowingCases] = useState(false);

  const fetchCases = async () => {
    try {
      const response = await axios.get('http://10.100.237.49:5000/api/cases');
      console.log("Fetched cases:", response.data); // 👈 check what this logs
      setCases(response.data.cases);
      setShowingCases(true);
    } catch (error) {
      console.error('Error fetching cases:', error);
      alert('Failed to load cases');
    }
  };


  return (
    <div className="container">
      <h1 className="title">TraceLink</h1>

      <div>
        <Link to="/add-case">
          <button className="btn add">Add Case</button>
        </Link>
        <button className="btn show" onClick={fetchCases}>
          Show All Cases
        </button>
      </div>

      {showingCases && (
        <div className="cases-grid">
          {cases.map((c) => (
            <button
              key={c.id}
              className="case-btn"
              onClick={() => navigate(`/cases/${c.id}/add-device`, { state: { caseName: c.name } })}
            >
              <strong>{c.name}</strong><br />
              <small>ID: {c.id}</small><br />
              <small>{new Date(c.created_at.replace(' ', 'T')).toLocaleString()}</small>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

export default Home;





