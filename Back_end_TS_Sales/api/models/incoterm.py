from sqlalchemy import Column, String, Integer
from api.models import BaseModel


class Incoterm(BaseModel):
    """Incoterm model - International commercial terms master data"""
    __tablename__ = "incoterm"

    incoterm_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(10), nullable=True)  # FOB, CIF, etc.
    description = Column(String(100), nullable=True)
    version = Column(String(10), nullable=True)  # 2020, 2010, etc.
    status = Column(String(20), nullable=True,
                    default="ACTIVE")  # ACTIVE, INACTIVE
