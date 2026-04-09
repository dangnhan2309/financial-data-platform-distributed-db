# VietFarm API Architecture Analysis & Back_end_TS_Sales Reorganization Plan

**Date**: April 9, 2026  
**Purpose**: Extract architecture patterns from VietFarm_API and provide step-by-step reorganization plan for Back_end_TS_Sales

---

## 1. VietFarm_API Architecture Overview

### 1.1 Directory Structure

```
Vietfarm_API/
├── api/
│   ├── __init__.py
│   ├── main.py                          # FastAPI app initialization
│   ├── constants/                       # Empty (for future expansion)
│   ├── dependencies/
│   │   ├── __init__.py
│   │   └── db.py                        # Dependency injection (get_db)
│   ├── models/
│   │   ├── __init__.py
│   │   ├── master_data_models.py        # SQLAlchemy ORM models
│   │   ├── production_models.py
│   │   ├── processing_models.py
│   │   ├── quality_models.py
│   │   ├── aloe_models.py
│   │   └── farming_models.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── base_repository.py           # Generic CRUD base class
│   │   ├── master_data_repository.py    # Concrete repositories
│   │   └── transaction_repository.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── master_data_router.py        # API endpoints (CRUD)
│   │   └── transaction_router.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── master_data.py               # Pydantic schemas
│   │   └── transaction_data.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── master_data_service.py       # Business logic & error handling
│   │   └── transaction_service.py
│   └── utils/
│       ├── __init__.py
│       ├── database.py                  # SQLAlchemy setup
│       ├── db.py                        # get_db generator
│       ├── oracle_connection.py         # Raw Oracle connections
│       └── oracle_settings.py           # DB config & env vars
├── generator/                           # Data generation utilities
├── DB_query/                            # SQL initialization scripts
├── Dockerfile
└── Script_activate_api.bat
```

### 1.2 Core Patterns Explained

#### **Pattern 1: Model Definition (SQLAlchemy ORM)**

```python
# api/models/master_data_models.py
from sqlalchemy import Boolean, Column, Date, Numeric, String
from sqlalchemy.orm import relationship
from api.utils.database import Base

class AloeFarm(Base):
    __tablename__ = "aloefarm"
    
    farm_id = Column("farm_id", String(50), primary_key=True)
    farm_name = Column("farm_name", String(100), unique=True, nullable=False)
    farmer_name = Column("farmer_name", String(100))
    location = Column("location", String(255))
    status = Column("status", Boolean)
    
    # Relationships
    fields = relationship("AloeField", back_populates="farm")
    harvest_batches = relationship("AloeHarvestBatch", back_populates="farm")
```

**Key Points:**
- Models inherit from `Base` (declarative_base)
- Column names explicitly map to database columns
- Relationships link related models
- String IDs are common (not auto-incrementing)

#### **Pattern 2: Schema Validation (Pydantic)**

```python
# api/schemas/master_data.py
from pydantic import BaseModel, ConfigDict

# Base schema: Common fields
class AloeFarmBase(BaseModel):
    farm_name: str
    farmer_name: str | None = None
    location: str | None = None
    province: str | None = None
    status: bool | None = None

# Create schema: For POST requests
class AloeFarmCreate(AloeFarmBase):
    farm_id: str  # Client must provide ID

# Update schema: For PUT requests
class AloeFarmUpdate(AloeFarmBase):
    pass  # Same as base, all fields optional

# Response schema: For responses
class AloeFarmResponse(AloeFarmCreate):
    model_config = ConfigDict(from_attributes=True)
```

**Key Points:**
- Inheritance: Base → Create → Update → Response
- `from_attributes=True` allows reading from SQLAlchemy objects
- Optional fields use `field: type | None = None`
- No business logic, only data validation

#### **Pattern 3: BaseRepository (Generic CRUD)**

```python
# api/repositories/base_repository.py
from typing import Any, Generic, TypeVar
from sqlalchemy import select
from sqlalchemy.orm import Session

T = TypeVar("T")

class BaseRepository(Generic[T]):
    def __init__(self, model: type[T]):
        self.model = model

    def list(self, db: Session, offset: int = 0, limit: int = 100) -> list[T]:
        stmt = select(self.model).offset(offset).limit(limit)
        return list(db.scalars(stmt).all())

    def get(self, db: Session, entity_id: Any) -> T | None:
        return db.get(self.model, entity_id)

    def create(self, db: Session, payload: dict[str, Any]) -> T:
        entity = self.model(**payload)
        db.add(entity)
        db.commit()
        db.refresh(entity)
        return entity

    def update(self, db: Session, entity: T, payload: dict[str, Any]) -> T:
        for field, value in payload.items():
            setattr(entity, field, value)
        db.commit()
        db.refresh(entity)
        return entity

    def delete(self, db: Session, entity: T) -> None:
        db.delete(entity)
        db.commit()
```

**Key Points:**
- Generic base class works with any model
- CRUD operations: list, get, create, update, delete
- Automatic commit/refresh for consistency
- Easy to extend for custom queries

#### **Pattern 4: Concrete Repositories**

```python
# api/repositories/master_data_repository.py
from api.models.master_data_models import AloeFarm, Factory, Machine
from api.repositories.base_repository import BaseRepository

# Factory pattern: Instantiate repositories per model
aloe_farm_repository = BaseRepository[AloeFarm](AloeFarm)
factory_repository = BaseRepository[Factory](Factory)
machine_repository = BaseRepository[Machine](Machine)
```

**Key Points:**
- Simple instantiation of BaseRepository with each model
- Repositories are singletons (module-level)
- Can be extended for custom queries later

#### **Pattern 5: Service Layer (Business Logic)**

