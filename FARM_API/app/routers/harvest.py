from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import SessionLocal
from ..models import harvest as models
from ..schemas import schemas

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- WEIGHING TICKET ---
@router.post("/weighing-tickets/", response_model=schemas.WeighingTicket)
def create_weighing_ticket(ticket: schemas.WeighingTicketCreate, db: Session = Depends(get_db)):
    db_ticket = models.WeighingTicket(**ticket.dict())
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

@router.get("/weighing-tickets/", response_model=List[schemas.WeighingTicket])
def read_weighing_tickets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.WeighingTicket).offset(skip).limit(limit).all()
