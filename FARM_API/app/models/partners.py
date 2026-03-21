from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from ..database import Base

class Supplier(Base):
    __tablename__ = "supplier"
    
    supplier_id = Column(String, primary_key=True)
    supplier_name = Column(String)
    supplier_type = Column(String)
    phone = Column(String)
    address = Column(String)
    
    contracts = relationship("PurchaseContract", back_populates="supplier")
    purchase_tickets = relationship("PurchaseTicket", back_populates="supplier")
