from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import text

from api.database import engine, Base
from api.dependencies.db import get_db

from api.routers import (
    customer_router,
    quotation_router,
    proforma_router,
    contract_router,
    sale_order_router
)


# =========================================================
# 1. Khởi tạo FastAPI
# =========================================================

app = FastAPI(
    title="HQ CRM/ERP API",
    version="1.0.0",
    description="Headquarter CRM/ERP API for Customer, Quotation, Contract and Sales Order management"
)

# =========================================================
# 1.5. Mount Static Files (UI)
# =========================================================
app.mount("/static", StaticFiles(directory="api/static"), name="static")

# =========================================================
# 2. Tạo bảng (chỉ dùng cho development)
# Production nên dùng Alembic migration
# =========================================================

# Base.metadata.create_all(bind=engine)


# =========================================================
# 3. Register Routers
# =========================================================

app.include_router(customer_router.router)
app.include_router(quotation_router.router)
app.include_router(proforma_router.router)
app.include_router(contract_router.router)
app.include_router(sale_order_router.router)


# =========================================================
# 4. Root Endpoint
# =========================================================

@app.get("/")
def read_root():
    return RedirectResponse(url="/static/index.html")


# =========================================================
# 5. Health Check Endpoint
# Kiểm tra kết nối Oracle
# =========================================================

@app.get("/health-check")
def health_check(db: Session = Depends(get_db)):
    try:

        result = db.execute(
            text("SELECT 'Connection OK' FROM DUAL")
        ).fetchone()

        return {
            "database_status": "Connected",
            "oracle_response": result[0]
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Database connection failed: {str(e)}"
        )