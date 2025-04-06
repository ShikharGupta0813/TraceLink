import React from 'react';

function PageContainer({ title, data }) {
  const items = Array.isArray(data) ? data : [data];
  const headers = items.length > 0 ? Object.keys(items[0]) : [];

  return (
    <div style={{ padding: '2rem', backgroundColor: '#6a0dad', minHeight: '100vh', color: '#fff' }}>
      <h1 style={{ marginBottom: '1.5rem', fontSize: '2rem' }}>{title}</h1>
      
      {items.length === 0 || headers.length === 0 ? (
        <p>No data available.</p>
      ) : (
        <table style={{ width: '100%', backgroundColor: '#4a0072', borderCollapse: 'collapse' }}>
          <thead>
            <tr>
              {headers.map((header) => (
                <th key={header} style={{ padding: '12px', border: '1px solid #ccc', textAlign: 'left' }}>
                  {header.toUpperCase()}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {items.map((row, idx) => (
              <tr key={idx}>
                {headers.map((key) => (
                  <td key={key} style={{ padding: '10px', border: '1px solid #ccc' }}>
                    {row[key]}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default PageContainer;
