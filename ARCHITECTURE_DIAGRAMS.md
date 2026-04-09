# Architecture Pattern Diagrams

## 1. Folder Structure Comparison

### VietFarm_API (Current - Best Practice)

```
Vietfarm_API/
│
├── api/
│   ├── __init__.py
│   ├── main.py                          # ⭐ FastAPI app initialization
│   │
│   ├── constants/                       # Constants and enums
│   │   └── __init__.py
│   │
│   ├── dependencies/                    # 💉 Dependency Injection
│   │   ├── __init__.py
│   │   └── db.py                        # get_db: Session provider
│   │
│   ├── models/                          # 📊 Database Models (SQLAlchemy ORM)
│   │   ├── __init__.py
│   │   ├── master_data_models.py        # AloeFarm, Factory, Machine, etc.
│   │   ├── production_models.py         # Production-related entities
│   │   ├── processing_models.py        # Processing-related entities
│   │   ├── aloe_models.py              # Aloe-specific entities
│   │   ├── farming_models.py           # Farming-related entities
│   │   └── quality_models.py           # Quality control entities
│   │
│   ├── repositories/                    # 📚 Data Access Layer
│   │   ├── __init__.py
│   │   ├── base_repository.py          # BaseRepository<T> - generic CRUD
│   │   ├── master_data_repository.py   # Concrete repository instances
│   │   └── transaction_repository.py   # Transaction-specific repos
│   │
│   ├── routers/                         # 🚀 API Endpoints
│   │   ├── __init__.py
│   │   ├── master_data_router.py       # CRUD endpoints for master data
│   │   └── transaction_router.py       # Transaction creation endpoints
│   │
│   ├── schemas/                         # ✅ Request/Response Validation (Pydantic)
│   │   ├── __init__.py
│   │   ├── master_data.py              # AloeFarmBase, AloeFarmCreate, etc.
│   │   └── transaction_data.py         # Transaction schemas
│   │
│   ├── services/                        # 🎯 Business Logic Layer
│   │   ├── __init__.py
│   │   ├── master_data_service.py      # Generic CRUD service functions
│   │   └── transaction_service.py      # Transaction-specific logic
│   │
│   └── utils/                           # 🔧 Utilities & Configuration
│       ├── __init__.py
│       ├── database.py                 # SQLAlchemy engine & session factory
│       ├── db.py                       # get_db() generator
│       ├── oracle_settings.py          # DB credentials & connection string
│       └── oracle_connection.py        # Raw Oracle connections
│
├── generator/                           # Data generation utilities
├── DB_query/                            # SQL initialization scripts
├── Dockerfile
└── Script_activate_api.bat
```

### Back_end_TS_Sales (Current - Incomplete)

```
Back_end_TS_Sales/
│
├── schemas/                             # ✅ Only this exists
│   ├── contract_schema.py
│   ├── customer_schema.py
│   ├── product_schema.py
│   ├── sale_order_schema.py
│   ├── quotation_schema.py
│   └── ... (other schemas)
│
├── test.py
├── api_test_log.json
└── [Missing: api/, models/, repositories/, routers/, services/, utils/]
```

### Back_end_TS_Sales (Target - After Reorganization)

```
Back_end_TS_Sales/
│
├── api/                                 # 🎁 New structure
│   ├── __init__.py
│   ├── main.py                          # ⭐ FastAPI app (CREATE NEW)
│   │
│   ├── constants/                       # Constants and enums
│   │   └── __init__.py
│   │
│   ├── dependencies/                    # 💉 Dependency Injection
│   │   ├── __init__.py
│   │   └── db.py                        # get_db: Session provider
│   │
│   ├── models/                          # 📊 Database Models
│   │   ├── __init__.py
│   │   └── master_data_models.py        # Customer, Product, Staff, etc. (CREATE NEW)
│   │
│   ├── repositories/                    # 📚 Data Access Layer
│   │   ├── __init__.py
│   │   ├── base_repository.py          # Generic CRUD (COPY FROM VIETFARM)
│   │   └── master_data_repository.py   # Concrete repos (CREATE NEW)
│   │
│   ├── routers/                         # 🚀 API Endpoints
│   │   ├── __init__.py
│   │   └── master_data_router.py       # CRUD endpoints (CREATE NEW)
│   │
│   ├── schemas/                         # ✅ Pydantic validation
│   │   ├── __init__.py
│   │   └── master_data.py              # Migrate & consolidate existing schemas
│   │
│   ├── services/                        # 🎯 Business Logic
│   │   ├── __init__.py
│   │   └── master_data_service.py      # Generic functions (COPY FROM VIETFARM)
│   │
│   └── utils/                           # 🔧 Utilities
│       ├── __init__.py
│       ├── database.py                 # COPY FROM VIETFARM
│       ├── db.py                       # COPY FROM VIETFARM
│       └── oracle_settings.py          # COPY FROM VIETFARM
│
├── run.py                               # Application entry point (CREATE NEW)
├── requirements.txt                     # Update with fastapi, uvicorn
├── test.py                              # Keep for reference
└── README.md
```

