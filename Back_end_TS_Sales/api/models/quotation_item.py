from sqlalchemy import Column, String, Integer, Float, Date, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from api.models import BaseModel
from datetime import datetime


class QuotationItem(BaseModel):
    """QuotationItem model - Line items in quotation"""
    __tablename__ = "quotation_item"

    quotation_id = Column(Integer, ForeignKey(
        "quotation.quotation_id"), primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey(
        "product.product_id"), primary_key=True, index=True)
    quantity = Column(Integer, nullable=True)
    unit_price = Column(Float, nullable=True)
    discount = Column(Float, nullable=True)  # Discount percentage or amount
    tax_rate = Column(Float, nullable=True)
    total_price = Column(Float, nullable=True)
    created_at = Column(Date, nullable=True)

    # Relationships
    quotation = relationship("Quotation", back_populates="items")
    product = relationship("Product")

    __table_args__ = (
        PrimaryKeyConstraint("quotation_id", "product_id"),
    )
