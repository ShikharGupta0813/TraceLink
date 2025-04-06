import React, { useState } from 'react';
import { useLocation, useParams } from 'react-router-dom';
import '../index.css';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function AddDevice() {
    const { caseId } = useParams();
    const location = useLocation();
    const caseName = location.state?.caseName || 'Unknown Case';

    const [deviceType, setDeviceType] = useState(null);
    const [deviceName, setDeviceName] = useState('');
    const [submitted, setSubmitted] = useState(false);
    const [devices, setDevices] = useState([]);

    const navigate = useNavigate();

    const handleTypeClick = (type) => {
        setDeviceType(type);
        setSubmitted(false);
        setDeviceName('');
    };

    const handleSubmit = async () => {
        if (!deviceName || !deviceType) {
            alert('Please fill in all fields');
            return;
        }

        try {
            const payload = {
                caseId,
                deviceType,
                deviceName,
            };

            await axios.post('http://10.100.237.49:5000/api/devices', payload);
            alert('Device added successfully!');
            setDeviceName('');
            setSubmitted(true);
            // Optionally, refetch devices:
            fetchDevices();
        } catch (err) {
            console.error(err);
            alert('Failed to add device');
        }
    };

    const fetchDevices = async () => {
        try {
            const response = await axios.get(`http://10.100.237.49:5000/api/cases/${caseId}/devices`);
            console.log("Fetched devices:", response.data);
            setDevices(response.data.devices); // ✅ Corrected
        } catch (err) {
            console.error('Failed to fetch devices:', err);
            alert('Could not fetch devices for this case.');
        }
    };


    return (
        <div className="container">
            <h1 className="title">Add Device</h1>
            <h2>Case: {caseName}</h2>

            <div className="case-form">
                <button className="btn android" onClick={() => handleTypeClick('Android')}>
                    Android
                </button>
                <button className="btn os" onClick={() => handleTypeClick('Operating System')}>
                    Operating System
                </button>
            </div>

            {deviceType && (
                <div className="case-form">
                    <h3>Adding: {deviceType}</h3>
                    <input
                        type="text"
                        placeholder="Enter device name"
                        value={deviceName}
                        onChange={(e) => setDeviceName(e.target.value)}
                    />
                    <button className="btn submit" onClick={handleSubmit}>
                        Submit Device
                    </button>
                </div>
            )}

            {submitted && (
                <p style={{ marginTop: '20px', color: 'lightgreen' }}>
                    ✅ Device added successfully!
                </p>
            )}

<div style={{ display: 'flex', gap: '20px', marginTop: '30px' }}>
  <button
    className="btn show"
    style={{
      flex: 1,
      padding: '20px 40px',
      fontSize: '1.5rem',
      fontWeight: 'bold',
      backgroundColor: '#4CAF50',
      color: 'white',
      borderRadius: '12px',
      cursor: 'pointer',
    }}
    onClick={fetchDevices}
  >
    Show All Devices of This Case
  </button>

  <button
    className="btn evaluate"
    style={{
      flex: 1,
      padding: '20px 40px',
      fontSize: '1.5rem',
      fontWeight: 'bold',
      backgroundColor: '#ff9800',
      color: 'white',
      borderRadius: '12px',
      cursor: 'pointer',
    }}
    onClick={() => navigate(`/cases/${caseId}/evaluate`)}
  >
    Evaluate
  </button>
</div>

            {/* Display Fetched Devices */}
            {devices.length > 0 && (
                <div className="device-grid" style={{ marginTop: '20px' }}>
                    {devices.map((device) => (
                        <button
                            key={device.id}
                            className="device-card"
                            onClick={() =>
                                navigate(`/cases/${caseId}/devices/${device.id}`, {
                                    state: { device },
                                })
                            }
                        >
                            <p><strong>ID:</strong> {device.id}</p>
                            <p><strong>Name:</strong> {device.name}</p>
                            <p><strong>Type:</strong> {device.type}</p>
                            <p><strong>Case ID:</strong> {device.caseId}</p>
                        </button>
                    ))}
                </div>
            )}
        </div>
    );
}

export default AddDevice;
