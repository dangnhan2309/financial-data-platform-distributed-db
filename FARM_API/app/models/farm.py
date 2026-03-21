from sqlalchemy import Column, String, Float, Integer, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Farm(Base):
    __tablename__ = "farm"
    
    farm_id = Column(String, primary_key=True)
    farm_name = Column(String)
    location = Column(String)
    created_at = Column(DateTime)
    
    plots = relationship("FarmPlot", back_populates="farm")

class FarmPlot(Base):
    __tablename__ = "farm_plot"
    
    plot_id = Column(String, primary_key=True)
    farm_id = Column(String, ForeignKey("farm.farm_id"))
    plot_name = Column(String)
    crop_type = Column(String)
    area_m2 = Column(Float)
    
    farm = relationship("Farm", back_populates="plots")
    beds = relationship("FarmBed", back_populates="plot")
    iot_sensors = relationship("IotSensor", back_populates="plot")

class FarmBed(Base):
    __tablename__ = "farm_bed"
    
    bed_id = Column(String, primary_key=True)
    plot_id = Column(String, ForeignKey("farm_plot.plot_id"))
    bed_number = Column(Integer)
    planting_date = Column(Date)
    status = Column(String)
    
    plot = relationship("FarmPlot", back_populates="beds")
    cultivation_logs = relationship("CultivationLog", back_populates="bed")
    weighing_tickets = relationship("WeighingTicket", back_populates="bed")
