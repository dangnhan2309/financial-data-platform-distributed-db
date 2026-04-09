'use client';

import { useState } from 'react';

const oracleSObjects = {
    Procedures: [
        { name: 'sp_create_quotation', params: ['p_customer_id', 'p_staff_id', 'p_quotation_date'] },
        { name: 'sp_update_quotation', params: ['p_quotation_id', 'p_status'] },
        { name: 'sp_generate_proforma', params: ['p_quotation_id'] },
    ],
    Functions: [
        { name: 'get_customer_by_code', params: ['p_code'] },
        { name: 'calculate_quotation_total', params: ['p_quotation_id'] },
        { name: 'check_contract_active', params: ['p_contract_id'] },
    ],
    Packages: [
        { name: 'PKG_QUOTATION_MGMT', params: [] },
        { name: 'PKG_CONTRACT_MGMT', params: [] },
        { name: 'PKG_EXPORT_DOCS', params: [] },
    ],
    Indexes: [
        { name: 'idx_quotation_customer', params: [] },
        { name: 'idx_contract_status', params: [] },
        { name: 'idx_sale_order_date', params: [] },
    ],
    Triggers: [
        { name: 'trg_quotation_audit', params: [] },
        { name: 'trg_contract_update', params: [] },
        { name: 'trg_sale_order_insert', params: [] },
    ],
    Sequences: [
        { name: 'seq_quotation_id', params: [] },
        { name: 'seq_contract_id', params: [] },
        { name: 'seq_sale_order_id', params: [] },
    ],
};

