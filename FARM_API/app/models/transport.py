from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class TransportTicket(Base):
    __tablename__ = "transport_ticket"
    
    transport_id = Column(String, primary_key=True)
    source_type = Column(String) # 'HARVEST' or 'PURCHASE'
    source_ticket_id = Column(String) # ID of WeighingTicket or PurchaseTicket
    
    destination_warehouse_id = Column(String, ForeignKey("warehouse.warehouse_id"))
    
    driver = Column(String)
    vehicle = Column(String)
    depart_time = Column(DateTime)
    arrive_time = Column(DateTime)
    status = Column(String) # 'In Transit', 'Delivered'
    
    destination_warehouse = relationship("Warehouse", back_populates="transport_tickets")
