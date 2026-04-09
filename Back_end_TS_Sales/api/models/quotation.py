from sqlalchemy import Column, String, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from api.models import BaseModel


class Quotation(BaseModel):
    """Quotation model - Sales quotation/offer"""
    __tablename__ = "quotation"

    quotation_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey(
        "customer.customer_id"), nullable=False, index=True)
    staff_id = Column(Integer, ForeignKey("staff.staff_id"),
                      nullable=False, index=True)
    quotation_date = Column(Date, nullable=True)
    expiry_date = Column(Date, nullable=True)
    total_amount = Column(Float, default=0.0, nullable=True)
    currency = Column(String(10), default="USD", nullable=True)
    # DRAFT, APPROVED, REJECTED, EXPIRED, PENDING_REVIEW
    status = Column(String(20), nullable=True)
    created_at = Column(Date, nullable=True)

    # Relationships
    customer = relationship("Customer", foreign_keys=[customer_id])
    staff = relationship("Staff", foreign_keys=[staff_id])
    items = relationship(
        "QuotationItem", back_populates="quotation", cascade="all, delete-orphan")
