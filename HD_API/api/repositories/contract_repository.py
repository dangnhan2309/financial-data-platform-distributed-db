from sqlalchemy.orm import Session
from api.models.contract import Contract


def create_contract(db: Session, contract: Contract):
    db.add(contract)
    db.commit()
    db.refresh(contract)
    return contract


def get_contract_by_id(db: Session, contract_id: str):
    return db.query(Contract).filter(
        Contract.contract_id == contract_id
    ).first()


def get_contracts_by_customer(db: Session, customer_id: str):
    return db.query(Contract).filter(
        Contract.customer_id == customer_id
    ).all()


def get_all_contracts(db: Session):
    return db.query(Contract).all()