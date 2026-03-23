from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.dependencies.db import get_db
from api.schemas.proforma import ProformaCreate, ProformaResponse
from api.services.proforma_service import create_proforma_service

router = APIRouter(
    prefix="/proforma",
    tags=["Proforma Invoice"]
)


@router.post("/", response_model=ProformaResponse)
def create_proforma(
    proforma: ProformaCreate,
    db: Session = Depends(get_db)
):
    return create_proforma_service(db, proforma)