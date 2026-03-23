from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import text

# Import database and dependencies
from app.database import engine, Base, get_db

# Import Routers
from app.routers import (
    farm,
    iot,
    cultivation,
    catalog,
    harvest,
    procurement,
    quality,
    warehouse,
    sales
)

# =========================================================
# 1. Khởi tạo FastAPI
# =========================================================

app = FastAPI(
    title="Smart Farm API",
    version="1.0.0",
    description="Smart Farm Management API for IoT, Cultivation, Harvest, and Procurement"
)

# =========================================================
# 1.5. Mount Static Files (UI)
# =========================================================

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# =========================================================
# 2. Tạo bảng (chỉ dùng cho development)
# =========================================================
# Base.metadata.create_all(bind=engine)

# =========================================================
# 3. Register Routers
# =========================================================

app.include_router(farm.router, tags=["Farm Management"])
app.include_router(iot.router, tags=["IoT System"])
app.include_router(cultivation.router, tags=["Cultivation"])
app.include_router(catalog.router, tags=["Catalog"])
app.include_router(harvest.router, tags=["Harvest"])
app.include_router(procurement.router, tags=["Procurement"])
app.include_router(quality.router, tags=["Quality Control"])
app.include_router(warehouse.router, tags=["Inventory & Warehouse"])
app.include_router(sales.router, tags=["B2C Sales"])


# =========================================================
# 4. Root Endpoint
# =========================================================

@app.get("/")
def read_root():
    return RedirectResponse(url="/static/index.html")


# =========================================================
# 5. Health Check Endpoint
# Kiểm tra kết nối Database (SQLite)
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


# =========================================================
# 6. DB Explorer (cho trang tĩnh cũ)
# =========================================================

@app.get("/api/db/tables")
def list_tables(db: Session = Depends(get_db)):
    """Liệt kê bảng của schema hiện tại (Oracle)."""
    result = db.execute(text("SELECT table_name FROM user_tables ORDER BY table_name"))
    return [row[0] for row in result]


@app.get("/api/db/preview/{table_name}")
def preview_table(table_name: str, limit: int = 100, db: Session = Depends(get_db)):
    """Xem nhanh dữ liệu bảng (tối đa `limit` dòng)."""
    # Lấy danh sách bảng hợp lệ để tránh SQL injection
    tables = [row[0] for row in db.execute(text("SELECT table_name FROM user_tables"))]
    if table_name.upper() not in tables:
        raise HTTPException(status_code=404, detail="Table not found")

    # Oracle mặc định lưu tên bảng UPPER; dùng FETCH FIRST để giới hạn
    query = text(f"SELECT * FROM {table_name.upper()} FETCH FIRST :limit ROWS ONLY")
    result = db.execute(query, {"limit": limit})
    rows = [dict(row._mapping) for row in result]
    return rows