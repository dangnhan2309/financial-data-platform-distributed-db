'use client';

import { useState } from 'react';
import { Quotation } from '@core/services/types';
import { mockQuotations, mockQuotationItems } from '../models/mock-data';
import { mockCustomers, mockStaff, mockProducts } from '@modules/master_data/models/mock-data';
import { formatDate, formatCurrency } from '@core/utils/formatters';

export default function QuotationDashboard() {
    const [showForm, setShowForm] = useState(false);
    const [quotations] = useState<Quotation[]>(mockQuotations);
    const [selectedQuotation, setSelectedQuotation] = useState<Quotation | null>(null);

    const statusColors: Record<string, string> = {
        Draft: 'bg-yellow-100 text-yellow-800',
        Sent: 'bg-blue-100 text-blue-800',
        Interested: 'bg-purple-100 text-purple-800',
        Sampling: 'bg-orange-100 text-orange-800',
        Closed: 'bg-red-100 text-red-800',
        Won: 'bg-green-100 text-green-800',
    };

    return (
        <div className="space-y-8">
            <div>
                <h1 className="text-3xl font-bold text-gray-900 mb-2">📄 Quản lý Báo giá Kỹ thuật</h1>
                <p className="text-gray-600">Tạo, quản lý và theo dõi báo giá kỹ thuật với các thông số Specification</p>
            </div>

            {/* Statistics */}
            <div className="grid grid-cols-4 gap-4">
                <div className="bg-white rounded-lg shadow p-6">
                    <div className="text-3xl font-bold text-primary-600">{quotations.length}</div>
                    <div className="text-gray-600 mt-2">Tổng báo giá</div>
                </div>
                <div className="bg-white rounded-lg shadow p-6">
                    <div className="text-3xl font-bold text-blue-600">{quotations.filter(q => q.status === 'Sent').length}</div>
                    <div className="text-gray-600 mt-2">Đã gửi</div>
                </div>
                <div className="bg-white rounded-lg shadow p-6">
                    <div className="text-3xl font-bold text-green-600">{quotations.filter(q => q.status === 'Won').length}</div>
                    <div className="text-gray-600 mt-2">Thành công</div>
                </div>
                <div className="bg-white rounded-lg shadow p-6">
                    <div className="text-3xl font-bold text-purple-600">
                        {formatCurrency(quotations.reduce((sum, q) => sum + q.total_amount, 0), 'USD')}
                    </div>
                    <div className="text-gray-600 mt-2">Tổng giá trị</div>
                </div>
            </div>

            {/* Main List */}
            <div className="bg-white rounded-lg shadow p-6 space-y-4">
                <div className="flex justify-between items-center">
                    <h2 className="text-2xl font-bold text-gray-900">Danh sách Báo giá</h2>
                    <button
                        onClick={() => {
                            setShowForm(true);
                            setSelectedQuotation(null);
                        }}
                        className="bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 font-semibold"
                    >
                        ➕ Tạo Báo giá
                    </button>
                </div>

                <div className="overflow-x-auto">
                    <table className="w-full">
                        <thead className="bg-primary-100 border-b-2 border-primary-600">
                            <tr>
                                <th className="px-6 py-3 text-left font-semibold text-gray-900">ID</th>
                                <th className="px-6 py-3 text-left font-semibold text-gray-900">Khách hàng</th>
                                <th className="px-6 py-3 text-left font-semibold text-gray-900">Nhân viên</th>
                                <th className="px-6 py-3 text-left font-semibold text-gray-900">Ngày báo giá</th>
                                <th className="px-6 py-3 text-left font-semibold text-gray-900">Tổng giá</th>
                                <th className="px-6 py-3 text-left font-semibold text-gray-900">Trạng thái</th>
                                <th className="px-6 py-3 text-left font-semibold text-gray-900">Hành động</th>
                            </tr>
                        </thead>
                        <tbody>
                            {quotations.map((q) => {
                                const customer = mockCustomers.find(c => c.customer_id === q.customer_id);
                                const staff = mockStaff.find(s => s.staff_id === q.staff_id);
                                return (
                                    <tr key={q.quotation_id} className="border-b hover:bg-gray-50">
                                        <td className="px-6 py-4 font-mono text-gray-900">#{q.quotation_id}</td>
                                        <td className="px-6 py-4 text-gray-900">{customer?.company_name}</td>
                                        <td className="px-6 py-4 text-gray-900">{staff?.name}</td>
                                        <td className="px-6 py-4 text-gray-600">{formatDate(q.quotation_date)}</td>
                                        <td className="px-6 py-4 font-semibold text-gray-900">{formatCurrency(q.total_amount, q.currency)}</td>
                                        <td className="px-6 py-4">
                                            <span className={`px-3 py-1 rounded-full text-sm font-semibold ${statusColors[q.status] || 'bg-gray-100 text-gray-800'}`}>
                                                {q.status}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4">
                                            <button
                                                onClick={() => {
                                                    setSelectedQuotation(q);
                                                    setShowForm(false);
                                                }}
                                                className="text-primary-600 hover:text-primary-800 font-semibold"
                                            >
                                                Xem chi tiết
                                            </button>
                                        </td>
                                    </tr>
                                );
                            })}
                        </tbody>
                    </table>
                </div>
            </div>

            {/* Quotation Details */}
            {selectedQuotation && !showForm && (
                <QuotationDetails quotation={selectedQuotation} onClose={() => setSelectedQuotation(null)} />
            )}

            {/* Create/Edit Form */}
            {showForm && (
                <QuotationForm onClose={() => setShowForm(false)} />
            )}
        </div>
    );
}

