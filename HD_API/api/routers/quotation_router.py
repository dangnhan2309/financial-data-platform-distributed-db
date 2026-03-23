from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.dependencies.db import get_db
from api.schemas.quotation import QuotationCreate, QuotationResponse
from api.services.quotation_service import (
    create_quotation_service,
    get_quotation_service
)

router = APIRouter(
    prefix="/quotations",
    tags=["Quotation"]
)


@router.post("/", response_model=QuotationResponse)
def create_quotation(
    quotation: QuotationCreate,
    db: Session = Depends(get_db)
):
    return create_quotation_service(db, quotation)


@router.get("/{quotation_id}", response_model=QuotationResponse)
def get_quotation(
    quotation_id: str,
    db: Session = Depends(get_db)
):
    return get_quotation_service(db, quotation_id)