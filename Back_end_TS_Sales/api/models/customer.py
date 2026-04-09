from sqlalchemy import Column, String, Integer, Date
from api.models import BaseModel


class Customer(BaseModel):
    """Customer model - Client information"""
    __tablename__ = "customer"

    customer_id = Column(Integer, primary_key=True, index=True)
    customer_type = Column(String(50), nullable=True)  # B2B, B2C, etc.
    customer_code = Column(String(50), nullable=True, unique=True, index=True)
    company_name = Column(String(100), nullable=False)
    short_name = Column(String(50), nullable=True)
    tax_id = Column(String(50), nullable=True)
    country = Column(String(50), nullable=True)
    city = Column(String(50), nullable=True)
    address = Column(String(200), nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True, index=True)
    website = Column(String(100), nullable=True)
    industry = Column(String(50), nullable=True)
    # ACTIVE, INACTIVE, PENDING, SUSPENDED, VERIFIED, TRIAL
    status = Column(String(20), nullable=True)
    preferred_currency = Column(String(10), default="USD", nullable=True)
    created_at = Column(Date, nullable=True)
