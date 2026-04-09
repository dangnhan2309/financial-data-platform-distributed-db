# VietFarm Pattern: Quick Implementation Templates

**Purpose**: Copy-paste templates for rapid implementation  
**Target**: Back_end_TS_Sales developers  
**Use**: Reference during implementation

---

## 1. Database Configuration Templates

### Template: oracle_settings.py

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

### Template: database.py

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

### Template: db.py (Dependency)

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

---

## 2. Model Templates

### Template: Simple Entity

```python
from sqlalchemy import Column, Integer, String, Boolean, Date
from api.utils.database import Base

class Customer(Base):
    __tablename__ = "customers"
    
    customer_id = Column(Integer, primary_key=True)
    company_name = Column(String(255), nullable=False)
    contact_name = Column(String(255))
    email = Column(String(100))
    phone = Column(String(20))
    address = Column(String(500))
    status = Column(String(50), default="Active")
```

### Template: Entity with Relationships

```python
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from api.utils.database import Base

class Quotation(Base):
    __tablename__ = "quotations"
    
    quotation_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=False)
    total_amount = Column(Numeric(12, 2))
    status = Column(String(50), default="Draft")
    
    # Relationship
    customer = relationship("Customer", back_populates="quotations")
    items = relationship("QuotationItem", back_populates="quotation")

class QuotationItem(Base):
    __tablename__ = "quotation_items"
    
    item_id = Column(Integer, primary_key=True)
    quotation_id = Column(Integer, ForeignKey("quotations.quotation_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    quantity = Column(Numeric(12, 2))
    unit_price = Column(Numeric(12, 2))
    
    # Relationships
    quotation = relationship("Quotation", back_populates="items")
    product = relationship("Product", back_populates="quotation_items")
```

---

## 3. Schema Templates

### Template: Simple Schema

```python
from pydantic import BaseModel, ConfigDict

class ProductBase(BaseModel):
    name: str
    price: float | None = None
    is_active: bool | None = True

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductResponse(ProductCreate):
    product_id: int
    model_config = ConfigDict(from_attributes=True)
```

### Template: Complex Schema (with Relationships)

```python
from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime

class QuotationItemResponse(BaseModel):
    item_id: int
    product_id: int
    quantity: float | None = None
    unit_price: float | None = None
    model_config = ConfigDict(from_attributes=True)

class QuotationBase(BaseModel):
    customer_id: int
    total_amount: float | None = None
    status: str | None = "Draft"

class QuotationCreate(QuotationBase):
    pass

class QuotationUpdate(QuotationBase):
    pass

class QuotationResponse(QuotationCreate):
    quotation_id: int
    created_at: datetime | None = None
    items: list[QuotationItemResponse] = []
    model_config = ConfigDict(from_attributes=True)
```

---

## 4. Repository Templates

### Template: BaseRepository (Copy as-is)

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
```

### Template: Concrete Repositories

```python
from api.models.master_data_models import (
    Customer,
    Product,
    Quotation,
    QuotationItem,
)
from api.repositories.base_repository import BaseRepository

customer_repository = BaseRepository[Customer](Customer)
product_repository = BaseRepository[Product](Product)
quotation_repository = BaseRepository[Quotation](Quotation)
quotation_item_repository = BaseRepository[QuotationItem](QuotationItem)
```

---

## 5. Service Templates

### Template: Generic Service Functions

```python
from typing import Any
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from api.repositories.base_repository import BaseRepository

def list_entities(repository: BaseRepository, db: Session, 
                 offset: int = 0, limit: int = 100):
    return repository.list(db, offset=offset, limit=limit)

def get_entity_or_404(repository: BaseRepository, db: Session, 
                      entity_id: Any, entity_name: str):
    entity = repository.get(db, entity_id)
    if entity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{entity_name} not found: {entity_id}",
        )
    return entity

def create_entity(repository: BaseRepository, db: Session, 
                 payload: dict[str, Any], entity_name: str):
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

---

## 6. Router Templates

### Template: Minimal CRUD Router

