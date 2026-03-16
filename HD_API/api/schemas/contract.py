from api.database import Base
from datetime import date
from typing import Optional
from pydantic import BaseModel


class ContractBase(BaseModel):
    customer_id: str
    payment_term_id: str
    proforma_invoice_id: str
    staff_id: str
    contract_type_id: str
    incoterm_id: str

    contract_date: date
    effective_date: date
    expiry_date: date

    total_value: float

    loading_port: str
    destination_port: str
    currency: str

    total_contract_value: float
    total_quantity: float

    status: Optional[str]
    signed_date: Optional[date]


class ContractCreate(ContractBase):
    contract_id: str


class ContractResponse(ContractBase):
    contract_id: str

    class Config:
        from_attributes = True