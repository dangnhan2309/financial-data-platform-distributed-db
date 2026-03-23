from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.dependencies.db import get_db
from api.schemas.customer import CustomerCreate, CustomerResponse
from api.services.customer_service import (
    create_customer_service,
    get_all_customers_service,
    get_customer_service
)

router = APIRouter(
    prefix="/customers",
    tags=["Customer"]
)


@router.post("/", response_model=CustomerResponse)
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):
    return create_customer_service(db, customer)


@router.get("/", response_model=list[CustomerResponse])
def get_customers(db: Session = Depends(get_db)):
    return get_all_customers_service(db)


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(
    customer_id: str,
    db: Session = Depends(get_db)
):
    return get_customer_service(db, customer_id)