```python
# api/services/master_data_service.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from api.repositories.base_repository import BaseRepository

def list_entities(repository: BaseRepository, db: Session, 
                 offset: int = 0, limit: int = 100):
    return repository.list(db, offset=offset, limit=limit)

def get_entity_or_404(repository: BaseRepository, db: Session, 
                      entity_id: str, entity_name: str):
    entity = repository.get(db, entity_id)
    if entity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{entity_name} not found: {entity_id}",
        )
    return entity

def create_entity(repository: BaseRepository, db: Session, 
                 payload: dict, entity_name: str):
    try:
        return repository.create(db, payload)
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create {entity_name}: {str(exc)}",
        ) from exc

def update_entity(repository: BaseRepository, db: Session, 
                 entity: Any, payload: dict, entity_name: str):
    try:
        return repository.update(db, entity, payload)
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update {entity_name}: {str(exc)}",
        ) from exc

def delete_entity(repository: BaseRepository, db: Session, 
                 entity: Any, entity_name: str):
    try:
        repository.delete(db, entity)
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to delete {entity_name}: {str(exc)}",
        ) from exc
```

**Key Points:**
- Generic service functions (can handle all entities)
- Error handling with rollback on failure
- 404 checks for GET operations
- Status codes: 201 for creation, 400 for errors

#### **Pattern 6: Routers (API Endpoints)**

```python
# api/routers/master_data_router.py
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from api.dependencies.db import get_db
from api.repositories.master_data_repository import factory_repository
from api.schemas.master_data import (
    FactoryCreate, FactoryUpdate, FactoryResponse
)
from api.services.master_data_service import (
    create_entity, delete_entity, get_entity_or_404, 
    list_entities, update_entity
)

router = APIRouter(prefix="/master-data", tags=["Master Data CRUD"])

# LIST - GET /master-data/factories
@router.get("/factories", response_model=list[FactoryResponse])
def list_factories(offset: int = 0, limit: int = 100, 
                  db: Session = Depends(get_db)):
    return list_entities(factory_repository, db, offset, limit)

# CREATE - POST /master-data/factories
@router.post("/factories", response_model=FactoryResponse, 
            status_code=status.HTTP_201_CREATED)
def create_factory(payload: FactoryCreate, db: Session = Depends(get_db)):
    return create_entity(factory_repository, db, 
                        payload.model_dump(), "factory")

# READ - GET /master-data/factories/{factory_id}
@router.get("/factories/{factory_id}", response_model=FactoryResponse)
def get_factory(factory_id: str, db: Session = Depends(get_db)):
    return get_entity_or_404(factory_repository, db, 
                            factory_id, "Factory")

# UPDATE - PUT /master-data/factories/{factory_id}
@router.put("/factories/{factory_id}", response_model=FactoryResponse)
def update_factory(factory_id: str, payload: FactoryUpdate, 
                  db: Session = Depends(get_db)):
    entity = get_entity_or_404(factory_repository, db, 
                              factory_id, "Factory")
    return update_entity(factory_repository, db, entity, 
                        payload.model_dump(), "factory")

# DELETE - DELETE /master-data/factories/{factory_id}
@router.delete("/factories/{factory_id}", 
              status_code=status.HTTP_204_NO_CONTENT)
def delete_factory(factory_id: str, db: Session = Depends(get_db)):
    entity = get_entity_or_404(factory_repository, db, 
                              factory_id, "Factory")
    delete_entity(factory_repository, db, entity, "factory")
```

**Key Points:**
- APIRouter with prefix and tags
- Dependency injection with `Depends(get_db)`
- Response models for validation
- Status codes: 200 (GET), 201 (POST), 204 (DELETE)
- Consistent endpoint pattern for all entities

#### **Pattern 7: Database Configuration**

```python
# api/utils/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from api.utils.oracle_settings import DB_ECHO, get_sqlalchemy_oracle_url

SQLALCHEMY_DATABASE_URL = get_sqlalchemy_oracle_url()

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=DB_ECHO,              # Log SQL queries
    pool_pre_ping=True,        # Test connections before use
    pool_recycle=1800,         # Recycle connections after 30 min
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()
```

**Key Points:**
- Engine configuration with connection pooling
- `pool_pre_ping=True` prevents stale connections
- `SessionLocal` factory for creating database sessions
- `Base` for model inheritance

#### **Pattern 8: Environment Configuration**

```python
# api/utils/oracle_settings.py
import os
from urllib.parse import quote_plus

def _get_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None or str(value).strip() == "":
        raise ValueError(f"Missing required environment variable: {name}")
    return value

DB_USER = _get_env("ORACLE_USER", "vietfarm_user")
DB_PASSWORD = _get_env("ORACLE_PASSWORD", "GCFood2026")
DB_HOST = _get_env("ORACLE_HOST", "localhost")
DB_PORT = _get_env("ORACLE_PORT", "1521")
DB_SERVICE = _get_env("ORACLE_SERVICE", "FREEPDB1")
DB_ECHO = os.getenv("ORACLE_SQL_ECHO", "false").lower() in {"1", "true"}

def get_sqlalchemy_oracle_url() -> str:
    encoded_password = quote_plus(DB_PASSWORD)
    return (
        f"oracle+oracledb://{DB_USER}:{encoded_password}@"
        f"{DB_HOST}:{DB_PORT}/?service_name={DB_SERVICE}"
    )
```

**Key Points:**
- Environment-based configuration
- Password encoding for special characters
- Default values for common settings
- Oracle connection string format

#### **Pattern 9: Dependency Injection**

```python
# api/dependencies/db.py
from collections.abc import Generator
from sqlalchemy.orm import Session
from api.utils.database import SessionLocal

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Usage in routers:
@router.get("/factories")
def list_factories(db: Session = Depends(get_db)):
    # db is automatically injected and closed after response
    return ...
```

**Key Points:**
- Generator-based dependency for automatic cleanup
- Used with `Depends(get_db)` in route handlers
- Ensures database session is closed after each request

