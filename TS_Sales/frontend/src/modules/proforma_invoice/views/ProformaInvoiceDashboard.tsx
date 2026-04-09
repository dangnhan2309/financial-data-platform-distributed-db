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

    const statusColors: Record<string, string> = {
        Draft: 'bg-yellow-100 text-yellow-800',
        Confirmed: 'bg-blue-100 text-blue-800',
        Issued: 'bg-green-100 text-green-800',
        Cancelled: 'bg-red-100 text-red-800',
    };

    return (
        <div className="space-y-8">
            <div>
                <h1 className="text-3xl font-bold text-gray-900 mb-2">📋 Hóa đơn Tạm tính (Proforma Invoice)</h1>
                <p className="text-gray-600">Tạo và quản lý hóa đơn tạm tính từ báo giá</p>
            </div>

            <div className="grid grid-cols-3 gap-4">
                <div className="bg-white rounded-lg shadow p-6">
                    <div className="text-3xl font-bold text-primary-600">{mockProformaInvoices.length}</div>
                    <div className="text-gray-600 mt-2">Tổng PI</div>
                </div>
                <div className="bg-white rounded-lg shadow p-6">
                    <div className="text-3xl font-bold text-blue-600">
                        {mockProformaInvoices.filter(p => p.status === 'Draft').length}
                    </div>
                    <div className="text-gray-600 mt-2">Nháp</div>
                </div>
                <div className="bg-white rounded-lg shadow p-6">
                    <div className="text-3xl font-bold text-green-600">
                        {formatCurrency(mockProformaInvoices.reduce((sum, p) => sum + p.total_contract_value, 0))}
                    </div>
                    <div className="text-gray-600 mt-2">Tổng giá trị</div>
                </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6 space-y-4">
                <div className="flex justify-between items-center">
                    <h2 className="text-2xl font-bold text-gray-900">Danh sách Hóa đơn Tạm tính</h2>
                    <button
                        onClick={() => setShowForm(true)}
                        className="bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 font-semibold"
                    >
                        ➕ Tạo PI
                    </button>
                </div>

                <div className="overflow-x-auto">
                    <table className="w-full">
                        <thead className="bg-primary-100 border-b-2 border-primary-600">
                            <tr>
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
