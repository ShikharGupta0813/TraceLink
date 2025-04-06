import React from 'react';
import { useLocation, useNavigate, useParams } from 'react-router-dom';
import '../index.css';


function DeviceDetail() {
  const location = useLocation();
  const navigate = useNavigate();
  const { deviceId } = useParams(); 

  const device = location.state?.device;

  if (!device) {
    return (
      <h2 style={{ textAlign: 'center', marginTop: '2rem', color: '#fff', fontWeight: 'bold' }}>
        ⚠️ No device data found.
      </h2>
    );
  }

  const isAndroid = device.type === 'Android';

  return (
    <div
      className="container"
      style={{ backgroundColor: '#6a0dad', minHeight: '100vh', padding: '2rem' }}
    >
      <h1 style={{ fontSize: '2.5rem', fontWeight: 'bold', color: '#ffffff' }}>
        Device Details
      </h1>

      <div
        style={{
          marginTop: '1.5rem',
          color: '#f0e6ff',
          fontSize: '1.5rem',
          fontWeight: 'bold',
        }}
      >
        <p>📱 Device Name: {device.name}</p>
        <p>🔧 Type: {device.type}</p>
        <p>🗂️ Case ID: {device.caseId}</p>
        <p>🆔 Device ID: {deviceId}</p>

      </div>

      {isAndroid && (
        <div
          style={{
            marginTop: '2.5rem',
            fontSize: '1.4rem',
            fontWeight: 'bold',
            color: '#fff',
          }}
        >
          <p>📲 Please download our mobile application.</p>
          <p>➡️ Inside the app, press the following buttons:</p>
          <p>• Get Call Log</p>
          <p>• Get SMS Log</p>
          <p>• Get Installed Apps</p>
        </div>
      )}

      <div className="case-form" style={{ marginTop: '3rem' }}>
        {isAndroid ? (
          <>
            <button className="btn" onClick={() => navigate(`/device/${device.id}/call-logs`)}>
              📞 Show Call Details
            </button>
            <button className="btn" onClick={() => navigate(`/device/${device.id}/sms-logs`)}>
              💬 Show SMS Details
            </button>
            <button className="btn" onClick={() => navigate(`/device/${device.id}/installed-apps`)}>
              📦 Show Application Details
            </button>
          </>
        ) : (
          <button className="btn" onClick={() => navigate(`/device/${device.id}/os-details`)}>
            🖥️ Get OS Details
          </button>
        )}
      </div>
    </div>
  );
}

export default DeviceDetail;
