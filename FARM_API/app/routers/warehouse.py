from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import SessionLocal
from ..models import warehouse as models
from ..schemas import schemas

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- WAREHOUSE ---
@router.post("/warehouses/", response_model=schemas.Warehouse)
def create_warehouse(warehouse: schemas.WarehouseCreate, db: Session = Depends(get_db)):
    db_warehouse = models.Warehouse(**warehouse.dict())
    db.add(db_warehouse)
    db.commit()
    db.refresh(db_warehouse)
    return db_warehouse

@router.get("/warehouses/", response_model=List[schemas.Warehouse])
def read_warehouses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Warehouse).offset(skip).limit(limit).all()

# --- INVENTORY ---
@router.post("/inventory/", response_model=schemas.Inventory)
def create_inventory(inventory: schemas.InventoryCreate, db: Session = Depends(get_db)):
    db_inventory = models.Inventory(**inventory.dict())
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

@router.get("/inventory/", response_model=List[schemas.Inventory])
def read_inventory(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Inventory).offset(skip).limit(limit).all()

@router.get("/inventory/by-warehouse/{warehouse_id}", response_model=List[schemas.Inventory])
def read_inventory_by_warehouse(warehouse_id: str, db: Session = Depends(get_db)):
    return db.query(models.Inventory).filter(models.Inventory.warehouse_id == warehouse_id).all()
