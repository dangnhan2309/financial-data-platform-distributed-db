from sqlalchemy import Column, String, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from api.models import BaseModel


class SaleOrder(BaseModel):
    """SaleOrder model - Sales order"""
    __tablename__ = "sale_order"

    sale_order_id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey(
        "contract.contract_id"), nullable=False, index=True)
    order_date = Column(Date, nullable=True)
    delivery_date = Column(Date, nullable=True)
    total_amount = Column(Float, default=0.0, nullable=True)
    currency = Column(String(10), default="USD", nullable=True)
    # DRAFT, PENDING, IN_PROGRESS, DELIVERED, COMPLETED, CANCELLED
    status = Column(String(20), nullable=True)
    created_at = Column(Date, nullable=True)
    updated_at = Column(Date, nullable=True)

    # Relationships
    contract = relationship("Contract", back_populates="sale_orders")
    export_documents = relationship(
        "ExportDocumentSet", back_populates="sale_order", cascade="all, delete-orphan")
