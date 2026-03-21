from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import SessionLocal
from ..models import cultivation as models
from ..schemas import schemas

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- CULTIVATION LOG ---
@router.post("/cultivation-logs/", response_model=schemas.CultivationLog)
def create_cultivation_log(log: schemas.CultivationLogCreate, db: Session = Depends(get_db)):
    db_log = models.CultivationLog(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

@router.get("/cultivation-logs/", response_model=List[schemas.CultivationLog])
def read_cultivation_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.CultivationLog).offset(skip).limit(limit).all()
