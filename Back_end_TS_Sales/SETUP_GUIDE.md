# GC Food TS Sales Backend - Setup & Connection Guide

✅ **Foundation Setup Complete!**

---

## 📁 Folder Structure Created

```
Back_end_TS_Sales/
├── api/
│   ├── main.py                    ← FastAPI app (routers to be added)
│   ├── models/
│   │   └── __init__.py            ← Base model definition
│   ├── schemas/                   ← (existing) Pydantic schemas
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── base_repository.py     ← Generic CRUD class
│   ├── services/
│   │   └── __init__.py            ← Service implementations go here
│   ├── routers/
│   │   └── __init__.py            ← API endpoint files go here
│   ├── dependencies/
│   │   ├── __init__.py
│   │   └── db.py                  ← Database session injection
│   └── utils/
│       ├── __init__.py
│       └── database.py            ← Oracle connection & config
├── .env.example                   ← Environment variables template
├── run.py                         ← Entry point to start server
└── test_db_connection.py          ← Test connection utility
```

---

## 🔌 Database Connection Setup

### Step 1: Install Required Packages

```bash
# Microsoft Windows
pip install fastapi uvicorn sqlalchemy python-oracledb python-dotenv

# Or if using conda
conda install fastapi uvicorn sqlalchemy python-oracledb python-dotenv
```

### Step 2: Configure Environment Variables

Copy `.env.example` to `.env` and update:

```env
# Database Configuration
DB_USER=ts_sales
DB_PASSWORD=ts_sales_pwd
DB_HOST=localhost           # Or your Oracle server IP
DB_PORT=1521
DB_SERVICE=orcl             # Your Oracle service name
```

**For VPN Access (26.110.112.160):**

If Backend is running on VPN machine, update to:
```env
DB_HOST=<VPN_IP_OF_ORACLE_SERVER>
```

### Step 3: Test Connection

Run the test script:

```bash
python test_db_connection.py
```

**Expected Output:**
```
✓ Connection Configuration:
  - User: ts_sales
  - Host: localhost
  - Port: 1521
  - Service: orcl

✅ SUCCESS: Database connection is working!
✅ SUCCESS: Session created successfully
✅ SUCCESS: Session closed successfully
```

If it fails, see **Troubleshooting** section below.

---

## 🚀 Starting the Server

```bash
python run.py
```

**Expected Output:**
```
🔍 Testing database connection...
✅ Database connection successful

🚀 Starting GC Food TS Sales API...
📍 API will run at: http://localhost:8000
📚 Swagger Docs: http://localhost:8000/docs
📖 ReDoc: http://localhost:8000/redoc

⏹️  Press Ctrl+C to stop the server
```

---

## 📚 API Documentation

When server is running, visit:

- **Swagger UI (Interactive):** http://localhost:8000/docs
- **ReDoc (Documentation):** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

---

## 🏗️ Architecture Components

### 1. **database.py** - Database Connection
- Creates SQLAlchemy engine
- Manages connection pooling
- Provides `SessionLocal` factory
- Helper functions: `init_db()`, `test_connection()`

### 2. **dependencies/db.py** - Session Injection
- FastAPI dependency for automatic session management
- Used in endpoints: `db: Session = Depends(get_db)`

### 3. **base_repository.py** - Generic CRUD
Generic operations for any model:
```python
repo = BaseRepository(db=session, model=Customer)
repo.get_all()              # Get all records
repo.get_by_id(1)           # Get by ID
repo.create(new_customer)   # Create
repo.update(1, data)        # Update
repo.delete(1)              # Delete
```

### 4. **models/__init__.py** - Base Model
- `BaseModel` class with `id`, `created_at`, `updated_at`
- All models inherit from this

### 5. **main.py** - FastAPI App
- Initializes FastAPI with CORS
- Auto-creates database tables on startup
- Health check endpoint
- Router registration point

---

## 📝 Next Steps - Creating API Endpoints

### Example: Create Customer Router

Create `api/routers/customer_router.py`:

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.dependencies import get_db
from api.repositories import BaseRepository
from api.models import Customer  # Will create this
from api.schemas.customer_schema import CustomerCreate, CustomerRead

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.get("/", response_model=list[CustomerRead])
async def list_customers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    repo = BaseRepository(db, Customer)
    return repo.get_all(skip=skip, limit=limit)

@router.post("/", response_model=CustomerRead)
async def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):
    repo = BaseRepository(db, Customer)
    new_customer = Customer(**customer.dict())
    return repo.create(new_customer)

@router.get("/{id}", response_model=CustomerRead)
async def get_customer(id: int, db: Session = Depends(get_db)):
    repo = BaseRepository(db, Customer)
    customer = repo.get_by_id(id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.put("/{id}", response_model=CustomerRead)
async def update_customer(
    id: int,
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):
    repo = BaseRepository(db, Customer)
    return repo.update(id, customer.dict())

@router.delete("/{id}")
async def delete_customer(id: int, db: Session = Depends(get_db)):
    repo = BaseRepository(db, Customer)
    if not repo.delete(id):
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": "Customer deleted"}
```

Then register in `api/main.py`:
```python
from api.routers import customer_router
app.include_router(customer_router.router, prefix="/api")
```

---

## 🐛 Troubleshooting

### Error: "Cannot connect to Oracle"

**Possible causes:**

1. **Oracle not running**
   ```bash
   # Check Oracle is running
   lsnrctl status
   ```

2. **Wrong credentials**
   ```bash
   # Test with SQL*Plus
   sqlplus ts_sales/ts_sales_pwd@//localhost:1521/orcl
   ```

3. **Python package missing**
   ```bash
   pip install --upgrade python-oracledb sqlalchemy
   ```

4. **Connection string error**
   - Check `.env` file for spaces or typos
   - Try quotes if password has special chars: `DB_PASSWORD="pass@word"`

### Error: "RelationalAlchemy" or Import errors

```bash
# Reinstall dependencies
pip uninstall sqlalchemy -y
pip install sqlalchemy oracledb
```

### Port 8000 already in use

Change port in `api/main.py` or `run.py`:
```python
uvicorn.run(..., port=8001)
```

---

## 🔍 Development Checklist

- [ ] Created `.env` file from `.env.example`
- [ ] Updated Oracle credentials in `.env`
- [ ] Tested connection with `python test_db_connection.py`
- [ ] Started server with `python run.py`
- [ ] Accessed Swagger UI at http://localhost:8000/docs
- [ ] API health check passes at http://localhost:8000/health
- [ ] Created first model in `api/models/`
- [ ] Created repository for model
- [ ] Created router with CRUD endpoints
- [ ] Tested endpoints in Swagger UI
- [ ] Connected frontend to backend API

---

## 📞 Support

For issues:
1. Check logs in terminal running `python run.py`
2. Run `python test_db_connection.py` to isolate DB issues
3. Check `.env` file syntax
4. Verify Oracle service name and credentials
5. Check firewall/network if using remote Oracle

---

**Ready to create models and endpoints!** 🚀
