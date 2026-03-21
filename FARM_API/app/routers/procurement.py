from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import SessionLocal
from ..models import partners as partners_models
from ..models import procurement as procurement_models
from ..schemas import schemas

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- SUPPLIER ---
@router.post("/suppliers/", response_model=schemas.Supplier)
def create_supplier(supplier: schemas.SupplierCreate, db: Session = Depends(get_db)):
    db_supplier = partners_models.Supplier(**supplier.dict())
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier

@router.get("/suppliers/", response_model=List[schemas.Supplier])
def read_suppliers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(partners_models.Supplier).offset(skip).limit(limit).all()


# --- CONTRACT ---
@router.post("/contracts/", response_model=schemas.PurchaseContract)
def create_contract(contract: schemas.PurchaseContractCreate, db: Session = Depends(get_db)):
    db_contract = procurement_models.PurchaseContract(**contract.dict())
    db.add(db_contract)
    db.commit()
    db.refresh(db_contract)
    return db_contract

@router.get("/contracts/", response_model=List[schemas.PurchaseContract])
def read_contracts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(procurement_models.PurchaseContract).offset(skip).limit(limit).all()

# --- BATCH ---
@router.post("/batches/", response_model=schemas.PurchaseBatch)
def create_batch(batch: schemas.PurchaseBatchCreate, db: Session = Depends(get_db)):
    db_batch = procurement_models.PurchaseBatch(**batch.dict())
    db.add(db_batch)
    db.commit()
    db.refresh(db_batch)
    return db_batch

@router.get("/batches/", response_model=List[schemas.PurchaseBatch])
def read_batches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(procurement_models.PurchaseBatch).offset(skip).limit(limit).all()

# --- PURCHASE TICKET ---
@router.post("/purchase-tickets/", response_model=schemas.PurchaseTicket)
def create_purchase_ticket(ticket: schemas.PurchaseTicketCreate, db: Session = Depends(get_db)):
    db_ticket = procurement_models.PurchaseTicket(**ticket.dict())
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

@router.get("/purchase-tickets/", response_model=List[schemas.PurchaseTicket])
def read_purchase_tickets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(procurement_models.PurchaseTicket).offset(skip).limit(limit).all()
