from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from api.dependencies.db import get_db
from api.routers.master_data_router import router as master_data_router
from api.routers.transaction_router import router as transaction_router

app = FastAPI(
    title="VietFarm Aloe Supply Chain API",
    version="1.0.0",
    description="API for master data CRUD and transaction data creation",
)

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
        result = db.execute(
            text("SELECT 'Connection OK' FROM DUAL")).fetchone()
        return {
            "database_status": "Connected",
            "oracle_response": result[0],
        }
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail=f"Database connection failed: {str(exc)}") from exc
