from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Warehouse(Base):
    __tablename__ = "warehouse"
    
    warehouse_id = Column(String, primary_key=True)
    warehouse_name = Column(String)
    location = Column(String)
    capacity_ton = Column(Float)
    
    inventory_items = relationship("Inventory", back_populates="warehouse")
    transport_tickets = relationship("TransportTicket", back_populates="destination_warehouse")

class Inventory(Base):
    __tablename__ = "inventory"
    
    inventory_id = Column(String, primary_key=True)
    warehouse_id = Column(String, ForeignKey("warehouse.warehouse_id"))
    
    inventory_type = Column(String) # 'INGREDIENT' or 'PRODUCT'
    item_id = Column(String) # Generic ID for Ingredient or Product
    
    lot_number = Column(String) # For traceability
    origin_source = Column(String) # 'PURCHASE' or 'PRODUCTION'
    origin_ref_id = Column(String) # Batch ID or Lot ID
    
    quantity_kg = Column(Float)
    updated_at = Column(DateTime)
    
    warehouse = relationship("Warehouse", back_populates="inventory_items")
    # Ingredient relationship removed as it's now generic item_id

