const DataTable = ({ data }) => {
    // If data is an object with call_log array, use that
    const actualData = Array.isArray(data) ? data : data?.call_log || [];
  
    if (actualData.length === 0) {
      return <p style={{ color: '#fff' }}>No data available.</p>;
    }
  
    const headers = Object.keys(actualData[0]);
  
    return (
      <table style={{
        marginTop: '2rem',
        width: '100%',
        color: '#fff',
        backgroundColor: '#4a0072',
        borderCollapse: 'collapse'
      }}>
        <thead>
          <tr>
            {headers.map((key) => (
              <th key={key} style={{
                border: '1px solid #ddd',
                padding: '10px',
                fontWeight: 'bold'
              }}>
                {key.toUpperCase()}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {actualData.map((row, idx) => (
            <tr key={idx}>
              {headers.map((key) => (
                <td key={key} style={{
                  border: '1px solid #ccc',
                  padding: '10px'
                }}>
                  {row[key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    );
  };
  
  export default DataTable;
  