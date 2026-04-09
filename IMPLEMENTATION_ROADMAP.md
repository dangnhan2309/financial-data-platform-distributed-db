# Implementation Roadmap & Task Tracker

## 🗺️ Implementation Timeline

```
WEEK 1: Foundation & Core CRUD
├── Day 1: Initial Setup & Bug Fixes
│   ├── Fix quotation_service bug (1h)
│   ├── Add CORS configuration (30m)
│   ├── Create update/delete schemas (2h)
│   └── Setup frontend API constants (1h)
│
├── Day 2-3: Backend Core Endpoints
│   ├── Add missing DB columns & commit migrations (2h)
│   ├── Implement all GET endpoints (6h)
│   ├── Implement PUT/DELETE methods in services (4h)
│   └── Create master data routers (4h)
│
└── Day 4-5: Frontend Integration
    ├── Implement all hooks (5h)
    ├── Replace mock data with API calls (4h)
    ├── Add form handlers (3h)
    └── Testing & debugging (3h)

WEEK 2: Enhancement & Polish
├── Day 1-2: Advanced Features
│   ├── Filtering & search (3h)
│   ├── Pagination (2h)
│   ├── Batch operations (2h)
│   └── Workflow transitions (2h)
│
├── Day 3-4: Testing & Documentation
│   ├── Unit tests (4h)
│   ├── Integration tests (3h)
│   ├── API documentation (2h)
│   └── User documentation (2h)
│
└── Day 5: Deployment & Handoff
    ├── Environment setup (1h)
    ├── Performance optimization (2h)
    ├── Security review (1h)
    └── Deployment (1h)
```

---

## 📋 Detailed Task List

### PHASE 1: CRITICAL BUG FIXES & SETUP (Day 1)

#### Backend Setup Tasks
- [ ] **CRITICAL**: Fix quotation_service.py line bug
  - Location: `HD_API/api/services/quotation_service.py`
  - Change: `items.apiend()` → `items.append()`
  - Time: 15 minutes
  
- [ ] **CRITICAL**: Add CORS middleware
  - Location: `HD_API/api/main.py`
  - Code: Add `CORSMiddleware` import and configuration
  - Time: 20 minutes
  - Impact: HIGH - Frontend can call backend

- [ ] **HIGH**: Create Update request schemas
  - Tasks:
    - [ ] `QuotationUpdate` schema
    - [ ] `CustomerUpdate` schema
    - [ ] `SaleOrderUpdate` schema
    - [ ] `ContractUpdate` schema
    - [ ] `ProformaUpdate` schema (exists but incomplete)
  - Location: `HD_API/api/schemas/`
  - Time: 2 hours
  - Depends on: None

#### Frontend Setup Tasks
- [ ] **HIGH**: Create API endpoints constants
  - Location: Create `src/core/services/api-endpoints.ts`
  - Content: All endpoint URLs as constants
  - Time: 1 hour
  - Template provided in spec
  
- [ ] **HIGH**: Create API service layer
  - Location: Create `src/core/services/quotation-service.ts`
  - And similar for other entities
  - Time: 2 hours
  - Template provided in spec

---

### PHASE 2: DATABASE MODEL UPDATES (Day 2 morning)

#### Model Updates
- [ ] **CRITICAL**: Update Quotation model
  - Add columns:
    - [ ] `currency: String(50)` with default 'USD'
    - [ ] `status: String(50)` with default 'Draft'
    - [ ] `total_amount: Float`
  - File: `HD_API/api/models/quotation.py`
  - Time: 30 min
  - Database migration: Need to ALTER TABLE or use migration tool

- [ ] **CRITICAL**: Update ProformaInvoice model
  - Add columns:
    - [ ] `status: String(50)` with default 'Draft'
  - File: `HD_API/api/models/proforma.py`
  - Time: 15 min

- [ ] **CRITICAL**: Update SaleOrder model
  - Add columns:
    - [ ] `status: String(50)` with default 'Confirmed'
  - File: `HD_API/api/models/sale_order.py`
  - Time: 15 min

- [ ] **CRITICAL**: Create ContractItem model
  - File: `HD_API/api/models/contract.py` (or new file)
  - Schema:
    ```python
    class ContractItem(Base):
        __tablename__ = "contract_item"
        contract_id = Column(String(50), FK, PK)
        product_id = Column(String(50), FK, PK)
        quantity = Column(Float)
        unit_price = Column(Float)
        discount = Column(Float, default=0)
        tax_rate = Column(Float, default=0)
        total_price = Column(Float)
    ```
  - Time: 30 min

