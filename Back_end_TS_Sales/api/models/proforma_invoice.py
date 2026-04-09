from sqlalchemy import Column, String, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from api.models import BaseModel


class ProformaInvoice(BaseModel):
    """ProformaInvoice model - Proforma invoice/PI"""
    __tablename__ = "proforma_invoice"

    proforma_invoice_id = Column(Integer, primary_key=True, index=True)
    quotation_id = Column(Integer, ForeignKey(
        "quotation.quotation_id"), nullable=False, index=True)
    payment_term_id = Column(Integer, ForeignKey(
        "payment_term.payment_term_id"), nullable=True, index=True)
    staff_id = Column(Integer, ForeignKey(
        "staff.staff_id"), nullable=True, index=True)
    total_contract_value = Column(Float, default=0.0, nullable=True)
    currency = Column(String(10), default="USD", nullable=True)
    port_of_loading = Column(String(100), nullable=True)
    port_of_discharge = Column(String(100), nullable=True)
    delivery_time = Column(Date, nullable=True)
    # DRAFT, ISSUED, ACCEPTED, REJECTED, CANCELLED
    status = Column(String(20), nullable=True)
    file_path = Column(String(200), nullable=True)
    created_at = Column(Date, nullable=True)
    updated_at = Column(Date, nullable=True)

    # Relationships
    quotation = relationship("Quotation")
    payment_term = relationship("PaymentTerm")
    staff = relationship("Staff")
