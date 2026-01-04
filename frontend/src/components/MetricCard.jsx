import React from 'react';
import { motion } from 'framer-motion';

const MetricCard = ({ title, value, subValue, trend, icon: Icon }) => {
    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl hover:border-slate-700 transition-colors"
        >
            <div className="flex items-center justify-between mb-4">
                <span className="text-slate-400 text-sm font-medium">{title}</span>
                <div className="p-2 bg-slate-800 rounded-lg">
                    <Icon className="w-5 h-5 text-brand" />
                </div>
            </div>
            <div className="flex flex-col">
                <span className="text-2xl font-bold text-slate-50">{value}</span>
                {subValue && (
                    <div className="flex items-center mt-1">
                        <span className={`text-xs font-semibold ${trend >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
                            {trend >= 0 ? '+' : ''}{trend}%
                        </span>
                        <span className="text-slate-500 text-xs ml-2">{subValue}</span>
                    </div>
                )}
            </div>
        </motion.div>
    );
};

export default MetricCard;
