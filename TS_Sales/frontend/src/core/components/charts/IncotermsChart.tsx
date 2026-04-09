'use client';

import { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { incotermsData } from '@core/services/chart-data';

export default function IncotermsChart() {
    const [selectedIncoterm, setSelectedIncoterm] = useState<string | null>(null);
    const colors = ['#546B41', '#99AD7A', '#DCCCAC'];

    return (
        <div className="bg-white rounded-lg border-l-4 border-secondary-500 p-5 shadow-sm">
            <div className="flex items-center justify-between mb-1">
                <h3 className="text-lg font-bold text-secondary-700">📦 Incoterms</h3>
                <button className="text-xs px-3 py-1 bg-secondary-100 text-secondary-700 rounded hover:bg-secondary-200 transition">📥 Xuất</button>
            </div>
            <p className="text-sm text-gray-600 mb-4">Chiến lược Logistics theo Điều khoản (kích để xem)</p>

            <ResponsiveContainer width="100%" height={160}>
                <BarChart data={incotermsData} margin={{ top: 10, right: 15, left: 0, bottom: 30 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" vertical={false} />
                    <XAxis dataKey="incoterm" style={{ fontSize: '12px' }} />
                    <YAxis style={{ fontSize: '12px' }} />
                    <Tooltip
                        formatter={(value) => `${value} HĐ`}
                        contentStyle={{ backgroundColor: '#f9fafb', border: '1px solid #d1d5db', fontSize: '12px' }}
                    />
                    <Bar
                        dataKey="count"
                        radius={[8, 8, 0, 0]}
                        onClick={(e: any) => setSelectedIncoterm(e.payload.incoterm)}
                    >
                        {incotermsData.map((item, index) => (
                            <Cell
                                key={`cell-${index}`}
                                fill={colors[index]}
                                opacity={!selectedIncoterm || selectedIncoterm === item.incoterm ? 1 : 0.4}
                            />
                        ))}
                    </Bar>
                </BarChart>
            </ResponsiveContainer>

            {/* Details Grid */}
            <div className="grid grid-cols-3 gap-2 mt-4 border-t pt-4">
                {incotermsData.map((item, idx) => (
                    <div
                        key={idx}
                        className={`p-3 rounded-lg cursor-pointer transition-all border-2 ${selectedIncoterm === item.incoterm
                                ? 'border-secondary-500 bg-secondary-50'
                                : 'border-gray-200 bg-gray-50 hover:border-secondary-300'
                            }`}
                        onClick={() => setSelectedIncoterm(item.incoterm)}
                    >
                        <div className="flex items-center gap-2 mb-2">
                            <div className="w-3 h-3 rounded" style={{ backgroundColor: colors[idx] }}></div>
                            <h4 className="font-bold text-gray-700 text-sm">{item.incoterm}</h4>
                        </div>
                        <p className="text-2xl font-bold text-gray-900">{item.count}</p>
                        <p className="text-xs text-gray-600 mt-1 font-semibold">{item.percentage}% HĐ</p>

                        {/* Info Box */}
                        <div className="mt-2 text-xs text-gray-700 p-2 bg-white rounded border-l-2" style={{ borderColor: colors[idx] }}>
                            {item.incoterm === 'FOB' && '🚢 Chi phí từ thế nhập phát'}
                            {item.incoterm === 'CIF' && '✈️ Toàn bộ chi phí vận chuyển'}
                            {item.incoterm === 'EXW' && '📍 Khách tự chịu từ kho'}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
