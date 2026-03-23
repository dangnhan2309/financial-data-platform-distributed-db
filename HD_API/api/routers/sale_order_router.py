from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.dependencies.db import get_db
from api.schemas.sale_order import SaleOrderCreate, SaleOrderResponse
from api.services.sale_order_service import create_sale_order_service

router = APIRouter(
    prefix="/sale-orders",
    tags=["Sale Order"]
)
@router.post("/", response_model=SaleOrderResponse)
def create_sale_order(
    order: SaleOrderCreate,
    db: Session = Depends(get_db)
):
    return create_sale_order_service(db, order)