#### **Pattern 10: Application Initialization**

```python
# api/main.py
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from api.dependencies.db import get_db
from api.routers.master_data_router import router as master_data_router
from api.routers.transaction_router import router as transaction_router

app = FastAPI(
    title="VietFarm Aloe Supply Chain API",
    version="1.0.0",
    description="API for master data CRUD and transaction data creation",
)

# Include routers
app.include_router(master_data_router)
app.include_router(transaction_router)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to VietFarm API",
        "docs": "/docs",
    }

@app.get("/health-check")
def health_check(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 'Connection OK' FROM DUAL")).fetchone()
        return {
            "database_status": "Connected",
            "oracle_response": result[0],
        }
    except Exception as exc:
        raise HTTPException(
            status_code=500, 
            detail=f"Database connection failed: {str(exc)}"
        ) from exc
```

**Key Points:**
- FastAPI initialization with metadata
- Router inclusion with prefixes/tags
- Health check endpoint for monitoring
- Root endpoint for documentation

---

## 2. Comparison: VietFarm_API vs Back_end_TS_Sales

### Current State of Back_end_TS_Sales

```
Back_end_TS_Sales/
├── schemas/
│   ├── contract_schema.py        ✓ Exists
│   ├── customer_schema.py        ✓ Exists
│   ├── product_schema.py         ✓ Exists
│   ├── sale_order_schema.py      ✓ Exists
│   ├── quotation_schema.py       ✓ Exists
│   └── ... (other schemas)       ✓ Exist
├── test.py                        # Test file with manual API calls
└── api_test_log.json             # Test results
```

### What's Missing

| Component | VietFarm_API | Back_end_TS_Sales |
|-----------|--------------|-------------------|
| models/   | ✓ SQLAlchemy ORM | ✗ Missing |
| repositories/ | ✓ BaseRepository + concrete | ✗ Missing |
| services/ | ✓ Business logic layer | ✗ Missing |
| routers/ | ✓ API endpoints | ✗ Missing |
| dependencies/ | ✓ DI utilities | ✗ Missing |
| utils/ | ✓ DB config, settings | ✗ Missing |
| main.py | ✓ FastAPI app | ✗ Missing |
| schemas/ | ✓ Pydantic models | ✓ Exists (but needs migration) |

### Key Differences in Approach

| Aspect | VietFarm_API | Back_end_TS_Sales |
|--------|--------------|-------------------|
| Database | Oracle + SQLAlchemy ORM | Unknown (no DB layer) |
| ID Type | String IDs (farm_id, factory_id) | Integer IDs (from schemas) |
| Schema Pattern | Base → Create → Update → Response | Base + Create + Update (exists) |
| API Pattern | Consistent CRUD for all entities | Not yet implemented |
| Error Handling | Centralized in services with 404 checks | Missing |
| Pagination | offset/limit parameters | Not mentioned |
| State Management | Models + Schemas clear separation | Schemas only |

---

## 3. Architecture Pattern Extraction

### 3.1 Naming Conventions

```
├── models/
│   ├── {domain}_models.py          (master_data_models.py)
│   └── {domain}_models.py          (production_models.py)
│
├── schemas/
│   ├── {entity}.py                 (master_data.py)
│   └── {entity}.py                 (transaction_data.py)
│
├── repositories/
│   ├── base_repository.py          (Always this name)
│   ├── {entity}_repository.py      (master_data_repository.py)
│   └── {entity}_repository.py      (transaction_repository.py)
│
├── services/
│   ├── {entity}_service.py         (master_data_service.py)
│   └── {entity}_service.py         (transaction_service.py)
│
├── routers/
│   ├── {entity}_router.py          (master_data_router.py)
│   └── {entity}_router.py          (transaction_router.py)
│
└── utils/
    ├── database.py                 (Always this name)
    ├── db.py                       (Always this name - get_db)
    ├── oracle_settings.py          (Config/env)
    └── oracle_connection.py        (Optional - raw connections)
```

### 3.2 Class Naming Patterns

```python
# Models (SQLAlchemy)
Class AloeFarm(Base)          # Singular entity name, PascalCase
Class aloefarm                # Mapped to table name (lowercase)

# Schemas (Pydantic)
class AloeFarmBase(BaseModel)       # Base schema
class AloeFarmCreate(AloeFarmBase)  # For POST
class AloeFarmUpdate(AloeFarmBase)  # For PUT
class AloeFarmResponse(AloeFarmCreate)  # For response

# Repositories
class BaseRepository(Generic[T])    # Generic base
instance: BaseRepository[AloeFarm] = BaseRepository[AloeFarm](AloeFarm)

# Services (Functions, not classes)
def list_entities(...)              # Generic list
def get_entity_or_404(...)          # Get with 404 handling
def create_entity(...)              # Create with error handling
def update_entity(...)              # Update with error handling
def delete_entity(...)              # Delete with error handling

# Routers (Module level)
router = APIRouter(prefix="/master-data", tags=["Master Data CRUD"])
```

### 3.3 HTTP Methods & Status Codes

```
LIST:   GET    /master-data/factories                  → 200 (OK)
CREATE: POST   /master-data/factories                  → 201 (Created)
READ:   GET    /master-data/factories/{factory_id}     → 200 (OK)
UPDATE: PUT    /master-data/factories/{factory_id}     → 200 (OK)
DELETE: DELETE /master-data/factories/{factory_id}     → 204 (No Content)
```

### 3.4 Error Handling Pattern

```python
# 404 Not Found
HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=f"Factory not found: {factory_id}",
)

# 400 Bad Request (validation/creation errors)
HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=f"Failed to create factory: {str(exc)}",
)

# 500 Internal Server Error (DB connection issues)
HTTPException(
    status_code=500,
    detail=f"Database connection failed: {str(exc)}",
)
```

