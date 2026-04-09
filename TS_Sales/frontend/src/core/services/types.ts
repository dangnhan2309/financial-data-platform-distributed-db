// Master Data Types
export interface Staff {
    staff_id: number;
    name: string;
    role: string;
    email: string;
    phone: string;
    department: string;
    status: 'ACTIVE' | 'INACTIVE' | 'TERMINATED' | 'FIRED';
}

export interface Customer {
    customer_id: number;
    customer_type: string;
    customer_code: string;
    company_name: string;
    short_name: string;
    tax_id: string;
    country: string;
    city: string;
    address: string;
    phone: string;
    email: string;
    website: string;
    industry: string;
    status: 'ACTIVE' | 'INACTIVE' | 'PENDING' | 'SUSPENDED' | 'VERIFIED' | 'TRIAL';
    preferred_currency: 'USD' | 'EUR' | 'VND';
    created_at: string;
}

export interface Product {
    product_id: number;
    product_type: string;
    name: string;
    description: string;
    price: number;
    application: string;
    brix: number;
    product_size: string;
    solid: number;
    ph: number;
    is_active: number;
    created_at: string;
    updated_at: string;
}

export interface PaymentTerm {
    payment_term_id: number;
    description: string;
    number_of_days: number;
    status: string;
}

export interface Incoterm {
    incoterm_id: number;
    name: string;
    description: string;
    version: string;
    status: string;
}

// Quotation Types
export interface QuotationSpecification {
    brix?: number;
    ph?: number;
    mesh_size?: string;
    [key: string]: any;
}

export interface QuotationItem {
    quotation_id: number;
    product_id: number;
    quantity: number;
    unit_price: number;
    discount?: number;
    tax_rate?: number;
    total_price: number;
    specifications?: QuotationSpecification;
    created_at?: string;
}

export interface Quotation {
    quotation_id: number;
    customer_id: number;
    staff_id: number;
    quotation_date: string;
    expiry_date: string;
    total_amount: number;
    currency: 'USD' | 'EUR' | 'VND';
    status: 'Draft' | 'Sent' | 'Interested' | 'Sampling' | 'Closed' | 'Won';
    items?: QuotationItem[];
    created_at: string;
}

// Proforma Invoice Types
export interface ProformaInvoice {
    proforma_invoice_id: number;
    quotation_id: number;
    payment_term_id: number;
    staff_id: number;
    total_contract_value: number;
    currency: string;
    port_of_loading: string;
    port_of_discharge: string;
    delivery_time: string;
    status: string;
    file_path?: string;
    created_at: string;
    updated_at: string;
}

// Contract Types
export interface ContractItem {
    contract_id: number;
    product_id: number;
    quantity: number;
    unit_price: number;
    discount?: number;
    tax_rate?: number;
    total_price: number;
    created_at?: string;
}

export interface Contract {
    contract_id: number;
    customer_id: number;
    contract_type: string;
    incoterm_id: number;
    proforma_invoice_id: number;
    contract_date: string;
    effective_date: string;
    expiry_date: string;
    total_contract_value: number;
    total_quantity: number;
    currency: string;
    loading_port: string;
    destination_port: string;
    status: string;
    signed_date?: string;
    items?: ContractItem[];
    created_at: string;
    updated_at: string;
}

// Sale Order Types
export interface SaleOrder {
    sale_order_id: number;
    contract_id: number;
    order_date: string;
    delivery_date: string;
    total_amount: number;
    currency: string;
    status: string;
    created_at: string;
    updated_at: string;
}

// Export Document Types
export interface ExportDocumentSet {
    document_set_id: number;
    sale_order_id: number;
    issue_date: string;
    document_type: 'CO' | 'CQ' | 'PACKING_LIST' | 'BILL_OF_LADING';
    file_path?: string;
    status: 'PENDING' | 'ISSUED' | 'COMPLETED';
    created_at: string;
    updated_at: string;
}
