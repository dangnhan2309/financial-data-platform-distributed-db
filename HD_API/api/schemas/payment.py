from pydantic import BaseModel
from datetime import date


class PaymentBase(BaseModel):
    payment_term_id: str
    sale_order_id: str
    payment_date: date
    amount: float


class PaymentCreate(PaymentBase):
    payment_id: str


class PaymentResponse(PaymentBase):
    payment_id: str

    class Config:
        from_attributes = True