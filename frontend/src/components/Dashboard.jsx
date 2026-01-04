import React, { useState, useEffect } from 'react';
import { portfolioService } from '../services/api';
import MetricCard from './MetricCard';
import HoldingsTable from './HoldingsTable';
import PortfolioChart from './PortfolioChart';
import SipDashboard from './SipDashboard';
import { Wallet, TrendingUp, PieChart, Activity, Loader2, LayoutDashboard, LineChart } from 'lucide-react';

const Dashboard = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [activeTab, setActiveTab] = useState('overview'); // 'overview' or 'sip'

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [summaryRes, benchmarkRes] = await Promise.all([
                    portfolioService.getSummary(),
                    portfolioService.getBenchmarkCompare()
                ]);
                setData({
                    portfolio: summaryRes.data,
                    benchmark: benchmarkRes.data
                });
            } catch (err) {
                console.error("Failed to fetch data:", err);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    if (loading) {
        return (
            <div className="flex flex-col items-center justify-center min-h-screen bg-black text-slate-400">
                <Loader2 className="w-10 h-10 animate-spin text-brand mb-4" />
                <p className="animate-pulse">Loading your financial data...</p>
            </div>
        );
    }

    if (!data) return <div className="text-white p-10">Error loading data. Is the backend running?</div>;

    const { summary } = data.portfolio;

    return (
        <div className="min-h-screen bg-black p-6 lg:p-10">
            <div className="max-w-7xl mx-auto">
                <header className="mb-10 flex flex-col md:flex-row md:items-end justify-between gap-6">
                    <div>
                        <h1 className="text-3xl font-bold text-white mb-2">Portfolio Insights</h1>
                        <p className="text-slate-400">Comprehensive view of your mutual fund investments</p>
                    </div>

                    {/* Tab Navigation */}
                    <div className="flex bg-slate-900 p-1 rounded-xl border border-slate-800 self-start md:self-auto">
                        <button
                            onClick={() => setActiveTab('overview')}
                            className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${activeTab === 'overview' ? 'bg-brand text-white shadow-lg' : 'text-slate-400 hover:text-slate-200'}`}
                        >
                            <LayoutDashboard className="w-4 h-4" />
                            Overview
                        </button>
                        <button
                            onClick={() => setActiveTab('sip')}
                            className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${activeTab === 'sip' ? 'bg-brand text-white shadow-lg' : 'text-slate-400 hover:text-slate-200'}`}
                        >
                            <LineChart className="w-4 h-4" />
                            SIP Performance
                        </button>
                    </div>
                </header>

                {activeTab === 'overview' ? (
                    <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
                        {/* Stats Grid */}
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
                            <MetricCard
                                title="Total Market Value"
                                value={`₹${summary.current_value.toLocaleString()}`}
                                icon={Wallet}
                            />
                            <MetricCard
                                title="Total Profit"
                                value={`₹${summary.total_profit_loss.toLocaleString()}`}
                                trend={((summary.total_profit_loss / summary.net_capital_invested) * 100).toFixed(2)}
                                subValue="Overall Returns"
                                icon={TrendingUp}
                            />
                            <MetricCard
                                title="Portfolio XIRR"
                                value={`${(summary.xirr * 100).toFixed(2)}%`}
                                icon={Activity}
                            />
                            <MetricCard
                                title="Net Invested"
                                value={`₹${summary.net_capital_invested.toLocaleString()}`}
                                icon={PieChart}
                            />
                        </div>

                        {/* Charts & Table */}
                        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                            <div className="lg:col-span-2">
                                <HoldingsTable holdings={data.portfolio.holdings} />
                            </div>
                            <div className="lg:col-span-1">
                                <PortfolioChart data={data} />
                            </div>
                        </div>
                    </div>
                ) : (
                    <SipDashboard />
                )}
            </div>
        </div>
    );
};

export default Dashboard;