---

## 2. Request/Response Flow Diagram

### HTTP Request → Database Read → HTTP Response

```
┌─────────────────────────────────────────────────────────────────┐
│ CLIENT REQUEST                                                   │
│ GET /master-data/customers/1                                    │
└────────────────────────────┬──────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ 1️⃣  ROUTER (api/routers/master_data_router.py)                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ @router.get("/customers/{customer_id}")                 │   │
│  │ def get_customer(customer_id: int,                       │   │
│  │                  db: Session = Depends(get_db)):         │   │
│  │   return get_entity_or_404(customer_repository, db, ...) │   │
│  └──────────────────────────────────────────────────────────┘   │
│                     ▼                                            │
│  ✓ Validation: customer_id is int ✓                            │
│  ✓ DI: db session injected                                      │
└────────────────────────────┬──────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2️⃣  SERVICE (api/services/master_data_service.py)               │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ def get_entity_or_404(repository, db, customer_id, ...): │   │
│  │   entity = repository.get(db, customer_id)              │   │
│  │   if entity is None:                                     │   │
│  │     raise HTTPException(404, "Customer not found")      │   │
│  │   return entity                                          │   │
│  └──────────────────────────────────────────────────────────┘   │
│                     ▼                                            │
│  ✓ Business logic: 404 handling                                 │
│  ✓ Error handling: HTTPException                                │
└────────────────────────────┬──────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3️⃣  REPOSITORY (api/repositories/base_repository.py)            │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ class BaseRepository(Generic[T]):                         │   │
│  │   def get(self, db: Session, entity_id):                │   │
│  │     return db.get(self.model, entity_id)                │   │
│  │                                                          │   │
│  │ instance = BaseRepository[Customer](Customer)           │   │
│  └──────────────────────────────────────────────────────────┘   │
│                     ▼                                            │
│  ✓ Query building: SELECT * FROM customers WHERE id = ?        │
│  ✓ SQLAlchemy abstraction                                       │
└────────────────────────────┬──────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4️⃣  DATABASE LAYER (api/utils/database.py)                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ engine = create_engine(SQLALCHEMY_DATABASE_URL,          │   │
│  │                        echo=True,                        │   │
│  │                        pool_pre_ping=True)               │   │
│  │ SessionLocal = sessionmaker(bind=engine)                 │   │
│  └──────────────────────────────────────────────────────────┘   │
│                     ▼                                            │
│  ✓ Connection pooling                                           │
│  ✓ Session management                                           │
└────────────────────────────┬──────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5️⃣  ORACLE DATABASE                                             │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ SELECT * FROM CUSTOMERS WHERE CUSTOMER_ID = 1           │   │
│  │                                                          │   │
│  │ Result: [ROW(customer_id=1, company_name="ABC Corp")]   │   │
│  └──────────────────────────────────────────────────────────┘   │
│                     ▼                                            │
│  ✓ Row retrieved                                                │
└────────────────────────────┬──────────────────────────────────┘
                             │
                             ▼ (Result back up the stack)
┌─────────────────────────────────────────────────────────────────┐
│ 6️⃣  MODEL INSTANTIATION                                         │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ customer = Customer(                                     │   │
│  │     customer_id=1,                                       │   │
│  │     company_name="ABC Corp",                             │   │
│  │     ...                                                  │   │
│  │ )                                                        │   │
│  └──────────────────────────────────────────────────────────┘   │
│                     ▼                                            │
│  ✓ SQLAlchemy model instance                                    │
└────────────────────────────┬──────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ 7️⃣  SCHEMA VALIDATION (api/schemas/master_data.py)              │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ class CustomerResponse(CustomerCreate):                  │   │
│  │   customer_id: int                                       │   │
│  │   model_config = ConfigDict(from_attributes=True)       │   │
│  │                                                          │   │
│  │ response = CustomerResponse.from_attributes(customer)   │   │
│  └──────────────────────────────────────────────────────────┘   │
│                     ▼                                            │
│  ✓ Pydantic validation                                          │
│  ✓ JSON serialization                                           │
└────────────────────────────┬──────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ HTTP RESPONSE (200 OK)                                          │
│ {                                                               │
│   "customer_id": 1,                                             │
│   "company_name": "ABC Corp",                                   │
│   "address": "123 Main St",                                     │
│   "status": "Active",                                           │
│   ...                                                           │
│ }                                                               │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Data Flow: POST Request (Create)

```
CLIENT REQUEST
│
│ POST /master-data/customers
│ {
│   "company_name": "New Company",
│   "address": "New Address",
│   ...
│ }
│
└─────► ROUTER: create_customer(payload: CustomerCreate, db: Session)
           │
           ├─► VALIDATION
           │   ✓ payload is valid CustomerCreate object (Pydantic)
           │   ✓ db session is injected
           │
           ├─► SERVICE: create_entity(customer_repository, db, payload.model_dump())
           │    │
           │    ├─► REPOSITORY: customer_repository.create(db, payload)
           │    │    │
           │    │    └─► DATABASE:
           │    │        1. CREATE customer instance: Customer(**payload)
           │    │        2. ADD to session: db.add(customer)
           │    │        3. COMMIT: db.commit()
           │    │        4. REFRESH: db.refresh(customer)
           │    │        5. RETURN customer
           │    │
           │    ├─► ERROR HANDLING:
           │    │    if Exception occur:
           │    │      - db.rollback()
           │    │      - raise HTTPException(400, "Failed to create...")
           │    │
           │    └─► RETURN customer instance
           │
           └─► SCHEMA VALIDATION: CustomerResponse.from_attributes(customer)
               │
               └─► JSON RESPONSE (201 Created)
                   {
                     "customer_id": 2,
                     "company_name": "New Company",
                     "address": "New Address",
                     ...
                   }
