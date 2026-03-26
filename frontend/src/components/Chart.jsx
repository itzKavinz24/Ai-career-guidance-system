import React from 'react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from 'recharts';

const Chart = ({ data, title = 'Skill Match Breakdown' }) => {
  const safeData = Array.isArray(data)
    ? data.map((item) => ({
        name: item.name,
        value: typeof item.value === 'number' ? item.value : Number(item.percentage ?? 0),
      }))
    : [];

  return (
    <section className="card-surface w-full p-4 sm:p-5">
      <div className="mb-3 flex items-center justify-between gap-3">
        <div>
          <h3 className="headline-display text-sm font-semibold text-[#f2fff9] sm:text-base">{title}</h3>
          <p className="text-[11px] text-[#8ec3b7] sm:text-xs">How your skills align with target roles</p>
        </div>
        <span className="pill-muted">Higher bars = stronger fit</span>
      </div>

      {safeData.length === 0 ? (
        <p className="text-xs text-[#8ec3b7] sm:text-sm">No data available yet. Complete the assessment to see your breakdown.</p>
      ) : (
        <div className="h-60 w-full sm:h-72">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={safeData} margin={{ top: 8, right: 8, left: -20, bottom: 4 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#234046" vertical={false} />
              <XAxis dataKey="name" tick={{ fontSize: 11, fill: '#9ccfc2' }} tickLine={false} axisLine={{ stroke: '#234046' }} />
              <YAxis domain={[0, 100]} tick={{ fontSize: 11, fill: '#9ccfc2' }} tickLine={false} axisLine={{ stroke: '#234046' }} tickFormatter={(v) => `${v}%`} />
              <Tooltip
                cursor={{ fill: 'rgba(7,31,35,0.5)' }}
                contentStyle={{
                  backgroundColor: '#071c20',
                  borderRadius: 12,
                  border: '1px solid rgba(66,121,114,0.9)',
                  padding: '8px 10px',
                }}
                labelStyle={{ color: '#e7fff8', fontSize: 11 }}
                itemStyle={{ color: '#e7fff8', fontSize: 11 }}
                formatter={(value) => [`${value}%`, 'Match']}
              />
              <Bar dataKey="value" radius={[6, 6, 0, 0]} fill="url(#skillGradient)" />
              <defs>
                <linearGradient id="skillGradient" x1="0" y1="0" x2="1" y2="1">
                  <stop offset="0%" stopColor="#24d0a8" />
                  <stop offset="45%" stopColor="#65eecf" />
                  <stop offset="100%" stopColor="#f7a86f" />
                </linearGradient>
              </defs>
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </section>
  );
};

export default Chart;
