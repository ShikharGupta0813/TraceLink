import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import '../index.css';
import axios from 'axios';

function DeviceList() {
    const [devices, setDevices] = useState([]);
    const navigate = useNavigate();
    const { caseId } = useParams(); // ✅ get caseId from URL

    useEffect(() => {
        const fetchDevices = async () => {
          try {
            const response = await axios.get(`http://10.100.237.49:5000/api/cases/${caseId}/devices`);
            setDevices(response.data.devices);
          } catch (error) {
            console.error('Error fetching devices:', error);
            alert('Failed to fetch devices.');
          }
        };
      
        fetchDevices();
      }, [caseId]);
      




    return (
        <div className="device-list-container">
            <h1 className="title">All Devices Of Case {caseId}</h1>

            <button className="btn add-device" onClick={() => navigate(-1)}>
                ➕ Add Device
            </button>

            <div className="device-grid">
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
        </div>
    );
}

export default DeviceList;



