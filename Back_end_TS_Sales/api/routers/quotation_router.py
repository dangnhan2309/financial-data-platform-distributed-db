"""Quotation Router - FastAPI endpoints for Quotation"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from api.dependencies.db import get_db
from api.services.quotation_service import QuotationService
from schemas.quotation_schema import QuotationCreate, QuotationUpdate, QuotationResponse
from typing import List
from datetime import date

router = APIRouter(
    prefix="/quotations",
    tags=["Quotations"]
)


@router.get("/", response_model=List[QuotationResponse], summary="Get all quotations")
async def list_quotations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all quotations with pagination"""
    service = QuotationService(db=db)
    return service.get_all_quotations(skip=skip, limit=limit)


@router.get("/active", response_model=List[QuotationResponse], summary="Get active quotations")
async def list_active_quotations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get active quotations only"""
    service = QuotationService(db=db)
    return service.get_active_quotations(skip=skip, limit=limit)


@router.get("/customer/{customer_id}", response_model=List[QuotationResponse], summary="Get quotations by customer")
async def get_quotations_by_customer(
    customer_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get quotations for a customer"""
    service = QuotationService(db=db)
    return service.get_quotations_by_customer(customer_id, skip=skip, limit=limit)


@router.get("/status/{status}", response_model=List[QuotationResponse], summary="Get quotations by status")
async def get_quotations_by_status(
    status: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get quotations by status (DRAFT, APPROVED, REJECTED, EXPIRED, PENDING_REVIEW)"""
    service = QuotationService(db=db)
    return service.get_quotations_by_status(status, skip=skip, limit=limit)


@router.get("/{quotation_id}", response_model=QuotationResponse, summary="Get quotation by ID")
async def get_quotation(quotation_id: int, db: Session = Depends(get_db)):
    """Get specific quotation by ID"""
    service = QuotationService(db=db)
    quotation = service.get_quotation(quotation_id)
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")
    return quotation


@router.post("/", response_model=QuotationResponse, status_code=201, summary="Create new quotation")
async def create_quotation(
    quotation_data: QuotationCreate,
    db: Session = Depends(get_db)
):
    """Create new quotation"""
    service = QuotationService(db=db)
    try:
        return service.create_quotation(quotation_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{quotation_id}", response_model=QuotationResponse, summary="Update quotation")
async def update_quotation(
    quotation_id: int,
    quotation_data: QuotationUpdate,
    db: Session = Depends(get_db)
):
    """Update quotation information"""
    service = QuotationService(db=db)
    quotation = service.update_quotation(quotation_id, quotation_data)
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")
    return quotation


@router.delete("/{quotation_id}", status_code=204, summary="Delete quotation")
async def delete_quotation(quotation_id: int, db: Session = Depends(get_db)):
    """Delete quotation"""
    service = QuotationService(db=db)
    success = service.delete_quotation(quotation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Quotation not found")
    return None
