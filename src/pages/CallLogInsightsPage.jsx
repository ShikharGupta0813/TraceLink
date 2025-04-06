import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  PieChart,
  Pie,
  Cell,
  Legend,
} from "recharts";

const COLORS = ["#0088FE", "#00C49F", "#FFBB28"];

const CallLogInsightsPage = () => {

    const sampleInsights = {
        totalCalls: 120,
        missedCalls: 25,
        incomingCalls: 55,
        outgoingCalls: 40,
        mostFrequentCaller: {
          number: "+1234567890",
          count: 18,
        },
        callDurationByType: [
          { type: "Incoming", duration: 3000 },
          { type: "Outgoing", duration: 4500 },
          { type: "Missed", duration: 0 },
        ],
        callCountByHour: [
          { hour: "00:00", count: 2 },
          { hour: "01:00", count: 1 },
          { hour: "10:00", count: 12 },
          { hour: "13:00", count: 20 },
          { hour: "17:00", count: 10 },
          { hour: "20:00", count: 25 },
        ],
      };
      
  const data = sampleInsights;

  return (
    <div style={{ padding: "2rem", backgroundColor: "#6a0dad", minHeight: "100vh", color: "#fff" }}>
      <h1>📊 Call Log Insights</h1>

      <div style={{ marginBottom: "1rem" }}>
        <p><strong>Total Calls:</strong> {data.totalCalls}</p>
        <p><strong>Missed Calls:</strong> {data.missedCalls}</p>
        <p><strong>Incoming Calls:</strong> {data.incomingCalls}</p>
        <p><strong>Outgoing Calls:</strong> {data.outgoingCalls}</p>
        <p><strong>Most Frequent Caller:</strong> {data.mostFrequentCaller.number} ({data.mostFrequentCaller.count} times)</p>
      </div>

      <h2>📈 Call Duration by Type</h2>
      <PieChart width={400} height={300}>
        <Pie
          data={data.callDurationByType}
          dataKey="duration"
          nameKey="type"
          cx="50%"
          cy="50%"
          outerRadius={100}
          fill="#8884d8"
          label
        >
          {data.callDurationByType.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Legend />
        <Tooltip />
      </PieChart>

      <h2>🕓 Calls By Hour</h2>
      <BarChart width={600} height={300} data={data.callCountByHour}>
        <XAxis dataKey="hour" stroke="#ffffff" />
        <YAxis stroke="#ffffff" />
        <Tooltip />
        <Legend />
        <Bar dataKey="count" fill="#00C49F" />
      </BarChart>
    </div>
  );
};

export default CallLogInsightsPage;
