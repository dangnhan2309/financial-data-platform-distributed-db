'use client';

import { useState } from 'react';
import { formatDate, formatCurrency } from '@core/utils/formatters';
import { mockIncoterms } from '@modules/master_data/models/mock-data';
import { mockCustomers } from '@modules/master_data/models/mock-data';

const mockContracts = [
    {
        contract_id: 1,
        customer_id: 1,
        contract_type: 'Frame Contract',
        incoterm_id: 1,
        proforma_invoice_id: 1,
        contract_date: '2025-01-15',
        effective_date: '2025-01-20',
        expiry_date: '2025-12-31',
        total_contract_value: 250000,
        total_quantity: 1000,
        currency: 'USD',
        loading_port: 'Ho Chi Minh',
        destination_port: 'Osaka',
        status: 'Active',
        signed_date: '2025-01-16',
        created_at: '2025-01-15',
        updated_at: '2025-01-15',
    },
];

export default function ContractDashboard() {
    const [showForm, setShowForm] = useState(false);
    const [selectedContract, setSelectedContract] = useState<any>(null);
    const [dateRange, setDateRange] = useState('thisMonth');
    const [selectedCategory, setSelectedCategory] = useState('all');

    const statusColors: Record<string, string> = {
        Active: 'bg-green-50 text-green-800',
        Pending: 'bg-accent-light text-primary-700',
        Suspended: 'bg-yellow-50 text-yellow-800',
        Closed: 'bg-red-50 text-red-800',
    };

    return (
        <div className="space-y-6">
            {/* Page Header */}
            <div>
                <h1 className="text-4xl font-bold text-primary-700 mb-1">📝 Quản lý Hợp đồng</h1>
                <p className="text-gray-600">Tạo, quản lý hợp đồng khung và các chi tiết hợp đồng</p>
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
                        <h3 className="text-sm font-semibold text-gray-800">Tổng hợp đồng</h3>
                        <span className="text-2xl">📝</span>
                    </div>
                    <div className="flex items-baseline gap-2">
                        <p className="text-3xl font-bold text-primary-700">{mockContracts.length}</p>
                        <span className="text-green-600 text-xs font-bold">↑ 15%</span>
                    </div>
                </div>
                <div className="bg-white rounded-lg border-t-4 p-5 shadow-sm hover:shadow-md transition-shadow" style={{ borderTopColor: '#10b981' }}>
                    <div className="flex items-center justify-between mb-3">
                        <h3 className="text-sm font-semibold text-gray-800">Đang hiệu lực</h3>
                        <span className="text-2xl">✅</span>
                    </div>
                    <div className="flex items-baseline gap-2">
                        <p className="text-3xl font-bold text-green-700">
                            {mockContracts.filter(c => c.status === 'Active').length}
                        </p>
                        <span className="text-green-600 text-xs font-bold">↑ 10%</span>
                    </div>
                </div>
                <div className="bg-white rounded-lg border-t-4 p-5 shadow-sm hover:shadow-md transition-shadow" style={{ borderTopColor: '#99AD7A' }}>
                    <div className="flex items-center justify-between mb-3">
                        <h3 className="text-sm font-semibold text-gray-800">Tổng số lượng</h3>
                        <span className="text-2xl">📦</span>
                    </div>
                    <div className="flex items-baseline gap-2">
                        <p className="text-3xl font-bold text-secondary-700">{mockContracts[0]?.total_quantity}</p>
                        <span className="text-green-600 text-xs font-bold">↑ 8%</span>
                    </div>
                </div>
                <div className="bg-white rounded-lg border-t-4 p-5 shadow-sm hover:shadow-md transition-shadow" style={{ borderTopColor: '#DCCCAC' }}>
                    <div className="flex items-center justify-between mb-3">
                        <h3 className="text-sm font-semibold text-gray-800">Tổng giá trị</h3>
                        <span className="text-2xl">💰</span>
                    </div>
                    <div className="flex items-baseline gap-2">
                        <p className="text-3xl font-bold text-accent-700">
                            {formatCurrency(mockContracts.reduce((sum, c) => sum + c.total_contract_value, 0))}
                        </p>
                        <span className="text-green-600 text-xs font-bold">↑ 20%</span>
                    </div>
                </div>
            </div>

            {/* Main List */}
            <div className="bg-white rounded-lg shadow p-6 space-y-4 border-l-4 border-primary-700">
                <div className="flex justify-between items-center">
                    <h2 className="text-2xl font-bold text-primary-700">Danh sách Hợp đồng</h2>
                    <button
                        onClick={() => setShowForm(true)}
                        className="bg-primary-700 text-white px-6 py-2 rounded-lg hover:bg-primary-800 font-semibold"
                    >
                        ➕ Tạo Hợp đồng
                    </button>
                </div>

                <div className="overflow-x-auto">
                    <table className="w-full">
                        <thead className="bg-primary-50 border-b-2 border-primary-200">
                            <tr className="text-primary-700">
                                <th className="px-6 py-3 text-left font-semibold">Mã HĐ</th>
                                <th className="px-6 py-3 text-left font-semibold">Khách hàng</th>
                                <th className="px-6 py-3 text-left font-semibold">Loại</th>
                                <th className="px-6 py-3 text-left font-semibold">Incoterm</th>
                                <th className="px-6 py-3 text-left font-semibold">Ngày ký</th>
                                <th className="px-6 py-3 text-left font-semibold">Hạn</th>
                                <th className="px-6 py-3 text-left font-semibold">Giá trị</th>
                                <th className="px-6 py-3 text-left font-semibold">Trạng thái</th>
                                <th className="px-6 py-3 text-left font-semibold">Hành động</th>
                            </tr>
                        </thead>
                        <tbody>
                            {mockContracts.map((c) => {
                                const customer = mockCustomers.find(cu => cu.customer_id === c.customer_id);
                                const incoterm = mockIncoterms.find(i => i.incoterm_id === c.incoterm_id);
                                return (
                                    <tr key={c.contract_id} className="border-b hover:bg-gray-50">
                                        <td className="px-6 py-4 font-mono">#{c.contract_id}</td>
                                        <td className="px-6 py-4">{customer?.company_name}</td>
                                        <td className="px-6 py-4">{c.contract_type}</td>
                                        <td className="px-6 py-4">{incoterm?.name}</td>
                                        <td className="px-6 py-4">{formatDate(c.signed_date || c.contract_date)}</td>
                                        <td className="px-6 py-4">{formatDate(c.expiry_date)}</td>
                                        <td className="px-6 py-4 font-semibold">{formatCurrency(c.total_contract_value)}</td>
                                        <td className="px-6 py-4">
                                            <span className={`px-3 py-1 rounded-full text-sm font-semibold ${statusColors[c.status]}`}>
                                                {c.status}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4">
                                            <button
                                                onClick={() => setSelectedContract(c)}
                                                className="text-primary-600 hover:text-primary-800 font-semibold"
                                            >
                                                Xem
                                            </button>
                                        </td>
                                    </tr>
                                );
                            })}
                        </tbody>
                    </table>
                </div>
            </div>

            {selectedContract && !showForm && (
                <div className="bg-white rounded-lg shadow p-8">
                    <div className="flex justify-between items-center mb-6">
                        <h2 className="text-2xl font-bold">Hợp đồng #{selectedContract.contract_id}</h2>
                        <button onClick={() => setSelectedContract(null)} className="text-2xl">✕</button>
                    </div>
                    <div className="grid grid-cols-3 gap-6">
                        <div>
                            <p className="text-sm text-gray-600">Khách hàng</p>
                            <p className="font-semibold">{mockCustomers.find(c => c.customer_id === selectedContract.customer_id)?.company_name}</p>
                        </div>
                        <div>
                            <p className="text-sm text-gray-600">Loại hợp đồng</p>
                            <p className="font-semibold">{selectedContract.contract_type}</p>
                        </div>
                        <div>
                            <p className="text-sm text-gray-600">Incoterm</p>
                            <p className="font-semibold">{mockIncoterms.find(i => i.incoterm_id === selectedContract.incoterm_id)?.name}</p>
                        </div>
                        <div>
                            <p className="text-sm text-gray-600">Cảng tải</p>
                            <p className="font-semibold">{selectedContract.loading_port}</p>
                        </div>
                        <div>
                            <p className="text-sm text-gray-600">Cảng đến</p>
                            <p className="font-semibold">{selectedContract.destination_port}</p>
                        </div>
                        <div>
                            <p className="text-sm text-gray-600">Tổng số lượng</p>
                            <p className="font-semibold">{selectedContract.total_quantity} đơn vị</p>
                        </div>
                    </div>
                    <div className="mt-6 pt-6 border-t">
                        <p className="text-xl font-bold">Tổng giá trị: {formatCurrency(selectedContract.total_contract_value)}</p>
                    </div>
                </div>
            )}

            {showForm && (
                <ContractForm onClose={() => setShowForm(false)} />
            )}

            {/* Insights Footer */}
            <div className="bg-accent-light border-l-4 border-primary-700 rounded-lg p-6">
                <h3 className="text-base font-bold text-primary-700 mb-4 flex items-center gap-2">
                    💡 Những Thông tin Chính
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-sm">
                    <div>
                        <p className="font-semibold text-primary-700 mb-1">📋 Tỷ lệ Hoàn tất Hợp đồng</p>
                        <p className="text-gray-700">92% hợp đồng khung đã ký kết. Chỉ 8% còn đang trong giai đoạn thương lượng.</p>
                    </div>
                    <div>
                        <p className="font-semibold text-primary-700 mb-1">🎯 Loại Hợp đồng Phổ biến</p>
                        <p className="text-gray-700">Frame Contract 70%, Supply Agreement 25%, Spot 5%. Khách lớn yếu thích khung.</p>
                    </div>
                    <div>
                        <p className="font-semibold text-primary-700 mb-1">💱 Điều khoản Thanh toán</p>
                        <p className="text-gray-700">L/C 45%, T/T 40%, D/A 15%. L/C là an toàn nhất cho xuất khẩu.</p>
                    </div>
                    <div>
                        <p className="font-semibold text-primary-700 mb-1">⏳ Thời hiệu Hợp đồng</p>
                        <p className="text-gray-700">Trung bình 12 tháng. 30% mở rộng 6-12 tháng tiếp theo.</p>
                    </div>
                </div>
            </div>
        </div>
    );
}

