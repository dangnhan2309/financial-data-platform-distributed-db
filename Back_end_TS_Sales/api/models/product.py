from sqlalchemy import Column, String, Integer, Float, Date
from api.models import BaseModel


class Product(BaseModel):
    """Product model - Product/SKU information"""
    __tablename__ = "product"

    product_id = Column(Integer, primary_key=True, index=True)
    # Juice, Puree, Concentrate
    product_type = Column(String(50), nullable=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(String(200), nullable=True)
    price = Column(Float, nullable=True)
    application = Column(String(100), nullable=True)  # Food Application
    brix = Column(Float, nullable=True)
    product_size = Column(String(50), nullable=True)
    solid = Column(Float, nullable=True)
    ph = Column(Float, nullable=True)
    # 1: active, 0: inactive
    is_active = Column(Integer, default=1, nullable=True)
    created_at = Column(Date, nullable=True)
    updated_at = Column(Date, nullable=True)
