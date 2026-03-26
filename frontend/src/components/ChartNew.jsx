import React from 'react';
import './Chart.css';

const Chart = ({ data = [] }) => {
  if (!data || data.length === 0) {
    return (
      <div className="chart">
        <p className="no-data">No data available for visualization</p>
      </div>
    );
  }

  // Normalize data
  const normalizedData = data.map((item) => {
    let name, percentage;

    if (typeof item === 'string') {
      name = item;
      percentage = Math.random() * 100;
    } else if (item.name && item.percentage !== undefined) {
      name = item.name;
      percentage = Math.min(item.percentage, 100);
    } else {
      return null;
    }

    return { name, percentage: Math.round(percentage) };
  }).filter(Boolean);

  return (
    <div className="chart">
      <h3>Career Compatibility Chart</h3>
      <div className="chart-container">
        {normalizedData.map((item, index) => (
          <div key={index} className="chart-item">
            <div className="chart-label">{item.name}</div>
            <div className="chart-bar">
              <div
                className="chart-progress"
                style={{ width: `${item.percentage}%` }}
              />
            </div>
            <div className="chart-value">{item.percentage}%</div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Chart;
