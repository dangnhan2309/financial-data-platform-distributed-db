# 📊 GC Food TS Sales - SQLAlchemy Models Structure

## Overview
Tất cả **12 SQLAlchemy Models** đã được tạo dựa vào SQL schema từ `hq_create_schema.sql`

---

## ✅ Models Created

### 1️⃣ **Staff** (`api/models/staff.py`)
**Nhân viên/Employees**
```
Columns: staff_id (PK), name, role, email, phone, department, status
Status: ACTIVE, INACTIVE, TERMINATED, FIRED
```

### 2️⃣ **Customer** (`api/models/customer.py`)
**Khách hàng/Clients**
```
Columns: customer_id (PK), customer_type, customer_code, company_name, 
         short_name, tax_id, country, city, address, phone, email, 
         website, industry, status, preferred_currency, created_at
Status: ACTIVE, INACTIVE, PENDING, SUSPENDED, VERIFIED, TRIAL
```

### 3️⃣ **Product** (`api/models/product.py`)
**Sản phẩm/SKUs**
```
Columns: product_id (PK), product_type, name, description, price,
         application, brix, product_size, solid, ph, is_active,
         created_at, updated_at
Type: Juice, Puree, Concentrate
```

### 4️⃣ **PaymentTerm** (`api/models/payment_term.py`)
**Điều khoản thanh toán**
```
Columns: payment_term_id (PK), description, number_of_days, status
Example: Net30, Net60, etc.
```

### 5️⃣ **Incoterm** (`api/models/incoterm.py`)
**Điều khoản thương mại quốc tế**
```
Columns: incoterm_id (PK), name, description, version, status
Example: FOB, CIF (version 2020, 2010)
```

### 6️⃣ **Quotation** (`api/models/quotation.py`)
**Báo giá/Offers**
```
Columns: quotation_id (PK), customer_id (FK), staff_id (FK),
         quotation_date, expiry_date, total_amount, currency, status, created_at
Status: DRAFT, APPROVED, REJECTED, EXPIRED, PENDING_REVIEW
Relationships:
  - customer: Customer
  - staff: Staff
  - items: List[QuotationItem] (one-to-many)
```

### 7️⃣ **QuotationItem** (`api/models/quotation_item.py`) ⭐
**Chi tiết báo giá (Composite PK)**
```
Columns: quotation_id (PK,FK), product_id (PK,FK),
         quantity, unit_price, discount, tax_rate, total_price, created_at
PrimaryKey: (quotation_id, product_id)
Relationships:
  - quotation: Quotation
  - product: Product
```

### 8️⃣ **ProformaInvoice** (`api/models/proforma_invoice.py`)
**Hóa đơn tờ khai/PI**
```
Columns: proforma_invoice_id (PK), quotation_id (FK), payment_term_id (FK),
         staff_id (FK), total_contract_value, currency, port_of_loading,
         port_of_discharge, delivery_time, status, file_path,
         created_at, updated_at
Status: DRAFT, ISSUED, ACCEPTED, REJECTED, CANCELLED
```

### 9️⃣ **Contract** (`api/models/contract.py`)
**Hợp đồng/Contracts**
```
Columns: contract_id (PK), customer_id (FK), contract_type, incoterm_id (FK),
         proforma_invoice_id (FK), contract_date, effective_date, expiry_date,
         total_contract_value, total_quantity, currency, loading_port,
         destination_port, status, signed_date, created_at, updated_at
Status: ACTIVE, EXPIRED, PENDING, COMPLETED, CANCELLED
Type: Standard, Long-term, Trial, Partnership
Relationships:
  - customer: Customer
  - incoterm: Incoterm
  - proforma_invoice: ProformaInvoice
  - items: List[ContractItem] (one-to-many)
  - sale_orders: List[SaleOrder] (one-to-many)
```

### 🔟 **ContractItem** (`api/models/contract_item.py`) ⭐
**Chi tiết hợp đồng (Composite PK)**
```
Columns: contract_id (PK,FK), product_id (PK,FK),
         quantity, unit_price, discount, tax_rate, total_price, created_at
PrimaryKey: (contract_id, product_id)
Relationships:
  - contract: Contract (back_populates="items")
  - product: Product
```

### 1️⃣1️⃣ **SaleOrder** (`api/models/sale_order.py`)
**Đơn hàng bán hàng/Sales Orders**
```
Columns: sale_order_id (PK), contract_id (FK), order_date, delivery_date,
         total_amount, currency, status, created_at, updated_at
Status: DRAFT, PENDING, IN_PROGRESS, DELIVERED, COMPLETED, CANCELLED
Relationships:
  - contract: Contract
  - export_documents: List[ExportDocumentSet] (one-to-many)
```

### 1️⃣2️⃣ **ExportDocumentSet** (`api/models/export_document_set.py`)
**Bộ giấy tờ xuất khẩu**
```
Columns: document_set_id (PK), sale_order_id (FK), issue_date, document_type,
         file_path, status, created_at, updated_at
Type: B/L, Invoice, Packing List, Certificate of Origin, Health Certificate
Status: COMPLETED, IN_PROGRESS, PENDING
```

---

## 🔗 Entity Relationship Diagram (ERD)