---

## 4. Step-by-Step Reorganization Plan for Back_end_TS_Sales

### Phase 1: Setup Foundation (Week 1)

#### Step 1.1: Create Directory Structure

```bash
cd Back_end_TS_Sales
mkdir -p api/constants
mkdir -p api/dependencies
mkdir -p api/models
mkdir -p api/repositories
mkdir -p api/routers
mkdir -p api/services
mkdir -p api/utils
```

#### Step 1.2: Create Configuration Files

**api/__init__.py**
```python
"""Back_end_TS_Sales API Package"""
```

**api/utils/oracle_settings.py**
```python
import os
from urllib.parse import quote_plus

def _get_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None or str(value).strip() == "":
        raise ValueError(f"Missing required environment variable: {name}")
    return value

DB_USER = _get_env("ORACLE_USER", "ts_sales_user")
DB_PASSWORD = _get_env("ORACLE_PASSWORD", "GCFood2026")
DB_HOST = _get_env("ORACLE_HOST", "localhost")
DB_PORT = _get_env("ORACLE_PORT", "1521")
DB_SERVICE = _get_env("ORACLE_SERVICE", "FREEPDB1")
DB_ECHO = os.getenv("ORACLE_SQL_ECHO", "false").lower() in {"1", "true"}

def get_sqlalchemy_oracle_url() -> str:
    encoded_password = quote_plus(DB_PASSWORD)
    return (
        f"oracle+oracledb://{DB_USER}:{encoded_password}@"
        f"{DB_HOST}:{DB_PORT}/?service_name={DB_SERVICE}"
    )

def get_raw_dsn() -> str:
    return f"{DB_HOST}:{DB_PORT}/{DB_SERVICE}"
```

**api/utils/database.py**
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from api.utils.oracle_settings import DB_ECHO, get_sqlalchemy_oracle_url

SQLALCHEMY_DATABASE_URL = get_sqlalchemy_oracle_url()

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=DB_ECHO,
    pool_pre_ping=True,
    pool_recycle=1800,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()
```

**api/utils/db.py**
```python
from collections.abc import Generator
from sqlalchemy.orm import Session
from api.utils.database import SessionLocal

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**api/utils/__init__.py**
```python
from api.utils.db import get_db

__all__ = ["get_db"]
```

#### Step 1.3: Setup Dependencies

**api/dependencies/__init__.py**
```python
from api.utils.db import get_db

__all__ = ["get_db"]
```

**api/dependencies/db.py**
```python
from api.utils.db import get_db

__all__ = ["get_db"]
```

### Phase 2: Create Models (Week 1-2)

#### Step 2.1: Analyze Existing Schemas

The existing schemas in `Back_end_TS_Sales/schemas/` need to become SQLAlchemy models.

Current entities:
- Customer
- Product
- Staff
- Quotation & QuotationItem
- ProformaInvoice
- SaleOrder & SaleOrderItem
- Contract & ContractItem
- PaymentTerm
- IncoTerm
- ExportDocumentSet

#### Step 2.2: Create Models

**api/models/master_data_models.py**
```python
from sqlalchemy import Boolean, Column, Date, Integer, Numeric, String, ForeignKey
from sqlalchemy.orm import relationship
from api.utils.database import Base

class Customer(Base):
    __tablename__ = "customers"
    
    customer_id = Column(Integer, primary_key=True)
    customer_type = Column(String(50))
    customer_code = Column(String(100))
    company_name = Column(String(255), nullable=False)
    short_name = Column(String(100))
    tax_id = Column(String(50))
    country = Column(String(100))
    city = Column(String(100))
    address = Column(String(500))
    phone = Column(String(20))
    email = Column(String(100))
    website = Column(String(255))
    industry = Column(String(100))
    status = Column(String(50), default="Active")
    preferred_currency = Column(String(10), default="USD")
    
    # Relationships
    quotations = relationship("Quotation", back_populates="customer")
    contracts = relationship("Contract", back_populates="customer")
    orders = relationship("SaleOrder", back_populates="customer")

class Product(Base):
    __tablename__ = "products"
    
    product_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1000))
    price = Column(Numeric(12, 2))
    product_type = Column(String(100))
    is_active = Column(Boolean, default=True)
    
    # Relationships
    quotation_items = relationship("QuotationItem", back_populates="product")
    order_items = relationship("SaleOrderItem", back_populates="product")

class Staff(Base):
    __tablename__ = "staff"
    
    staff_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(100))
    phone = Column(String(20))
    department = Column(String(100))
    position = Column(String(100))

class Quotation(Base):
    __tablename__ = "quotations"
    
    quotation_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=False)
    quotation_date = Column(Date)
    total_amount = Column(Numeric(12, 2))
    currency = Column(String(10), default="USD")
    status = Column(String(50), default="Draft")
    
    # Relationships
    customer = relationship("Customer", back_populates="quotations")
    items = relationship("QuotationItem", back_populates="quotation")

class QuotationItem(Base):
    __tablename__ = "quotation_items"
    
    item_id = Column(Integer, primary_key=True)
    quotation_id = Column(Integer, ForeignKey("quotations.quotation_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    quantity = Column(Numeric(12, 2))
    unit_price = Column(Numeric(12, 2))
    total_price = Column(Numeric(12, 2))
    
    # Relationships
    quotation = relationship("Quotation", back_populates="items")
    product = relationship("Product", back_populates="quotation_items")

# ... Continue for other entities (ProformaInvoice, SaleOrder, Contract, etc.)
```

**api/models/__init__.py**
```python
from api.models.master_data_models import (
    Customer,
    Product,
    Staff,
    Quotation,
    QuotationItem,
)

__all__ = ["Customer", "Product", "Staff", "Quotation", "QuotationItem"]
```

### Phase 3: Migrate & Organize Schemas (Week 2)