#### Database Migration
- [ ] Execute SQL to add new columns OR use Alembic
  - Option A: Manual SQL execution
    ```sql
    ALTER TABLE quotation ADD (
      currency VARCHAR2(50) DEFAULT 'USD',
      status VARCHAR2(50) DEFAULT 'Draft',
      total_amount FLOAT
    );
    ALTER TABLE proforma_invoice ADD status VARCHAR2(50) DEFAULT 'Draft';
    ALTER TABLE sale_order ADD status VARCHAR2(50) DEFAULT 'Confirmed';
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
  - Option B: Use Alembic migration
  - Time: 1 hour

---

### PHASE 3: BACKEND GET ENDPOINTS (Day 2 afternoon)

#### Quotation Endpoints
- [ ] **Quotation List GET** `/quotations/`
  - Service method: `get_quotations_service(db, customer_id, status, skip, limit)`
  - Router method: `get_quotations()`
  - Filters: customer_id, status
  - Pagination: skip, limit
  - Time: 1 hour
  
- [ ] **Quotation Items GET** `/quotations/{id}/items`
  - Returns: `List[QuotationItem]`
  - Time: 30 min

#### Proforma Endpoints
- [ ] **Proforma List GET** `/proforma/`
  - Pagination support
  - Time: 30 min
  
- [ ] **Proforma Detail GET** `/proforma/{id}`
  - Time: 20 min
  
- [ ] **Proforma by Quotation GET** `/proforma/quotation/{quotation_id}`
  - Time: 20 min

#### Contract Endpoints
- [ ] **Contract List GET** `/contracts/`
  - Filters: customer_id, status
  - Time: 30 min
  
- [ ] **Contract Detail GET** `/contracts/{id}`
  - Time: 20 min
  
- [ ] **Contracts by Customer GET** `/contracts/customer/{customer_id}`
  - Time: 20 min
  
- [ ] **Contract Items GET** `/contracts/{id}/items`
  - Time: 30 min

#### Sale Order Endpoints
- [ ] **Sale Order List GET** `/sale-orders/`
  - Filters: contract_id, status
  - Time: 30 min
  
- [ ] **Sale Order Detail GET** `/sale-orders/{id}`
  - Time: 20 min
  
- [ ] **Sale Orders by Contract GET** `/sale-orders/contract/{id}`
  - Time: 20 min

**Subtotal for Phase 3**: 5-6 hours

---

### PHASE 4: MASTER DATA ROUTERS (Day 2 evening)

#### Product Router
- [ ] Create `product_repository.py`
  - Methods: CRUD operations
  - Time: 1 hour
  
- [ ] Create `product_service.py`
  - Time: 1 hour
  
- [ ] Create `product_router.py`
  - Endpoints: GET (list/detail), POST, PUT, DELETE
  - Time: 1 hour
  
- [ ] Create `ProductCreate` and `ProductResponse` schemas
  - Time: 30 min
  
- [ ] Register router in `main.py`
  - Time: 10 min

#### Payment Terms Router
- [ ] Create with same pattern as Product
  - Time: 2 hours

#### Incoterms Router
- [ ] Create with same pattern as Product
  - Time: 2 hours

#### Staff Router
- [ ] Create with same pattern as Product
  - Time: 2 hours

#### Customer Types, Contract Types Routers
- [ ] Create endpoints for reference data
  - Time: 3 hours

**Subtotal for Phase 4**: 8-9 hours

---

### PHASE 5: REPOSITORY & SERVICE UPDATES (Day 3 morning)

#### Update All Repositories
- [ ]  Quotation Repository
  - Add: `update_quotation()`, `delete_quotation()`
  - Time: 30 min
  
- [ ] Proforma Repository
  - Add: `update_proforma()`, `delete_proforma()`
  - Time: 30 min
  
- [ ] Contract Repository
  - Add: `update_contract()`, `delete_contract()`
  - Time: 30 min
  
- [ ] Sale Order Repository
  - Add: `update_sale_order()`, `delete_sale_order()`
  - Time: 30 min
  
- [ ] Customer Repository
  - Add: `update_customer()`, `delete_customer()` (may exist)
  - Time: 20 min

#### Update All Services
- [ ] Quotation Service
  - Add: `update_quotation_service()`, `delete_quotation_service()`
  - Time: 1 hour
  
- [ ] Proforma Service
  - Add: `update_proforma_service()`, `delete_proforma_service()`
  - Time: 1 hour
  
- [ ] Contract Service
  - Add: `update_contract_service()`, `delete_contract_service()`
  - Time: 1 hour
  
- [ ] Sale Order Service
  - Add: `update_sale_order_service()`, `delete_sale_order_service()`
  - Time: 1 hour
  
- [ ] Customer Service
  - Add: `update_customer_service()`, `delete_customer_service()`
  - Time: 1 hour

**Subtotal for Phase 5**: 6-7 hours

---

### PHASE 6: BACKEND PUT/DELETE ENDPOINTS (Day 3 afternoon)

#### Add PUT/DELETE to All Routers
- [ ] Customer Router: PUT, DELETE
  - Time: 30 min
  
- [ ] Quotation Router
  - Add: PUT, DELETE, GET (list), GET /items, POST /items
  - Time: 1 hour
  
- [ ] Proforma Router
  - Add: PUT, DELETE, GET (list), GET (detail)
  - Time: 1 hour
  
- [ ] Contract Router
  - Add: PUT, DELETE, GET (list), GET (detail), GET /items, POST /items
  - Time: 1 hour
  
- [ ] Sale Order Router
  - Add: PUT, DELETE, GET (list), GET (detail)
  - Time: 1 hour

**Subtotal for Phase 6**: 4-5 hours

---

### PHASE 7: FRONTEND HOOKS IMPLEMENTATION (Day 3-4)

#### Hook Implementations
- [ ] **useQuotation** hook
  - Methods: fetchAll, fetchById, create, update, delete
  - Location: `src/modules/quotation/controllers/useQuotation.ts`
  - Time: 1.5 hours
  - Template: Provided in spec
  
- [ ] **useSaleOrder** hook
  - Time: 1 hour
  
- [ ] **useProformaInvoice** hook
  - Time: 1 hour
  
- [ ] **useContract** hook
  - Time: 1 hour
  
- [ ] **useMasterData** hook
  - Methods: fetchCustomers, fetchStaff, fetchProducts, fetchPaymentTerms, fetchIncoterms
  - Time: 1.5 hours

#### Service Layer Creation
- [ ] Create service files for each entity
  - `src/core/services/quotation-service.ts`
  - `src/core/services/customer-service.ts`
  - `src/core/services/sale-order-service.ts`
  - `src/core/services/proforma-service.ts`
  - `src/core/services/contract-service.ts`
  - `src/core/services/master-data-service.ts`
  - Time: 3 hours
  - Template: Provided in spec

**Subtotal for Phase 7**: 8-9 hours

---

### PHASE 8: REPLACE MOCK DATA WITH API (Day 4)

#### Update Dashboard Components
- [ ] **QuotationDashboard**
  - Remove: `import { mockQuotations }`
  - Add: `const { quotations, fetchQuotations, ... } = useQuotation()`
  - Add: `useEffect(() => { fetchQuotations() }, [])`
  - Time: 1 hour
  
- [ ] **SaleOrderDashboard**
  - Time: 45 min
  
- [ ] **ProformaInvoiceDashboard**
  - Time: 45 min
  
- [ ] **ContractDashboard**
  - Time: 45 min
  
- [ ] Components using `mockCustomers`, `mockProducts`, etc.
  - Fetch all master data on app load from `useMasterData`
  - Time: 1 hour

#### Add Form Handlers
- [ ] Create form submission handlers
  - Call `createQuotation(formData)`
  - Show success/error toast
  - Refresh list
  - Time: 2 hours

#### Add Delete Confirmations
- [ ] Add modal confirmations before delete
  - Time: 1 hour

**Subtotal for Phase 8**: 6-7 hours

---

### PHASE 9: ERROR HANDLING & LOADING STATES (Day 4 evening)

#### Loading States
- [ ] Add `isLoading` to each hook
  - Show loading spinner in components
  - Time: 1.5 hours

#### Error Handling
- [ ] Add error state to hooks
  - Display error toast/modal
  - Time: 1.5 hours

#### Form Validation
- [ ] Add client-side validation
  - Required fields
  - Date range validation
  - Amount validation
  - Time: 2 hours

**Subtotal for Phase 9**: 5 hours

---

### PHASE 10: TESTING (Day 5)

#### Backend Testing
- [ ] Unit tests for quotation_service.py
  - Test: create, read, update, delete, list with filters
  - Time: 2 hours
  
- [ ] Integration tests for quotation endpoints
  - Test: full CRUD flow via API
  - Time: 2 hours
  
- [ ] Tests for remaining services
  - Time: 2 hours

#### Frontend Testing
- [ ] Unit tests for hooks
  - Time: 2 hours
  
- [ ] Component tests for dashboards
  - Time: 2 hours

#### End-to-End Testing
- [ ] Complete quotation workflow
  - Create → Update Status → Convert to Proforma → Create Contract → Create Sale Order
  - Manual testing
  - Time: 2 hours

**Subtotal for Phase 10**: 12 hours

---

### PHASE 11: DOCUMENTATION & DEPLOYMENT (Week 2, Day 5)

#### Documentation
- [ ] API documentation (Swagger/OpenAPI)
  - Generate from FastAPI
  - Time: 1 hour
  
- [ ] User guide for dashboards
  - Time: 2 hours
  
- [ ] Developer API reference
  - Time: 1 hour

#### Deployment Checklist
- [ ] Environment variables configured
  - DB credentials
  - API base URLs
  - Time: 30 min
  
- [ ] Database backup tested
  - Time: 30 min
  
- [ ] Performance optimization
  - Add database indexes
  - Time: 1 hour
  
- [ ] Security review
  - SQL injection prevention
  - XSS prevention
  - CORS settings
  - Auth implementation
  - Time: 2 hours
  
- [ ] Deployment to staging
  - Time: 1 hour

**Subtotal for Phase 11**: 8 hours

---

## 📊 Task Status Tracker

Copy this table and update as you complete tasks:

```
| Phase | Task | Status | Owner | Hours | Start | End | Notes |
|-------|------|--------|-------|-------|-------|-----|-------|
| 1 | Fix quotation_service bug | ☐ TODO | - | 0.25h | - | - | |
| 1 | Add CORS middleware | ☐ TODO | - | 0.33h | - | - | |
| 1 | Create Update schemas | ☐ TODO | - | 2h | - | - | |
| 1 | Create API endpoints constants | ☐ TODO | - | 1h | - | - | |
| 1 | Create API service layer | ☐ TODO | - | 2h | - | - | |
| 2 | Update Quotation model | ☐ TODO | - | 0.5h | - | - | |
| 2 | Update Proforma model | ☐ TODO | - | 0.25h | - | - | |
| 2 | Update SaleOrder model | ☐ TODO | - | 0.25h | - | - | |
| 2 | Create ContractItem model | ☐ TODO | - | 0.5h | - | - | |
| 2 | Database migration | ☐ TODO | - | 1h | - | - | |
| 3 | Quotation List GET | ☐ TODO | - | 1h | - | - | |
| 3 | Quotation Items GET | ☐ TODO | - | 0.5h | - | - | |
| 3 | Proforma endpoints | ☐ TODO | - | 1h | - | - | |
| 3 | Contract endpoints | ☐ TODO | - | 1.5h | - | - | |
| 3 | Sale Order endpoints | ☐ TODO | - | 1h | - | - | |
| 4 | Product router | ☐ TODO | - | 3.5h | - | - | |
| 4 | Payment Terms router | ☐ TODO | - | 2h | - | - | |
| 4 | Incoterms router | ☐ TODO | - | 2h | - | - | |
| 4 | Staff router | ☐ TODO | - | 2h | - | - | |
| 4 | Reference data routers | ☐ TODO | - | 3h | - | - | |
| 5 | Update all repositories | ☐ TODO | - | 2h | - | - | |
| 5 | Update all services | ☐ TODO | - | 4h | - | - | |
| 6 | Add PUT/DELETE to routers | ☐ TODO | - | 4.5h | - | - | |
| 7 | Implement all hooks | ☐ TODO | - | 6h | - | - | |
| 7 | Create service layer | ☐ TODO | - | 3h | - | - | |
| 8 | Replace mock data | ☐ TODO | - | 3.5h | - | - | |
| 8 | Add form handlers | ☐ TODO | - | 2h | - | - | |
| 8 | Add delete confirmations | ☐ TODO | - | 1h | - | - | |
| 9 | Add loading states | ☐ TODO | - | 1.5h | - | - | |
| 9 | Add error handling | ☐ TODO | - | 1.5h | - | - | |
| 9 | Form validation | ☐ TODO | - | 2h | - | - | |
| 10 | Backend testing | ☐ TODO | - | 6h | - | - | |
| 10 | Frontend testing | ☐ TODO | - | 4h | - | - | |
| 10 | E2E testing | ☐ TODO | - | 2h | - | - | |
| 11 | Documentation | ☐ TODO | - | 4h | - | - | |
| 11 | Deployment prep | ☐ TODO | - | 4h | - | - | |
```

---

## 🎯 Key Milestones

### Day 1 - Foundation
- [ ] All critical bugs fixed
- [ ] CORS working
- [ ] Frontend can make API calls to backend (even if endpoints not all ready)
- [ ] **Definition of Done**: Simple test API call returns 200

### Day 2 - Core Endpoints
- [ ] All GET endpoints working
- [ ] Master data endpoints responding
- [ ] Frontend hooks implemented
- [ ] **Definition of Done**: Can fetch quotation list from API and display in component

### Day 3 - Full CRUD
- [ ] All CRUD operations working (C, R, U, D)
- [ ] Forms submitting to backend
- [ ] Data persisting in database
- [ ] **Definition of Done**: Can create, update, delete quotation via UI

### Day 4 - Polish
- [ ] Error handling visible
- [ ] Loading states working
- [ ] Validation preventing bad data
- [ ] **Definition of Done**: User sees feedback for all actions

### Day 5 - Testing & Deployment
- [ ] Tests passing
- [ ] Documentation complete
- [ ] Ready for staging deploy
- [ ] **Definition of Done**: Code review approved, ready for QA

---

## 🚨 Blockers & Dependencies

### Blockers
1. **Database Access**: Need write access to add columns/tables
   - Decision: Use SQL scripts or Alembic?
   
2. **Oracle Connection**: Credentials locked?
   - Current: `admin_user:Nhan0944906711#@localhost:1521`
   - Need: Verify connection works from dev machine

