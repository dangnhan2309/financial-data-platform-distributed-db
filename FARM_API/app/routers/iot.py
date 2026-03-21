from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import SessionLocal
from ..models import iot as models
from ..schemas import schemas

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- SENSOR ---
@router.post("/sensors/", response_model=schemas.IotSensor)
def create_sensor(sensor: schemas.IotSensorCreate, db: Session = Depends(get_db)):
    db_sensor = models.IotSensor(**sensor.dict())
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    return db_sensor

@router.get("/sensors/", response_model=List[schemas.IotSensor])
def read_sensors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.IotSensor).offset(skip).limit(limit).all()

# --- SENSOR DATA ---
@router.post("/sensor-data/", response_model=schemas.SensorData)
def create_sensor_data(data: schemas.SensorDataCreate, db: Session = Depends(get_db)):
    db_data = models.SensorData(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

@router.get("/sensor-data/", response_model=List[schemas.SensorData])
def read_sensor_data(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.SensorData).offset(skip).limit(limit).all()