#### Step 3.1: Reorganize Existing Schemas

Keep existing schemas in `Back_end_TS_Sales/schemas/` but update them to use the new model naming convention.

**api/schemas/master_data.py** (NEW - consolidate all master data schemas)
```python
from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from datetime import date

# ==================== CUSTOMER ====================
class CustomerBase(BaseModel):
    customer_type: Optional[str] = None
    customer_code: Optional[str] = None
    company_name: str
    short_name: Optional[str] = None
    tax_id: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    status: Optional[str] = "Active"
    preferred_currency: Optional[str] = "USD"

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    company_name: Optional[str] = None

class CustomerResponse(CustomerCreate):
    customer_id: int
    model_config = ConfigDict(from_attributes=True)

# ==================== PRODUCT ====================
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: Optional[float] = None
    product_type: Optional[str] = None
    is_active: Optional[bool] = True

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductResponse(ProductCreate):
    product_id: int
    model_config = ConfigDict(from_attributes=True)

# ==================== STAFF ====================
class StaffBase(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None

class StaffCreate(StaffBase):
    pass

class StaffUpdate(StaffBase):
    pass

class StaffResponse(StaffCreate):
    staff_id: int
    model_config = ConfigDict(from_attributes=True)

# ... Continue for other entities
```

**api/schemas/__init__.py**
```python
# Re-export commonly used schemas
from api.schemas.master_data import (
    CustomerCreate,
    CustomerResponse,
    CustomerUpdate,
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)

__all__ = [
    "CustomerCreate",
    "CustomerResponse",
    "CustomerUpdate",
    "ProductCreate",
    "ProductResponse",
    "ProductUpdate",
]
```

### Phase 4: Create Repository Layer (Week 2-3)

#### Step 4.1: Create BaseRepository

**api/repositories/base_repository.py**
```python
from typing import Any, Generic, TypeVar
from sqlalchemy import select
from sqlalchemy.orm import Session

T = TypeVar("T")

class BaseRepository(Generic[T]):
    def __init__(self, model: type[T]):
        self.model = model

    def list(self, db: Session, offset: int = 0, limit: int = 100) -> list[T]:
        stmt = select(self.model).offset(offset).limit(limit)
        return list(db.scalars(stmt).all())

    def get(self, db: Session, entity_id: Any) -> T | None:
        return db.get(self.model, entity_id)

    def create(self, db: Session, payload: dict[str, Any]) -> T:
        entity = self.model(**payload)
        db.add(entity)
        db.commit()
        db.refresh(entity)
        return entity

    def update(self, db: Session, entity: T, payload: dict[str, Any]) -> T:
        for field, value in payload.items():
            if hasattr(entity, field):
                setattr(entity, field, value)
        db.commit()
        db.refresh(entity)
        return entity

    def delete(self, db: Session, entity: T) -> None:
        db.delete(entity)
        db.commit()

    # Custom query methods can be added here
    def filter_by(self, db: Session, **kwargs) -> list[T]:
        """Filter entities by attributes"""
        stmt = select(self.model).filter_by(**kwargs)
        return list(db.scalars(stmt).all())
```

#### Step 4.2: Create Concrete Repositories

**api/repositories/master_data_repository.py**
```python
from api.models.master_data_models import (
    Customer,
    Product,
    Staff,
    Quotation,
    QuotationItem,
)
from api.repositories.base_repository import BaseRepository

# Instantiate repositories for each model
customer_repository = BaseRepository[Customer](Customer)
product_repository = BaseRepository[Product](Product)
staff_repository = BaseRepository[Staff](Staff)
quotation_repository = BaseRepository[Quotation](Quotation)
quotation_item_repository = BaseRepository[QuotationItem](QuotationItem)
```

**api/repositories/__init__.py**
```python
from api.repositories.master_data_repository import (
    customer_repository,
    product_repository,
    staff_repository,
    quotation_repository,
)

__all__ = [
    "customer_repository",
    "product_repository",
    "staff_repository",
    "quotation_repository",
]
```

### Phase 5: Create Service Layer (Week 3)

#### Step 5.1: Create Generic Services

**api/services/master_data_service.py**
```python
from typing import Any
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from api.repositories.base_repository import BaseRepository

def list_entities(repository: BaseRepository, db: Session, 
                 offset: int = 0, limit: int = 100):
    """List entities with pagination"""
    return repository.list(db, offset=offset, limit=limit)

def get_entity_or_404(repository: BaseRepository, db: Session, 
                      entity_id: Any, entity_name: str):
    """Get entity by ID or raise 404"""
    entity = repository.get(db, entity_id)
    if entity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{entity_name} not found: {entity_id}",
        )
    return entity

def create_entity(repository: BaseRepository, db: Session, 
                 payload: dict[str, Any], entity_name: str):
    """Create entity with error handling"""
    try:
        return repository.create(db, payload)
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create {entity_name}: {str(exc)}",
        ) from exc

def update_entity(repository: BaseRepository, db: Session, 
                 entity: Any, payload: dict[str, Any], entity_name: str):
    """Update entity with error handling"""
    try:
        return repository.update(db, entity, payload)
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update {entity_name}: {str(exc)}",
        ) from exc

def delete_entity(repository: BaseRepository, db: Session, 
                 entity: Any, entity_name: str):
    """Delete entity with error handling"""
    try:
        repository.delete(db, entity)
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to delete {entity_name}: {str(exc)}",
        ) from exc
```

**api/services/__init__.py**
```python
from api.services.master_data_service import (
    create_entity,
    delete_entity,
    get_entity_or_404,
    list_entities,
    update_entity,
)

__all__ = [
    "create_entity",
    "delete_entity",
    "get_entity_or_404",
    "list_entities",
    "update_entity",
]
```

### Phase 6: Create API Routers (Week 3-4)

#### Step 6.1: Create Master Data Router

