from sqlalchemy import Column, String, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from api.models import BaseModel


class Contract(BaseModel):
    """Contract model - Sales contract"""
    __tablename__ = "contract"

    contract_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey(
        "customer.customer_id"), nullable=False, index=True)
    # Standard, Long-term, Trial, Partnership
    contract_type = Column(String(50), nullable=True)
    incoterm_id = Column(Integer, ForeignKey(
        "incoterm.incoterm_id"), nullable=True, index=True)
    proforma_invoice_id = Column(Integer, ForeignKey(
        "proforma_invoice.proforma_invoice_id"), nullable=True, index=True)
    contract_date = Column(Date, nullable=True)
    effective_date = Column(Date, nullable=True)
    expiry_date = Column(Date, nullable=True)
    total_contract_value = Column(Float, default=0.0, nullable=True)
    total_quantity = Column(Integer, nullable=True)
    currency = Column(String(10), default="USD", nullable=True)
    loading_port = Column(String(100), nullable=True)
    destination_port = Column(String(100), nullable=True)
    # ACTIVE, EXPIRED, PENDING, COMPLETED, CANCELLED
    status = Column(String(20), nullable=True)
    signed_date = Column(Date, nullable=True)
    created_at = Column(Date, nullable=True)
    updated_at = Column(Date, nullable=True)

    # Relationships
    customer = relationship("Customer", foreign_keys=[customer_id])
    incoterm = relationship("Incoterm")
    proforma_invoice = relationship("ProformaInvoice")
    items = relationship(
        "ContractItem", back_populates="contract", cascade="all, delete-orphan")
    sale_orders = relationship("SaleOrder", back_populates="contract")