function ContractForm({ onClose }: { onClose: () => void }) {
    const [formData, setFormData] = useState({
        customer_id: '',
        contract_type: '',
        incoterm_id: '',
        contract_date: new Date().toISOString().split('T')[0],
        effective_date: '',
        expiry_date: '',
        loading_port: '',
        destination_port: '',
        currency: 'USD',
    });

    return (
        <div className="bg-white rounded-lg shadow p-8 space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-2xl font-bold">Tạo Hợp đồng Mới</h2>
                <button onClick={onClose} className="text-2xl">✕</button>
            </div>

            <div className="grid grid-cols-2 gap-6">
                <div>
                    <label className="block text-sm font-semibold mb-2">Khách hàng *</label>
                    <select
                        value={formData.customer_id}
                        onChange={(e) => setFormData({ ...formData, customer_id: e.target.value })}
                        className="w-full border border-gray-300 rounded-lg px-4 py-2"
                    >
                        <option value="">Chọn khách hàng</option>
                        {mockCustomers.map((c) => (
                            <option key={c.customer_id} value={c.customer_id}>
                                {c.company_name}
                            </option>
                        ))}
                    </select>
                </div>

                <div>
                    <label className="block text-sm font-semibold mb-2">Loại hợp đồng *</label>
                    <input
                        type="text"
                        value={formData.contract_type}
                        onChange={(e) => setFormData({ ...formData, contract_type: e.target.value })}
                        className="w-full border border-gray-300 rounded-lg px-4 py-2"
                        placeholder="e.g. Frame Contract"
                    />
                </div>

                <div>
                    <label className="block text-sm font-semibold mb-2">Incoterm *</label>
                    <select
                        value={formData.incoterm_id}
                        onChange={(e) => setFormData({ ...formData, incoterm_id: e.target.value })}
                        className="w-full border border-gray-300 rounded-lg px-4 py-2"
                    >
                        <option value="">Chọn Incoterm</option>
                        {mockIncoterms.map((i) => (
                            <option key={i.incoterm_id} value={i.incoterm_id}>
                                {i.name} - {i.description}
                            </option>
                        ))}
                    </select>
                </div>

                <div>
                    <label className="block text-sm font-semibold mb-2">Cảng tải *</label>
                    <input
                        type="text"
                        value={formData.loading_port}
                        onChange={(e) => setFormData({ ...formData, loading_port: e.target.value })}
                        className="w-full border border-gray-300 rounded-lg px-4 py-2"
                        placeholder="e.g. Ho Chi Minh"
                    />
                </div>

                <div>
                    <label className="block text-sm font-semibold mb-2">Cảng đến *</label>
                    <input
                        type="text"
                        value={formData.destination_port}
                        onChange={(e) => setFormData({ ...formData, destination_port: e.target.value })}
                        className="w-full border border-gray-300 rounded-lg px-4 py-2"
                        placeholder="e.g. Osaka"
                    />
                </div>

                <div>
                    <label className="block text-sm font-semibold mb-2">Ngày ký hợp đồng</label>
                    <input
                        type="date"
                        value={formData.contract_date}
                        onChange={(e) => setFormData({ ...formData, contract_date: e.target.value })}
                        className="w-full border border-gray-300 rounded-lg px-4 py-2"
                    />
                </div>

                <div>
                    <label className="block text-sm font-semibold mb-2">Ngày hiệu lực</label>
                    <input
                        type="date"
                        value={formData.effective_date}
                        onChange={(e) => setFormData({ ...formData, effective_date: e.target.value })}
                        className="w-full border border-gray-300 rounded-lg px-4 py-2"
                    />
                </div>

                <div>
                    <label className="block text-sm font-semibold mb-2">Hạn hiệu lực</label>
                    <input
                        type="date"
                        value={formData.expiry_date}
                        onChange={(e) => setFormData({ ...formData, expiry_date: e.target.value })}
                        className="w-full border border-gray-300 rounded-lg px-4 py-2"
                    />
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
                        alert('Hợp đồng đã được tạo!');
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
