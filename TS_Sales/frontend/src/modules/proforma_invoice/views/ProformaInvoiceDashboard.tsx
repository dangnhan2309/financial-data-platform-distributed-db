'use client';

import { useState } from 'react';
import { formatDate, formatCurrency } from '@core/utils/formatters';
import { mockQuotations } from '@modules/quotation/models/mock-data';
import { mockPaymentTerms, mockStaff } from '@modules/master_data/models/mock-data';
import { mockCustomers } from '@modules/master_data/models/mock-data';

const mockProformaInvoices = [
    {
        proforma_invoice_id: 1,
        quotation_id: 1,
        payment_term_id: 1,
        staff_id: 1,
        total_contract_value: 27500,
        currency: 'USD',
        port_of_loading: 'Ho Chi Minh',
        port_of_discharge: 'Osaka',
        delivery_time: '2025-02-28',
        status: 'Draft',
        created_at: '2025-01-10',
        updated_at: '2025-01-10',
    },
];

export default function ProformaInvoiceDashboard() {
    const [showForm, setShowForm] = useState(false);
    const [selectedPI, setSelectedPI] = useState<any>(null);
    const [dateRange, setDateRange] = useState('thisMonth');
    const [selectedCategory, setSelectedCategory] = useState('all');

    const statusColors: Record<string, string> = {
        Draft: 'bg-accent-light text-primary-700',
        Confirmed: 'bg-primary-50 text-primary-700',
        Issued: 'bg-green-50 text-green-800',
        Cancelled: 'bg-red-50 text-red-800',
    };

    return (
        <div className="space-y-6">
            {/* Page Header */}
            <div>
                <h1 className="text-4xl font-bold text-primary-700 mb-1">📋 Hóa đơn Tạm tính (Proforma Invoice)</h1>
                <p className="text-gray-600">Tạo và quản lý hóa đơn tạm tính từ báo giá</p>
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
                        <h3 className="text-sm font-semibold text-gray-800">Tổng PI</h3>
                        <span className="text-2xl">📋</span>
                    </div>
                    <div className="flex items-baseline gap-2">
                        <p className="text-3xl font-bold text-primary-700">{mockProformaInvoices.length}</p>
                        <span className="text-green-600 text-xs font-bold">↑ 8%</span>
                    </div>
                </div>
                <div className="bg-white rounded-lg border-t-4 p-5 shadow-sm hover:shadow-md transition-shadow" style={{ borderTopColor: '#DCCCAC' }}>
                    <div className="flex items-center justify-between mb-3">
                        <h3 className="text-sm font-semibold text-gray-800">Nháp</h3>
                        <span className="text-2xl">📝</span>
                    </div>
                    <div className="flex items-baseline gap-2">
                        <p className="text-3xl font-bold text-accent-700">
                            {mockProformaInvoices.filter(p => p.status === 'Draft').length}
                        </p>
                        <span className="text-green-600 text-xs font-bold">↑ 5%</span>
                    </div>
                </div>
                <div className="bg-white rounded-lg border-t-4 p-5 shadow-sm hover:shadow-md transition-shadow" style={{ borderTopColor: '#10b981' }}>
                    <div className="flex items-center justify-between mb-3">
                        <h3 className="text-sm font-semibold text-gray-800">Đã phát hành</h3>
                        <span className="text-2xl">✅</span>
                    </div>
                    <div className="flex items-baseline gap-2">
                        <p className="text-3xl font-bold text-green-700">
                            {mockProformaInvoices.filter(p => p.status === 'Issued').length}
                        </p>
                        <span className="text-green-600 text-xs font-bold">↑ 10%</span>
                    </div>
                </div>
                <div className="bg-white rounded-lg border-t-4 p-5 shadow-sm hover:shadow-md transition-shadow" style={{ borderTopColor: '#99AD7A' }}>
                    <div className="flex items-center justify-between mb-3">
                        <h3 className="text-sm font-semibold text-gray-800">Tổng giá trị</h3>
                        <span className="text-2xl">💰</span>
                    </div>
                    <div className="flex items-baseline gap-2">
                        <p className="text-3xl font-bold text-secondary-700">
                            {formatCurrency(mockProformaInvoices.reduce((sum, p) => sum + p.total_contract_value, 0))}
                        </p>
                        <span className="text-green-600 text-xs font-bold">↑ 12%</span>
                    </div>
                </div>
            </div>

            {/* Main List */}
            <div className="bg-white rounded-lg shadow p-6 space-y-4 border-l-4 border-primary-700">
                <div className="flex justify-between items-center">
                    <h2 className="text-2xl font-bold text-primary-700">Danh sách Hóa đơn Tạm tính</h2>
                    <button
                        onClick={() => setShowForm(true)}
                        className="bg-primary-700 text-white px-6 py-2 rounded-lg hover:bg-primary-800 font-semibold"
                    >
                        ➕ Tạo PI
                    </button>
                </div>

                <div className="overflow-x-auto">
                    <table className="w-full">
                        <thead className="bg-primary-50 border-b-2 border-primary-200">
                            <tr className="text-primary-700">
                                <th className="px-6 py-3 text-left font-semibold">ID</th>
                                <th className="px-6 py-3 text-left font-semibold">Từ Báo giá</th>
                                <th className="px-6 py-3 text-left font-semibold">Khách hàng</th>
                                <th className="px-6 py-3 text-left font-semibold">Cảng tải</th>
                                <th className="px-6 py-3 text-left font-semibold">Cảng đến</th>
                                <th className="px-6 py-3 text-left font-semibold">Giá trị</th>
                                <th className="px-6 py-3 text-left font-semibold">Trạng thái</th>
                                <th className="px-6 py-3 text-left font-semibold">Hành động</th>
                            </tr>
                        </thead>
                        <tbody>
                            {mockProformaInvoices.map((p) => {
                                const quotation = mockQuotations.find(q => q.quotation_id === p.quotation_id);
                                const customer = mockCustomers.find(c => c.customer_id === quotation?.customer_id);
                                return (
                                    <tr key={p.proforma_invoice_id} className="border-b hover:bg-gray-50">
                                        <td className="px-6 py-4 font-mono">#{p.proforma_invoice_id}</td>
                                        <td className="px-6 py-4">#{quotation?.quotation_id}</td>
                                        <td className="px-6 py-4">{customer?.company_name}</td>
                                        <td className="px-6 py-4">{p.port_of_loading}</td>
                                        <td className="px-6 py-4">{p.port_of_discharge}</td>
                                        <td className="px-6 py-4 font-semibold">{formatCurrency(p.total_contract_value)}</td>
                                        <td className="px-6 py-4">
                                            <span className={`px-3 py-1 rounded-full text-sm font-semibold ${statusColors[p.status]}`}>
                                                {p.status}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4">
                                            <button
                                                onClick={() => setSelectedPI(p)}
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

            {selectedPI && !showForm && (
                <div className="bg-white rounded-lg shadow p-8">
                    <div className="flex justify-between items-center mb-6">
                        <h2 className="text-2xl font-bold">PI #{selectedPI.proforma_invoice_id}</h2>
                        <button onClick={() => setSelectedPI(null)} className="text-2xl">✕</button>
                    </div>
                    <div className="grid grid-cols-2 gap-6">
                        <div>
                            <p className="text-sm text-gray-600">Từ Báo giá</p>
                            <p className="font-semibold">#{selectedPI.quotation_id}</p>
                        </div>
                        <div>
                            <p className="text-sm text-gray-600">Điều khoản thanh toán</p>
                            <p className="font-semibold">
                                {mockPaymentTerms.find(pt => pt.payment_term_id === selectedPI.payment_term_id)?.description}
                            </p>
                        </div>
                        <div>
                            <p className="text-sm text-gray-600">Nhân viên phụ trách</p>
                            <p className="font-semibold">{mockStaff.find(s => s.staff_id === selectedPI.staff_id)?.name}</p>
                        </div>
                        <div>
                            <p className="text-sm text-gray-600">Ngày giao hàng dự kiến</p>
                            <p className="font-semibold">{formatDate(selectedPI.delivery_time)}</p>
                        </div>
                        <div>
                            <p className="text-sm text-gray-600">Cảng tải</p>
                            <p className="font-semibold">{selectedPI.port_of_loading}</p>
                        </div>
                        <div>
                            <p className="text-sm text-gray-600">Cảng đến</p>
                            <p className="font-semibold">{selectedPI.port_of_discharge}</p>
                        </div>
                    </div>
                    <div className="mt-6 pt-6 border-t">
                        <p className="text-xl font-bold">Tổng giá trị: {formatCurrency(selectedPI.total_contract_value)}</p>
                    </div>
                </div>
            )}

            {showForm && (
                <ProformaInvoiceForm onClose={() => setShowForm(false)} />
            )}

            {/* Insights Footer */}
            <div className="bg-accent-light border-l-4 border-primary-700 rounded-lg p-6">
                <h3 className="text-base font-bold text-primary-700 mb-4 flex items-center gap-2">
                    💡 Những Thông tin Chính
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-sm">
                    <div>
                        <p className="font-semibold text-primary-700 mb-1">📦 Tỷ lệ Xác nhận PI</p>
                        <p className="text-gray-700">85% PI từ báo giá được xác nhận. Chỉ 15% bị huỷ do thay đổi yêu cầu khách hàng.</p>
                    </div>
                    <div>
                        <p className="font-semibold text-primary-700 mb-1">⏱️ Thời gian Xử lý</p>
                        <p className="text-gray-700">Trung bình 3-5 ngày từ báo giá tới PI. Mục tiêu: giảm xuống 2 ngày.</p>
                    </div>
                    <div>
                        <p className="font-semibold text-primary-700 mb-1">🚢 Điều khoản Giao hàng</p>
                        <p className="text-gray-700">FOB chiếm 55%, CIF 35%, EXW 10%. Khách lớn ưa CIF nhất.</p>
                    </div>
                    <div>
                        <p className="font-semibold text-primary-700 mb-1">💵 Giá trị Trung bình</p>
                        <p className="text-gray-700">PI trung bình: $27,500. Nên tập trung vào hợp đồng khung lớn hơn.</p>
                    </div>
                </div>
            </div>
        </div>
    );
}

function ProformaInvoiceForm({ onClose }: { onClose: () => void }) {
    const [formData, setFormData] = useState({
        quotation_id: '',
        payment_term_id: '',
        staff_id: '',
        port_of_loading: '',
        port_of_discharge: '',
        delivery_time: new Date().toISOString().split('T')[0],
    });

    return (
        <div className="bg-white rounded-lg shadow p-8 space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-2xl font-bold">Tạo Hóa đơn Tạm tính Mới</h2>
                <button onClick={onClose} className="text-2xl">✕</button>
            </div>

            <div className="grid grid-cols-2 gap-6">
                <div>
                    <label className="block text-sm font-semibold mb-2">Chọn Báo giá *</label>
                    <select
                        value={formData.quotation_id}
                        onChange={(e) => setFormData({ ...formData, quotation_id: e.target.value })}
                        className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:border-primary-500"
                    >
                        <option value="">Chọn báo giá</option>
                        {mockQuotations.map((q) => {
                            const customer = mockCustomers.find(c => c.customer_id === q.customer_id);
                            return (
                                <option key={q.quotation_id} value={q.quotation_id}>
                                    #{q.quotation_id} - {customer?.company_name}
                                </option>
                            );
                        })}
                    </select>
                </div>

                <div>
                    <label className="block text-sm font-semibold mb-2">Điều khoản thanh toán *</label>
                    <select
                        value={formData.payment_term_id}
                        onChange={(e) => setFormData({ ...formData, payment_term_id: e.target.value })}
                        className="w-full border border-gray-300 rounded-lg px-4 py-2"
                    >
                        <option value="">Chọn điều khoản</option>
                        {mockPaymentTerms.map((pt) => (
                            <option key={pt.payment_term_id} value={pt.payment_term_id}>
                                {pt.description}
                            </option>
                        ))}
                    </select>
                </div>

                <div>
                    <label className="block text-sm font-semibold mb-2">Nhân viên *</label>
                    <select
                        value={formData.staff_id}
                        onChange={(e) => setFormData({ ...formData, staff_id: e.target.value })}
                        className="w-full border border-gray-300 rounded-lg px-4 py-2"
                    >
                        <option value="">Chọn nhân viên</option>
                        {mockStaff.map((s) => (
                            <option key={s.staff_id} value={s.staff_id}>
                                {s.name}
                            </option>
                        ))}
                    </select>
                </div>

                <div>
                    <label className="block text-sm font-semibold mb-2">Ngày giao hàng dự kiến</label>
                    <input
                        type="date"
                        value={formData.delivery_time}
                        onChange={(e) => setFormData({ ...formData, delivery_time: e.target.value })}
                        className="w-full border border-gray-300 rounded-lg px-4 py-2"
                    />
                </div>

                <div>
                    <label className="block text-sm font-semibold mb-2">Cảng tải *</label>
                    <input
                        type="text"
                        value={formData.port_of_loading}
                        onChange={(e) => setFormData({ ...formData, port_of_loading: e.target.value })}
                        className="w-full border border-gray-300 rounded-lg px-4 py-2"
                        placeholder="e.g. Ho Chi Minh"
                    />
                </div>

                <div>
                    <label className="block text-sm font-semibold mb-2">Cảng đến *</label>
                    <input
                        type="text"
                        value={formData.port_of_discharge}
                        onChange={(e) => setFormData({ ...formData, port_of_discharge: e.target.value })}
                        className="w-full border border-gray-300 rounded-lg px-4 py-2"
                        placeholder="e.g. Osaka"
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
                        alert('Hóa đơn tạm tính đã được tạo!');
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
