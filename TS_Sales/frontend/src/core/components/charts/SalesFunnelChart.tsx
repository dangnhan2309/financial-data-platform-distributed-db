'use client';

import { useState } from 'react';
import { funnelData } from '@core/services/chart-data';

export default function SalesFunnelChart() {
    const [selectedStage, setSelectedStage] = useState<string | null>(null);
    const maxValue = funnelData[0].value;

    return (
        <div className="bg-white rounded-lg border-l-4 border-primary-700 p-6 shadow-sm">
            <div className="flex items-center justify-between mb-2">
                <h3 className="text-lg font-bold text-primary-700">📊 Phễu Chuyển đổi Bán hàng</h3>
                <button className="text-xs px-3 py-1 bg-primary-100 text-primary-700 rounded hover:bg-primary-200 transition">📥 Xuất</button>
            </div>
            <p className="text-sm text-gray-600 mb-5">Tỷ lệ rơi rụng từ Báo giá → Đơn hàng (kích để xem chi tiết)</p>

            {/* Funnel Chart */}
            <div className="space-y-2 mb-6">
                {funnelData.map((item, idx) => {
                    const percentage = Math.round((item.value / maxValue) * 100);
                    const width = percentage;

                    return (
                        <div
                            key={idx}
                            className="cursor-pointer"
                            onClick={() => setSelectedStage(item.stage)}
                        >
                            <div className="flex justify-between text-sm mb-1">
                                <span className="font-semibold text-gray-700">{item.stage}</span>
                                <span className="font-bold" style={{ color: item.color }}>{item.value}</span>
                            </div>
                            <div
                                className="h-8 rounded flex items-center justify-center text-white text-sm font-bold hover:opacity-80 transition-all"
                                style={{ width: `${width}%`, backgroundColor: item.color }}
                            >
                                {percentage}%
                            </div>
                        </div>
                    );
                })}
            </div>

            {/* Metrics Grid */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 border-t pt-4">
                {funnelData.map((item, idx) => {
                    const percentage = idx === 0 ? 100 : Math.round((item.value / funnelData[0].value) * 100);
                    const dropoffRate = idx === 0 ? 0 : 100 - percentage;

                    return (
                        <div
                            key={idx}
                            className={`p-3 rounded-lg border-2 transition-all cursor-pointer ${selectedStage === item.stage
                                    ? 'border-primary-700 bg-primary-50'
                                    : 'border-gray-200 bg-gray-50 hover:border-primary-300'
                                }`}
                            onClick={() => setSelectedStage(item.stage)}
                        >
                            <p className="text-xs font-bold text-gray-600 uppercase mb-1">{item.stage}</p>
                            <p className="text-2xl font-bold" style={{ color: item.color }}>{item.value}</p>
                            <p className="text-xs mt-2 text-gray-600">{percentage}% từ báo giá</p>
                            {dropoffRate > 0 && (
                                <p className="text-xs text-red-600 font-semibold mt-1">↓ -{dropoffRate}%</p>
                            )}
                        </div>
                    );
                })}
            </div>

            {/* Details Panel */}
            {selectedStage && (
                <div className="mt-4 p-3 bg-accent-light border border-primary-200 rounded-lg text-sm">
                    <p className="text-gray-700"><strong>{selectedStage}:</strong> Đang hiển thị dữ liệu mẫu</p>
                    <p className="text-xs text-gray-600 mt-1">Khi kết nối API, sẽ tải danh sách chi tiết từ Backend</p>
                </div>
            )}
        </div>
    );
}
