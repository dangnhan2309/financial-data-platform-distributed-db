from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db, engine, Base

# 1. Khởi tạo ứng dụng FastAPI
app = FastAPI(title="Financial Data Platform API")

# 2. Tạo các bảng trong Database (nếu bạn đã định nghĩa Model)
# Lưu ý: Trong thực tế, người ta thường dùng Alembic để quản lý migration
# Base.metadata.create_all(bind=engine)

# 3. Root Endpoint: Kiểm tra server có sống hay không
@app.get("/")
def read_root():
    return {
        "message": "Welcome to Financial Data Platform API",
        "status": "Server is running",
        "docs": "/docs"
    }

# 4. Health Check Endpoint: Kiểm tra kết nối trực tiếp tới Oracle
@app.get("/health-check")
def health_check(db: Session = Depends(get_db)):
    try:
        # Thực hiện một câu lệnh SQL đơn giản nhất trên Oracle
        result = db.execute(text("SELECT 'Connection OK' FROM DUAL")).fetchone()
        return {
            "database_status": "Connected",
            "oracle_response": result[0]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")