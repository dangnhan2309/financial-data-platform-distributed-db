from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.dependencies.db import get_db
from api.schemas.contract import ContractCreate, ContractResponse
from api.services.contract_service import create_contract_service

router = APIRouter(
    prefix="/contracts",
    tags=["Contract"]
)
@router.post("/", response_model=ContractResponse)
def create_contract(
    contract: ContractCreate,
    db: Session = Depends(get_db)
):
    return create_contract_service(db, contract)
