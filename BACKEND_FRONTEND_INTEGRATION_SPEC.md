# Complete Backend-Frontend Integration Technical Specification

**Project**: Financial Data Platform - TS Sales Module  
**Document Version**: 1.0  
**Date**: April 9, 2026  
**Status**: Analysis Complete - Ready for Implementation

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Backend Architecture Analysis](#backend-architecture-analysis)
3. [Frontend Architecture Analysis](#frontend-architecture-analysis)
4. [Data Structure Mapping](#data-structure-mapping)
5. [API Endpoints Inventory](#api-endpoints-inventory)
6. [Missing Implementations](#missing-implementations)
7. [Data Flow Diagrams](#data-flow-diagrams)
8. [Implementation Priorities](#implementation-priorities)
9. [Step-by-Step Implementation Plan](#step-by-step-implementation-plan)
10. [Code Examples & Integration Patterns](#code-examples--integration-patterns)

---

## Executive Summary

### Current State
- **Backend**: Partially implemented FastAPI with 5 core modules (Customer, Quotation, Proforma Invoice, Contract, Sale Order)
- **Frontend**: React/Next.js with complete UI dashboards but **zero API integration** - all data is mocked
- **Database**: Oracle with models defined but incomplete repositories and services

### Critical Findings
1. **API Endpoints**: Only 8 endpoints implemented (mostly read-only)
2. **Missing functionality**: No UPDATE, DELETE, or BULK operations
3. **Frontend-Backend Disconnect**: Complete - frontend uses mock data with placeholder hooks
4. **Missing Master Data Endpoints**: No endpoints for Customers, Products, Payment Terms, Incoterms, Staff
5. **Missing CRUD Operations**: Update/Delete not implemented for any entity

### Effort Estimate
- **Backend Enhancements**: 15-20 hours
- **Frontend Integration**: 25-30 hours
- **Testing & Integration**: 10-15 hours
- **Total**: 50-65 hours (2 weeks with 1 developer)

---

## Backend Architecture Analysis

### Current Technology Stack
- **Framework**: FastAPI with SQLAlchemy ORM
- **Database**: Oracle Database
- **Authentication**: Placeholder (token-based in API client config)
- **CORS**: Not explicitly configured

### Database Connection
```python
# Location: HD_API/api/database.py
SQLALCHEMY_DATABASE_URL = f"oracle+oracledb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/?service_name={DB_SERVICE}"
```

### Core Models (Implemented)

#### 1. **Customer Model**
```python
# table: customer
- customer_id (PK): String(50)
- customer_type_id (FK): String(50)
- customer_code: String(50)
- company_name: String(200)
- short_name: String(100)
- tax_id: String(100)
- country: String(100)
- city: String(100)
- address: String(300)
- phone: String(50)
- email: String(200)
- website: String(200)
- industry: String(200)
- status: String(50)
- preferred_currency: String(50)
```

#### 2. **Product Model**
```python
# table: product
- product_id (PK): String(50)
- product_type_id (FK): String(50)
- name: String(200)
- description: String(500)
- price: Float
- application: String(200)
- brix: String(50)
- size: String(50)
- solid: Float
- ph: Float
- is_active: Integer

# Related Tables:
- ingredient_product_detail (Many-to-Many)
- product_specification
```

#### 3. **Quotation Model**
```python
# table: quotation
- quotation_id (PK): String(50)
- customer_id (FK): String(50)
- staff_id (FK): String(50)
- quotation_date: Date
- expiry_date: Date
- incoterm_id (FK): String(50)
- payment_term_id (FK): String(50)

# Related Table: quotation_item
- quotation_id, product_id (Composite PK)
- quantity: Float
- unit_price: Float
```

#### 4. **Proforma Invoice Model**
```python
# table: proforma_invoice
- proforma_invoice_id (PK): String(50)
- quotation_id (FK): String(50) [REQUIRED]
- payment_term_id (FK): String(50)
- bank_id (FK): String(50)
- staff_id (FK): String(50)
- total_contract_value: Float
- port_of_loading: String(100)
- port_of_discharge: String(100)
- delivery_time: Date
- file_path: String(500)
```

#### 5. **Contract Model**
```python
# table: contract
- contract_id (PK): String(50)
- customer_id (FK): String(50)
- payment_term_id (FK): String(50)
- proforma_invoice_id (FK): String(50)
- staff_id (FK): String(50)
- contract_type_id (FK): String(50)
- incoterm_id (FK): String(50)
- contract_date: Date
- effective_date: Date
- expiry_date: Date
- total_value: Float
- loading_port: String(100)
- destination_port: String(100)
- currency: String(50)
- total_contract_value: Float
- total_quantity: Float
- status: String(50)
- signed_date: Date
```

#### 6. **Sale Order Model**
```python
# table: sale_order
- sale_order_id (PK): String(50)
- contract_id (FK): String(50)
- order_date: Date
- delivery_date: Date
- total_amount: Float
```

#### 7. **Master Data Models** (Reference Tables)
- `payment_term`: payment_term_id, description, (number_of_days in frontend)
- `incoterm`: incoterm_id, name, description
- `customer_type`: customer_type_id, name
- `contract_type`: contract_type_id, name
- `staff`: staff_id, name, role, email, phone
- `product_type`: product_type_id, name
- `bank`: bank_id, bank_name

### Implemented API Endpoints

#### Customer Routes
| Method | Endpoint | Input | Output | Status |
|--------|----------|-------|--------|--------|
| POST | `/customers/` | CustomerCreate | CustomerResponse | ✓ Implemented |
| GET | `/customers/` | - | List[CustomerResponse] | ✓ Implemented |
| GET | `/customers/{customer_id}` | customer_id | CustomerResponse | ✓ Implemented |
| PUT | `/customers/{customer_id}` | CustomerUpdate | CustomerResponse | **❌ MISSING** |
| DELETE | `/customers/{customer_id}` | customer_id | - | **❌ MISSING** |

#### Quotation Routes
| Method | Endpoint | Input | Output | Status |
|--------|----------|-------|--------|--------|
| POST | `/quotations/` | QuotationCreate | QuotationResponse | ✓ Implemented |
| GET | `/quotations/{quotation_id}` | quotation_id | QuotationResponse | ✓ Implemented |
| GET | `/quotations/` | - | List[QuotationResponse] | **❌ MISSING** |
| PUT | `/quotations/{quotation_id}` | QuotationUpdate | QuotationResponse | **❌ MISSING** |
| DELETE | `/quotations/{quotation_id}` | quotation_id | - | **❌ MISSING** |

#### Proforma Invoice Routes
| Method | Endpoint | Input | Output | Status |
|--------|----------|-------|--------|--------|
| POST | `/proforma/` | ProformaCreate | ProformaResponse | ✓ Implemented |
| GET | `/proforma/{proforma_id}` | proforma_id | ProformaResponse | **❌ MISSING** |
| GET | `/proforma/` | - | List[ProformaResponse] | **❌ MISSING** |
| GET | `/proforma/quotation/{quotation_id}` | quotation_id | ProformaResponse | **❌ MISSING** |
| PUT | `/proforma/{proforma_id}` | ProformaUpdate | ProformaResponse | **❌ MISSING** |
| DELETE | `/proforma/{proforma_id}` | proforma_id | - | **❌ MISSING** |

#### Contract Routes
| Method | Endpoint | Input | Output | Status |
|--------|----------|-------|--------|--------|
| POST | `/contracts/` | ContractCreate | ContractResponse | ✓ Implemented |
| GET | `/contracts/{contract_id}` | contract_id | ContractResponse | **❌ MISSING** |
| GET | `/contracts/` | - | List[ContractResponse] | **❌ MISSING** |
| GET | `/contracts/customer/{customer_id}` | customer_id | List[ContractResponse] | **❌ MISSING** |
| PUT | `/contracts/{contract_id}` | ContractUpdate | ContractResponse | **❌ MISSING** |
| DELETE | `/contracts/{contract_id}` | contract_id | - | **❌ MISSING** |

#### Sale Order Routes
| Method | Endpoint | Input | Output | Status |
|--------|----------|-------|--------|--------|
| POST | `/sale-orders/` | SaleOrderCreate | SaleOrderResponse | ✓ Implemented |
| GET | `/sale-orders/{sale_order_id}` | sale_order_id | SaleOrderResponse | **❌ MISSING** |
| GET | `/sale-orders/` | - | List[SaleOrderResponse] | **❌ MISSING** |
| GET | `/sale-orders/contract/{contract_id}` | contract_id | List[SaleOrderResponse] | **❌ MISSING** |
| PUT | `/sale-orders/{sale_order_id}` | SaleOrderUpdate | SaleOrderResponse | **❌ MISSING** |
| DELETE | `/sale-orders/{sale_order_id}` | sale_order_id | - | **❌ MISSING** |

#### Master Data Routes (NOT IMPLEMENTED)
| Resource | GET List | GET Detail | CREATE | UPDATE | DELETE | Status |
|----------|----------|-----------|--------|--------|--------|--------|
| Customers | ✓ | ✓ | ✓ | ❌ | ❌ | Partial |
| Products | ❌ | ❌ | ❌ | ❌ | ❌ | **MISSING** |
| Payment Terms | ❌ | ❌ | ❌ | ❌ | ❌ | **MISSING** |
| Incoterms | ❌ | ❌ | ❌ | ❌ | ❌ | **MISSING** |
| Staff | ❌ | ❌ | ❌ | ❌ | ❌ | **MISSING** |
| Certifications | ❌ | ❌ | ❌ | ❌ | ❌ | **MISSING** |
| Packaging Specs | ❌ | ❌ | ❌ | ❌ | ❌ | **MISSING** |

### Service Layer Analysis

**Service Classes Located**: `HD_API/api/services/`
- ✓ `quotation_service.py` - Partial implementation (has bug: `items.apiend` typo)
- ✓ `customer_service.py` - Complete CRUD
- ✓ `proforma_service.py` - Create only
- ✓ `contract_service.py` - Create only
- ✓ `sale_order_service.py` - Create only

**Issues Found**:
1. **Quotation Service Bug**: Line in quotation_service.py has `items.apiend()` instead of `items.append()`
2. **Transaction Management**: Inconsistent commit patterns (quotation_service manually commits, others rely on repository)
3. **Missing Validation**: No comprehensive input validation
4. **Error Handling**: Basic try-catch but not consistent

### Repository Layer Analysis

**Repository Classes Located**: `HD_API/api/repositories/`
- ✓ Customer Repository - Full CRUD + get_all
- ✓ Quotation Repository - Basic CRUD
- ✓ Proforma Repository - Basic CRUD + custom get_by_quotation
- ✓ Contract Repository - Basic CRUD + get_by_customer
- ✓ Sale Order Repository - Basic CRUD + get_by_contract

### Missing Repositories
- Product Repository
- Master Data Repositories (Staff, PaymentTerm, Incoterm)
- Payment Repository
- Shipment Repository

---

## Frontend Architecture Analysis

### Current Technology Stack
- **Framework**: Next.js 14 with TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Local React State (useState)
- **API Client**: Axios with interceptors
- **Mocking**: Mock data in model files

### Project Structure
```
TS_Sales/frontend/src/
├── core/
│   ├── services/
│   │   ├── api-client.ts       (✓ Configured)
│   │   └── types.ts             (✓ Comprehensive type definitions)
│   ├── components/
│   ├── layouts/
│   └── utils/
├── modules/
│   ├── customer/
│   ├── quotation/               (Available: views, models, controllers)
│   ├── sale_order/              (Available: views, models, controllers)
│   ├── proforma_invoice/        (Available: views, models, controllers)
│   ├── contract/                (Available: views, models, controllers)
│   ├── export_document/
│   ├── master_data/             (Available: models, controllers)
│   └── oracle_execution/
└── app/
```

### Frontend TypeScript Type Definitions (Comprehensive)

#### Staff Type
```typescript
interface Staff {
  staff_id: number;
  name: string;
  role: string;
  email: string;
  phone: string;
  department: string;
  status: 'ACTIVE' | 'INACTIVE' | 'TERMINATED' | 'FIRED';
}
```

#### Customer Type
```typescript
interface Customer {
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
```

#### Product Type
```typescript
interface Product {
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
```

#### Quotation Type
```typescript
interface Quotation {
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

interface QuotationItem {
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
```

#### ProformaInvoice Type
```typescript
interface ProformaInvoice {
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
```

#### Contract Type
```typescript
interface Contract {
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
```

#### SaleOrder Type
```typescript
interface SaleOrder {
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
```

### Implemented Frontend Hooks (Empty/Stubbed)

| Hook | Location | Implementation Status |
|------|----------|----------------------|
| `useQuotation()` | quotation/controllers/useQuotation.ts | **❌ STUBBED** - Empty functions |
| `useSaleOrder()` | sale_order/controllers/useSaleOrder.ts | **❌ STUBBED** - Returns empty object |
| `useProformaInvoice()` | proforma_invoice/controllers/useProformaInvoice.ts | **❌ STUBBED** - Returns empty object |
| `useContract()` | contract/controllers/useContract.ts | **❌ STUBBED** - Returns empty object |
| `useMasterData()` | master_data/controllers/useMasterData.ts | **❌ STUBBED** - Empty implementation |

### Mock Data Available

**Location**: `src/modules/*/models/mock-data.ts`

#### Quotation Mock Data
```typescript
mockQuotations: [
  {
    quotation_id: 1,
    customer_id: 1,
    staff_id: 1,
    quotation_date: '2025-01-10',
    expiry_date: '2025-02-10',
    total_amount: 50000,
    currency: 'USD',
    status: 'Draft',
  },
  // ... more items
]

mockQuotationItems: [
  {
    quotation_id: 1,
    product_id: 1,
    quantity: 100,
    unit_price: 250,
    discount: 0,
    tax_rate: 10,
    total_price: 27500,
    specifications: { brix: 12.5, ph: 4.5, mesh_size: 'Medium' }
  },
  // ... more items
]
```

#### Master Data Mock
```typescript
mockCustomers: [
  {
    customer_id: 1,
    company_name: 'Osaka Foods Co., Ltd',
    customer_type: 'B2B',
    // ... more fields
  },
]

mockStaff: [
  { staff_id: 1, name: 'Nguyễn Văn A', role: 'Sales Manager', ... },
]

mockProducts: [
  { product_id: 1, name: 'Nha đam cắt hạt lựu', price: 250, ... },
]

mockPaymentTerms: [
  { payment_term_id: 1, description: 'Net 30', number_of_days: 30 },
]

mockIncoterms: [
  { incoterm_id: 1, name: 'FOB', description: 'Free on Board' },
]
```

### Dashboard Views (All Using Mock Data)

| Dashboard | Component | Location | Features |
|-----------|-----------|----------|----------|
| Quotation | QuotationDashboard.tsx | quotation/views/ | List, View, Create, KPI Cards |
| Sale Order | SaleOrderDashboard.tsx | sale_order/views/ | List, View, Create, Filters |
| Proforma | ProformaInvoiceDashboard.tsx | proforma_invoice/views/ | List, View, Create, Filters |
| Contract | ContractDashboard.tsx | contract/views/ | List, View, Create, Filters |

---

## Data Structure Mapping

### Frontend Model vs Backend Schema Comparison

#### Customer
| Frontend Type | Backend Schema | Backend Model | Status |
|--------------|---|---|---|
| customer_id | customer_id (String(50)) | customer_id | ✓ Match |
| company_name | company_name | company_name | ✓ Match |
| customer_type (String) | customer_type_id (FK) | customer_type_id | ⚠️ Field mismatch - FE expects type name, BE stores ID |
| preferred_currency | preferred_currency | preferred_currency | ✓ Match |
| status | status | status | ✓ Match (Enums differ) |
| email | email | email | ✓ Match |
| address | address | address | ✓ Match |

**Mismatch Issues**:
- `customer_type`: Frontend expects enum string ('B2B'), backend stores foreign key
- Status values: Frontend uses 'ACTIVE', 'INACTIVE'; Backend uses different strings

#### Quotation
| Frontend Type | Backend Schema | Status |
|--|--|--|
| quotation_id (number) | quotation_id (String(50)) | ⚠️ Type mismatch: FE-number, BE-string |
| customer_id | customer_id | ✓ Match |
| staff_id | staff_id | ✓ Match |
| quotation_date (YYYY-MM-DD) | quotation_date (Date) | ✓ Match |
| status | NOT IN MODEL | ❌ MISSING in DB |
| currency | NOT IN MODEL | ❌ MISSING in DB |
| items (array) | quotation_item table | ✓ Match structure |

**Critical Issue**: Backend Quotation model is missing:
- `currency` column
- `status` column
- `total_amount` column

#### Proforma Invoice
| Frontend Type | Backend Schema | Status |
|--|--|--|
| proforma_invoice_id | proforma_invoice_id | ✓ Match |
| quotation_id | quotation_id | ✓ Match |
| payment_term_id | payment_term_id | ✓ Match |
| total_contract_value | total_contract_value | ✓ Match |
| port_of_loading | port_of_loading | ✓ Match |
| port_of_discharge | port_of_discharge | ✓ Match |
| delivery_time | delivery_time | ✓ Match |
| status | NOT IN MODEL | ❌ MISSING |
| file_path | file_path | ✓ Match |

#### Contract
| Frontend Type | Backend Schema | Status |
|--|--|--|
| contract_id | contract_id | ✓ Match |
| customer_id | customer_id | ✓ Match |
| contract_type (string) | contract_type_id (FK) | ⚠️ Type mismatch |
| proforma_invoice_id | proforma_invoice_id | ✓ Match |
| total_contract_value | total_contract_value | ✓ Match |
| loading_port | loading_port | ✓ Match |
| destination_port | destination_port | ✓ Match |
| status | status | ✓ Match |
| items (array) | NOT MODELED | ❌ MISSING |

**Issue**: Contract doesn't have contract_items table in backend

#### Sale Order
| Frontend Type | Backend Schema | Status |
|--|--|--|
| sale_order_id | sale_order_id | ✓ Match |
| contract_id | contract_id | ✓ Match |
| order_date | order_date | ✓ Match |
| delivery_date | delivery_date | ✓ Match |
| total_amount | total_amount | ✓ Match |
| status | NOT IN MODEL | ❌ MISSING |

### ID Type Inconsistency
- **Backend**: All IDs are `String(50)`
- **Frontend TypeScript**: All IDs are `number`
- **Impact**: Type conversions needed in API client

---

## API Endpoints Inventory

### Complete Backend API Endpoints

#### ✓ EXISTING ENDPOINTS

**Customer Management**
```
POST   /customers/
  Request: {customer_id, customer_type_id, customer_code, company_name, ...}
  Response: {customer_id, customer_type_id, customer_code, company_name, ...}
  
GET    /customers/
  Response: List of Customers
  
GET    /customers/{customer_id}
  Response: Customer details
```

**Quotation Management**
```
POST   /quotations/
  Request: {quotation_id, customer_id, staff_id, quotation_date, expiry_date, ...}
  Response: QuotationResponse
  
GET    /quotations/{quotation_id}
  Response: Quotation details
```

**Proforma Invoice Management**
```
POST   /proforma/
  Request: {quotation_id, payment_term_id, bank_id, staff_id, ...}
  Response: ProformaResponse
```

**Contract Management**
```
POST   /contracts/
  Request: {contract_id, customer_id, payment_term_id, proforma_invoice_id, ...}
  Response: ContractResponse
```

**Sale Order Management**
```
POST   /sale-orders/
  Request: {sale_order_id, contract_id, order_date, delivery_date, total_amount}
  Response: SaleOrderResponse
```

**System**
```
GET    /
  Response: {message, status, docs}
  
GET    /health-check
  Response: {database_status, oracle_response}
```

---

### ❌ MISSING ENDPOINTS (CRITICAL)

#### Priority 1: Core CRUD Operations

**Customer Management**
```
PUT    /customers/{customer_id}           - Update customer
DELETE /customers/{customer_id}           - Delete customer
GET    /customers/?status=ACTIVE          - Filter by status
GET    /customers/?search=...             - Search by name/code
```

**Quotation Management**
```
GET    /quotations/                       - List all quotations
  Optional: ?status=Draft&customer_id=123&date_from=2025-01-01
PUT    /quotations/{quotation_id}         - Update quotation
DELETE /quotations/{quotation_id}         - Delete quotation
GET    /quotations/{quotation_id}/items   - Get line items
POST   /quotations/{quotation_id}/items   - Add line items
PUT    /quotations/{quotation_id}/items/{product_id} - Update line item
DELETE /quotations/{quotation_id}/items/{product_id} - Remove line item
```

**Proforma Invoice Management**
```
GET    /proforma/                         - List all proformas
GET    /proforma/{proforma_id}            - Get details
GET    /proforma/quotation/{quotation_id} - Get by quotation
PUT    /proforma/{proforma_id}            - Update proforma
DELETE /proforma/{proforma_id}            - Delete proforma
POST   /proforma/{proforma_id}/upload     - Upload file
```

**Contract Management**
```
GET    /contracts/                        - List all contracts
  Optional: ?status=Active&customer_id=123
GET    /contracts/{contract_id}           - Get details
GET    /contracts/customer/{customer_id}  - Get all by customer
PUT    /contracts/{contract_id}           - Update contract
DELETE /contracts/{contract_id}           - Delete contract
GET    /contracts/{contract_id}/items     - Get line items
POST   /contracts/{contract_id}/items     - Add line items
```

**Sale Order Management**
```
GET    /sale-orders/                      - List all orders
  Optional: ?contract_id=123&status=Confirmed
GET    /sale-orders/{sale_order_id}       - Get details
GET    /sale-orders/contract/{contract_id} - Get all by contract
PUT    /sale-orders/{sale_order_id}       - Update order
DELETE /sale-orders/{sale_order_id}       - Delete order
```

#### Priority 2: Master Data Endpoints (NEW ROUTERS NEEDED)

**Products**
```
GET    /products/                         - List all products
GET    /products/{product_id}             - Get product details
POST   /products/                         - Create product
PUT    /products/{product_id}             - Update product
DELETE /products/{product_id}             - Delete product
GET    /products/?type=Juice&active=true  - Filter products
```

**Payment Terms**
```
GET    /payment-terms/                    - List all payment terms
GET    /payment-terms/{payment_term_id}   - Get details
POST   /payment-terms/                    - Create payment term
PUT    /payment-terms/{payment_term_id}   - Update payment term
DELETE /payment-terms/{payment_term_id}   - Delete payment term
```

**Incoterms**
```
GET    /incoterms/                        - List all incoterms
GET    /incoterms/{incoterm_id}           - Get details
POST   /incoterms/                        - Create incoterm
PUT    /incoterms/{incoterm_id}           - Update incoterm
DELETE /incoterms/{incoterm_id}           - Delete incoterm
```

**Staff**
```
GET    /staff/                            - List all staff
GET    /staff/{staff_id}                  - Get staff details
POST   /staff/                            - Create staff
PUT    /staff/{staff_id}                  - Update staff
DELETE /staff/{staff_id}                  - Delete staff
GET    /staff/?department=Sales           - Filter by department
```

**Reference Data** (Certifications, Packaging, Customer Types, etc.)
```
GET    /certifications/                   - List certifications
GET    /packaging-specs/                  - List packaging specs
GET    /customer-types/                   - List customer types
GET    /contract-types/                   - List contract types
GET    /banks/                            - List banks
```

#### Priority 3: Advanced Features

**Batch Operations**
```
POST   /quotations/bulk-create            - Create multiple quotations
PUT    /quotations/bulk-update            - Update multiple quotations
DELETE /quotations/bulk-delete            - Delete multiple quotations
```

**Workflow Transitions**
```
POST   /quotations/{id}/send              - Transition to "Sent" status
POST   /quotations/{id}/convert-proforma  - Convert quotation → proforma
POST   /contracts/{id}/sign               - Mark contract as signed
POST   /contracts/{id}/activate           - Activate contract
```

**Reports & Analytics**
```
GET    /quotations/report/summary         - Quotation summary stats
GET    /quotations/report/by-status       - Quotations grouped by status
GET    /sales/report/by-customer          - Sales by customer
GET    /sales/report/by-product           - Sales by product
GET    /contracts/report/revenue          - Contract revenue analysis
```

---

## Missing Implementations

### Backend Deficiencies (Summary)

| Category | Item | Impact | Priority |
|----------|------|--------|----------|
| **Models** | Quotation missing: currency, status, total_amount | HIGH | P0 |
| **Models** | ProformaInvoice missing: status field | MEDIUM | P1 |
| **Models** | Sale Order missing: status field | MEDIUM | P1 |
| **Models** | Contract Items not modeled | HIGH | P0 |
| **Routers** | No Product router | HIGH | P0 |
| **Routers** | No Master Data routers | HIGH | P0 |
| **Services** | quotation_service bug (items.apiend → items.append) | CRITICAL | P0 |
| **Services** | All services missing UPDATE logic | HIGH | P0 |
| **Services** | All services missing DELETE logic | HIGH | P0 |
| **Repositories** | No Product repository | HIGH | P0 |
| **Repositories** | No Master Data repositories | HIGH | P0 |
| **Repositories** | Missing bulk operations | MEDIUM | P1 |
| **Schemas** | No Update schemas defined | HIGH | P0 |
| **Documentation** | No API documentation/Swagger | LOW | P2 |
| **Authentication** | Not implemented | MEDIUM | P1 |
| **CORS** | Not configured | HIGH | P0 |

### Frontend Deficiencies (Summary)

| Category | Item | Impact | Priority |
|----------|------|--------|----------|
| **Hooks** | All hooks are stubbed/empty | CRITICAL | P0 |
| **Services** | No API service calls implemented | CRITICAL | P0 |
| **Types** | ID type mismatch (String vs number) | MEDIUM | P1 |
| **Master Data** | No fetching of master data from API | HIGH | P0 |
| **State Management** | Only useState, no global state | MEDIUM | P1 |
| **Forms** | No form integration with backend | CRITICAL | P0 |
| **Error Handling** | No error handling UI | MEDIUM | P1 |
| **Loading States** | No loading states in components | MEDIUM | P1 |
| **Validation** | No form validation | MEDIUM | P1 |
| **Pagination** | Not implemented | LOW | P2 |

---

## Data Flow Diagrams

### Current State: Mock-Based Flow (Frontend Only)
```
User Action → Component → Mock Data → Render → UI Update
(No Backend Involved)
```

### Target State: Full Integration Flow
```
User Action 
  ↓
Component (e.g., QuotationDashboard)
  ↓
Hook (e.g., useQuotation.fetchQuotations())
  ↓
Service Call (apiClient.get('/quotations/'))
  ↓
Backend API Route (/quotations/)
  ↓
Service Layer (quotation_service.get_all_quotations())
  ↓
Repository Layer (quotation_repository.get_all())
  ↓
Database Query (SELECT * FROM quotation)
  ↓
Response: QuotationResponse[]
  ↓
Hook State Update (setQuotations)
  ↓
Component Re-render
  ↓
UI Update with Real Data
```

### Business Process Flow: Quotation → Proforma → Contract → Sale Order

```
┌─────────────────┐
│ Create Quotation│
└────────┬────────┘
         │
         ▼
    ┌───────────┐
    │ Quotation │ ← API: POST /quotations
    │ Created   │   Model: Quotation + QuotationItems
    └─────┬─────┘
          │
          ▼
    [Customer Reviews]
          │
          ├─ Interested → Quotation.status = "Interested"
          ├─ Request Sampling → Quotation.status = "Sampling"
          └─ Won → Quotation.status = "Won"
                        │
                        ▼
        ┌───────────────────────────┐
        │ Create Proforma Invoice   │ ← API: POST /proforma
        │ (from Quotation)          │   Requires: quotation_id
        └──────────┬────────────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │ Proforma Invoice     │
        │ Ready for Customer   │
        └──────────┬───────────┘
                   │
        [Customer Accepts]
                   │
                   ▼
        ┌──────────────────────┐
        │ Create Contract      │ ← API: POST /contracts
        │ (from Proforma)      │   Requires: proforma_invoice_id
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │ Contract Active      │
        │ (Ready to Ship)      │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │ Create Sale Order    │ ← API: POST /sale-orders
        │ (Release Stock)      │   Requires: contract_id
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │ Sale Order Ready     │
        │ for Fulfillment      │
        └──────────────────────┘
```

### Master Data Dependency Graph
```
┌─────────────────────────────────┐
│   Master Reference Data         │
├─────────────────────────────────┤
│ • Customer Types                │
│ • Contract Types                │
│ • Payment Terms                 │
│ • Incoterms                     │
│ • Banks                         │
│ • Staff Resources               │
│ • Product Catalog               │
│   - Product Types               │
│   - Packaging Specs             │
│   - Certifications              │
│   - Quality Assurance           │
└────────┬────────────────────────┘
         │ Used by
         ▼
    ┌──────────────────┐
    │ Transaction     │
    │ Documents       │
    │ (Quotation,     │
    │  Proforma,      │
    │  Contract,      │
    │  SaleOrder)     │
    └──────────────────┘
```

---

## Implementation Priorities

### Phase 1: Foundation (Week 1 - Days 1-3)
**Goal**: Fix critical bugs and implement all GET endpoints

#### Backend Tasks
- [ ] Fix quotation_service bug: `items.apiend` → `items.append`
- [ ] Add missing columns to models:
  - Quotation: `currency`, `status`, `total_amount`
  - ProformaInvoice: `status`
  - SaleOrder: `status`
- [ ] Create Contract Items model and table
- [ ] Implement all GET endpoints (list + detail) for:
  - Quotation (with filters)
  - Proforma
  - Contract
  - Sale Order
- [ ] Add CORS configuration
- [ ] Implement master data routers:
  - Products
  - Payment Terms
  - Incoterms
  - Staff
  - Customer Types

#### Frontend Tasks
- [ ] Create constants file for API endpoints
- [ ] Implement useQuotation hook with real API calls
- [ ] Implement useSaleOrder hook
- [ ] Implement useProformaInvoice hook
- [ ] Implement useContract hook
- [ ] Implement useMasterData hook
- [ ] Replace mock data with API calls in QuotationDashboard
- [ ] Add loading and error states

**Effort**: 15 hours

### Phase 2: CRUD Operations (Week 1 - Days 4-5)
**Goal**: Implement full Create, Read, Update, Delete

#### Backend Tasks
- [ ] Create/Update all schemas (Add UpdateRequest variants)
- [ ] Implement PUT endpoints for all entities
- [ ] Implement DELETE endpoints for all entities
- [ ] Implement Quotation Items CRUD endpoints
- [ ] Implement Contract Items CRUD endpoints
- [ ] Add comprehensive error handling
- [ ] Add input validation schemas

#### Frontend Tasks
- [ ] Implement form submissions (create & update)
- [ ] Add form validation
- [ ] Implement delete confirmations
- [ ] Add success/error toast notifications
- [ ] Update all dashboards with real data

**Effort**: 20 hours

### Phase 3: Enhancement (Week 2 - Days 1-2)
**Goal**: Advanced features and polish

#### Backend Tasks
- [ ] Implement filtering and search parameters
- [ ] Implement pagination
- [ ] Implement sorting
- [ ] Add batch operations endpoints
- [ ] Create workflow transition endpoints
- [ ] Add basic reporting endpoints
- [ ] Implement request/response logging

#### Frontend Tasks
- [ ] Add filter UI components
- [ ] Implement pagination
- [ ] Add bulk operations UI
- [ ] Implement workflow action buttons
- [ ] Add data export functionality

**Effort**: 15 hours

### Phase 4: Final Polish (Week 2 - Days 3-5)
**Goal**: Testing, documentation, and deployment

- [ ] Unit tests for services and repositories
- [ ] Integration tests for API endpoints
- [ ] Frontend component tests
- [ ] E2E testing for critical workflows
- [ ] API documentation (Swagger/OpenAPI)
- [ ] User documentation
- [ ] Performance optimization
- [ ] Security review
- [ ] Deployment preparation

**Effort**: 15 hours

---

## Step-by-Step Implementation Plan

### BACKEND IMPLEMENTATION

#### Step 1: Fix Critical Bugs
**File**: `HD_API/api/services/quotation_service.py`
```python
# Line to fix:
# WRONG: items.apiend(QuotationItem(...))
# RIGHT: items.append(QuotationItem(...))
```

#### Step 2: Create Database Migrations (or Alembic)
Add missing columns to existing tables:
```sql
-- Quotation table additions
ALTER TABLE quotation ADD (
  currency VARCHAR2(50) DEFAULT 'USD',
  status VARCHAR2(50) DEFAULT 'Draft',
  total_amount FLOAT
);

-- ProformaInvoice additions
ALTER TABLE proforma_invoice ADD (
  status VARCHAR2(50) DEFAULT 'Draft'
);

-- SaleOrder additions
ALTER TABLE sale_order ADD (
  status VARCHAR2(50) DEFAULT 'Confirmed'
);

-- New ContractItems table
CREATE TABLE contract_item (
  contract_id VARCHAR2(50),
  product_id VARCHAR2(50),
  quantity FLOAT,
  unit_price FLOAT,
  discount FLOAT DEFAULT 0,
  tax_rate FLOAT DEFAULT 0,
  total_price FLOAT,
  PRIMARY KEY (contract_id, product_id),
  FOREIGN KEY (contract_id) REFERENCES contract(contract_id),
  FOREIGN KEY (product_id) REFERENCES product(product_id)
);
```

#### Step 3: Update Python Models
```python
# File: HD_API/api/models/quotation.py
class Quotation(Base):
    __tablename__ = "quotation"
    # ... existing fields ...
    currency = Column(String(50), default='USD')
    status = Column(String(50), default='Draft')
    total_amount = Column(Float)

# File: HD_API/api/models/contract.py
class ContractItem(Base):
    __tablename__ = "contract_item"
    contract_id = Column(String(50), ForeignKey("contract.contract_id"), primary_key=True)
    product_id = Column(String(50), ForeignKey("product.product_id"), primary_key=True)
    quantity = Column(Float)
    unit_price = Column(Float)
    discount = Column(Float, default=0)
    tax_rate = Column(Float, default=0)
    total_price = Column(Float)
```

#### Step 4: Create Update Schemas
```python
# File: HD_API/api/schemas/quotation.py
class QuotationUpdate(BaseModel):
    customer_id: Optional[str] = None
    staff_id: Optional[str] = None
    quotation_date: Optional[date] = None
    expiry_date: Optional[date] = None
    incoterm_id: Optional[str] = None
    payment_term_id: Optional[str] = None
    currency: Optional[str] = None
    status: Optional[str] = None
    total_amount: Optional[float] = None

# Similar for Contract, SaleOrder, Proforma, etc.
```

#### Step 5: Extend Repositories with Update/Delete Methods
```python
# File: HD_API/api/repositories/quotation_repository.py
def update_quotation(db: Session, quotation_id: str, quotation_data: dict):
    quotation = db.query(Quotation).filter(
        Quotation.quotation_id == quotation_id
    ).first()
    if quotation:
        for key, value in quotation_data.items():
            setattr(quotation, key, value)
        db.commit()
        db.refresh(quotation)
    return quotation

def delete_quotation(db: Session, quotation_id: str):
    quotation = db.query(Quotation).filter(
        Quotation.quotation_id == quotation_id
    ).first()
    if quotation:
        db.delete(quotation)
        db.commit()
    return quotation
```

#### Step 6: Implement Master Data Repositories and Services
```python
# File: HD_API/api/repositories/product_repository.py
from sqlalchemy.orm import Session
from api.models.product import Product

def create_product(db: Session, product: Product):
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def get_product_by_id(db: Session, product_id: str):
    return db.query(Product).filter(Product.product_id == product_id).first()

def get_all_products(db: Session):
    return db.query(Product).all()

def update_product(db: Session, product_id: str, product_data: dict):
    product = get_product_by_id(db, product_id)
    if product:
        for key, value in product_data.items():
            setattr(product, key, value)
        db.commit()
        db.refresh(product)
    return product

def delete_product(db: Session, product_id: str):
    product = get_product_by_id(db, product_id)
    if product:
        db.delete(product)
        db.commit()
    return product
```

#### Step 7: Create Master Data Routers
```python
# File: HD_API/api/routers/product_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.dependencies.db import get_db
from api.schemas.product import ProductCreate, ProductResponse
from api.services.product_service import (
    create_product_service,
    get_all_products_service,
    get_product_service,
    update_product_service,
    delete_product_service
)

router = APIRouter(
    prefix="/products",
    tags=["Product"]
)

@router.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product_service(db, product)

@router.get("/", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return get_all_products_service(db)

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: str, db: Session = Depends(get_db)):
    return get_product_service(db, product_id)

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: str, product: ProductUpdate, db: Session = Depends(get_db)):
    return update_product_service(db, product_id, product)

@router.delete("/{product_id}")
def delete_product(product_id: str, db: Session = Depends(get_db)):
    return delete_product_service(db, product_id)
```

#### Step 8: Extend Router with Additional Endpoints
```python
# File: HD_API/api/routers/quotation_router.py - Add these endpoints

@router.get("/", response_model=list[QuotationResponse])
def get_quotations(
    db: Session = Depends(get_db),
    customer_id: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
):
    return get_quotations_service(db, customer_id, status, skip, limit)

@router.put("/{quotation_id}", response_model=QuotationResponse)
def update_quotation(quotation_id: str, quotation: QuotationUpdate, db: Session = Depends(get_db)):
    return update_quotation_service(db, quotation_id, quotation)

@router.delete("/{quotation_id}")
def delete_quotation(quotation_id: str, db: Session = Depends(get_db)):
    return delete_quotation_service(db, quotation_id)
```

#### Step 9: Register New Routers in Main App
```python
# File: HD_API/api/main.py
from api.routers import (
    customer_router,
    quotation_router,
    proforma_router,
    contract_router,
    sale_order_router,
    product_router,        # NEW
    payment_term_router,   # NEW
    incoterm_router,       # NEW
    staff_router,          # NEW
)

# Register all routers
app.include_router(product_router.router)
app.include_router(payment_term_router.router)
app.include_router(incoterm_router.router)
app.include_router(staff_router.router)
```

#### Step 10: Add CORS Configuration
```python
# File: HD_API/api/main.py - Add after FastAPI initialization
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### FRONTEND IMPLEMENTATION

#### Step 1: Create API Service Constants
```typescript
// File: src/core/services/api-endpoints.ts
export const API_ENDPOINTS = {
  // Customer
  CUSTOMERS: '/customers',
  CUSTOMER_DETAIL: (id: string) => `/customers/${id}`,

  // Quotation
  QUOTATIONS: '/quotations',
  QUOTATION_DETAIL: (id: string) => `/quotations/${id}`,
  QUOTATION_ITEMS: (id: string) => `/quotations/${id}/items`,

  // Proforma
  PROFORMAS: '/proforma',
  PROFORMA_DETAIL: (id: string) => `/proforma/${id}`,
  PROFORMA_BY_QUOTATION: (id: string) => `/proforma/quotation/${id}`,

  // Contract
  CONTRACTS: '/contracts',
  CONTRACT_DETAIL: (id: string) => `/contracts/${id}`,
  CONTRACTS_BY_CUSTOMER: (id: string) => `/contracts/customer/${id}`,

  // Sale Order
  SALE_ORDERS: '/sale-orders',
  SALE_ORDER_DETAIL: (id: string) => `/sale-orders/${id}`,
  SALE_ORDERS_BY_CONTRACT: (id: string) => `/sale-orders/contract/${id}`,

  // Master Data
  PRODUCTS: '/products',
  PRODUCT_DETAIL: (id: string) => `/products/${id}`,
  PAYMENT_TERMS: '/payment-terms',
  INCOTERMS: '/incoterms',
  STAFF: '/staff',
};
```

#### Step 2: Create Service Layer
```typescript
// File: src/core/services/quotation-service.ts
import { apiClient } from './api-client';
import { API_ENDPOINTS } from './api-endpoints';
import { Quotation, QuotationCreate, QuotationUpdate } from './types';

export const quotationService = {
  async fetchAllQuotations(filters?: {
    customer_id?: string;
    status?: string;
    skip?: number;
    limit?: number;
  }): Promise<Quotation[]> {
    const response = await apiClient.get(API_ENDPOINTS.QUOTATIONS, { params: filters });
    return response.data;
  },

  async fetchQuotationById(id: string): Promise<Quotation> {
    const response = await apiClient.get(API_ENDPOINTS.QUOTATION_DETAIL(id));
    return response.data;
  },

  async createQuotation(data: QuotationCreate): Promise<Quotation> {
    const response = await apiClient.post(API_ENDPOINTS.QUOTATIONS, data);
    return response.data;
  },

  async updateQuotation(id: string, data: QuotationUpdate): Promise<Quotation> {
    const response = await apiClient.put(API_ENDPOINTS.QUOTATION_DETAIL(id), data);
    return response.data;
  },

  async deleteQuotation(id: string): Promise<void> {
    await apiClient.delete(API_ENDPOINTS.QUOTATION_DETAIL(id));
  },
};

// Similar services for other entities
```

#### Step 3: Implement Hooks with Real API Calls
```typescript
// File: src/modules/quotation/controllers/useQuotation.ts
import { useState, useCallback } from 'react';
import { quotationService } from '@core/services/quotation-service';
import { Quotation, QuotationCreate, QuotationUpdate } from '@core/services/types';

export const useQuotation = () => {
  const [quotations, setQuotations] = useState<Quotation[]>([]);
  const [selectedQuotation, setSelectedQuotation] = useState<Quotation | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchQuotations = useCallback(async (filters?: any) => {
    try {
      setLoading(true);
      setError(null);
      const data = await quotationService.fetchAllQuotations(filters);
      setQuotations(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchQuotationById = useCallback(async (id: string) => {
    try {
      setLoading(true);
      setError(null);
      const data = await quotationService.fetchQuotationById(id);
      setSelectedQuotation(data);
      return data;
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  const createQuotation = useCallback(async (data: QuotationCreate) => {
    try {
      setLoading(true);
      setError(null);
      const newQuotation = await quotationService.createQuotation(data);
      setQuotations([...quotations, newQuotation]);
      return newQuotation;
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [quotations]);

  const updateQuotation = useCallback(async (id: string, data: QuotationUpdate) => {
    try {
      setLoading(true);
      setError(null);
      const updated = await quotationService.updateQuotation(id, data);
      setQuotations(quotations.map(q => q.quotation_id === id ? updated : q));
      if (selectedQuotation?.quotation_id === id) {
        setSelectedQuotation(updated);
      }
      return updated;
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [quotations, selectedQuotation]);

  const deleteQuotation = useCallback(async (id: string) => {
    try {
      setLoading(true);
      setError(null);
      await quotationService.deleteQuotation(id);
      setQuotations(quotations.filter(q => q.quotation_id !== id));
      if (selectedQuotation?.quotation_id === id) {
        setSelectedQuotation(null);
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [quotations, selectedQuotation]);

  return {
    quotations,
    selectedQuotation,
    loading,
    error,
    fetchQuotations,
    fetchQuotationById,
    createQuotation,
    updateQuotation,
    deleteQuotation,
  };
};
```

#### Step 4: Update Dashboard Components
```typescript
// File: src/modules/quotation/views/QuotationDashboard.tsx
'use client';

import { useEffect, useState } from 'react';
import { useQuotation } from '../controllers/useQuotation';
import { Quotation } from '@core/services/types';
import { formatDate, formatCurrency } from '@core/utils/formatters';

export default function QuotationDashboard() {
  const {
    quotations,
    loading,
    error,
    fetchQuotations,
    createQuotation,
    deleteQuotation,
  } = useQuotation();

  const [showForm, setShowForm] = useState(false);
  const [selectedQuotation, setSelectedQuotation] = useState<Quotation | null>(null);

  // Fetch quotations on component mount
  useEffect(() => {
    fetchQuotations();
  }, [fetchQuotations]);

  const handleCreateQuotation = async (formData: any) => {
    try {
      await createQuotation(formData);
      setShowForm(false);
      // Show success toast
    } catch (err) {
      // Show error toast
    }
  };

  const handleDeleteQuotation = async (id: string) => {
    if (!confirm('Are you sure?')) return;
    try {
      await deleteQuotation(id);
      // Show success toast
    } catch (err) {
      // Show error toast
    }
  };

  if (loading && quotations.length === 0) {
    return <div className="p-6">Loading...</div>;
  }

  if (error) {
    return <div className="p-6 text-red-600">Error: {error}</div>;
  }

  const statusColors: Record<string, string> = {
    Draft: 'bg-accent-light text-primary-700',
    Sent: 'bg-primary-50 text-primary-700',
    Interested: 'bg-secondary-50 text-secondary-700',
    Sampling: 'bg-yellow-50 text-yellow-800',
    Closed: 'bg-red-50 text-red-800',
    Won: 'bg-green-50 text-green-800',
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-primary-700 mb-1">📄 Quản lý Báo giá Kỹ thuật</h1>
        <p className="text-gray-600">Tạo, quản lý và theo dõi báo giá kỹ thuật với các thông số Specification</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-5">
        <div className="bg-white rounded-lg border-t-4 p-5 shadow-sm" style={{ borderTopColor: '#546B41' }}>
          <h3 className="text-sm font-semibold text-gray-800">Tổng báo giá</h3>
          <p className="text-3xl font-bold text-primary-700 mt-2">{quotations.length}</p>
        </div>
        <div className="bg-white rounded-lg border-t-4 p-5 shadow-sm" style={{ borderTopColor: '#99AD7A' }}>
          <h3 className="text-sm font-semibold text-gray-800">Đã gửi</h3>
          <p className="text-3xl font-bold text-secondary-700 mt-2">{quotations.filter(q => q.status === 'Sent').length}</p>
        </div>
        <div className="bg-white rounded-lg border-t-4 p-5 shadow-sm" style={{ borderTopColor: '#10b981' }}>
          <h3 className="text-sm font-semibold text-gray-800">Thành công</h3>
          <p className="text-3xl font-bold text-green-700 mt-2">{quotations.filter(q => q.status === 'Won').length}</p>
        </div>
        <div className="bg-white rounded-lg border-t-4 p-5 shadow-sm" style={{ borderTopColor: '#DCCCAC' }}>
          <h3 className="text-sm font-semibold text-gray-800">Tổng giá trị</h3>
          <p className="text-3xl font-bold text-accent-700 mt-2">
            {formatCurrency(quotations.reduce((sum, q) => sum + (q.total_amount || 0), 0), 'USD')}
          </p>
        </div>
      </div>

      {/* Main List */}
      <div className="bg-white rounded-lg shadow p-6 space-y-4 border-l-4 border-primary-700">
        <div className="flex justify-between items-center">
          <h2 className="text-2xl font-bold text-primary-700">Danh sách Báo giá</h2>
          <button
            onClick={() => setShowForm(true)}
            className="bg-primary-700 text-white px-6 py-2 rounded-lg hover:bg-primary-800 font-semibold"
          >
            ➕ Tạo Báo giá
          </button>
        </div>

        {loading ? (
          <div className="text-center py-8">Loading...</div>
        ) : quotations.length === 0 ? (
          <div className="text-center py-8 text-gray-500">No quotations found</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-primary-50 border-b-2 border-primary-200">
                <tr className="text-primary-700">
                  <th className="px-6 py-3 text-left font-semibold">ID</th>
                  <th className="px-6 py-3 text-left font-semibold">Khách hàng</th>
                  <th className="px-6 py-3 text-left font-semibold">Ngày báo giá</th>
                  <th className="px-6 py-3 text-left font-semibold">Tổng giá</th>
                  <th className="px-6 py-3 text-left font-semibold">Trạng thái</th>
                  <th className="px-6 py-3 text-left font-semibold">Hành động</th>
                </tr>
              </thead>
              <tbody>
                {quotations.map((q) => (
                  <tr key={q.quotation_id} className="border-b hover:bg-gray-50">
                    <td className="px-6 py-4 font-mono">#{q.quotation_id}</td>
                    <td className="px-6 py-4">{q.customer_id}</td>
                    <td className="px-6 py-4">{formatDate(q.quotation_date)}</td>
                    <td className="px-6 py-4 font-semibold">{formatCurrency(q.total_amount, q.currency)}</td>
                    <td className="px-6 py-4">
                      <span className={`px-3 py-1 rounded-full text-sm font-semibold ${statusColors[q.status] || 'bg-gray-100'}`}>
                        {q.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 space-x-2">
                      <button
                        onClick={() => setSelectedQuotation(q)}
                        className="text-primary-600 hover:text-primary-800 font-semibold"
                      >
                        Xem
                      </button>
                      <button
                        onClick={() => handleDeleteQuotation(q.quotation_id.toString())}
                        className="text-red-600 hover:text-red-800 font-semibold"
                      >
                        Xóa
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Form Modal */}
      {showForm && (
        <QuotationFormModal onClose={() => setShowForm(false)} onSubmit={handleCreateQuotation} />
      )}

      {/* Detail View */}
      {selectedQuotation && (
        <QuotationDetailModal quotation={selectedQuotation} onClose={() => setSelectedQuotation(null)} />
      )}
    </div>
  );
}
```

---

## Code Examples & Integration Patterns

### Backend: Complete Quotation Service Example (Fixed)
```python
# File: HD_API/api/services/quotation_service.py
from sqlalchemy.orm import Session
from api.models.quotation import Quotation, QuotationItem
from api.repositories import quotation_repository, customer_repository
from api.utils.id_generator import generate_quotation_id
from api.schemas.quotation import QuotationCreate, QuotationUpdate

def create_quotation_service(db: Session, quotation_data: QuotationCreate):
    """Create a new quotation with line items"""
    
    # 1. Validate customer exists
    customer = customer_repository.get_customer_by_id(db, quotation_data.customer_id)
    if not customer:
        raise ValueError(f"Customer {quotation_data.customer_id} not found")
    
    # 2. Generate quotation ID
    quotation_id = generate_quotation_id()
    
    try:
        # 3. Create quotation object
        quotation = Quotation(
            quotation_id=quotation_id,
            customer_id=quotation_data.customer_id,
            staff_id=quotation_data.staff_id,
            quotation_date=quotation_data.quotation_date,
            expiry_date=quotation_data.expiry_date,
            incoterm_id=quotation_data.incoterm_id,
            payment_term_id=quotation_data.payment_term_id,
            currency=quotation_data.currency or 'USD',
            status=quotation_data.status or 'Draft',
            total_amount=quotation_data.total_amount or 0.0
        )
        
        # 4. Save quotation
        quotation_repository.create_quotation(db, quotation)
        
        # 5. Create and save line items if provided
        if quotation_data.items:
            items = []
            for item in quotation_data.items:
                items.append(
                    QuotationItem(
                        quotation_id=quotation_id,
                        product_id=item.product_id,
                        quantity=item.quantity,
                        unit_price=item.unit_price,
                        discount=item.discount or 0,
                        tax_rate=item.tax_rate or 0,
                        total_price=item.total_price or 0
                    )
                )
            quotation_repository.create_quotation_items(db, items)
        
        db.commit()
        db.refresh(quotation)
        
        return quotation
        
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to create quotation: {str(e)}")

def get_quotations_service(db: Session, customer_id: str = None, status: str = None, skip: int = 0, limit: int = 100):
    """Get quotations with optional filtering"""
    query = db.query(Quotation)
    
    if customer_id:
        query = query.filter(Quotation.customer_id == customer_id)
    if status:
        query = query.filter(Quotation.status == status)
    
    return query.offset(skip).limit(limit).all()

def get_quotation_service(db: Session, quotation_id: str):
    """Get single quotation by ID"""
    quotation = quotation_repository.get_quotation_by_id(db, quotation_id)
    if not quotation:
        raise ValueError(f"Quotation {quotation_id} not found")
    return quotation

def update_quotation_service(db: Session, quotation_id: str, quotation_data: QuotationUpdate):
    """Update quotation"""
    quotation = quotation_repository.get_quotation_by_id(db, quotation_id)
    if not quotation:
        raise ValueError(f"Quotation {quotation_id} not found")
    
    try:
        update_data = quotation_data.dict(exclude_unset=True)
        quotation_repository.update_quotation(db, quotation_id, update_data)
        db.refresh(quotation)
        return quotation
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to update quotation: {str(e)}")

def delete_quotation_service(db: Session, quotation_id: str):
    """Delete quotation and its items"""
    quotation = quotation_repository.get_quotation_by_id(db, quotation_id)
    if not quotation:
        raise ValueError(f"Quotation {quotation_id} not found")
    
    try:
        # Delete items first
        db.query(QuotationItem).filter(QuotationItem.quotation_id == quotation_id).delete()
        # Delete quotation
        quotation_repository.delete_quotation(db, quotation_id)
        return {"message": "Quotation deleted successfully"}
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to delete quotation: {str(e)}")
```

### Frontend: Complete Hook Example
```typescript
// File: src/core/services/hooks/useQuotations.ts
import { useState, useCallback, useEffect } from 'react';
import { quotationService } from '../quotation-service';
import { Quotation, QuotationCreate, QuotationUpdate } from '../types';

interface UseQuotationsOptions {
  auto Fetch?: boolean;
  filters?: {
    customer_id?: string;
    status?: string;
  };
}

export const useQuotations = (options: UseQuotationsOptions = {}) => {
  const [quotations, setQuotations] = useState<Quotation[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchQuotations = useCallback(async (filters?: any) => {
    try {
      setLoading(true);
      setError(null);
      const data = await quotationService.fetchAllQuotations(filters);
      setQuotations(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  const createQuotation = useCallback(async (data: QuotationCreate) => {
    try {
      setLoading(true);
      const newQuotation = await quotationService.createQuotation(data);
      setQuotations(prev => [...prev, newQuotation]);
      return newQuotation;
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const updateQuotation = useCallback(async (id: string, data: QuotationUpdate) => {
    try {
      setLoading(true);
      const updated = await quotationService.updateQuotation(id, data);
      setQuotations(prev => prev.map(q => q.quotation_id === id ? updated : q));
      return updated;
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const deleteQuotation = useCallback(async (id: string) => {
    try {
      setLoading(true);
      await quotationService.deleteQuotation(id);
      setQuotations(prev => prev.filter(q => q.quotation_id !== id));
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (options.autoFetch) {
      fetchQuotations(options.filters);
    }
  }, []);

  return {
    quotations,
    loading,
    error,
    fetchQuotations,
    createQuotation,
    updateQuotation,
    deleteQuotation,
  };
};
```

---

## API Request/Response Examples

### Create Quotation

**Request**: `POST /quotations/`
```json
{
  "quotation_id": "QT20250401001",
  "customer_id": "C001",
  "staff_id": "S001",
  "quotation_date": "2025-04-01",
  "expiry_date": "2025-05-01",
  "incoterm_id": "INC001",
  "payment_term_id": "PT001",
  "currency": "USD",
  "status": "Draft",
  "total_amount": 125000.00,
  "items": [
    {
      "quotation_id": "QT20250401001",
      "product_id": "P001",
      "quantity": 100,
      "unit_price": 1000,
      "discount": 5,
      "tax_rate": 10,
      "total_price": 99000
    }
  ]
}
```

**Response**: `200 OK`
```json
{
  "quotation_id": "QT20250401001",
  "customer_id": "C001",
  "staff_id": "S001",
  "quotation_date": "2025-04-01",
  "expiry_date": "2025-05-01",
  "incoterm_id": "INC001",
  "payment_term_id": "PT001",
  "currency": "USD",
  "status": "Draft",
  "total_amount": 125000.00
}
```

### Update Quotation Status

**Request**: `PUT /quotations/QT20250401001`
```json
{
  "status": "Sent",
  "total_amount": 120000.00
}
```

**Response**: `200 OK`
```json
{
  "quotation_id": "QT20250401001",
  "customer_id": "C001",
  "staff_id": "S001",
  "quotation_date": "2025-04-01",
  "expiry_date": "2025-05-01",
  "status": "Sent",
  "total_amount": 120000.00
}
```

---

## Testing Checklist

### Backend Testing
- [ ] All CRUD operations work correctly
- [ ] Validation prevents invalid data
- [ ] Foreign key constraints enforced
- [ ] Filtering and pagination work
- [ ] Error messages are meaningful
- [ ] Database transactions roll back on error

### Frontend Testing
- [ ] Hooks fetch data correctly
- [ ] Forms submit valid data
- [ ] Error messages display
- [ ] Loading states show/hide
- [ ] Delete confirmations work
- [ ] Navigation between modules works
- [ ] Responsive design on mobile

### Integration Testing
- [ ] End-to-end quotation creation workflow
- [ ] Quotation to Proforma conversion
- [ ] Proforma to Contract conversion
- [ ] Contract to Sale Order creation
- [ ] Filter/search functionality
- [ ] Concurrent user updates

---

## Deployment Checklist

- [ ] Environment variables configured (DB credentials, API base URL)
- [ ] Database migrations executed
- [ ] Backend tests passing (>80% coverage)
- [ ] Frontend tests passing
- [ ] E2E tests passing for critical workflows
- [ ] API documentation (Swagger) generated
- [ ] Performance optimized (query optimization, caching)
- [ ] Security reviewed (SQL injection, XSS, CSRF)
- [ ] Error logging configured
- [ ] Backups tested
- [ ] Deployment runbook created

---

## Performance Considerations

### Database
```python
# Add indexes to frequently queried columns
- quotation.customer_id
- quotation.status
- quotation.quotation_date
- contract.customer_id
- contract.status
- sale_order.contract_id
```

### Frontend
```typescript
// Implement pagination for large lists
const ITEMS_PER_PAGE = 20;

// Implement caching
const quotationCache = new Map();

// Debounce search
const debouncedSearch = debounce(searchQuotations, 300);

// Lazy load components
const QuotationDetailModal = lazy(() => import('./QuotationDetailModal'));
```

---

## Success Metrics

| Metric | Target | Current |
|--------|--------|---------|
| API Endpoints | 50+ | 8 |
| Test Coverage | >80% | 0% |
| Frontend-Backend Integration | 100% | 0% |
| Average API Response Time | <200ms | N/A |
| Load Time (3G) | <3s | N/A |
| User Ability to Complete Quotation Workflow | 100% | 0% |

---

**Document End**

**Next Steps**: 
1. Review this specification with the team
2. Split work into sprints based on priorities
3. Begin Phase 1 implementation
4. Set up CI/CD pipeline for automated testing
5. Schedule daily standups for progress tracking

