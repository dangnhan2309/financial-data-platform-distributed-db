from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class IotSensor(Base):
    __tablename__ = "iot_sensor"
    
    sensor_id = Column(String, primary_key=True)
    plot_id = Column(String, ForeignKey("farm_plot.plot_id"))
    sensor_type = Column(String)
    manufacturer = Column(String)
    status = Column(String)
    installed_at = Column(DateTime)
    
    plot = relationship("FarmPlot", back_populates="iot_sensors")
    sensor_data = relationship("SensorData", back_populates="sensor")

class SensorData(Base):
    __tablename__ = "sensor_data"
    
    data_id = Column(String, primary_key=True)
    sensor_id = Column(String, ForeignKey("iot_sensor.sensor_id"))
    temperature = Column(Float)
    humidity = Column(Float)
    soil_moisture = Column(Float)
    light_intensity = Column(Float)
    recorded_at = Column(DateTime)
    
    sensor = relationship("IotSensor", back_populates="sensor_data")
