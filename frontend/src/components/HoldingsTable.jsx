import React from 'react';

const HoldingsTable = ({ holdings }) => {
    return (
        <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
            <div className="px-6 py-4 border-b border-slate-800 bg-slate-900/50">
                <h3 className="text-lg font-semibold text-slate-100">Holdings Breakdown</h3>
            </div>
            <div className="overflow-x-auto">
                <table className="w-full text-left">
                    <thead>
                        <tr className="bg-slate-800/20 text-slate-400 text-xs uppercase tracking-wider">
                            <th className="px-6 py-4 font-semibold">Scheme Name</th>
                            <th className="px-6 py-4 font-semibold text-right">Units</th>
                            <th className="px-6 py-4 font-semibold text-right">Net Capital</th>
                            <th className="px-6 py-4 font-semibold text-right">Current Value</th>
                            <th className="px-6 py-4 font-semibold text-right">Returns</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800/50">
                        {holdings.map((h, i) => (
                            <tr key={i} className="hover:bg-slate-800/30 transition-colors">
                                <td className="px-6 py-4">
                                    <span className="text-sm font-medium text-slate-200 block truncate max-w-xs" title={h.scheme}>
                                        {h.scheme}
                                    </span>
                                </td>
                                <td className="px-6 py-4 text-right text-sm text-slate-300">
                                    {h.units.toLocaleString(undefined, { minimumFractionDigits: 3 })}
                                </td>
                                <td className="px-6 py-4 text-right text-sm text-slate-300">
                                    ₹{h.net_capital.toLocaleString()}
                                </td>
                                <td className="px-6 py-4 text-right text-sm font-semibold text-slate-100">
                                    ₹{h.value.toLocaleString()}
                                </td>
                                <td className={`px-6 py-4 text-right text-sm font-bold ${h.returns_pct >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
                                    {h.returns_pct.toFixed(2)}%
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default HoldingsTable;