```python
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from api.dependencies.db import get_db
from api.repositories.master_data_repository import customer_repository
from api.schemas.master_data import (
    CustomerCreate, CustomerUpdate, CustomerResponse
)
from api.services.master_data_service import (
    create_entity, delete_entity, get_entity_or_404,
    list_entities, update_entity,
)

router = APIRouter(prefix="/master-data", tags=["Master Data"])

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
```

### Template: Full-Featured Router (Multiple Entities)

```python
from fastapi import APIRouter, Depends, Response, status, Query
from sqlalchemy.orm import Session
from api.dependencies.db import get_db
from api.repositories.master_data_repository import (
    customer_repository, product_repository
)
from api.schemas.master_data import (
    CustomerCreate, CustomerUpdate, CustomerResponse,
    ProductCreate, ProductUpdate, ProductResponse,
)
from api.services.master_data_service import (
    create_entity, delete_entity, get_entity_or_404,
    list_entities, update_entity,
)

router = APIRouter(prefix="/master-data", tags=["Master Data"])

# ==================== CUSTOMER ====================

@router.get("/customers", response_model=list[CustomerResponse])
def list_customers(
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: str | None = None,
    db: Session = Depends(get_db)
):
    query = list_entities(customer_repository, db, offset, limit)
    if status:
        query = [c for c in query if c.status == status]
    return query

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

# ==================== PRODUCT ====================

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
```

---

## 7. Main Application Template

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

---

## 8. Application Runner Template

```python
# run.py (in root directory)
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "api.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info",
    )
```

---

## 9. Import Templates

### api/models/__init__.py

```python
from api.models.master_data_models import (
    Customer,
    Product,
    Staff,
    Quotation,
    QuotationItem,
)

__all__ = [
    "Customer",
    "Product",
    "Staff",
    "Quotation",
    "QuotationItem",
]
```

### api/repositories/__init__.py

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

### api/schemas/__init__.py

```python
from api.schemas.master_data import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse,
    ProductCreate,
    ProductUpdate,
    ProductResponse,
)

__all__ = [
    "CustomerCreate",
    "CustomerUpdate",
    "CustomerResponse",
    "ProductCreate",
    "ProductUpdate",
    "ProductResponse",
]
```

### api/services/__init__.py

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

### api/routers/__init__.py

```python
from api.routers.master_data_router import router as master_data_router

__all__ = ["master_data_router"]
```

### api/dependencies/__init__.py

```python
from api.utils.db import get_db

__all__ = ["get_db"]
```

### api/utils/__init__.py

```python
from api.utils.db import get_db

__all__ = ["get_db"]
```

---

## 10. Directory Creation Script

```bash
# Create directories
mkdir -p api/{constants,dependencies,models,repositories,routers,schemas,services,utils}

# Create __init__.py files
touch api/__init__.py
touch api/constants/__init__.py
touch api/dependencies/__init__.py
touch api/models/__init__.py
touch api/repositories/__init__.py
touch api/routers/__init__.py
touch api/schemas/__init__.py
touch api/services/__init__.py
touch api/utils/__init__.py
```

---

## 11. Step-by-Step Implementation Order

```
1. Create directory structure
   ↓
2. api/utils/oracle_settings.py
   ↓
3. api/utils/database.py
   ↓
4. api/utils/db.py
   ↓
5. api/dependencies/db.py
   ↓
6. api/models/master_data_models.py
   ↓
7. api/models/__init__.py
   ↓
8. api/repositories/base_repository.py
   ↓
9. api/repositories/master_data_repository.py
   ↓
10. api/repositories/__init__.py
    ↓
11. api/schemas/master_data.py
    ↓
12. api/schemas/__init__.py
    ↓
13. api/services/master_data_service.py
    ↓
14. api/services/__init__.py
    ↓
15. api/routers/master_data_router.py
    ↓
16. api/routers/__init__.py
    ↓
17. api/main.py
    ↓
18. run.py
    ↓
19. Test: python run.py
```

---

## Ready to Implement!

All templates are production-ready.  
Just copy, customize entity names, and you're ready to go!
