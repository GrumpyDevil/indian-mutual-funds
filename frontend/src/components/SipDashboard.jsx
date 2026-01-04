import React, { useState, useEffect } from 'react';
import { portfolioService } from '../services/api';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { Activity, TrendingUp, Wallet, Loader2, Award } from 'lucide-react';
import MetricCard from './MetricCard';

const SipDashboard = () => {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchSipData = async () => {
            try {
                const res = await portfolioService.getSipPerformance();
                setData(res.data);
            } catch (err) {
                console.error("Failed to fetch SIP data:", err);
            } finally {
                setLoading(false);
            }
        };
        fetchSipData();
    }, []);

    if (loading) {
        return (
            <div className="flex flex-col items-center justify-center min-h-[400px] text-slate-400">
                <Loader2 className="w-10 h-10 animate-spin text-brand mb-4" />
                <p>Calculating investment trajectory...</p>
            </div>
        );
    }

    if (!data || data.length === 0) {
        return <div className="text-white p-10">No SIP data available.</div>;
    }

    const latest = data[data.length - 1];
    const totalProfit = latest.portfolio_value - latest.invested;
    const absReturn = (totalProfit / latest.invested) * 100;

    // Calculate benchmark performance
    const nifty50Profit = latest.nifty50_price - latest.invested;
    const nifty50Return = (nifty50Profit / latest.invested) * 100;

    const niftyTriProfit = latest.nifty50_tri - latest.invested;
    const niftyTriReturn = (niftyTriProfit / latest.invested) * 100;

    return (
        <div className="animate-in fade-in duration-500">
            {/* SIP Header Stats */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
                <MetricCard
                    title="Total Invested"
                    value={`₹${latest.invested.toLocaleString()}`}
                    icon={Wallet}
                />
                <MetricCard
                    title="Portfolio Value"
                    value={`₹${latest.portfolio_value.toLocaleString()}`}
                    trend={absReturn.toFixed(2)}
                    subValue="Absolute Return"
                    icon={Activity}
                />
                <MetricCard
                    title="Nifty 50 (Price)"
                    value={`₹${latest.nifty50_price.toLocaleString()}`}
                    trend={nifty50Return.toFixed(2)}
                    subValue="Benchmark Return"
                    icon={TrendingUp}
                />
                <MetricCard
                    title="Nifty 50 TRI"
                    value={`₹${latest.nifty50_tri.toLocaleString()}`}
                    trend={niftyTriReturn.toFixed(2)}
                    subValue="TRI Return"
                    icon={Award}
                />
            </div>

            {/* Growth Chart */}
            <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl mb-10">
                <h3 className="text-lg font-semibold text-slate-100 mb-6">Wealth Accumulation vs Benchmarks</h3>
                <div className="h-[500px] w-full">
                    <ResponsiveContainer width="100%" height="100%">
                        <AreaChart data={data}>
                            <defs>
                                <linearGradient id="colorPortfolio" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor="#646cff" stopOpacity={0.3} />
                                    <stop offset="95%" stopColor="#646cff" stopOpacity={0} />
                                </linearGradient>
                                <linearGradient id="colorInvested" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor="#94a3b8" stopOpacity={0.1} />
                                    <stop offset="95%" stopColor="#94a3b8" stopOpacity={0} />
                                </linearGradient>
                                <linearGradient id="colorNifty50" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.2} />
                                    <stop offset="95%" stopColor="#f59e0b" stopOpacity={0} />
                                </linearGradient>
                                <linearGradient id="colorNiftyTRI" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.2} />
                                    <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                                </linearGradient>
                            </defs>
                            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                            <XAxis
                                dataKey="date"
                                axisLine={false}
                                tickLine={false}
                                tick={{ fill: '#94a3b8', fontSize: 12 }}
                                minTickGap={50}
                            />
                            <YAxis
                                axisLine={false}
                                tickLine={false}
                                tick={{ fill: '#94a3b8', fontSize: 12 }}
                                tickFormatter={(val) => `₹${(val / 100000).toFixed(1)}L`}
                            />
                            <Tooltip
                                contentStyle={{
                                    backgroundColor: '#0f172a',
                                    border: '1px solid #1e293b',
                                    borderRadius: '12px',
                                    color: '#f8fafc'
                                }}
                                formatter={(value) => [`₹${value.toLocaleString()}`, '']}
                            />
                            <Legend
                                verticalAlign="top"
                                height={36}
                                wrapperStyle={{ paddingBottom: '20px' }}
                            />
                            <Area
                                type="monotone"
                                dataKey="portfolio_value"
                                name="Your Portfolio"
                                stroke="#646cff"
                                strokeWidth={3}
                                fillOpacity={1}
                                fill="url(#colorPortfolio)"
                            />
                            <Area
                                type="monotone"
                                dataKey="nifty50_tri"
                                name="Nifty 50 TRI"
                                stroke="#10b981"
                                strokeWidth={2}
                                fillOpacity={1}
                                fill="url(#colorNiftyTRI)"
                            />
                            <Area
                                type="monotone"
                                dataKey="nifty50_price"
                                name="Nifty 50 (Price)"
                                stroke="#f59e0b"
                                strokeWidth={2}
                                fillOpacity={1}
                                fill="url(#colorNifty50)"
                            />
                            <Area
                                type="monotone"
                                dataKey="invested"
                                name="Invested Capital"
                                stroke="#94a3b8"
                                strokeWidth={2}
                                strokeDasharray="5 5"
                                fillOpacity={1}
                                fill="url(#colorInvested)"
                            />
                        </AreaChart>
                    </ResponsiveContainer>
                </div>
            </div>

            {/* Performance Summary */}
            <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl">
                <h3 className="text-lg font-semibold text-slate-100 mb-4">Performance Summary</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="bg-slate-800/50 p-4 rounded-xl">
                        <p className="text-slate-400 text-sm mb-1">Portfolio Outperformance</p>
                        <p className={`text-2xl font-bold ${(absReturn - nifty50Return) >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
                            {(absReturn - nifty50Return) >= 0 ? '+' : ''}{(absReturn - nifty50Return).toFixed(2)}%
                        </p>
                        <p className="text-slate-500 text-xs mt-1">vs Nifty 50</p>
                    </div>
                    <div className="bg-slate-800/50 p-4 rounded-xl">
                        <p className="text-slate-400 text-sm mb-1">Portfolio Outperformance</p>
                        <p className={`text-2xl font-bold ${(absReturn - niftyTriReturn) >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
                            {(absReturn - niftyTriReturn) >= 0 ? '+' : ''}{(absReturn - niftyTriReturn).toFixed(2)}%
                        </p>
                        <p className="text-slate-500 text-xs mt-1">vs Nifty 50 TRI</p>
                    </div>
                    <div className="bg-slate-800/50 p-4 rounded-xl">
                        <p className="text-slate-400 text-sm mb-1">Total Capital Gain</p>
                        <p className={`text-2xl font-bold ${totalProfit >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
                            ₹{totalProfit.toLocaleString()}
                        </p>
                        <p className="text-slate-500 text-xs mt-1">{absReturn.toFixed(2)}% absolute return</p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default SipDashboard;
