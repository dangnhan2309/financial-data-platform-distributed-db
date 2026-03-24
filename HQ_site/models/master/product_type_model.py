from numbers import Number  
from sqlalchemy import Integer, String, Column
from core.database import Base


class ProductType(Base):
    __tablename__ = "product_type"
    product_type_id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    is_active = Column(Integer, default=1)