```

---

## 4. Dependency Injection Pattern

```
┌──────────────────────────────────────────────────────────────┐
│ Dependency Injection Flow                                     │
└──────────────────────────────────────────────────────────────┘

Request comes in:

  def get_customer(
      customer_id: int,
      db: Session = Depends(get_db)  ◄─── FastAPI sees Depends()
  ):
      pass

                    │
                    ▼

FastAPI calls get_db():

  def get_db() -> Generator[Session, None, None]:
      db = SessionLocal()        # Create session
      try:
          yield db               # ◄─── Inject into route handler
      finally:
          db.close()             # ◄─── Close after response

                    │
                    ▼

Route handler receives db:

  get_customer(customer_id=1, db=<Session object>)

                    │
                    ▼

After response, finally block closes db:

  db.close()  # ◄─── Automatic cleanup

                    │
                    ▼

Response sent to client with closed db
```

---

## 5. Repository Pattern Generic Type

```
┌──────────────────────────────────────────────────────────────┐
│ Generic Repository with Type Hints                            │
└──────────────────────────────────────────────────────────────┘

TypeVar T defines a generic type:

  T = TypeVar("T")  # T can be any model type

class BaseRepository(Generic[T]):
    def __init__(self, model: type[T]):
        self.model = model  # Store the actual model class

    def list(self, db: Session) -> list[T]:
        # Returns a list of T (e.g., list[Customer])
        pass

    def get(self, db: Session, id: Any) -> T | None:
        # Returns T or None (e.g., Customer | None)
        pass

    def create(self, db: Session, payload: dict) -> T:
        # Returns T (e.g., Customer)
        pass

Usage:

  customer_repo: BaseRepository[Customer] = BaseRepository[Customer](Customer)
  # Now customer_repo has type information:
  # - list() returns list[Customer]
  # - get() returns Customer | None
  # - create() returns Customer

  factory_repo: BaseRepository[Factory] = BaseRepository[Factory](Factory)
  # Now factory_repo has type information:
  # - list() returns list[Factory]
  # - get() returns Factory | None
  # - create() returns Factory

Benefits:

  ✓ Type safety: IDE knows what type is returned
  ✓ Auto-complete: IDE can suggest Customer properties
  ✓ No code duplication: One class handles all models
  ✓ Runtime safety: model parameter stores actual class
```

---

## 6. Schema Inheritance Chain

```
┌──────────────────────────────────────────────────────────────┐
│ Pydantic Schema Inheritance Pattern                           │
└──────────────────────────────────────────────────────────────┘