**api/routers/master_data_router.py**
```python
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from api.dependencies.db import get_db
from api.repositories.master_data_repository import (
    customer_repository,
    product_repository,
    staff_repository,
)
from api.schemas.master_data import (
    CustomerCreate,
    CustomerResponse,
    CustomerUpdate,
    ProductCreate,
    ProductResponse,
    ProductUpdate,
    StaffCreate,
    StaffResponse,
    StaffUpdate,
)
from api.services.master_data_service import (
    create_entity,
    delete_entity,
    get_entity_or_404,
    list_entities,
    update_entity,
)

router = APIRouter(prefix="/master-data", tags=["Master Data"])

# ==================== CUSTOMER ENDPOINTS ====================
@router.get("/customers", response_model=list[CustomerResponse])
def list_customers(offset: int = 0, limit: int = 100, 
                  db: Session = Depends(get_db)):
    return list_entities(customer_repository, db, offset, limit)

@router.post("/customers", response_model=CustomerResponse, 
            status_code=status.HTTP_201_CREATED)
def create_customer(payload: CustomerCreate, db: Session = Depends(get_db)):
    return create_entity(customer_repository, db, 
                        payload.model_dump(), "customer")

@router.get("/customers/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    return get_entity_or_404(customer_repository, db, 
                            customer_id, "Customer")

@router.put("/customers/{customer_id}", response_model=CustomerResponse)
def update_customer(customer_id: int, payload: CustomerUpdate, 
                   db: Session = Depends(get_db)):
    entity = get_entity_or_404(customer_repository, db, 
                              customer_id, "Customer")
    return update_entity(customer_repository, db, entity, 
                        payload.model_dump(exclude_unset=True), "customer")

@router.delete("/customers/{customer_id}", 
              status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    entity = get_entity_or_404(customer_repository, db, 
                              customer_id, "Customer")
    delete_entity(customer_repository, db, entity, "customer")

# ==================== PRODUCT ENDPOINTS ====================
@router.get("/products", response_model=list[ProductResponse])
def list_products(offset: int = 0, limit: int = 100, 
                 db: Session = Depends(get_db)):
    return list_entities(product_repository, db, offset, limit)

@router.post("/products", response_model=ProductResponse, 
            status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    return create_entity(product_repository, db, 
                        payload.model_dump(), "product")

@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return get_entity_or_404(product_repository, db, 
                            product_id, "Product")

@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, payload: ProductUpdate, 
                  db: Session = Depends(get_db)):
    entity = get_entity_or_404(product_repository, db, 
                              product_id, "Product")
    return update_entity(product_repository, db, entity, 
                        payload.model_dump(exclude_unset=True), "product")

@router.delete("/products/{product_id}", 
              status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    entity = get_entity_or_404(product_repository, db, 
                              product_id, "Product")
    delete_entity(product_repository, db, entity, "product")

# ==================== STAFF ENDPOINTS ====================
@router.get("/staff", response_model=list[StaffResponse])
def list_staff(offset: int = 0, limit: int = 100, 
              db: Session = Depends(get_db)):
    return list_entities(staff_repository, db, offset, limit)

@router.post("/staff", response_model=StaffResponse, 
            status_code=status.HTTP_201_CREATED)
def create_staff(payload: StaffCreate, db: Session = Depends(get_db)):
    return create_entity(staff_repository, db, 
                        payload.model_dump(), "staff")

@router.get("/staff/{staff_id}", response_model=StaffResponse)
def get_staff(staff_id: int, db: Session = Depends(get_db)):
    return get_entity_or_404(staff_repository, db, 
                            staff_id, "Staff")

@router.put("/staff/{staff_id}", response_model=StaffResponse)
def update_staff(staff_id: int, payload: StaffUpdate, 
                db: Session = Depends(get_db)):
    entity = get_entity_or_404(staff_repository, db, 
                              staff_id, "Staff")
    return update_entity(staff_repository, db, entity, 
                        payload.model_dump(exclude_unset=True), "staff")

@router.delete("/staff/{staff_id}", 
              status_code=status.HTTP_204_NO_CONTENT)
def delete_staff(staff_id: int, db: Session = Depends(get_db)):
    entity = get_entity_or_404(staff_repository, db, 
                              staff_id, "Staff")
    delete_entity(staff_repository, db, entity, "staff")
```

**api/routers/__init__.py**
```python
from api.routers.master_data_router import router as master_data_router

__all__ = ["master_data_router"]
```

### Phase 7: Create Main Application (Week 4)

#### Step 7.1: Create FastAPI Application

**api/main.py**
```python
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from api.dependencies.db import get_db
from api.routers.master_data_router import router as master_data_router

app = FastAPI(
    title="Back_end TS Sales API",
    version="1.0.0",
    description="API for Trading and Sales management system",
)

# Include routers
app.include_router(master_data_router)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Back_end TS Sales API",
        "docs": "/docs",
        "version": "1.0.0",
    }

@app.get("/health-check")
def health_check(db: Session = Depends(get_db)):
    try:
        result = db.execute(
            text("SELECT 'Connection OK' FROM DUAL")
        ).fetchone()
        return {
            "database_status": "Connected",
            "oracle_response": result[0],
        }
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Database connection failed: {str(exc)}",
        ) from exc
```

**run.py** (in Back_end_TS_Sales root)
```python
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "api.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
```

### Phase 8: Final Structure & Testing

#### Step 8.1: Final Directory Structure