3. **Frontend Build**: Any monorepo issues?
   - Test: `npm run build` from TS_Sales/frontend

### Dependencies
1. Database schema changes → Must complete before testing
2. CORS config → Required before frontend-backend communication
3. Backend hooks → Required before form submissions work
4. Master data endpoints → Required before dropdowns populate

---

## 👥 Team Allocation

### Backend Developer (1-2 days)
- Day 1-2: All BACKEND setup, models, migrations
- Day 3: Testing & debugging

### Frontend Developer (1.5 days)
- Day 1 lunch: Setup constants & API client
- Day 3-4: Hooks implementation & component updates
- Day 5: Testing

### Full Stack (2-3 days)
- Day 2-3: Integration testing
- Day 4: Error handling & validation
- Day 5: Final testing & documentation

### No specialist required if done sequentially
- **Sequential (1 developer, 50-65 hours)**:
  - Day 1-2: Backend setup & core endpoints
  - Day 3: Master data & CRUD
  - Day 4: Frontend integration
  - Day 5: Testing & deployment

---

## 📞 Getting Help

**Stuck on a task?**

1. Check the BACKEND_FRONTEND_INTEGRATION_SPEC.md for detailed examples
2. Look for code templates in "Code Examples" section
3. Verify file paths in "File Structure Reference"
4. Check database config in HD_API/api/database.py
5. Verify API Client config in core/services/api-client.ts

**Common Issues**:
- **"Module not found"**: Check imports match actual file structure
- **"Cannot POST /quotations"**: Verify router registered in main.py
- **"TypeScript error on ID"**: Remember string/number mismatch between BE/FE
- **"Database connection error"**: Verify Oracle service running, credentials correct
- **"CORS error"**: Make sure CORSMiddleware added to app

---

**Last Updated**: April 9, 2026  
**Estimated Total Effort**: 50-65 hours  
**Recommended Team**: 1 full stack OR 1 backend + 1 frontend  
**Deadline Feasibility**: 2 weeks ✅

