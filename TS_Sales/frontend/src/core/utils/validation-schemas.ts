import { z } from 'zod';

export const QuotationItemSchema = z.object({
    product_id: z.number().min(1, 'Vui lòng chọn sản phẩm'),
    quantity: z.number().min(1, 'Số lượng phải >= 1'),
    unit_price: z.number().min(0, 'Giá phải >= 0'),
    discount: z.number().min(0, 'Chiết khấu phải >= 0').optional(),
    tax_rate: z.number().min(0, 'Thuế phải >= 0').optional(),
    brix: z.number().optional(),
    ph: z.number().optional(),
    mesh_size: z.string().optional(),
});

export const QuotationSchema = z.object({
    customer_id: z.number().min(1, 'Vui lòng chọn khách hàng'),
    staff_id: z.number().min(1, 'Vui lòng chọn nhân viên'),
    quotation_date: z.string().min(1, 'Ngày báo giá bắt buộc'),
    expiry_date: z.string().min(1, 'Ngày hết hiệu lực bắt buộc'),
    currency: z.enum(['USD', 'EUR', 'VND']),
    items: z.array(QuotationItemSchema).min(1, 'Báo giá phải có ít nhất 1 sản phẩm'),
});

export const ContractSchema = z.object({
    customer_id: z.number().min(1, 'Vui lòng chọn khách hàng'),
    contract_type: z.string().min(1, 'Loại hợp đồng bắt buộc'),
    incoterm_id: z.number().min(1, 'Vui lòng chọn Incoterm'),
    proforma_invoice_id: z.number().min(1, 'Vui lòng chọn Proforma Invoice'),
    contract_date: z.string().min(1, 'Ngày hợp đồng bắt buộc'),
    effective_date: z.string().min(1, 'Ngày hiệu lực bắt buộc'),
    expiry_date: z.string().min(1, 'Ngày hết hiệu lực bắt buộc'),
    loading_port: z.string().min(1, 'Cảng tải bắt buộc'),
    destination_port: z.string().min(1, 'Cảng đến bắt buộc'),
    currency: z.enum(['USD', 'EUR', 'VND']),
});

export const ProformaInvoiceSchema = z.object({
    quotation_id: z.number().min(1, 'Vui lòng chọn Quotation'),
    payment_term_id: z.number().min(1, 'Vui lòng chọn Payment Term'),
    staff_id: z.number().min(1, 'Vui lòng chọn nhân viên'),
    port_of_loading: z.string().min(1, 'Cảng tải bắt buộc'),
    port_of_discharge: z.string().min(1, 'Cảng đến bắt buộc'),
    delivery_time: z.string().min(1, 'Thời gian giao hàng bắt buộc'),
    currency: z.enum(['USD', 'EUR', 'VND']),
});

export const SaleOrderSchema = z.object({
    contract_id: z.number().min(1, 'Vui lòng chọn Hợp đồng'),
    order_date: z.string().min(1, 'Ngày lệnh bắt buộc'),
    delivery_date: z.string().min(1, 'Ngày giao hàng bắt buộc'),
    currency: z.enum(['USD', 'EUR', 'VND']),
});

export type QuotationFormData = z.infer<typeof QuotationSchema>;
export type ContractFormData = z.infer<typeof ContractSchema>;
export type ProformaInvoiceFormData = z.infer<typeof ProformaInvoiceSchema>;
export type SaleOrderFormData = z.infer<typeof SaleOrderSchema>;
