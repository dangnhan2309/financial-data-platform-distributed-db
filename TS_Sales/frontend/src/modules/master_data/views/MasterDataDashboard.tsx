'use client';

import { useState } from 'react';
import DataTable from '@core/components/DataTable';
import { mockCustomers, mockStaff, mockProducts, mockPaymentTerms, mockIncoterms } from '../models/mock-data';

export default function MasterDataDashboard() {
    const [activeTab, setActiveTab] = useState<'customers' | 'staff' | 'products' | 'payment-terms' | 'incoterms'>('customers');
    const [loading] = useState(false);

    const tabs = [
        { id: 'customers', label: '👥 Khách hàng', count: mockCustomers.length },
        { id: 'staff', label: '👤 Nhân viên', count: mockStaff.length },
        { id: 'products', label: '📦 Sản phẩm', count: mockProducts.length },
        { id: 'payment-terms', label: '💳 Điều khoản thanh toán', count: mockPaymentTerms.length },
        { id: 'incoterms', label: '🚢 Incoterm', count: mockIncoterms.length },
    ];

    return (
        <div className="space-y-8">
            <div>
                <h1 className="text-3xl font-bold text-primary-700 mb-2">Quản lý Dữ liệu</h1>
                <p className="text-gray-600">Quản lý các thông tin cơ bản như khách hàng, nhân viên, sản phẩm...</p>
            </div>

            {/* Tabs */}
            <div className="flex gap-2 flex-wrap">
                {tabs.map((tab) => (
                    <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id as any)}
                        className={`px-6 py-3 rounded-lg font-semibold transition-all ${activeTab === tab.id
                            ? 'bg-primary-700 text-white shadow-md'
                            : 'bg-white text-gray-700 border-2 border-primary-200 hover:bg-primary-50'
                            }`}
                    >
                        {tab.label} ({tab.count})
                    </button>
                ))}
            </div>

            {/* Customers Tab */}
            {activeTab === 'customers' && (
                <div className="space-y-4">
                    <div className="flex justify-between items-center">
                        <h2 className="text-2xl font-bold text-primary-700">Danh sách Khách hàng</h2>
                        <button className="bg-primary-700 text-white px-6 py-2 rounded-lg hover:bg-primary-800 font-semibold">
                            ➕ Thêm Khách hàng
                        </button>
                    </div>
                    <DataTable
                        columns={[
                            { header: 'Mã', accessor: (c) => c.customer_code, width: '80px' },
                            { header: 'Tên công ty', accessor: (c) => c.company_name },
                            { header: 'Quốc gia', accessor: (c) => c.country },
                            { header: 'Email', accessor: (c) => c.email },
                            { header: 'Trạng thái', accessor: (c) => <span className="bg-green-50 text-green-800 px-3 py-1 rounded-full text-sm border-l-2 border-green-600">{c.status}</span> },
                        ]}
                        data={mockCustomers}
                        isLoading={loading}
                        onRowClick={(customer) => console.log('Click:', customer)}
                    />
                </div>
            )}

            {/* Staff Tab */}
            {activeTab === 'staff' && (
                <div className="space-y-4">
                    <div className="flex justify-between items-center">
                        <h2 className="text-2xl font-bold text-primary-700">Danh sách Nhân viên</h2>
                        <button className="bg-primary-700 text-white px-6 py-2 rounded-lg hover:bg-primary-800 font-semibold">
                            ➕ Thêm Nhân viên
                        </button>
                    </div>
                    <DataTable
                        columns={[
                            { header: 'Họ tên', accessor: (s) => s.name },
                            { header: 'Vị trí', accessor: (s) => s.role },
                            { header: 'Email', accessor: (s) => s.email },
                            { header: 'Phòng ban', accessor: (s) => s.department },
                            { header: 'Trạng thái', accessor: (s) => <span className={`px-3 py-1 rounded-full text-sm ${s.status === 'ACTIVE' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>{s.status}</span> },
                        ]}
                        data={mockStaff}
                        isLoading={loading}
                    />
                </div>
            )}

            {/* Products Tab */}
            {activeTab === 'products' && (
                <div className="space-y-4">
                    <div className="flex justify-between items-center">
                        <h2 className="text-2xl font-bold text-gray-900">Danh sách Sản phẩm</h2>
                        <button className="bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 font-semibold">
                            ➕ Thêm Sản phẩm
                        </button>
                    </div>
                    <DataTable
                        columns={[
                            { header: 'Tên sản phẩm', accessor: (p) => p.name },
                            { header: 'Loại', accessor: (p) => p.product_type },
                            { header: 'Giá', accessor: (p) => `$${p.price}` },
                            { header: 'Brix (%)', accessor: (p) => p.brix },
                            { header: 'pH', accessor: (p) => p.ph },
                        ]}
                        data={mockProducts}
                        isLoading={loading}
                    />
                </div>
            )}

            {/* Payment Terms Tab */}
            {activeTab === 'payment-terms' && (
                <div className="space-y-4">
                    <div className="flex justify-between items-center">
                        <h2 className="text-2xl font-bold text-gray-900">Điều khoản Thanh toán</h2>
                        <button className="bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 font-semibold">
                            ➕ Thêm
                        </button>
                    </div>
                    <DataTable
                        columns={[
                            { header: 'Mô tả', accessor: (p) => p.description },
                            { header: 'Số ngày', accessor: (p) => `${p.number_of_days} ngày` },
                            { header: 'Trạng thái', accessor: (p) => <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">{p.status}</span> },
                        ]}
                        data={mockPaymentTerms}
                        isLoading={loading}
                    />
                </div>
            )}

            {/* Incoterms Tab */}
            {activeTab === 'incoterms' && (
                <div className="space-y-4">
                    <div className="flex justify-between items-center">
                        <h2 className="text-2xl font-bold text-gray-900">Incoterm</h2>
                        <button className="bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 font-semibold">
                            ➕ Thêm
                        </button>
                    </div>
                    <DataTable
                        columns={[
                            { header: 'Mã', accessor: (i) => i.name },
                            { header: 'Mô tả', accessor: (i) => i.description },
                            { header: 'Phiên bản', accessor: (i) => i.version },
                            { header: 'Trạng thái', accessor: (i) => <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">{i.status}</span> },
                        ]}
                        data={mockIncoterms}
                        isLoading={loading}
                    />
                </div>
            )}
        </div>
    );
}