```
Back_end_TS_Sales/
├── api/
│   ├── __init__.py
│   ├── main.py                          # FastAPI app
│   ├── constants/
│   │   └── __init__.py
│   ├── dependencies/
│   │   ├── __init__.py
│   │   └── db.py                        # get_db
│   ├── models/
│   │   ├── __init__.py
│   │   └── master_data_models.py        # SQLAlchemy models
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── base_repository.py           # Generic CRUD
│   │   └── master_data_repository.py    # Concrete repos
│   ├── routers/
│   │   ├── __init__.py
│   │   └── master_data_router.py        # API endpoints
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── master_data.py               # Pydantic schemas
│   ├── services/
│   │   ├── __init__.py
│   │   └── master_data_service.py       # Business logic
│   └── utils/
│       ├── __init__.py
│       ├── database.py                  # SQLAlchemy setup
│       ├── db.py                        # get_db
│       └── oracle_settings.py           # DB config
├── run.py                               # Application entry point
├── requirements.txt
├── test.py                              # Tests
└── README.md
```

#### Step 8.2: Testing the API

```bash
# Install dependencies
pip install fastapi uvicorn sqlalchemy oracledb pydantic

# Set environment variables
set ORACLE_USER=ts_sales_user
set ORACLE_PASSWORD=GCFood2026
set ORACLE_HOST=localhost
set ORACLE_PORT=1521
set ORACLE_SERVICE=FREEPDB1

# Run the application
python run.py

# Test endpoints
curl http://localhost:8000/
curl http://localhost:8000/health-check
curl http://localhost:8000/docs  # Interactive API docs
```

---

## 5. Migration Strategy for Existing Schemas

### 5.1 Consolidate Schemas

The existing `Back_end_TS_Sales/schemas/` directory has many individual schema files. These should be consolidated into the new `api/schemas/` directory following the pattern:

```
OLD:  schemas/customer_schema.py → api/schemas/master_data.py
      schemas/product_schema.py   ↓
      schemas/staff_schema.py
```

### 5.2 Schema Compatibility

Ensure backward compatibility:
1. Keep all existing field names
2. Keep all existing field types
3. Update only the structure and location
4. Add `from_attributes=True` to Response models

### 5.3 Database Mapping

Schemas → Models → Database Tables:

```python
# Schema
class CustomerCreate(CustomerBase):
    pass

# Model
class Customer(Base):
    __tablename__ = "customers"
    customer_id = Column(Integer, primary_key=True)
    company_name = Column(String(255), nullable=False)
    # ...

# Database
CREATE TABLE customers (
    customer_id NUMBER PRIMARY KEY,
    company_name VARCHAR2(255) NOT NULL,
    -- ...
);
```

---

## 6. Quick Reference: From VietFarm to Back_end_TS_Sales

### Copy These Files (with modifications for entity names):

| File | From | To | Notes |
|------|------|-----|-------|
| `base_repository.py` | VietFarm_API/api/repositories/ | Back_end_TS_Sales/api/repositories/ | Use as-is |
| `database.py` | VietFarm_API/api/utils/ | Back_end_TS_Sales/api/utils/ | Update DB name |
| `oracle_settings.py` | VietFarm_API/api/utils/ | Back_end_TS_Sales/api/utils/ | Update user/password |
| `db.py` | VietFarm_API/api/utils/ | Back_end_TS_Sales/api/utils/ | Use as-is |
| `master_data_service.py` | VietFarm_API/api/services/ | Back_end_TS_Sales/api/services/ | Rename to master_data_service.py |
| `master_data_router.py` | VietFarm_API/api/routers/ | Back_end_TS_Sales/api/routers/ | Update entity names |

### Create Fresh (based on VietFarm pattern):

| File | Template From | Customize For |
|------|---------------|---------------|
| `api/models/master_data_models.py` | VietFarm_API/api/models/master_data_models.py | Customer, Product, Staff, Quotation, etc. |
| `api/schemas/master_data.py` | VietFarm_API/api/schemas/master_data.py | Your existing schemas |
| `api/repositories/master_data_repository.py` | VietFarm_API/api/repositories/master_data_repository.py | Your entities |
| `api/routers/master_data_router.py` | VietFarm_API/api/routers/master_data_router.py | Your endpoints |
| `api/main.py` | VietFarm_API/api/main.py | Your app metadata |

---

## 7. Implementation Checklist

- [ ] **Phase 1: Setup Foundation**
  - [ ] Create directory structure
  - [ ] Create `oracle_settings.py`
  - [ ] Create `database.py`
  - [ ] Create `db.py`
  - [ ] Create `dependencies/db.py`

- [ ] **Phase 2: Create Models**
  - [ ] Analyze existing schemas for field mapping
  - [ ] Create `master_data_models.py` with all entities
  - [ ] Define relationships between models
  - [ ] Create `__init__.py` exports

- [ ] **Phase 3: Migrate Schemas**
  - [ ] Create `api/schemas/master_data.py`
  - [ ] Migrate CustomerBase/CustomerCreate/CustomerUpdate/CustomerResponse
  - [ ] Migrate ProductBase/ProductCreate/ProductUpdate/ProductResponse
  - [ ] Migrate other entity schemas
  - [ ] Update schema imports

- [ ] **Phase 4: Repository Layer**
  - [ ] Create `base_repository.py`
  - [ ] Create `master_data_repository.py`
  - [ ] Instantiate repositories for each model
  - [ ] Create `repositories/__init__.py`

- [ ] **Phase 5: Service Layer**
  - [ ] Create `master_data_service.py`
  - [ ] Implement generic CRUD service functions
  - [ ] Create `services/__init__.py`

- [ ] **Phase 6: API Routers**
  - [ ] Create `master_data_router.py`
  - [ ] Define GET /master-data/{entities}
  - [ ] Define POST /master-data/{entities}
  - [ ] Define GET /master-data/{entities}/{id}
  - [ ] Define PUT /master-data/{entities}/{id}
  - [ ] Define DELETE /master-data/{entities}/{id}
  - [ ] Create `routers/__init__.py`

- [ ] **Phase 7: Main Application**
  - [ ] Create `api/main.py` with FastAPI app
  - [ ] Include routers
  - [ ] Create health-check endpoint
  - [ ] Create `run.py`

