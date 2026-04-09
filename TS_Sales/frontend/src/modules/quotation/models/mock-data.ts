import { Quotation, QuotationItem } from '@core/services/types';

export const mockQuotations: Quotation[] = [
    {
        quotation_id: 1,
        customer_id: 1,
        staff_id: 1,
        quotation_date: '2025-01-10',
        expiry_date: '2025-02-10',
        total_amount: 50000,
        currency: 'USD',
        status: 'Draft',
        created_at: '2025-01-10',
    },
    {
        quotation_id: 2,
        customer_id: 2,
        staff_id: 2,
        quotation_date: '2025-01-08',
        expiry_date: '2025-02-08',
        total_amount: 75000,
        currency: 'USD',
        status: 'Sent',
        created_at: '2025-01-08',
    },
];

export const mockQuotationItems: QuotationItem[] = [
    {
        quotation_id: 1,
        product_id: 1,
        quantity: 100,
        unit_price: 250,
        discount: 0,
        tax_rate: 10,
        total_price: 27500,
        specifications: { brix: 12.5, ph: 4.5, mesh_size: 'Medium' },
    },
    {
        quotation_id: 1,
        product_id: 2,
        quantity: 50,
        unit_price: 300,
        discount: 5,
        tax_rate: 10,
        total_price: 15925,
        specifications: { brix: 14, ph: 4.2, mesh_size: 'Fine' },
    },
];