class CustomerBase(BaseModel):
    """
    Base schema with common fields
    Used by all other schemas
    """
    company_name: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    status: Optional[str] = "Active"
           │
           ├─────────────────────┬──────────────────────┐
           │                     │                      │
           ▼                     ▼                      ▼

class CustomerCreate        class CustomerUpdate    class CustomerResponse
(CustomerBase):             (CustomerBase):          (CustomerCreate):
    """                        """                      """
    For POST requests       For PUT requests        For HTTP responses
    Client provides:        Client provides:        Server returns:
    - company_name          - All optional          - customer_id (DB)
    """                     """                     - All from Create
                                                    - model_config = 
                                                      ConfigDict(
                                                        from_attributes=True
                                                      )
                                                    """
           │                     │                      │
           └─────────────────────┴──────────────────────┘
                     │
                     ▼

HTTP Endpoints:

  POST /customers
  Request body: CustomerCreate
  Response: CustomerResponse(201)

  PUT /customers/1
  Request body: CustomerUpdate
  Response: CustomerResponse(200)

  GET /customers/1
  Response: CustomerResponse(200)

Benefits:

  ✓ DRY: Base fields defined once
  ✓ Consistency: All schemas share base definition
  ✓ Flexibility: Create/Update can customize fields
  ✓ Type safety: IDE knows what each endpoint expects
```

---

## 7. Error Handling Hierarchy

```
┌──────────────────────────────────────────────────────────────┐
│ Error Handling in Service Layer                              │
└──────────────────────────────────────────────────────────────┘

1. ROUTE HANDLER ERROR (in router)
   ├─ Invalid ID type: FastAPI returns 422 (Validation Error)
   ├─ Missing required field: Pydantic returns 422
   └─ Invalid query params: FastAPI returns 422

2. NOT FOUND ERROR (in service)
   │
   ├─► if entity is None:
   │       raise HTTPException(
   │           status_code=404,
   │           detail=f"Customer not found: {id}"
   │       )
   │
   └─► Response: 404 Not Found

3. DATABASE ERROR (in service/repository)
   │
   ├─► try:
   │       entity = model(**payload)
   │       db.add(entity)
   │       db.commit()
   │   except Exception as exc:
   │       db.rollback()
   │       raise HTTPException(
   │           status_code=400,
   │           detail=f"Failed to create customer: {str(exc)}"
   │       )
   │
   └─► Response: 400 Bad Request

4. CONNECTION ERROR (in main.py)
   │
   ├─► if db.execute(...) fails:
   │       raise HTTPException(
   │           status_code=500,
   │           detail=f"Database connection failed: {str(exc)}"
   │       )
   │
   └─► Response: 500 Internal Server Error

Status Code Summary:

  ┌─────────────────────────────────────────┐
  │ 200 OK          – Success (GET, PUT)     │
  │ 201 Created     – Created (POST)         │
  │ 204 No Content  – Deleted (DELETE)       │
  │ 400 Bad Request – Validation/DB fail     │
  │ 404 Not Found   – Entity not found       │
  │ 422 Validation  – Invalid input (auto)   │
  │ 500 Server Err  – Connection failed      │
  └─────────────────────────────────────────┘
```

---

## 8. Database Session Lifecycle

```
┌──────────────────────────────────────────────────────────────┐
│ Session Lifecycle per Request                                │
└──────────────────────────────────────────────────────────────┘

REQUEST ARRIVES
│
├─► FastAPI calls get_db() dependency
│   │
│   └─► def get_db():
│       ┌──────────────────────────────┐
│       │ db = SessionLocal()           │ ◄─ CREATE SESSION
│       │ try:                          │
│       │     yield db  ────────┐       │
│       │ finally:             │       │
│       │     db.close() ◄─────┼───┐   │
│       └──────────────────────┼───┼───┘
│                              │   │
│        ┌─────────────────────┘   │
│        │                         │
│        ▼                         │
├─► ROUTE HANDLER executes
│   │
│   ├─ get_customer(customer_id=1, db=<session>)
│   │
│   ├─ Service layer uses db
│   │  └─ repository.get(db, 1)
│   │     └─ db.get(Customer, 1)  ◄─ QUERIES
│   │
│   ├─ Returns response
│   │
│   └─ Exits function
│
├─► Finally block executes
│   │
│   └–────────────────────────────────────►
│                                          │
│        ┌──────────────────────────────┐  │
│        │ db.close()                   │◄─┘
│        │ • Closes DB connection       │
│        │ • Returns to connection pool │
│        │ • Session cleaned up         │
│        └──────────────────────────────┘
│
└─► RESPONSE SENT

