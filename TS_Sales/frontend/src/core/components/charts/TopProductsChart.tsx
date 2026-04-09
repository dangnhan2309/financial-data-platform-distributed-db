'use client';

import { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { topProductsData } from '@core/services/chart-data';

export default function TopProductsChart() {
    const [selectedProduct, setSelectedProduct] = useState<string | null>(null);
    const [filter, setFilter] = useState<'all' | 'VietFarm' | 'VinaCoco'>('all');

    const colorMap = { 'VietFarm': '#546B41', 'VinaCoco': '#99AD7A' };
    const filteredData = filter === 'all' ? topProductsData : topProductsData.filter(p => p.category === filter);

    return (
        <div className="bg-white rounded-lg border-l-4 border-primary-700 p-5 shadow-sm">
            <div className="flex items-center justify-between mb-1">
                <h3 className="text-lg font-bold text-primary-700">🏆 Top Sản phẩm</h3>
                <button className="text-xs px-3 py-1 bg-primary-100 text-primary-700 rounded hover:bg-primary-200 transition">📥 Xuất</button>
            </div>
            <p className="text-sm text-gray-600 mb-3">Được chào hàng nhiều nhất (kích để xem)</p>

            {/* Filters */}
            <div className="flex gap-2 mb-4 pb-3 border-b">
                {(['all', 'VietFarm', 'VinaCoco'] as const).map(cat => (
                    <button
                        key={cat}
                        onClick={() => { setFilter(cat); setSelectedProduct(null); }}
                        className={`text-xs font-semibold px-3 py-1 rounded transition-all ${filter === cat
                                ? 'bg-primary-700 text-white'
                                : 'bg-gray-200 text-gray-700 hover:bg-primary-200'
                            }`}
                    >
                        {cat === 'all' ? '📊 Tất cả' : `${cat === 'VietFarm' ? '🌿' : '🥥'} ${cat}`}
                    </button>
                ))}
            </div>

            <ResponsiveContainer width="100%" height={180}>
                <BarChart
                    data={filteredData}
                    layout="vertical"
                    margin={{ top: 5, right: 20, left: 140, bottom: 5 }}
                >
                    <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" horizontal={false} />
                    <XAxis type="number" style={{ fontSize: '12px' }} />
                    <YAxis dataKey="name" type="category" width={135} tick={{ fontSize: '11px' }} />
                    <Tooltip
                        formatter={(value) => `${value} lần chào`}
                        contentStyle={{ backgroundColor: '#f9fafb', border: '1px solid #d1d5db', fontSize: '12px' }}
                    />
                    <Bar
                        dataKey="sales"
                        radius={[0, 6, 6, 0]}
                        onClick={(e: any) => setSelectedProduct(e.payload.name)}
                    >
                        {filteredData.map((item, index) => (
                            <Cell
                                key={`cell-${index}`}
                                fill={colorMap[item.category as keyof typeof colorMap]}
                                opacity={!selectedProduct || selectedProduct === item.name ? 1 : 0.4}
                            />
                        ))}
                    </Bar>
                </BarChart>
            </ResponsiveContainer>

            {/* Legend */}
            <div className="flex gap-4 mt-3 border-t pt-3 justify-center text-xs">
                <div className="flex items-center gap-1">
                    <div className="w-3 h-3 rounded" style={{ backgroundColor: '#546B41' }}></div>
                    <span>VietFarm</span>
                </div>
                <div className="flex items-center gap-1">
                    <div className="w-3 h-3 rounded" style={{ backgroundColor: '#99AD7A' }}></div>
                    <span>VinaCoco</span>
                </div>
            </div>
        </div>
    );
}
