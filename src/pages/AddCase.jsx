import React, { useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import '../index.css';

function AddCase() {
  const [caseName, setCaseName] = useState('');



  const handleAddCase = async () => {
    if (!caseName.trim()) {
      alert('Please enter a case name');
      return;
    }

    try {
      const response = await axios.post('http://10.100.237.49:5000/api/cases', {
        name: caseName,
      });
      alert(`Case  added successfully!`);
      setCaseName('');
    } catch (error) {
      console.error('Error adding case:', error);
      alert('Failed to add case.');
    }
  };


  return (
    <div className="container">
      <h1 className="title">Add New Case</h1>
      <div className="case-form">
        <input
          type="text"
          placeholder="Enter case name"
          value={caseName}
          onChange={(e) => setCaseName(e.target.value)}
        />
        <button className="btn add" onClick={handleAddCase}>Add Case</button>
        <Link to="/">
          <button className="btn back">Back to Home</button>
        </Link>
      </div>
    </div>
  );
}

export default AddCase;
