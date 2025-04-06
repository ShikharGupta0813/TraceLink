import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { FaMobileAlt, FaLaptop, FaSearch } from 'react-icons/fa'; // Importing FaSearch icon
import '../index.css';

function Home() {
  const navigate = useNavigate();
  const [cases, setCases] = useState([]);
  const [showingCases, setShowingCases] = useState(false);

  const fetchCases = async () => {
    try {
      const response = await axios.get('http://10.100.237.49:5000/api/cases');
      console.log("Fetched cases:", response.data);
      setCases(response.data.cases);
      setShowingCases(true);
    } catch (error) {
      console.error('Error fetching cases:', error);
      alert('Failed to load cases');
    }
  };

  return (
    <div className="container">
      <h1 className="track-trace">
        <FaSearch style={{ marginRight: '10px', fontSize: '8rem', color: '#fff' }} /> TraceLink
      </h1>


      <div className="project-description">
        <p>
          The **Multi-Device Forensics Tool** is a powerful and comprehensive solution designed for digital forensics investigations. This tool enables investigators to extract, analyze, and correlate critical data from multiple devices, including **Android phones** and **Operating System**. With its easy-to-use interface, the tool allows users to retrieve vital information such as call logs, text messages, app data, system logs, and much more. By supporting a variety of digital devices, it provides a versatile and scalable solution for analyzing and tracking data across different platforms, ensuring efficient and thorough investigations.
        </p>
      </div>

      <div>
        <Link to="/add-case">
          <button className="btn add">Add Case</button>
        </Link>
        <button className="btn show" onClick={fetchCases}>
          Show All Cases
        </button>
      </div>

      <div className="icon-container">
        <div className="icon">
          <FaMobileAlt size={80} />
          <p>Android</p>
        </div>
        <div className="icon">
          <FaLaptop size={80} />
          <p>Operating System</p>
        </div>
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