function QuotationDetails({ quotation, onClose }: { quotation: Quotation; onClose: () => void }) {
    const items = mockQuotationItems.filter(item => item.quotation_id === quotation.quotation_id);
    const customer = mockCustomers.find(c => c.customer_id === quotation.customer_id);
    const staff = mockStaff.find(s => s.staff_id === quotation.staff_id);

    return (
        <div className="bg-white rounded-lg shadow p-8 space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-2xl font-bold text-gray-900">Chi tiết Báo giá #{quotation.quotation_id}</h2>
                <button onClick={onClose} className="text-gray-600 hover:text-gray-900 text-2xl">✕</button>
            </div>

            <div className="grid grid-cols-2 gap-6">
                <div>
                    <p className="text-sm text-gray-600 mb-1">Khách hàng</p>
                    <p className="text-lg font-semibold text-gray-900">{customer?.company_name}</p>
                    <p className="text-sm text-gray-600 mt-2">{customer?.address}</p>
                </div>
                <div>
                    <p className="text-sm text-gray-600 mb-1">Nhân viên phụ trách</p>
                    <p className="text-lg font-semibold text-gray-900">{staff?.name}</p>
                    <p className="text-sm text-gray-600 mt-2">{staff?.email}</p>
                </div>
                <div>
                    <p className="text-sm text-gray-600 mb-1">Ngày báo giá</p>
                    <p className="text-lg font-semibold text-gray-900">{formatDate(quotation.quotation_date)}</p>
                </div>
                <div>
                    <p className="text-sm text-gray-600 mb-1">Hạn hiệu lực</p>
                    <p className="text-lg font-semibold text-gray-900">{formatDate(quotation.expiry_date)}</p>
                </div>
            </div>

            <div className="border-t pt-6">
                <h3 className="text-xl font-bold text-gray-900 mb-4">Các sản phẩm trong báo giá</h3>
                <div className="overflow-x-auto">
                    <table className="w-full">
                        <thead className="bg-gray-100 border-b">
                            <tr>
                                <th className="px-4 py-2 text-left font-semibold text-gray-900">Sản phẩm</th>
                                <th className="px-4 py-2 text-left font-semibold text-gray-900">Số lượng</th>
                                <th className="px-4 py-2 text-left font-semibold text-gray-900">Giá/SP</th>
                                <th className="px-4 py-2 text-left font-semibold text-gray-900">Brix (%)</th>
                                <th className="px-4 py-2 text-left font-semibold text-gray-900">pH</th>
                                <th className="px-4 py-2 text-left font-semibold text-gray-900">Mesh Size</th>
                                <th className="px-4 py-2 text-left font-semibold text-gray-900">Tổng</th>
                            </tr>
                        </thead>
                        <tbody>
                            {items.map((item) => {
                                const product = mockProducts.find(p => p.product_id === item.product_id);
                                return (
                                    <tr key={`${item.quotation_id}-${item.product_id}`} className="border-b hover:bg-gray-50">
                                        <td className="px-4 py-3 text-gray-900">{product?.name}</td>
                                        <td className="px-4 py-3 text-gray-900">{item.quantity}</td>
                                        <td className="px-4 py-3 text-gray-900">{formatCurrency(item.unit_price)}</td>
                                        <td className="px-4 py-3 text-gray-900">{item.specifications?.brix || '-'}</td>
                                        <td className="px-4 py-3 text-gray-900">{item.specifications?.ph || '-'}</td>
                                        <td className="px-4 py-3 text-gray-900">{item.specifications?.mesh_size || '-'}</td>
                                        <td className="px-4 py-3 font-bold text-gray-900">{formatCurrency(item.total_price)}</td>
                                    </tr>
                                );
                            })}
                        </tbody>
                    </table>
                </div>
                <div className="text-right mt-4 pt-4 border-t-2">
                    <p className="text-xl font-bold text-gray-900">
                        Tổng cộng: {formatCurrency(quotation.total_amount, quotation.currency)}
                    </p>
                </div>
            </div>
        </div>
    );
}

