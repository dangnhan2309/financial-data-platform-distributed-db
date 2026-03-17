from pydantic import BaseModel
from datetime import date
from typing import Optional


# =========================
# Base Schema
# =========================

class ProformaBase(BaseModel):

    quotation_id: str

    payment_term_id: Optional[str] = None
    bank_id: Optional[str] = None
    staff_id: Optional[str] = None

    total_contract_value: Optional[float] = None

    port_of_loading: Optional[str] = None
    port_of_discharge: Optional[str] = None

    delivery_time: Optional[date] = None

    file_path: Optional[str] = None


# =========================
# Create Schema
# =========================

class ProformaCreate(ProformaBase):
    pass


# =========================
# Update Schema (optional)
# =========================

class ProformaUpdate(BaseModel):

    payment_term_id: Optional[str] = None
    bank_id: Optional[str] = None
    staff_id: Optional[str] = None

    total_contract_value: Optional[float] = None

    port_of_loading: Optional[str] = None
    port_of_discharge: Optional[str] = None

    delivery_time: Optional[date] = None

    file_path: Optional[str] = None


# =========================
# Response Schema
# =========================

class ProformaResponse(ProformaBase):

    proforma_invoice_id: str
    created_at: Optional[date] = None

    class Config:
        from_attributes = True