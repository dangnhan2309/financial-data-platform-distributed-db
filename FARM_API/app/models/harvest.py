from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class WeighingTicket(Base):
    __tablename__ = "weighing_ticket"
    
    ticket_id = Column(String, primary_key=True)
    bed_id = Column(String, ForeignKey("farm_bed.bed_id"))
    ingredient_id = Column(String, ForeignKey("ingredient.ingredient_id"))
    raw_weight = Column(Float)
    harvested_by = Column(String)
    timestamp = Column(DateTime)
    
    bed = relationship("FarmBed", back_populates="weighing_tickets")
    ingredient = relationship("Ingredient", back_populates="harvest_tickets")
    
    # Use string "QcRecord" and define foreign key path in QcRecord
    qc_records = relationship("QcRecord", back_populates="weighing_ticket")
