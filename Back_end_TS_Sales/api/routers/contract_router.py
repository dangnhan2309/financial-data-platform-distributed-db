"""Contract Router - FastAPI endpoints for Contract"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from api.dependencies.db import get_db
from api.services.contract_service import ContractService
from schemas.contract_schema import ContractCreate, ContractUpdate, ContractResponse
from typing import List

router = APIRouter(
    prefix="/contracts",
    tags=["Contracts"]
)


@router.get("/", response_model=List[ContractResponse], summary="Get all contracts")
async def list_contracts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all contracts with pagination"""
    service = ContractService(db=db)
    return service.get_all_contracts(skip=skip, limit=limit)


@router.get("/active", response_model=List[ContractResponse], summary="Get active contracts")
async def list_active_contracts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get active contracts only"""
    service = ContractService(db=db)
    return service.get_active_contracts(skip=skip, limit=limit)


@router.get("/customer/{customer_id}", response_model=List[ContractResponse], summary="Get contracts by customer")
async def get_contracts_by_customer(
    customer_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get contracts for a customer"""
    service = ContractService(db=db)
    return service.get_contracts_by_customer(customer_id, skip=skip, limit=limit)


@router.get("/status/{status}", response_model=List[ContractResponse], summary="Get contracts by status")
async def get_contracts_by_status(
    status: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get contracts by status (ACTIVE, EXPIRED, PENDING, COMPLETED, CANCELLED)"""
    service = ContractService(db=db)
    return service.get_contracts_by_status(status, skip=skip, limit=limit)


@router.get("/type/{contract_type}", response_model=List[ContractResponse], summary="Get contracts by type")
async def get_contracts_by_type(
    contract_type: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get contracts by type (Standard, Long-term, Trial, Partnership)"""
    service = ContractService(db=db)
    return service.get_contracts_by_type(contract_type, skip=skip, limit=limit)


@router.get("/{contract_id}", response_model=ContractResponse, summary="Get contract by ID")
async def get_contract(contract_id: int, db: Session = Depends(get_db)):
    """Get specific contract by ID"""
    service = ContractService(db=db)
    contract = service.get_contract(contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    return contract


@router.post("/", response_model=ContractResponse, status_code=201, summary="Create new contract")
async def create_contract(
    contract_data: ContractCreate,
    db: Session = Depends(get_db)
):
    """Create new contract"""
    service = ContractService(db=db)
    try:
        return service.create_contract(contract_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{contract_id}", response_model=ContractResponse, summary="Update contract")
async def update_contract(
    contract_id: int,
    contract_data: ContractUpdate,
    db: Session = Depends(get_db)
):
    """Update contract information"""
    service = ContractService(db=db)
    contract = service.update_contract(contract_id, contract_data)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    return contract


@router.delete("/{contract_id}", status_code=204, summary="Delete contract")
async def delete_contract(contract_id: int, db: Session = Depends(get_db)):
    """Delete contract"""
    service = ContractService(db=db)
    success = service.delete_contract(contract_id)
    if not success:
        raise HTTPException(status_code=404, detail="Contract not found")
    return None
