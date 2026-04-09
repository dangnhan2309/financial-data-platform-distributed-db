from sqlalchemy import Column, String, Integer, Float, Date, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from api.models import BaseModel
from datetime import datetime


class ContractItem(BaseModel):
    """ContractItem model - Line items in contract"""
    __tablename__ = "contract_item"

    contract_id = Column(Integer, ForeignKey(
        "contract.contract_id"), primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey(
        "product.product_id"), primary_key=True, index=True)
    quantity = Column(Integer, nullable=True)
    unit_price = Column(Float, nullable=True)
    discount = Column(Float, nullable=True)  # Discount percentage or amount
    tax_rate = Column(Float, nullable=True)
    total_price = Column(Float, nullable=True)
    created_at = Column(Date, nullable=True)

    # Relationships
    contract = relationship("Contract", back_populates="items")
    product = relationship("Product")

    __table_args__ = (
        PrimaryKeyConstraint("contract_id", "product_id"),
    )
