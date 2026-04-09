'use client';

import { useState } from 'react';
import { formatDate, formatCurrency } from '@core/utils/formatters';

const mockSaleOrders = [
    {
        sale_order_id: 1,
        contract_id: 1,
        order_date: '2025-01-20',
        delivery_date: '2025-02-28',
        total_amount: 50000,
        currency: 'USD',
        status: 'Confirmed',
        created_at: '2025-01-20',
        updated_at: '2025-01-20',
    },
    {
        sale_order_id: 2,
        contract_id: 1,
        order_date: '2025-02-01',
        delivery_date: '2025-03-15',
        total_amount: 75000,
        currency: 'USD',
        status: 'Shipped',
        created_at: '2025-02-01',
        updated_at: '2025-02-05',
    },
];

export default function SaleOrderDashboard() {
    const [showForm, setShowForm] = useState(false);
    const [selectedSO, setSelectedSO] = useState<any>(null);
    const [dateRange, setDateRange] = useState('thisMonth');
    const [selectedCategory, setSelectedCategory] = useState('all');

    const statusColors: Record<string, string> = {
        Draft: 'bg-accent-light text-primary-700',
        Confirmed: 'bg-primary-50 text-primary-700',
        Shipped: 'bg-green-50 text-green-800',
        Delivered: 'bg-secondary-50 text-secondary-700',
        Cancelled: 'bg-red-50 text-red-800',
    };

    return (
        <div className="space-y-6">
            {/* Page Header */}
            <div>
                <h1 className="text-4xl font-bold text-primary-700 mb-1">🛒 Quản lý Đơn hàng</h1>
                <p className="text-gray-600">Tạo và theo dõi các lệnh xuất hàng lẻ từ hợp đồng khung</p>
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
                <div className="bg-white rounded-lg border-t-4 p-5 shadow-sm hover:shadow-md transition-shadow" style={{ borderTopColor: '#546B41' }}>
                    <div className="flex items-center justify-between mb-3">
                        <h3 className="text-sm font-semibold text-gray-800">Tổng đơn hàng</h3>
                        <span className="text-2xl">🛒</span>
                    </div>
                    <div className="flex items-baseline gap-2">
                        <p className="text-3xl font-bold text-primary-700">{mockSaleOrders.length}</p>
                        <span className="text-green-600 text-xs font-bold">↑ 18%</span>
                    </div>
                </div>
                <div className="bg-white rounded-lg border-t-4 p-5 shadow-sm hover:shadow-md transition-shadow" style={{ borderTopColor: '#DCCCAC' }}>
                    <div className="flex items-center justify-between mb-3">
                        <h3 className="text-sm font-semibold text-gray-800">Đã xác nhận</h3>
                        <span className="text-2xl">✔️</span>
                    </div>
                    <div className="flex items-baseline gap-2">
                        <p className="text-3xl font-bold text-accent-700">
                            {mockSaleOrders.filter(s => s.status === 'Confirmed').length}
                        </p>
                        <span className="text-green-600 text-xs font-bold">↑ 12%</span>
                    </div>
                </div>
                <div className="bg-white rounded-lg border-t-4 p-5 shadow-sm hover:shadow-md transition-shadow" style={{ borderTopColor: '#10b981' }}>
                    <div className="flex items-center justify-between mb-3">
                        <h3 className="text-sm font-semibold text-gray-800">Đã gửi</h3>
                        <span className="text-2xl">📦</span>
                    </div>
                    <div className="flex items-baseline gap-2">
                        <p className="text-3xl font-bold text-green-700">
                            {mockSaleOrders.filter(s => ['Shipped', 'Delivered'].includes(s.status)).length}
                        </p>
                        <span className="text-green-600 text-xs font-bold">↑ 14%</span>
                    </div>
                </div>
                <div className="bg-white rounded-lg border-t-4 p-5 shadow-sm hover:shadow-md transition-shadow" style={{ borderTopColor: '#99AD7A' }}>
                    <div className="flex items-center justify-between mb-3">
                        <h3 className="text-sm font-semibold text-gray-800">Tổng giá</h3>
                        <span className="text-2xl">💵</span>
                    </div>
                    <div className="flex items-baseline gap-2">
                        <p className="text-3xl font-bold text-secondary-700">
                            {formatCurrency(mockSaleOrders.reduce((sum, s) => sum + s.total_amount, 0))}
                        </p>
                        <span className="text-green-600 text-xs font-bold">↑ 22%</span>
                    </div>
                </div>
            </div>

            {/* Main List */}
            <div className="bg-white rounded-lg shadow p-6 space-y-4 border-l-4 border-primary-700">
                <div className="flex justify-between items-center">
                    <h2 className="text-2xl font-bold text-primary-700">Danh sách Đơn hàng</h2>
                    <button
                        onClick={() => setShowForm(true)}
                        className="bg-primary-700 text-white px-6 py-2 rounded-lg hover:bg-primary-800 font-semibold"
                    >
                        ➕ Tạo Đơn hàng
                    </button>
                </div>

                <div className="overflow-x-auto">
                    <table className="w-full">
                        <thead className="bg-primary-50 border-b-2 border-primary-200">
                            <tr className="text-primary-700">
                                <th className="px-6 py-3 text-left font-semibold">Mã SO</th>
                                <th className="px-6 py-3 text-left font-semibold">Hợp đồng</th>
                                <th className="px-6 py-3 text-left font-semibold">Ngày lệnh</th>
                                <th className="px-6 py-3 text-left font-semibold">Ngày giao</th>
                                <th className="px-6 py-3 text-left font-semibold">Giá trị</th>
                                <th className="px-6 py-3 text-left font-semibold">Trạng thái</th>
                                <th className="px-6 py-3 text-left font-semibold">Hành động</th>
                            </tr>
                        </thead>
                        <tbody>
                            {mockSaleOrders.map((s) => (
                                <tr key={s.sale_order_id} className="border-b hover:bg-gray-50">
                                    <td className="px-6 py-4 font-mono">#{s.sale_order_id}</td>
                                    <td className="px-6 py-4">#{s.contract_id}</td>
                                    <td className="px-6 py-4">{formatDate(s.order_date)}</td>
                                    <td className="px-6 py-4">{formatDate(s.delivery_date)}</td>
                                    <td className="px-6 py-4 font-semibold">{formatCurrency(s.total_amount)}</td>
                                    <td className="px-6 py-4">
                                        <span className={`px-3 py-1 rounded-full text-sm font-semibold ${statusColors[s.status]}`}>
                                            {s.status}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4">
                                        <button
                                            onClick={() => setSelectedSO(s)}
                                            className="text-primary-600 hover:text-primary-800 font-semibold"
                                        >
                                            Chi tiết
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>

            {selectedSO && !showForm && (
                <div className="bg-white rounded-lg shadow p-8">
                    <div className="flex justify-between items-center mb-6">
                        <h2 className="text-2xl font-bold">Đơn hàng #{selectedSO.sale_order_id}</h2>
                        <button onClick={() => setSelectedSO(null)} className="text-2xl">✕</button>
                    </div>
                    <div className="grid grid-cols-3 gap-6">
                        <div>
                            <p className="text-sm text-gray-600">Hợp đồng</p>
                            <p className="font-semibold">#{selectedSO.contract_id}</p>
                        </div>
                        <div>
                            <p className="text-sm text-gray-600">Ngày lệnh</p>
                            <p className="font-semibold">{formatDate(selectedSO.order_date)}</p>
                        </div>
                        <div>
                            <p className="text-sm text-gray-600">Ngày giao</p>
                            <p className="font-semibold">{formatDate(selectedSO.delivery_date)}</p>
                        </div>
                    </div>
                    <div className="mt-6 pt-6 border-t">
                        <p className="text-xl font-bold">Tổng giá: {formatCurrency(selectedSO.total_amount)}</p>
                    </div>
                </div>
            )}

            {showForm && (
                <SaleOrderForm onClose={() => setShowForm(false)} />
            )}

            {/* Insights Footer */}
            <div className="bg-accent-light border-l-4 border-primary-700 rounded-lg p-6">
                <h3 className="text-base font-bold text-primary-700 mb-4 flex items-center gap-2">
                    💡 Những Thông tin Chính
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-sm">
                    <div>
                        <p className="font-semibold text-primary-700 mb-1">📦 Tỷ lệ Giao hàng Đúng hạn</p>
                        <p className="text-gray-700">88% đơn hàng giao đúng hạn. Độ trễ trung bình: 2-3 ngày khi có lỗi.</p>
                    </div>
                    <div>
                        <p className="font-semibold text-primary-700 mb-1">⭐ Giá trị Đơn hàng TB</p>
                        <p className="text-gray-700">Trung bình: $62,500/đơn. Phạm vi: $20K-$150K. Lớn nhất: $250K.</p>
                    </div>
                    <div>
                        <p className="font-semibold text-primary-700 mb-1">📊 Tỷ lệ Hoàn thành SO</p>
                        <p className="text-gray-700">95% SO được giao đầy đủ. Chỉ 5% ghi nhận hàng bụi/thiếu.</p>
                    </div>
                    <div>
                        <p className="font-semibold text-primary-700 mb-1">🚢 Logistics Partner</p>
                        <p className="text-gray-700">3PL là chủ yếu (65%), Direct Ship (35%). Cần diversify thêm.</p>
                    </div>
                </div>
            </div>
        </div>
    );
}

function SaleOrderForm({ onClose }: { onClose: () => void }) {
    const [formData, setFormData] = useState({
        contract_id: '',
        order_date: new Date().toISOString().split('T')[0],
        delivery_date: '',
        currency: 'USD',
    });

    return (
        <div className="bg-white rounded-lg shadow p-8 space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-2xl font-bold">Tạo Đơn hàng Mới</h2>
                <button onClick={onClose} className="text-2xl">✕</button>
            </div>

            <div className="grid grid-cols-2 gap-6">
                <div>
                    <label className="block text-sm font-semibold mb-2">Chọn Hợp đồng *</label>
                    <input
                        type="text"
                        placeholder="Nhập hoặc chọn hợp đồng"
                        className="w-full border border-gray-300 rounded-lg px-4 py-2"
                    />
                </div>

                <div>
                    <label className="block text-sm font-semibold mb-2">Ngày lệnh</label>
                    <input
                        type="date"
                        value={formData.order_date}
                        onChange={(e) => setFormData({ ...formData, order_date: e.target.value })}
                        className="w-full border border-gray-300 rounded-lg px-4 py-2"
                    />
                </div>

                <div>
                    <label className="block text-sm font-semibold mb-2">Ngày giao hàng *</label>
                    <input
                        type="date"
                        value={formData.delivery_date}
                        onChange={(e) => setFormData({ ...formData, delivery_date: e.target.value })}
                        className="w-full border border-gray-300 rounded-lg px-4 py-2"
                    />
                </div>

                <div>
                    <label className="block text-sm font-semibold mb-2">Tiền tệ</label>
                    <select
                        value={formData.currency}
                        onChange={(e) => setFormData({ ...formData, currency: e.target.value })}
                        className="w-full border border-gray-300 rounded-lg px-4 py-2"
                    >
                        <option value="USD">USD</option>
                        <option value="EUR">EUR</option>
                        <option value="VND">VND</option>
                    </select>
                </div>
            </div>

            <div className="flex gap-4 justify-end">
                <button
                    onClick={onClose}
                    className="border border-gray-300 text-gray-700 px-6 py-2 rounded-lg hover:bg-gray-50 font-semibold"
                >
                    Hủy
                </button>
                <button
                    onClick={() => {
                        alert('Đơn hàng đã được tạo!');
                        onClose();
                    }}
                    className="bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 font-semibold"
                >
                    Lưu
                </button>
            </div>
        </div>
    );
}
