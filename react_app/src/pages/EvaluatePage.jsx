import React from 'react';
import { useNavigate, useParams } from 'react-router-dom';

const EvaluatePage = () => {
  const { caseId } = useParams();
  const navigate = useNavigate();

  return (
    <div style={{ backgroundColor: '#1e1e2f', minHeight: '100vh', padding: '2rem' }}>
      <h1 style={{ color: '#fff', fontSize: '2.5rem', fontWeight: 'bold' }}>
        📊 GET INSIGHTS
      </h1>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', marginTop: '3rem' }}>
        <button
          className="btn"
          style={{ fontSize: '1.5rem', padding: '1rem', backgroundColor: '#520f0a', color: '#fff', borderRadius: '12px' }}
          onClick={() => navigate(`/cases/${caseId}/evaluate/calllogs`)}  
        >
          📞 Call Logs
        </button>

        <button
          className="btn"
          style={{ fontSize: '1.5rem', padding: '1rem', backgroundColor: '#1e0752', color: '#fff', borderRadius: '12px' }}
          onClick={() => navigate(`/cases/${caseId}/evaluate/sms`)}
        >
          💬 SMS
        </button>


      </div>
    </div>
  );
};

export default EvaluatePage;