function QuotationForm({ onClose }: { onClose: () => void }) {
    const [formData, setFormData] = useState({
        customer_id: '',
        staff_id: '',
        quotation_date: new Date().toISOString().split('T')[0],
        expiry_date: '',
        currency: 'USD',
    });
    const [items, setItems] = useState<any[]>([]);

    const addItem = () => {
        setItems([...items, { product_id: '', quantity: 1, unit_price: 0, brix: '', ph: '', mesh_size: '' }]);
    };

    const removeItem = (index: number) => {
        setItems(items.filter((_, i) => i !== index));
    };

    return (
        <div className="bg-white rounded-lg shadow p-8 space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-2xl font-bold text-gray-900">Tạo Báo giá Mới</h2>
                <button onClick={onClose} className="text-gray-600 hover:text-gray-900 text-2xl">✕</button>
            </div>

            <div className="grid grid-cols-2 gap-6">
                <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">Khách hàng *</label>
                    <select
                        value={formData.customer_id}
                        onChange={(e) => setFormData({ ...formData, customer_id: e.target.value })}
                        className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:border-primary-500"
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
                    <label className="block text-sm font-semibold text-gray-700 mb-2">Nhân viên *</label>
                    <select
                        value={formData.staff_id}
                        onChange={(e) => setFormData({ ...formData, staff_id: e.target.value })}
                        className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:border-primary-500"
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
                    <label className="block text-sm font-semibold text-gray-700 mb-2">Ngày báo giá</label>
                    <input
                        type="date"
                        value={formData.quotation_date}
                        onChange={(e) => setFormData({ ...formData, quotation_date: e.target.value })}
                        className="w-full border border-gray-300 rounded-lg px-4 py-2"
                    />
                </div>
                <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">Hạn hiệu lực</label>
                    <input
                        type="date"
                        value={formData.expiry_date}
                        onChange={(e) => setFormData({ ...formData, expiry_date: e.target.value })}
                        className="w-full border border-gray-300 rounded-lg px-4 py-2"
                    />
                </div>
            </div>

            <div className="border-t pt-6">
                <div className="flex justify-between items-center mb-4">
                    <h3 className="text-xl font-bold text-gray-900">Chi tiết Sản phẩm *</h3>
                    <button
                        onClick={addItem}
                        className="bg-secondary-600 text-white px-6 py-2 rounded-lg hover:bg-secondary-700 font-semibold text-sm"
                    >
                        ➕ Thêm Sản phẩm
                    </button>
                </div>

                {items.length === 0 ? (
                    <p className="text-gray-600 py-4">Chưa có sản phẩm nào. Nhấn nút "Thêm Sản phẩm" để bắt đầu.</p>
                ) : (
                    <div className="space-y-4 overflow-x-auto">
                        <table className="w-full">
                            <thead className="bg-gray-100">
                                <tr>
                                    <th className="px-4 py-2 text-left font-semibold text-gray-900">Sản phẩm</th>
                                    <th className="px-4 py-2 text-left font-semibold text-gray-900">SL</th>
                                    <th className="px-4 py-2 text-left font-semibold text-gray-900">Giá</th>
                                    <th className="px-4 py-2 text-left font-semibold text-gray-900">Brix (%)</th>
                                    <th className="px-4 py-2 text-left font-semibold text-gray-900">pH</th>
                                    <th className="px-4 py-2 text-left font-semibold text-gray-900">Mesh Size</th>
                                    <th className="px-4 py-2 text-left font-semibold text-gray-900">Hành động</th>
                                </tr>
                            </thead>
                            <tbody>
                                {items.map((item, idx) => (
                                    <tr key={idx} className="border-b">
                                        <td className="px-4 py-3">
                                            <select
                                                value={item.product_id}
                                                onChange={(e) => {
                                                    const newItems = [...items];
                                                    newItems[idx].product_id = e.target.value;
                                                    setItems(newItems);
                                                }}
                                                className="border border-gray-300 rounded px-2 py-1 w-full"
                                            >
                                                <option value="">Chọn sản phẩm</option>
                                                {mockProducts.map((p) => (
                                                    <option key={p.product_id} value={p.product_id}>
                                                        {p.name}
                                                    </option>
                                                ))}
                                            </select>
                                        </td>
                                        <td className="px-4 py-3">
                                            <input
                                                type="number"
                                                min="1"
                                                value={item.quantity}
                                                onChange={(e) => {
                                                    const newItems = [...items];
                                                    newItems[idx].quantity = parseInt(e.target.value);
                                                    setItems(newItems);
                                                }}
                                                className="border border-gray-300 rounded px-2 py-1 w-full"
                                            />
                                        </td>
                                        <td className="px-4 py-3">
                                            <input
                                                type="number"
                                                min="0"
                                                value={item.unit_price}
                                                onChange={(e) => {
                                                    const newItems = [...items];
                                                    newItems[idx].unit_price = parseFloat(e.target.value);
                                                    setItems(newItems);
                                                }}
                                                className="border border-gray-300 rounded px-2 py-1 w-full"
                                            />
                                        </td>
                                        <td className="px-4 py-3">
                                            <input
                                                type="number"
                                                step="0.1"
                                                placeholder="e.g. 12.5"
                                                value={item.brix}
                                                onChange={(e) => {
                                                    const newItems = [...items];
                                                    newItems[idx].brix = e.target.value;
                                                    setItems(newItems);
                                                }}
                                                className="border border-gray-300 rounded px-2 py-1 w-full"
                                            />
                                        </td>
                                        <td className="px-4 py-3">
                                            <input
                                                type="number"
                                                step="0.1"
                                                placeholder="e.g. 4.5"
                                                value={item.ph}
                                                onChange={(e) => {
                                                    const newItems = [...items];
                                                    newItems[idx].ph = e.target.value;
                                                    setItems(newItems);
                                                }}
                                                className="border border-gray-300 rounded px-2 py-1 w-full"
                                            />
                                        </td>
                                        <td className="px-4 py-3">
                                            <input
                                                type="text"
                                                placeholder="e.g. Medium"
                                                value={item.mesh_size}
                                                onChange={(e) => {
                                                    const newItems = [...items];
                                                    newItems[idx].mesh_size = e.target.value;
                                                    setItems(newItems);
                                                }}
                                                className="border border-gray-300 rounded px-2 py-1 w-full"
                                            />
                                        </td>
                                        <td className="px-4 py-3">
                                            <button
                                                onClick={() => removeItem(idx)}
                                                className="text-red-600 hover:text-red-800 font-semibold"
                                            >
                                                ✕
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
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
                        alert('Báo giá đã được tạo thành công!');
                        onClose();
                    }}
                    className="bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 font-semibold"
                >
                    Lưu Báo giá
                </button>
            </div>
        </div>
    );
}