Key Points:

  ✓ Session created fresh for each request
  ✓ Automatically injected with Depends(get_db)
  ✓ Always closed in finally block (guaranteed)
  ✓ No connection leaks
  ✓ Supports connection pooling
```

---

## 9. Complete Request-Response Cycle

```
┌──────────────────────────────────────────────────────────────┐
│ Complete Lifecycle: POST /master-data/customers              │
└──────────────────────────────────────────────────────────────┘

Step 1: CLIENT SENDS REQUEST
─────────────────────────────────────────
  POST /master-data/customers HTTP/1.1
  Content-Type: application/json

  {
    "company_name": "ABC Corp",
    "address": "123 Main St",
    ...
  }

Step 2: FASTAPI ROUTING
─────────────────────────────────────────
  ✓ Receives request
  ✓ Matches route: POST /master-data/customers
  ✓ Finds handler: create_customer()
  ✓ Prepares dependencies

Step 3: DEPENDENCY INJECTION
─────────────────────────────────────────
  ✓ Calls get_db()
  ✓ Creates SessionLocal()
  ✓ Injects db: Session = <session_object>

Step 4: REQUEST BODY VALIDATION
─────────────────────────────────────────
  ✓ Parses JSON → Python dict
  ✓ Validates against CustomerCreate schema
  ✓ If invalid: raises HTTPException(422)
  ✓ If valid: payload: CustomerCreate = <validated_object>

Step 5: ROUTE HANDLER EXECUTION
─────────────────────────────────────────
  create_customer(payload: CustomerCreate, db: Session):
    return create_entity(customer_repository, db, 
                        payload.model_dump(), "customer")

Step 6: SERVICE LAYER
─────────────────────────────────────────
  create_entity(customer_repository, db, payload, "customer"):
    try:
        return repository.create(db, payload)  ◄─ Call repo
    except Exception as exc:
        db.rollback()  ◄─ Rollback on error
        raise HTTPException(400, "Failed to create...")

Step 7: REPOSITORY LAYER
─────────────────────────────────────────
  customer_repository.create(db, payload):
    entity = Customer(**payload)  ◄─ Instantiate model
    db.add(entity)                ◄─ Add to session
    db.commit()                   ◄─ Execute INSERT
    db.refresh(entity)            ◄─ Reload from DB
    return entity

Step 8: DATABASE LAYER
─────────────────────────────────────────
  ✓ SQLAlchemy builds INSERT statement
  ✓ Sends to Oracle:
    INSERT INTO CUSTOMERS (COMPANY_NAME, ADDRESS, ...)
    VALUES ('ABC Corp', '123 Main St', ...)
  ✓ Oracle executes, returns CUSTOMER_ID = 42
  ✓ SQLAlchemy refreshes entity with DB values

Step 9: RESPONSE VALIDATION
─────────────────────────────────────────
  ✓ Customer instance (entity) returned
  ✓ Route handler specifies response_model=CustomerResponse
  ✓ FastAPI validates entity against CustomerResponse schema
  ✓ Pydantic serializes to JSON

Step 10: SESSION CLEANUP
─────────────────────────────────────────
  ✓ Finally block of get_db() executes
  ✓ db.close() called
  ✓ Connection returned to pool

Step 11: HTTP RESPONSE
─────────────────────────────────────────
  HTTP/1.1 201 Created
  Content-Type: application/json

  {
    "customer_id": 42,
    "company_name": "ABC Corp",
    "address": "123 Main St",
    "status": "Active",
    "preferred_currency": "USD",
    ...
  }

Step 12: CLIENT RECEIVES RESPONSE
─────────────────────────────────────────
  ✓ Parse JSON
  ✓ Extract customer_id
  ✓ Update UI
  ✓ Show success message
```

---

## Summary

These diagrams illustrate:

1. **Folder Structure**: How to organize code
2. **Request/Response Flow**: How data flows through layers
3. **Data Flow**: Detailed POST request handling
4. **Dependency Injection**: How sessions are managed
5. **Repository Pattern**: Generic types and reusability
6. **Schema Inheritance**: Code reuse in validation
7. **Error Handling**: Status codes and exceptions
8. **Session Lifecycle**: Automatic connection management
9. **Complete Cycle**: End-to-end request processing

These patterns are proven in **VietFarm_API** and ready to be adopted in **Back_end_TS_Sales**!
