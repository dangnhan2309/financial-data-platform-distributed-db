from pydantic import BaseModel
from typing import Optional


class CustomerBase(BaseModel):
    customer_type_id: str
    customer_code: str
    company_name: str
    short_name: Optional[str]
    tax_id: Optional[str]

    country: str
    city: str
    address: str

    phone: Optional[str]
    email: Optional[str]
    website: Optional[str]

    industry: Optional[str]
    status: Optional[str]
    preferred_currency: Optional[str]


class CustomerCreate(CustomerBase):
    pass
class CustomerResponse(CustomerBase):
    customer_id: str

    class Config:
        from_attributes = True  