```
┌─────────────────┐
│     Staff       │─────────────────────┐
├─────────────────┤                    │
│ staff_id (PK)   │                    │
│ name            │                    │
│ role            │                    │
│ email           │                    │
└─────────────────┘                    ▼
                              ┌────────────────────┐
                              │   Quotation        │
                              ├────────────────────┤
                              │ quotation_id (PK)  │
                              │ customer_id (FK)───┼───────┐
                              │ staff_id (FK)──────┘       │
                              │ quotation_date     │       │
                              │ status             │       │
                              └─────────┬──────────┘       │
                                        │                  │
                                        ▼                  │
                              ┌────────────────────┐       │
                              │  QuotationItem     │       │
                              ├────────────────────┤       │
                              │ quotation_id (PK,FK)       │
                              │ product_id (PK,FK)─┼──┐    │
                              │ quantity           │  │    │
                              │ unit_price         │  │    │
                              └────────────────────┘  │    │
                                                      │    │
                              ┌──────────────────────┘    │
                              │                           │
                              ▼                           │
                    ┌────────────────────┐               │
                    │     Product        │               │
                    ├────────────────────┤               │
                    │ product_id (PK)    │               │
                    │ name               │               │
                    │ price              │               │
                    │ is_active          │               │
                    └────────────────────┘               │
                                                        │
                    ┌────────────────┐                  │
                    │    Customer    │◄─────────────────┘
                    ├────────────────┤
                    │ customer_id(PK)│
                    │ company_name   │
                    │ status         │
                    └────────────────┘
                         │
                         ▼
                    ┌────────────────┐
                    │   Contract     │
                    ├────────────────┤
                    │ contract_id(PK)│
                    │ customer_id(FK)│
                    │ incoterm_id(FK)│
                    │ proforma_id(FK)│
                    │ status         │
                    └────┬───────────┘
                         │
                         ▼
                    ┌────────────────┐
                    │ ContractItem   │
                    ├────────────────┤
                    │ contract_id(PK)│
                    │ product_id(PK) │◄──────┐
                    │ quantity       │       │
                    └────────────────┘    Product
                         │
                         ▼
                    ┌────────────────┐
                    │   SaleOrder    │
                    ├────────────────┤
                    │ sale_order_id  │
                    │ contract_id(FK)│
                    │ status         │
                    └────┬───────────┘
                         │
                         ▼
                    ┌────────────────────────────┐
                    │  ExportDocumentSet         │
                    ├────────────────────────────┤
                    │ document_set_id (PK)       │
                    │ sale_order_id (FK)         │
                    │ document_type              │
                    │ status                     │
                    └────────────────────────────┘
```

---

## 📊 Database Statistics

| Table | Record Count | Columns | Primary Key |
|-------|-------------|---------|------------|
| staff | 100 | 7 | staff_id |
| customer | 200 | 16 | customer_id |
| product | 500 | 13 | product_id |
| payment_term | 2 | 4 | payment_term_id |
| incoterm | 2 | 5 | incoterm_id |
| quotation | 3000 | 9 | quotation_id |
| quotation_item | 2000 | 8 | (quotation_id, product_id) |
| proforma_invoice | 500 | 13 | proforma_invoice_id |
| contract | 600 | 17 | contract_id |
| contract_item | 600 | 8 | (contract_id, product_id) |
| sale_order | 300 | 9 | sale_order_id |
| export_document_set | 300 | 8 | document_set_id |
| **TOTAL** | **8002** | - | - |

---

## 🔄 Model Relationships Summary

### One-to-Many (1:N)
- Staff ➜ Quotation (1 staff has many quotations)
- Customer ➜ Quotation (1 customer has many quotations)
- Quotation ➜ QuotationItem (1 quotation has many items)
- Customer ➜ Contract (1 customer has many contracts)
- Contract ➜ ContractItem (1 contract has many items)
- Contract ➜ SaleOrder (1 contract has many sale orders)
- SaleOrder ➜ ExportDocumentSet (1 sale order has many export docs)

### Many-to-One (N:1)
- Quotation ← Customer
- Quotation ← Staff
- ProformaInvoice ← Quotation
- ProformaInvoice ← PaymentTerm
- ProformaInvoice ← Staff
- Contract ← Customer
- Contract ← Incoterm
- Contract ← ProformaInvoice
- SaleOrder ← Contract
- ExportDocumentSet ← SaleOrder

### Many-to-Many (N:M) via Junction Tables
- Quotation ↔ Product (via QuotationItem)
- Contract ↔ Product (via ContractItem)

---

## 🚀 Current API Status

✅ **Database**: Connected to Oracle GCFood_Project  
✅ **Tables**: All 12 tables created  
✅ **Models**: All 12 SQLAlchemy models defined  
✅ **Server**: Running at http://localhost:8000  
✅ **Documentation**: Available at http://localhost:8000/docs  

---

## 📁 File Structure

```
api/models/
├── __init__.py                    (BaseModel + model imports)
├── staff.py
├── customer.py
├── product.py
├── payment_term.py
├── incoterm.py
├── quotation.py
├── quotation_item.py              ⭐ Composite PK
├── proforma_invoice.py
├── contract.py
├── contract_item.py               ⭐ Composite PK
├── sale_order.py
└── export_document_set.py

schemas/
├── __init__.py
├── staff_schema.py                (Pydantic schemas)
├── customer_schema.py
├── ... (other schema files)
└── (Already exist - no conflict!)
```

---

## 🎯 Next Step

Create **FastAPI Routers** for CRUD operations:
- [x] Models defined
- [ ] Routers (Customer, Product, Quotation, etc.)
- [ ] Services (Business logic)
- [ ] Endpoints tested in Swagger UI
- [ ] Frontend integration

---

**Created**: 2025-01-09  
**Author**: AI Assistant  
**Status**: ✅ COMPLETE
