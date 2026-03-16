from pydantic import BaseModel
from datetime import date


class SaleOrderBase(BaseModel):
    contract_id: str
    order_date: date
    delivery_date: date
    total_amount: float


class SaleOrderCreate(SaleOrderBase):
    sale_order_id: str


class SaleOrderResponse(SaleOrderBase):
    sale_order_id: str

    class Config:
        from_attributes = True