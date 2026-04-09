import { Customer } from '@core/services/types';

export const mockCustomers: Customer[] = [
    {
        customer_id: 1,
        customer_type: 'B2B',
        customer_code: 'C001',
        company_name: 'Osaka Foods Co., Ltd',
        short_name: 'Osaka Foods',
        tax_id: 'TAX00001',
        country: 'Japan',
        city: 'Tokyo',
        address: '1-2-1 Ginza, Chuo Ward, Tokyo',
        phone: '+81-3-xxxx-xxxx',
        email: 'sales@osakafood.jp',
        website: 'www.osakafood.jp',
        industry: 'Food & Beverage',
        status: 'ACTIVE',
        preferred_currency: 'USD',
        created_at: '2025-01-01',
    },
    {
        customer_id: 2,
        customer_type: 'B2B',
        customer_code: 'C002',
        company_name: 'Manhattan Beverages Inc',
        short_name: 'Manhattan Beverages',
        tax_id: 'TAX00002',
        country: 'USA',
        city: 'New York',
        address: '350 5th Ave, Manhattan, NY',
        phone: '+1-212-xxxx-xxxx',
        email: 'procurement@manhattan-bev.com',
        website: 'www.manhattan-bev.com',
        industry: 'Food & Beverage',
        status: 'ACTIVE',
        preferred_currency: 'USD',
        created_at: '2025-01-05',
    },
];

export const mockStaff = [
    { staff_id: 1, name: 'Nguyễn Văn A', role: 'Sales Manager', email: 'nva@gcfood.com', phone: '0901234567', department: 'Sales', status: 'ACTIVE' as const },
    { staff_id: 2, name: 'Trần Thị B', role: 'Export Specialist', email: 'ttb@gcfood.com', phone: '0901234568', department: 'Export', status: 'ACTIVE' as const },
    { staff_id: 3, name: 'Phạm Văn C', role: 'Sales Executive', email: 'pvc@gcfood.com', phone: '0901234569', department: 'Sales', status: 'ACTIVE' as const },
];

export const mockProducts = [
    { product_id: 1, product_type: 'Juice', name: 'Nha đam cắt hạt lựu', description: 'Fresh aloe vera pieces', price: 250, application: 'Food', brix: 12.5, product_size: '1000ml', solid: 5, ph: 4.5, is_active: 1, created_at: '2025-01-01', updated_at: '2025-01-01' },
    { product_id: 2, product_type: 'Puree', name: 'Nha đam xay', description: 'Aloe vera puree', price: 300, application: 'Food', brix: 14, product_size: '25kg', solid: 8, ph: 4.2, is_active: 1, created_at: '2025-01-01', updated_at: '2025-01-01' },
    { product_id: 3, product_type: 'Concentrate', name: 'Nha đam dạng lỏng', description: 'Aloe vera liquid concentrate', price: 400, application: 'Beverage', brix: 16, product_size: '200L', solid: 10, ph: 3.8, is_active: 1, created_at: '2025-01-01', updated_at: '2025-01-01' },
];

export const mockPaymentTerms = [
    { payment_term_id: 1, description: 'Net 30', number_of_days: 30, status: 'ACTIVE' },
    { payment_term_id: 2, description: 'Net 60', number_of_days: 60, status: 'ACTIVE' },
    { payment_term_id: 3, description: 'Advance Payment', number_of_days: 0, status: 'ACTIVE' },
];

export const mockIncoterms = [
    { incoterm_id: 1, name: 'FOB', description: 'Free on Board', version: '2020', status: 'ACTIVE' },
    { incoterm_id: 2, name: 'CIF', description: 'Cost, Insurance and Freight', version: '2020', status: 'ACTIVE' },
    { incoterm_id: 3, name: 'EXW', description: 'Ex Works', version: '2020', status: 'ACTIVE' },
];
