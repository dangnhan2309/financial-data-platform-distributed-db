from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class QCReceiving(Base):
    __tablename__ = "qc_receiving"
    
    qc_id = Column(String, primary_key=True)
    purchase_ticket_id = Column(String, ForeignKey("purchase_ticket.ticket_id"))
    
    inspector_name = Column(String)
    sample_size = Column(Float)
    defects_found = Column(Float)
    quality_score = Column(Float)
    pass_status = Column(String) # PASS/FAIL/CONDITIONAL
    notes = Column(String)
    checked_at = Column(DateTime)
    
    purchase_ticket = relationship("PurchaseTicket", back_populates="qc_receivings")

class QCHarvest(Base):
    __tablename__ = "qc_harvest"
    
    qc_id = Column(String, primary_key=True)
    weighing_ticket_id = Column(String, ForeignKey("weighing_ticket.ticket_id"))
    
    inspector_name = Column(String)
    appearance_grade = Column(String)
    defect_notes = Column(String)
    pass_status = Column(String)
    checked_at = Column(DateTime)
    
    weighing_ticket = relationship("WeighingTicket", back_populates="qc_harvests")

class QCProductLot(Base):
    __tablename__ = "qc_product_lot"
    
    qc_id = Column(String, primary_key=True)
    production_lot_id = Column(String, ForeignKey("production_lot.lot_id"))
    
    inspector_name = Column(String)
    brix_level = Column(Float)
    ph_level = Column(Float)
    pesticide_residue_check = Column(String)
    final_grade = Column(String)
    checked_at = Column(DateTime)
    
    production_lot = relationship("ProductionLot", back_populates="qc_product_lots")

