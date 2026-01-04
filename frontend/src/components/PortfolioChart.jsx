import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts';

const PortfolioChart = ({ data }) => {
    if (!data) return null;

    const chartData = [
        { name: 'Portfolio', xirr: (data.portfolio.summary.xirr || 0) * 100, color: '#646cff' },
        { name: 'Nifty 50', xirr: (data.benchmark.comparison.price.xirr || 0) * 100, color: '#94a3b8' },
        { name: 'Nifty 50 TRI', xirr: (data.benchmark.comparison.tri.xirr || 0) * 100, color: '#10b981' }
    ];

    return (
        <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl">
            <h3 className="text-lg font-semibold text-slate-100 mb-6">XIRR Comparison (%)</h3>
            <div className="h-80 w-full">
                <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={chartData}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                        <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fill: '#94a3b8' }} />
                        <YAxis axisLine={false} tickLine={false} tick={{ fill: '#94a3b8' }} />
                        <Tooltip
                            cursor={{ fill: 'rgba(30, 41, 59, 0.4)' }}
                            contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #1e293b', borderRadius: '12px', color: '#f8fafc' }}
                        />
                        <Bar dataKey="xirr" radius={[8, 8, 0, 0]}>
                            {chartData.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={entry.color} />
                            ))}
                        </Bar>
                    </BarChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
};

export default PortfolioChart;
