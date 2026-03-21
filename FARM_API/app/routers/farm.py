from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import SessionLocal
from ..models import farm as models
from ..schemas import schemas

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- FARM ---
@router.post("/farms/", response_model=schemas.Farm)
def create_farm(farm: schemas.FarmCreate, db: Session = Depends(get_db)):
    db_farm = models.Farm(**farm.dict())
    db.add(db_farm)
    db.commit()
    db.refresh(db_farm)
    return db_farm

@router.get("/farms/", response_model=List[schemas.Farm])
def read_farms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    farms = db.query(models.Farm).offset(skip).limit(limit).all()
    return farms

# --- PLOT ---
@router.post("/plots/", response_model=schemas.FarmPlot)
def create_plot(plot: schemas.FarmPlotCreate, db: Session = Depends(get_db)):
    db_plot = models.FarmPlot(**plot.dict())
    db.add(db_plot)
    db.commit()
    db.refresh(db_plot)
    return db_plot

@router.get("/plots/", response_model=List[schemas.FarmPlot])
def read_plots(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    plots = db.query(models.FarmPlot).offset(skip).limit(limit).all()
    return plots

# --- BED ---
@router.post("/beds/", response_model=schemas.FarmBed)
def create_bed(bed: schemas.FarmBedCreate, db: Session = Depends(get_db)):
    db_bed = models.FarmBed(**bed.dict())
    db.add(db_bed)
    db.commit()
    db.refresh(db_bed)
    return db_bed

@router.get("/beds/", response_model=List[schemas.FarmBed])
def read_beds(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    beds = db.query(models.FarmBed).offset(skip).limit(limit).all()
    return beds
