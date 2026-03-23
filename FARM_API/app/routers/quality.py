from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import SessionLocal
from ..models import quality as quality_models
from ..schemas import schemas

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- QC RECEIVING ---
@router.post("/qc-receiving/", response_model=schemas.QCReceiving)
def create_qc_receiving(qc: schemas.QCReceivingCreate, db: Session = Depends(get_db)):
    db_qc = quality_models.QCReceiving(**qc.dict())
    db = db
    db.add(db_qc)
    db.commit()
    db.refresh(db_qc)
    return db_qc

@router.get("/qc-receiving/", response_model=List[schemas.QCReceiving])
def read_qc_receiving(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(quality_models.QCReceiving).offset(skip).limit(limit).all()

# --- QC HARVEST ---
@router.post("/qc-harvest/", response_model=schemas.QCHarvest)
def create_qc_harvest(qc: schemas.QCHarvestCreate, db: Session = Depends(get_db)):
    db_qc = quality_models.QCHarvest(**qc.dict())
    db.add(db_qc)
    db.commit()
    db.refresh(db_qc)
    return db_qc

@router.get("/qc-harvest/", response_model=List[schemas.QCHarvest])
def read_qc_harvest(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(quality_models.QCHarvest).offset(skip).limit(limit).all()

# --- QC PRODUCT LOT ---
@router.post("/qc-product-lot/", response_model=schemas.QCProductLot)
def create_qc_product_lot(qc: schemas.QCProductLotCreate, db: Session = Depends(get_db)):
    db_qc = quality_models.QCProductLot(**qc.dict())
    db.add(db_qc)
    db.commit()
    db.refresh(db_qc)
    return db_qc

@router.get("/qc-product-lot/", response_model=List[schemas.QCProductLot])
def read_qc_product_lot(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(quality_models.QCProductLot).offset(skip).limit(limit).all()

