from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import SessionLocal
from ..models import sales as models
from ..schemas import schemas

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- CUSTOMER ---
@router.post("/customers/", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    db_customer = models.Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@router.get("/customers/", response_model=List[schemas.Customer])
def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Customer).offset(skip).limit(limit).all()

# --- SALES ORDER ---
@router.post("/orders/", response_model=schemas.SalesOrder)
def create_order(order: schemas.SalesOrderCreate, db: Session = Depends(get_db)):
    db_order = models.SalesOrder(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@router.get("/orders/", response_model=List[schemas.SalesOrder])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.SalesOrder).offset(skip).limit(limit).all()

# --- SALES ITEM ---
@router.post("/order-items/", response_model=schemas.SalesItem)
def create_order_item(item: schemas.SalesItemCreate, db: Session = Depends(get_db)):
    db_item = models.SalesItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/order-items/", response_model=List[schemas.SalesItem])
def read_order_items(order_id: str, db: Session = Depends(get_db)):
    return db.query(models.SalesItem).filter(models.SalesItem.order_id == order_id).all()

# --- PAYMENT ---
@router.post("/payments/", response_model=schemas.Payment)
def create_payment(payment: schemas.PaymentCreate, db: Session = Depends(get_db)):
    db_payment = models.Payment(**payment.dict())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

@router.get("/payments/", response_model=List[schemas.Payment])
def read_payments(order_id: str, db: Session = Depends(get_db)):
    return db.query(models.Payment).filter(models.Payment.order_id == order_id).all()
