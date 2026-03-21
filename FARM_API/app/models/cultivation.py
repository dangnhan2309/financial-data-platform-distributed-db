from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class CultivationLog(Base):
    __tablename__ = "cultivation_log"
    
    log_id = Column(String, primary_key=True)
    bed_id = Column(String, ForeignKey("farm_bed.bed_id"))
    action = Column(String)
    performed_by = Column(String)
    notes = Column(String)
    timestamp = Column(DateTime)
    
    bed = relationship("FarmBed", back_populates="cultivation_logs")
