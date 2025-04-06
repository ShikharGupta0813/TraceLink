import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home.jsx';
import AddCase from './pages/AddCase';
import AddDevice from './pages/AddDevice.jsx';
import DeviceList from './pages/DeviceList.jsx';
import DeviceDetail from './pages/DeviceDetail.jsx';
import CallLogsPage from './pages/CallLogsPage.jsx';
import SmsLogsPage from './pages/SmsLogsPage.jsx';
import AppsPage from './pages/AppsPage.jsx';
import OSDetailsPage from './pages/OS DetailsPage.jsx';
import EvaluatePage from './pages/EvaluatePage';
import CallLogInsightsPage from './pages/CallLogInsightsPage';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/add-case" element={<AddCase />} />
      <Route path="/cases/:caseId/add-device" element={<AddDevice />} />
      <Route path="/cases/:caseId/devices" element={<DeviceList />} />
      <Route path="/cases/:caseId/devices/:deviceId" element={<DeviceDetail />} />
      <Route path="/device/:id/call-logs" element={<CallLogsPage />} />
      <Route path="/device/:id/sms-logs" element={<SmsLogsPage />} />
      <Route path="/device/:id/installed-apps" element={<AppsPage />} />
      <Route path="/device/:id/os-details" element={<OSDetailsPage />} />
      <Route path="/cases/:caseId/evaluate" element={<EvaluatePage />} />
      <Route path="/cases/:caseId/evaluate/calllogs" element={<CallLogInsightsPage />} />
    </Routes>
  );
}

export default App;
