'use client';

import { useState } from 'react';
import DashboardLayout from '@core/layouts/DashboardLayout';
import SalesFunnelChart from '@core/components/charts/SalesFunnelChart';
import QuotationStatusChart from '@core/components/charts/QuotationStatusChart';
import TopProductsChart from '@core/components/charts/TopProductsChart';
import ExportReadinessChart from '@core/components/charts/ExportReadinessChart';
import IncotermsChart from '@core/components/charts/IncotermsChart';
import { kpiData } from '@core/services/chart-data';

export default function Dashboard() {
    const [dateRange, setDateRange] = useState('thisMonth');
    const [selectedCategory, setSelectedCategory] = useState('all');

    return (
        <DashboardLayout>
            <div className="space-y-6">
                {/* Page Header */}
                <div>
                    <h1 className="text-4xl font-bold text-primary-700 mb-1">📊 Bảng Điều Khiển Kinh Doanh</h1>
                    <p className="text-gray-600">GC Food - Theo dõi bán hàng & xuất khẩu</p>
                </div>

                {/* Filters Section */}
                <div className="bg-white rounded-lg border-l-4 border-primary-700 p-5 shadow-sm flex flex-wrap items-center gap-6">
                    <div className="flex items-center gap-2">
                        <label className="text-sm font-semibold text-gray-700">Khoảng thời gian:</label>
                        <select
                            value={dateRange}
                            onChange={(e) => setDateRange(e.target.value)}
                            className="px-4 py-2 border-2 border-gray-300 rounded-lg text-sm font-medium focus:outline-none focus:border-primary-700"
                        >
                            <option value="thisMonth">Tháng này</option>
                            <option value="last3Months">3 tháng qua</option>
                            <option value="thisYear">Năm nay</option>
                            <option value="allTime">Toàn bộ</option>
                        </select>
                    </div>

                    <div className="flex items-center gap-2">
                        <label className="text-sm font-semibold text-gray-700">Danh mục:</label>
                        <select
                            value={selectedCategory}
                            onChange={(e) => setSelectedCategory(e.target.value)}
                            className="px-4 py-2 border-2 border-gray-300 rounded-lg text-sm font-medium focus:outline-none focus:border-primary-700"
                        >
                            <option value="all">Tất cả sản phẩm</option>
                            <option value="vietfarm">VietFarm (Nha đam)</option>
                            <option value="vinacoco">VinaCoco (Thạch dừa)</option>
                        </select>
                    </div>

                    <button className="ml-auto px-6 py-2 bg-primary-700 text-white rounded-lg hover:bg-primary-800 font-semibold transition-colors">
                        🔄 Làm mới
                    </button>
                </div>

                {/* KPI Cards Grid */}
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
                    {kpiData.map((kpi, idx) => (
                        <div
                            key={idx}
                            className="bg-white rounded-lg border-t-4 p-5 shadow-sm hover:shadow-md transition-shadow"
                            style={{ borderTopColor: kpi.color }}
                        >
                            <div className="flex items-center justify-between mb-3">
                                <h3 className="text-sm font-semibold text-gray-800">{kpi.label}</h3>
                                <span className="text-2xl">{kpi.icon}</span>
                            </div>
                            <div className="flex items-baseline gap-2">
                                <p className="text-3xl font-bold" style={{ color: kpi.color }}>{kpi.value}</p>
                                <span className="text-green-600 text-xs font-bold">↑ {kpi.change}%</span>
                            </div>
                        </div>
                    ))}
                </div>

                {/* Charts Grid */}
                <div className="space-y-6">
                    {/* Full Width: Sales Funnel */}
                    <SalesFunnelChart />

                    {/* 2x2 Grid */}
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                        <QuotationStatusChart />
                        <TopProductsChart />
                        <ExportReadinessChart />
                        <IncotermsChart />
                    </div>
                </div>

                {/* Insights Footer */}
                <div className="bg-accent-light border-l-4 border-primary-700 rounded-lg p-6">
                    <h3 className="text-base font-bold text-primary-700 mb-4 flex items-center gap-2">
                        💡 Những Thông tin Chính
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-sm">
                        <div>
                            <p className="font-semibold text-primary-700 mb-1">📉 Tỷ lệ Rơi rụng Khách hàng</p>
                            <p className="text-gray-700">72% báo giá không chuyển đổi thành hợp đồng. Cần review đơn giá & thông số kỹ thuật.</p>
                        </div>
                        <div>
                            <p className="font-semibold text-primary-700 mb-1">⭐ Sản phẩm Bán Chạy</p>
                            <p className="text-gray-700">Nha đam VietFarm (hạt lựu) dẫn đầu với 48 báo giá, VinaCoco thạch dừa 42 báo giá.</p>
                        </div>
                        <div>
                            <p className="font-semibold text-primary-700 mb-1">📦 Sẵn sàng Xuất khẩu</p>
                            <p className="text-gray-700">81% chứng từ hoàn tất. Điểm yếu: B/L (68%), cần tăng cường verify logistics.</p>
                        </div>
                        <div>
                            <p className="font-semibold text-primary-700 mb-1">🚢 Chiến lược Logistics</p>
                            <p className="text-gray-700">FOB 42% chiếm ưu thế. CIF 35%, EXW 23% - tối ưu hóa chi phí vận chuyển.</p>
                        </div>
                    </div>
                </div>
            </div>
        </DashboardLayout>
    );
}
