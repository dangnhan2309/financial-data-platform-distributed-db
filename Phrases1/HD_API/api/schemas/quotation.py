from pydantic import BaseModel
from datetime import date


class QuotationBase(BaseModel):
    customer_id: str
    staff_id: str
    quotation_date: date
    expiry_date: date
    incoterm_id: str
    payment_term_id: str


class QuotationCreate(QuotationBase):
    quotation_id: str


class QuotationResponse(QuotationBase):
    quotation_id: str

    class Config:
        from_attributes = True


class QuotationItemBase(BaseModel):
    quotation_id: str
    product_id: str
    quantity: float
    unit_price: float


class QuotationItemCreate(QuotationItemBase):
    pass


class QuotationItemResponse(QuotationItemBase):

    class Config:
        from_attributes = True