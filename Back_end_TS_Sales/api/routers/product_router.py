"""Product Router - FastAPI endpoints for Product"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from api.dependencies.db import get_db
from api.services.product_service import ProductService
from schemas.product_schema import ProductCreate, ProductUpdate, ProductResponse
from typing import List

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get("/", response_model=List[ProductResponse], summary="Get all products")
async def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all products with pagination"""
    service = ProductService(db=db)
    return service.get_all_products(skip=skip, limit=limit)


@router.get("/active", response_model=List[ProductResponse], summary="Get active products")
async def list_active_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get active products only"""
    service = ProductService(db=db)
    return service.get_active_products(skip=skip, limit=limit)


@router.get("/type/{product_type}", response_model=List[ProductResponse], summary="Get products by type")
async def get_products_by_type(
    product_type: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get products by type (Juice, Puree, Concentrate)"""
    service = ProductService(db=db)
    return service.get_products_by_type(product_type, skip=skip, limit=limit)


@router.get("/price-range", response_model=List[ProductResponse], summary="Get products by price range")
async def get_products_by_price_range(
    min_price: float = Query(0, ge=0),
    max_price: float = Query(10000, ge=0),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get products within price range"""
    service = ProductService(db=db)
    return service.get_products_by_price_range(min_price, max_price, skip=skip, limit=limit)


@router.get("/{product_id}", response_model=ProductResponse, summary="Get product by ID")
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get specific product by ID"""
    service = ProductService(db=db)
    product = service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/", response_model=ProductResponse, status_code=201, summary="Create new product")
async def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db)
):
    """Create new product"""
    service = ProductService(db=db)
    try:
        return service.create_product(product_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{product_id}", response_model=ProductResponse, summary="Update product")
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db)
):
    """Update product information"""
    service = ProductService(db=db)
    product = service.update_product(product_id, product_data)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.delete("/{product_id}", status_code=204, summary="Delete product")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete product"""
    service = ProductService(db=db)
    success = service.delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return None
