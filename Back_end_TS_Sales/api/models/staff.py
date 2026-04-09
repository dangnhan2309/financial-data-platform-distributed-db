from sqlalchemy import Column, String, Integer
from api.models import BaseModel


class Staff(BaseModel):
    """Staff model - Employee information"""
    __tablename__ = "staff"

    staff_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=True)
    role = Column(String(50), nullable=True)
    email = Column(String(100), nullable=True, index=True)
    phone = Column(String(20), nullable=True)
    department = Column(String(50), nullable=True)
    # ACTIVE, INACTIVE, TERMINATED, FIRED
    status = Column(String(20), nullable=True)