export default function OracleExecutionHub() {
    const [activeTab, setActiveTab] = useState<'Procedures' | 'Functions' | 'Packages' | 'Indexes' | 'Triggers' | 'Sequences'>('Procedures');
    const [selectedObject, setSelectedObject] = useState<any>(null);
    const [parameters, setParameters] = useState<Record<string, string>>({});
    const [result, setResult] = useState<any>(null);
    const [isExecuting, setIsExecuting] = useState(false);

    const tabs = Object.keys(oracleSObjects) as Array<keyof typeof oracleSObjects>;

    const handleExecute = async () => {
        setIsExecuting(true);
        // Simulate execution
        setTimeout(() => {
            setResult({
                success: true,
                message: 'Execution completed successfully',
                data: {
                    executedAt: new Date().toISOString(),
                    affectedRows: Math.floor(Math.random() * 100),
                    duration: Math.random() * 1000,
                },
            });
            setIsExecuting(false);
        }, 1000);
    };

    return (
        <div className="space-y-8">
            <div>
                <h1 className="text-3xl font-bold text-gray-900 mb-2">🔧 Oracle DB Execution Hub</h1>
                <p className="text-gray-600">Công cụ kiểm thử Oracle Database Objects (dành cho Admin/Dev)</p>
            </div>

            {/* Tabs */}
            <div className="flex gap-2 flex-wrap bg-white rounded-lg shadow p-2">
                {tabs.map((tab) => (
                    <button
                        key={tab}
                        onClick={() => {
                            setActiveTab(tab);
                            setSelectedObject(null);
                            setResult(null);
                        }}
                        className={`px-6 py-3 rounded-lg font-semibold transition-all ${activeTab === tab
                                ? 'bg-primary-600 text-white shadow-md'
                                : 'text-gray-700 hover:bg-gray-100'
                            }`}
                    >
                        {tab === 'Procedures' && '▶️'} {tab === 'Functions' && 'ƒ()'} {tab === 'Packages' && '📦'}
                        {tab === 'Indexes' && '📇'} {tab === 'Triggers' && '⚡'} {tab === 'Sequences' && '🔢'} {tab}
                    </button>
                ))}
            </div>

            {/* Object List */}
            <div className="grid grid-cols-3 gap-6">
                {/* Object Selector */}
                <div className="bg-white rounded-lg shadow p-6">
                    <h3 className="text-lg font-bold text-gray-900 mb-4">Danh sách {activeTab}</h3>
                    <div className="space-y-2 max-h-96 overflow-y-auto">
                        {oracleSObjects[activeTab].map((obj) => (
                            <button
                                key={obj.name}
                                onClick={() => {
                                    setSelectedObject(obj);
                                    setResult(null);
                                    setParameters({});
                                }}
                                className={`w-full text-left px-4 py-3 rounded-lg transition-colors ${selectedObject?.name === obj.name
                                        ? 'bg-primary-100 text-primary-900 border-2 border-primary-600'
                                        : 'bg-gray-50 text-gray-900 hover:bg-gray-100 border border-gray-200'
                                    }`}
                            >
                                <div className="font-semibold text-sm">{obj.name}</div>
                                {obj.params.length > 0 && (
                                    <div className="text-xs text-gray-600 mt-1">
                                        {obj.params.length} tham số
                                    </div>
                                )}
                            </button>
                        ))}
                    </div>
                </div>

                {/* Parameters Form */}
                <div className="bg-white rounded-lg shadow p-6">
                    {selectedObject ? (
                        <>
                            <h3 className="text-lg font-bold text-gray-900 mb-4">Tham số</h3>
                            {selectedObject.params.length === 0 ? (
                                <p className="text-gray-600">Không có tham số</p>
                            ) : (
                                <div className="space-y-4">
                                    {selectedObject.params.map((param: string) => (
                                        <div key={param}>
                                            <label className="block text-sm font-semibold text-gray-700 mb-1">
                                                {param}
                                            </label>
                                            <input
                                                type="text"
                                                value={parameters[param] || ''}
                                                onChange={(e) =>
                                                    setParameters({ ...parameters, [param]: e.target.value })
                                                }
                                                className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:border-primary-500"
                                                placeholder="Nhập giá trị"
                                            />
                                        </div>
                                    ))}
                                </div>
                            )}
                            <button
                                onClick={handleExecute}
                                disabled={isExecuting}
                                className="w-full mt-6 bg-primary-600 text-white py-2 rounded-lg hover:bg-primary-700 disabled:opacity-50 font-semibold"
                            >
                                {isExecuting ? '⏳ Đang thực hiện...' : '▶️ Thực hiện'}
                            </button>
                        </>
                    ) : (
                        <p className="text-gray-600">Chọn một object để xem tham số</p>
                    )}
                </div>

                {/* Result Display */}
                <div className="bg-white rounded-lg shadow p-6">
                    <h3 className="text-lg font-bold text-gray-900 mb-4">Kết quả</h3>
                    {result ? (
                        <div className="space-y-4">
                            <div className="bg-green-50 border-l-4 border-green-600 p-4">
                                <p className="text-green-900 font-semibold">✅ Thành công</p>
                                <p className="text-green-700 text-sm mt-1">{result.message}</p>
                            </div>
                            <div className="bg-gray-50 rounded p-3">
                                <p className="text-xs text-gray-600 font-mono mb-2">Kết quả trả về:</p>
                                <pre className="text-xs whitespace-pre-wrap overflow-auto bg-white p-2 rounded border border-gray-200">
                                    {JSON.stringify(result.data, null, 2)}
                                </pre>
                            </div>
                        </div>
                    ) : (
                        <p className="text-gray-600">Chưa có kết quả. Thực hiện một query để xem kết quả.</p>
                    )}
                </div>
            </div>

            {/* Query Builder */}
            <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-bold text-gray-900 mb-4">Soạn thảo Oracle Query</h3>
                <div className="space-y-4">
                    <textarea
                        className="w-full border border-gray-300 rounded-lg p-4 font-mono text-sm h-48 focus:outline-none focus:border-primary-500"
                        placeholder="SELECT ...&#10;FROM ...&#10;WHERE ..."
                        defaultValue={selectedObject ? `EXEC ${selectedObject.name}` : ''}
                    />
                    <button className="bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 font-semibold">
                        ▶️ Thực hiện Query
                    </button>
                </div>
            </div>
        </div>
    );
}
