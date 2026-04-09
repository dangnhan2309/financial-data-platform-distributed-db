"""Customer Router - FastAPI endpoints for Customer"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from api.dependencies.db import get_db
from api.services.customer_service import CustomerService
from schemas.customer_schema import CustomerCreate, CustomerUpdate, CustomerResponse
from typing import List

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


@router.get("/", response_model=List[CustomerResponse], summary="Get all customers")
async def list_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all customers with pagination"""
    service = CustomerService(db=db)
    return service.get_all_customers(skip=skip, limit=limit)


@router.get("/active", response_model=List[CustomerResponse], summary="Get active customers")
async def list_active_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get active customers only"""
    service = CustomerService(db=db)
    return service.get_active_customers(skip=skip, limit=limit)


@router.get("/{customer_id}", response_model=CustomerResponse, summary="Get customer by ID")
async def get_customer(customer_id: int, db: Session = Depends(get_db)):
    """Get specific customer by ID"""
    service = CustomerService(db=db)
    customer = service.get_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.get("/code/{customer_code}", response_model=CustomerResponse, summary="Get customer by code")
async def get_customer_by_code(customer_code: str, db: Session = Depends(get_db)):
    """Get customer by customer code"""
    service = CustomerService(db=db)
    customer = service.get_customer_by_code(customer_code)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.post("/", response_model=CustomerResponse, status_code=201, summary="Create new customer")
async def create_customer(
    customer_data: CustomerCreate,
    db: Session = Depends(get_db)
):
    """Create new customer"""
    service = CustomerService(db=db)
    try:
        return service.create_customer(customer_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{customer_id}", response_model=CustomerResponse, summary="Update customer")
async def update_customer(
    customer_id: int,
    customer_data: CustomerUpdate,
    db: Session = Depends(get_db)
):
    """Update customer information"""
    service = CustomerService(db=db)
    customer = service.update_customer(customer_id, customer_data)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.delete("/{customer_id}", status_code=204, summary="Delete customer")
async def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    """Delete customer"""
    service = CustomerService(db=db)
    success = service.delete_customer(customer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Customer not found")
    return None
