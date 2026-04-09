'use client';

import { useState } from 'react';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts';
import { quotationStatusData } from '@core/services/chart-data';

export default function QuotationStatusChart() {
    const [selectedStatus, setSelectedStatus] = useState<string | null>(null);
    const total = quotationStatusData.reduce((sum, item) => sum + item.value, 0);

    return (
        <div className="bg-white rounded-lg border-l-4 border-secondary-500 p-5 shadow-sm">
            <div className="flex items-center justify-between mb-1">
                <h3 className="text-lg font-bold text-secondary-700">📊 Trạng thái Báo giá</h3>
                <button className="text-xs px-3 py-1 bg-secondary-100 text-secondary-700 rounded hover:bg-secondary-200 transition">📥 Xuất</button>
            </div>
            <p className="text-sm text-gray-600 mb-4">Phân bổ theo giai đoạn (kích để xem chi tiết)</p>

            <ResponsiveContainer width="100%" height={200}>
                <PieChart>
                    <Pie
                        data={quotationStatusData}
                        cx="50%"
                        cy="50%"
                        innerRadius={60}
                        outerRadius={95}
                        paddingAngle={1}
                        dataKey="value"
                        onClick={(entry: any) => setSelectedStatus(entry.name)}
                    >
                        {quotationStatusData.map((item, index) => (
                            <Cell
                                key={`cell-${index}`}
                                fill={item.color}
                                opacity={!selectedStatus || selectedStatus === item.name ? 1 : 0.5}
                            />
                        ))}
                    </Pie>
                    <Tooltip
                        formatter={(value) => `${value} báo giá`}
                        contentStyle={{ backgroundColor: '#f9fafb', border: '1px solid #d1d5db', fontSize: '12px' }}
                    />
                </PieChart>
            </ResponsiveContainer>

            {/* Legend/Filter Buttons */}
            <div className="grid grid-cols-2 gap-2 mt-4 border-t pt-4">
                {quotationStatusData.map((item, idx) => {
                    const percentage = Math.round((item.value / total) * 100);
                    return (
                        <div
                            key={idx}
                            className={`p-3 rounded-lg cursor-pointer transition-all border-2 ${selectedStatus === item.name
                                    ? 'border-secondary-500 bg-secondary-50'
                                    : 'border-gray-200 bg-gray-50 hover:border-secondary-300'
                                }`}
                            onClick={() => setSelectedStatus(item.name)}
                        >
                            <div className="flex items-center gap-2 mb-2">
                                <div className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }}></div>
                                <p className="text-sm font-semibold text-gray-700">{item.name}</p>
                            </div>
                            <p className="text-lg font-bold text-gray-900">{item.value}</p>
                            <p className="text-xs text-gray-600">{percentage}% tổng</p>
                        </div>
                    );
                })}
            </div>

            {/* Details */}
            {selectedStatus && (
                <div className="mt-3 p-3 bg-accent-light border border-secondary-200 rounded text-sm">
                    <p className="text-gray-700 font-semibold mb-1">📋 {selectedStatus}</p>
                    <p className="text-xs text-gray-600">Dữ liệu mẫu - API sẽ cung cấp chi tiết</p>
                </div>
            )}
        </div>
    );
}
