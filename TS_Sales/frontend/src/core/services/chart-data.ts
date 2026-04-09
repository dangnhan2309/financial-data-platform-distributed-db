// Mock data for dashboard charts

// 1. Sales Funnel Data
export const funnelData = [
    { stage: 'Báo giá', value: 150, color: '#546B41' },
    { stage: 'Hóa đơn Tạm tính', value: 85, color: '#99AD7A' },
    { stage: 'Hợp đồng', value: 42, color: '#DCCCAC' },
    { stage: 'Đơn hàng', value: 28, color: '#FFF8EC' },
];

// 2. Quotation Status Data
export const quotationStatusData = [
    { name: 'Draft', value: 45, color: '#546B41' },
    { name: 'Sent', value: 38, color: '#99AD7A' },
    { name: 'Approved', value: 42, color: '#DCCCAC' },
    { name: 'Rejected', value: 25, color: '#d32f2f' },
];

// 3. Top Selling Products Data
export const topProductsData = [
    { name: 'Nha đam cắt hạt lựu', sales: 48, category: 'VietFarm' },
    { name: 'Thạch dừa thô', sales: 42, category: 'VinaCoco' },
    { name: 'Nha đam xay', sales: 35, category: 'VietFarm' },
    { name: 'Sữa dừa cô đặc', sales: 32, category: 'VinaCoco' },
    { name: 'Nha đam dạng lỏng', sales: 28, category: 'VietFarm' },
    { name: 'Bột dừa sấy', sales: 22, category: 'VinaCoco' },
];

// 4. Export Readiness Score
export const exportReadinessData = [
    { document: 'C/O', completed: 92 },
    { document: 'CQ', completed: 78 },
    { document: 'PL', completed: 85 },
    { document: 'B/L', completed: 68 },
];

// 5. Incoterms Distribution
export const incotermsData = [
    { incoterm: 'FOB', count: 45, percentage: 42 },
    { incoterm: 'CIF', count: 38, percentage: 35 },
    { incoterm: 'EXW', count: 25, percentage: 23 },
];

// KPI Cards Data
export const kpiData = [
    { label: 'Báo giá', value: 150, change: 12, icon: '📄', color: '#546B41' },
    { label: 'Hóa đơn Tạm tính', value: 85, change: 8, icon: '📋', color: '#99AD7A' },
    { label: 'Hợp đồng', value: 42, change: 15, icon: '📝', color: '#DCCCAC' },
    { label: 'Đơn hàng', value: 28, change: 5, icon: '🛒', color: '#8B7355' },
];
