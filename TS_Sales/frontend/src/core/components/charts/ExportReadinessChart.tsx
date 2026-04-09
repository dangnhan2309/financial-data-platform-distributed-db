'use client';

import { useState } from 'react';
import { exportReadinessData } from '@core/services/chart-data';

export default function ExportReadinessChart() {
    const [selectedDoc, setSelectedDoc] = useState<string | null>(null);
    const avgCompletion = Math.round(
        exportReadinessData.reduce((sum, item) => sum + item.completed, 0) / exportReadinessData.length
    );

    return (
        <div className="bg-white rounded-lg border-l-4 border-accent-500 p-5 shadow-sm">
            <div className="flex items-center justify-between mb-1">
                <h3 className="text-lg font-bold text-accent-600">✈️ Sẵn sàng Xuất khẩu</h3>
                <button className="text-xs px-3 py-1 bg-accent-100 text-accent-700 rounded hover:bg-accent-200 transition">📥 Xuất</button>
            </div>
            <p className="text-sm text-gray-600 mb-4">Mức độ hoàn tất chứng từ (kích để xem chi tiết)</p>

            {/* Score Cards */}
            <div className="grid grid-cols-3 gap-2 mb-4">
                {exportReadinessData.map((item, idx) => {
                    const isReady = item.completed >= 90;
                    return (
                        <div
                            key={idx}
                            className={`p-3 rounded-lg cursor-pointer transition-all border-2 ${selectedDoc === item.document
                                    ? 'border-accent-500 bg-accent-50'
                                    : 'border-gray-200 bg-gray-50 hover:border-accent-300'
                                }`}
                            onClick={() => setSelectedDoc(item.document)}
                        >
                            <p className="text-xs font-bold text-gray-700 mb-1">{item.document}</p>
                            <div className="flex items-end gap-1 mb-2">
                                <span className="text-2xl font-bold text-gray-900">{item.completed}</span>
                                <span className="text-xs text-gray-600">%</span>
                            </div>
                            {/* Mini bar */}
                            <div className="w-full bg-gray-200 rounded-full h-1.5">
                                <div
                                    className={`h-1.5 rounded-full transition-all ${isReady ? 'bg-green-500' : item.completed >= 70 ? 'bg-yellow-500' : 'bg-red-500'
                                        }`}
                                    style={{ width: `${item.completed}%` }}
                                ></div>
                            </div>
                            <p className="text-xs mt-1 font-semibold" style={{ color: isReady ? '#10b981' : item.completed >= 70 ? '#f59e0b' : '#ef4444' }}>
                                {isReady ? '✅ Sẵn sàng' : item.completed >= 70 ? '⏰ Sắp xong' : '❌ Cần làm'}
                            </p>
                        </div>
                    );
                })}
            </div>

            {/* Overall gauge */}
            <div className="bg-gradient-to-r from-accent-50 to-primary-50 p-4 rounded-lg border border-accent-200 text-center mb-3">
                <p className="text-xs text-gray-700 mb-1"><strong>📊 Trung bình tổng thể</strong></p>
                <div className="flex items-end justify-center gap-2">
                    <span className="text-4xl font-bold text-accent-600">{avgCompletion}</span>
                    <span className="text-lg text-gray-600 mb-1">%</span>
                </div>
                <div className="w-full max-w-xs mx-auto bg-gray-300 rounded-full h-2 mt-2">
                    <div
                        className="bg-accent-500 h-2 rounded-full transition-all"
                        style={{ width: `${avgCompletion}%` }}
                    ></div>
                </div>
                <p className="text-xs text-gray-600 mt-2">Mục tiêu: 90% | {avgCompletion >= 90 ? '✅ Đạt mục tiêu' : '⏳ Cần cập nhật'}</p>
            </div>

            {/* Details Panel */}
            {selectedDoc && (
                <div className="p-3 bg-accent-light border border-accent-300 rounded text-sm">
                    <p className="font-semibold text-gray-800 mb-1">📋 {selectedDoc}</p>
                    <p className="text-xs text-gray-600">Hiển thị dữ liệu mẫu - Chi tiết từ API Backend</p>
                </div>
            )}
        </div>
    );
}