- [ ] **Phase 8: Testing & Documentation**
  - [ ] Test all CRUD endpoints
  - [ ] Verify database connections
  - [ ] Update `requirements.txt`
  - [ ] Create `README.md` with setup instructions

---

## 8. Code Examples: Side-by-Side Comparison

### Example 1: Creating a Customer

#### Before (Manual, no architecture):
```python
# test.py
response = requests.post(
    "http://127.0.0.1:8000/customers",
    json={
        "company_name": "ABC Corp",
        "address": "Street 1"
    }
)
print(response.json())
```

#### After (VietFarm pattern):
```python
# Direct initialization
from api.main import app
from api.dependencies.db import get_db
from api.schemas.master_data import CustomerCreate

# Via HTTP (FastAPI):
curl -X POST "http://localhost:8000/master-data/customers" \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "ABC Corp",
    "address": "Street 1",
    "country": "Vietnam",
    "city": "Hanoi"
  }'

# Response:
{
  "customer_id": 1,
  "company_name": "ABC Corp",
  "address": "Street 1",
  "country": "Vietnam",
  "city": "Hanoi",
  "status": "Active",
  "preferred_currency": "USD"
}
```

### Example 2: Getting a Customer

#### Before (Unclear):
```python
# test.py
response = requests.get("http://127.0.0.1:8000/customers/1")
```

#### After (VietFarm pattern):
```python
# Endpoint: GET /master-data/customers/1
curl "http://localhost:8000/master-data/customers/1"

# Response:
{
  "customer_id": 1,
  "company_name": "ABC Corp",
  "address": "Street 1",
  "country": "Vietnam",
  "city": "Hanoi",
  "status": "Active",
  "preferred_currency": "USD"
}

# If not found (404):
{
  "detail": "Customer not found: 1"
}
```

### Example 3: Code Flow (Request → Response)

```
Request: POST /master-data/customers

1. Router (api/routers/master_data_router.py):
   @router.post("/customers", response_model=CustomerResponse)
   def create_customer(payload: CustomerCreate, db: Session = Depends(get_db)):

2. Service (api/services/master_data_service.py):
   return create_entity(customer_repository, db, 
                       payload.model_dump(), "customer")

3. Repository (api/repositories/master_data_repository.py):
   repository.create(db, payload)

4. BaseRepository (api/repositories/base_repository.py):
   entity = Customer(**payload)             # Model instantiation
   db.add(entity)                          # Add to session
   db.commit()                             # Commit transaction
   db.refresh(entity)                      # Refresh from DB
   return entity

5. Database Connection (api/utils/database.py):
   INSERT INTO customers (company_name, ...) VALUES (...)

Response: CustomerResponse (200 OK)
```

---

## 9. Best Practices & Tips

### 9.1 Naming Conventions
- Entity names: CamelCase (Customer, Product)
- Database tables: lowercase (customers, products)
- Router prefixes: kebab-case (/master-data)
- Endpoint names: plural nouns (/customers)
- Function names: snake_case (list_entities, get_customer)
- File names: snake_case (master_data_router.py)

### 9.2 Error Handling
```python
# Good: Specific error messages
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=f"Customer not found: {customer_id}",
)

# Bad: Generic errors
raise HTTPException(status_code=404)
```

### 9.3 Database Sessions
```python
# Good: Always close sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Always use with Depends
@router.get("/customers")
def list_customers(db: Session = Depends(get_db)):
    pass
```

### 9.4 Pagination
```python
# Always support offset/limit
@router.get("/customers")
def list_customers(
    offset: int = 0, 
    limit: int = 100,  # Max 100
    db: Session = Depends(get_db)
):
    return repository.list(db, offset=offset, limit=limit)
```

### 9.5 Validation
```python
# Use Pydantic models for validation
class CustomerCreate(CustomerBase):
    pass  # Pydantic handles validation

# Use from_attributes for SQLAlchemy models
class CustomerResponse(CustomerCreate):
    model_config = ConfigDict(from_attributes=True)
```

---

## 10. Troubleshooting & FAQ

### Q: How do I handle relationships (Customer → Quotations)?
**A:** Use SQLAlchemy relationships in models:
```python
class Customer(Base):
    quotations = relationship("Quotation", back_populates="customer")

class Quotation(Base):
    customer = relationship("Customer", back_populates="quotations")
```

### Q: What if I have complex business logic?
**A:** Create domain-specific service functions:
```python
# api/services/quotation_service.py
def create_quotation_with_items(db, customer_id, items_data):
    # Custom business logic here
    ...
```

### Q: How do I handle database migrations?
**A:** Use Alembic (migration tool):
```bash
alembic init alembic
alembic revision --autogenerate -m "Create customers table"
alembic upgrade head
```

### Q: How do I test the API?
**A:** Use FastAPI's TestClient:
```python
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)
response = client.get("/master-data/customers")
assert response.status_code == 200
```

---

## Summary

The **VietFarm_API architecture** showcases a clean, scalable pattern for FastAPI applications:

1. **Models** (SQLAlchemy) ← Define database structure
2. **Schemas** (Pydantic) ← Validate request/response data
3. **Repositories** (Generic CRUD) ← Abstract database queries
4. **Services** (Business logic) ← Handle errors and workflow
5. **Routers** (Endpoints) ← Define HTTP interfaces
6. **Dependencies** (DI) ← Inject database sessions
7. **Utils** (Configuration) ← Manage settings and connections

**Back_end_TS_Sales** should adopt this architecture to:
- Reuse existing schemas
- Gain clear separation of concerns
- Enable easy testing and maintenance
- Follow industry best practices
- Support multiple entities with minimal code duplication

Follow the **8-phase implementation plan** to gradually migrate from the current schema-only state to a full-featured API!
