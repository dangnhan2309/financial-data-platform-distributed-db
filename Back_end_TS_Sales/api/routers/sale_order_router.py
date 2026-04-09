"""SaleOrder Router - FastAPI endpoints for SaleOrder"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from api.dependencies.db import get_db
from api.services.sale_order_service import SaleOrderService
from schemas.sale_order_schema import SaleOrderCreate, SaleOrderUpdate, SaleOrderResponse
from typing import List

router = APIRouter(
    prefix="/sale-orders",
    tags=["Sale Orders"]
)


@router.get("/", response_model=List[SaleOrderResponse], summary="Get all sale orders")
async def list_sale_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all sale orders with pagination"""
    service = SaleOrderService(db=db)
    return service.get_all_sale_orders(skip=skip, limit=limit)


@router.get("/pending", response_model=List[SaleOrderResponse], summary="Get pending sale orders")
async def list_pending_sale_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get pending sale orders"""
    service = SaleOrderService(db=db)
    return service.get_pending_sale_orders(skip=skip, limit=limit)


@router.get("/completed", response_model=List[SaleOrderResponse], summary="Get completed sale orders")
async def list_completed_sale_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get completed sale orders"""
    service = SaleOrderService(db=db)
    return service.get_completed_sale_orders(skip=skip, limit=limit)


@router.get("/contract/{contract_id}", response_model=List[SaleOrderResponse], summary="Get sale orders by contract")
async def get_sale_orders_by_contract(
    contract_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get sale orders for a contract"""
    service = SaleOrderService(db=db)
    return service.get_sale_orders_by_contract(contract_id, skip=skip, limit=limit)


@router.get("/status/{status}", response_model=List[SaleOrderResponse], summary="Get sale orders by status")
async def get_sale_orders_by_status(
    status: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get sale orders by status (DRAFT, PENDING, IN_PROGRESS, DELIVERED, COMPLETED, CANCELLED)"""
    service = SaleOrderService(db=db)
    return service.get_sale_orders_by_status(status, skip=skip, limit=limit)


@router.get("/{sale_order_id}", response_model=SaleOrderResponse, summary="Get sale order by ID")
async def get_sale_order(sale_order_id: int, db: Session = Depends(get_db)):
    """Get specific sale order by ID"""
    service = SaleOrderService(db=db)
    sale_order = service.get_sale_order(sale_order_id)
    if not sale_order:
        raise HTTPException(status_code=404, detail="Sale order not found")
    return sale_order


@router.post("/", response_model=SaleOrderResponse, status_code=201, summary="Create new sale order")
async def create_sale_order(
    sale_order_data: SaleOrderCreate,
    db: Session = Depends(get_db)
):
    """Create new sale order"""
    service = SaleOrderService(db=db)
    try:
        return service.create_sale_order(sale_order_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{sale_order_id}", response_model=SaleOrderResponse, summary="Update sale order")
async def update_sale_order(
    sale_order_id: int,
    sale_order_data: SaleOrderUpdate,
    db: Session = Depends(get_db)
):
    """Update sale order information"""
    service = SaleOrderService(db=db)
    sale_order = service.update_sale_order(sale_order_id, sale_order_data)
    if not sale_order:
        raise HTTPException(status_code=404, detail="Sale order not found")
    return sale_order


@router.delete("/{sale_order_id}", status_code=204, summary="Delete sale order")
async def delete_sale_order(sale_order_id: int, db: Session = Depends(get_db)):
    """Delete sale order"""
    service = SaleOrderService(db=db)
    success = service.delete_sale_order(sale_order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Sale order not found")
    return None
