from sqlalchemy import Column, String, Integer
from api.models import BaseModel


class PaymentTerm(BaseModel):
    """Payment Term model - Payment terms master data"""
    __tablename__ = "payment_term"

    payment_term_id = Column(Integer, primary_key=True, index=True)
    description = Column(String(100), nullable=True)
    number_of_days = Column(Integer, nullable=True)
    status = Column(String(20), nullable=True,
                    default="ACTIVE")  # ACTIVE, INACTIVE
