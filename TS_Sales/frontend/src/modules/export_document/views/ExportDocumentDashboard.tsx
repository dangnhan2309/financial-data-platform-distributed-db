'use client';

import { useState } from 'react';
import { formatDate } from '@core/utils/formatters';

const mockExportDocs = [
    {
        document_set_id: 1,
        sale_order_id: 1,
        issue_date: '2025-02-20',
        document_type: 'CO',
        file_path: '/docs/CO_001.pdf',
        status: 'ISSUED',
        created_at: '2025-02-20',
        updated_at: '2025-02-20',
    },
    {
        document_set_id: 2,
        sale_order_id: 1,
        issue_date: '2025-02-22',
        document_type: 'PACKING_LIST',
        file_path: '/docs/PL_001.pdf',
        status: 'ISSUED',
        created_at: '2025-02-22',
        updated_at: '2025-02-22',
    },
];

const docTypeLabels: Record<string, string> = {
    CO: '🏛️ Certificate of Origin',
    CQ: '🇻🇳 Customs Declaration',
    PACKING_LIST: '📦 Packing List',
    BILL_OF_LADING: '⛴️ Bill of Lading',
};

export default function ExportDocumentDashboard() {
    const [showForm, setShowForm] = useState(false);
    const [selectedDoc, setSelectedDoc] = useState<any>(null);

    const statusColors: Record<string, string> = {
        PENDING: 'bg-yellow-100 text-yellow-800',
        ISSUED: 'bg-green-100 text-green-800',
        COMPLETED: 'bg-emerald-100 text-emerald-800',
    };

    return (
        <div className="space-y-8">
            <div>
                <h1 className="text-3xl font-bold text-gray-900 mb-2">📑 Bộ Chứng từ Xuất khẩu</h1>
                <p className="text-gray-600">Quản lý các chứng từ xuất khẩu: C/O, CQ, Packing List, B/L</p>
            </div>

            {/* Kanban Board */}
            <div className="grid grid-cols-3 gap-6">
                {['PENDING', 'ISSUED', 'COMPLETED'].map((status) => {
                    const docs = mockExportDocs.filter(d => d.status === status);
                    return (
                        <div key={status} className="bg-white rounded-lg shadow p-6">
                            <h3 className="text-lg font-bold text-gray-900 mb-4">
                                {status === 'PENDING' ? '⏳ Chưa phát hành' : status === 'ISSUED' ? '✅ Đã phát hành' : '🎉 Hoàn thành'}
                                <span className="text-sm ml-2 bg-gray-200 text-gray-800 px-2 py-1 rounded-full">({docs.length})</span>
                            </h3>
                            <div className="space-y-3">
                                {docs.map((doc) => (
                                    <div
                                        key={doc.document_set_id}
                                        onClick={() => setSelectedDoc(doc)}
                                        className="bg-gray-50 p-4 rounded-lg cursor-pointer hover:bg-gray-100 transition-colors"
                                    >
                                        <div className="flex items-start gap-2 mb-2">
                                            <span className="text-2xl">{docTypeLabels[doc.document_type]?.split(' ')[0]}</span>
                                            <div className="flex-1">
                                                <p className="font-semibold text-gray-900">{doc.document_type}</p>
                                                <p className="text-sm text-gray-600">SO #{doc.sale_order_id}</p>
                                            </div>
                                        </div>
                                        <p className="text-xs text-gray-500">Phát hành: {formatDate(doc.issue_date)}</p>
                                    </div>
                                ))}
                            </div>
                        </div>
                    );
                })}
            </div>

            {/* List View */}
            <div className="bg-white rounded-lg shadow p-6 space-y-4">
                <div className="flex justify-between items-center">
                    <h2 className="text-2xl font-bold text-gray-900">Danh sách Chi tiết Chứng từ</h2>
                    <button
                        onClick={() => setShowForm(true)}
                        className="bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 font-semibold"
                    >
                        ➕ Thêm Chứng từ
                    </button>
                </div>

                <div className="overflow-x-auto">
                    <table className="w-full">
                        <thead className="bg-primary-100 border-b-2 border-primary-600">
                            <tr>
                                <th className="px-6 py-3 text-left font-semibold">Mã</th>
                                <th className="px-6 py-3 text-left font-semibold">SO</th>
                                <th className="px-6 py-3 text-left font-semibold">Loại chứng từ</th>
                                <th className="px-6 py-3 text-left font-semibold">Ngày phát hành</th>
                                <th className="px-6 py-3 text-left font-semibold">File</th>
                                <th className="px-6 py-3 text-left font-semibold">Trạng thái</th>
                                <th className="px-6 py-3 text-left font-semibold">Hành động</th>
                            </tr>
                        </thead>
                        <tbody>
                            {mockExportDocs.map((doc) => (
                                <tr key={doc.document_set_id} className="border-b hover:bg-gray-50">
                                    <td className="px-6 py-4 font-mono">#{doc.document_set_id}</td>
                                    <td className="px-6 py-4">#{doc.sale_order_id}</td>
                                    <td className="px-6 py-4">{docTypeLabels[doc.document_type]}</td>
                                    <td className="px-6 py-4">{formatDate(doc.issue_date)}</td>
                                    <td className="px-6 py-4">
                                        <a href={doc.file_path} className="text-primary-600 hover:underline">📥 Tải</a>
                                    </td>
                                    <td className="px-6 py-4">
                                        <span className={`px-3 py-1 rounded-full text-sm font-semibold ${statusColors[doc.status]}`}>
                                            {doc.status === 'PENDING' ? 'Chưa' : doc.status === 'ISSUED' ? 'Đã' : 'Hoàn'}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4">
                                        <button
                                            onClick={() => setSelectedDoc(doc)}
                                            className="text-primary-600 hover:text-primary-800 font-semibold"
                                        >
                                            Xem
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>

            {selectedDoc && !showForm && (
                <div className="bg-white rounded-lg shadow p-8">
                    <div className="flex justify-between items-center mb-6">
                        <h2 className="text-2xl font-bold">{docTypeLabels[selectedDoc.document_type]}</h2>
                        <button onClick={() => setSelectedDoc(null)} className="text-2xl">✕</button>
                    </div>
                    <div className="grid grid-cols-3 gap-6">
                        <div>
                            <p className="text-sm text-gray-600">Đơn hàng</p>
                            <p className="font-semibold">#{selectedDoc.sale_order_id}</p>
                        </div>
                        <div>
                            <p className="text-sm text-gray-600">Ngày phát hành</p>
                            <p className="font-semibold">{formatDate(selectedDoc.issue_date)}</p>
                        </div>
                        <div>
                            <p className="text-sm text-gray-600">Trạng thái</p>
                            <p className="font-semibold">{selectedDoc.status}</p>
                        </div>
                    </div>
                    <div className="mt-6 pt-6 border-t">
                        <a href={selectedDoc.file_path} className="text-primary-600 hover:underline font-semibold">
                            📥 Tải file chứng từ
                        </a>
                    </div>
                </div>
            )}

            {showForm && (
                <ExportDocForm onClose={() => setShowForm(false)} />
            )}
        </div>
    );
}

function ExportDocForm({ onClose }: { onClose: () => void }) {
    const [formData, setFormData] = useState({
        sale_order_id: '',
        document_type: 'CO',
        issue_date: new Date().toISOString().split('T')[0],
    });

    return (
        <div className="bg-white rounded-lg shadow p-8 space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-2xl font-bold">Thêm Chứng từ Xuất khẩu</h2>
                <button onClick={onClose} className="text-2xl">✕</button>
            </div>

            <div className="grid grid-cols-2 gap-6">
                <div>
                    <label className="block text-sm font-semibold mb-2">Đơn hàng *</label>
                    <input
                        type="number"
                        value={formData.sale_order_id}
                        onChange={(e) => setFormData({ ...formData, sale_order_id: e.target.value })}
                        className="w-full border border-gray-300 rounded-lg px-4 py-2"
                        placeholder="Nhập SO ID"
                    />
                </div>

                <div>
                    <label className="block text-sm font-semibold mb-2">Loại chứng từ *</label>
                    <select
                        value={formData.document_type}
                        onChange={(e) => setFormData({ ...formData, document_type: e.target.value })}
                        className="w-full border border-gray-300 rounded-lg px-4 py-2"
                    >
                        <option value="CO">🏛️ Certificate of Origin</option>
                        <option value="CQ">🇻🇳 Customs Declaration</option>
                        <option value="PACKING_LIST">📦 Packing List</option>
                        <option value="BILL_OF_LADING">⛴️ Bill of Lading</option>
                    </select>
                </div>

                <div className="col-span-2">
                    <label className="block text-sm font-semibold mb-2">Ngày phát hành</label>
                    <input
                        type="date"
                        value={formData.issue_date}
                        onChange={(e) => setFormData({ ...formData, issue_date: e.target.value })}
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
                        alert('Chứng từ đã được thêm!');
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
