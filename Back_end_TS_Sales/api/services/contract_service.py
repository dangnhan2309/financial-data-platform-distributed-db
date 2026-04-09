"""Contract Service - Business logic for Contract"""
from api.repositories.contract_repository import ContractRepository
from api.models import Contract
from schemas.contract_schema import ContractCreate, ContractUpdate
from sqlalchemy.orm import Session
from datetime import date


class ContractService:
    """Service layer for Contract operations"""

    def __init__(self, db: Session):
        self.repository = ContractRepository(db=db)
        self.db = db

    def create_contract(self, contract_data: ContractCreate) -> Contract:
        """Create new contract"""
        db_contract = Contract(**contract_data.dict())
        return self.repository.create(db_contract)

    def get_contract(self, contract_id: int) -> Contract:
        """Get contract by ID"""
        return self.repository.get_by_id(contract_id)

    def get_all_contracts(self, skip: int = 0, limit: int = 100) -> list:
        """Get all contracts with pagination"""
        return self.repository.get_all(skip=skip, limit=limit)

    def get_contracts_by_customer(self, customer_id: int, skip: int = 0, limit: int = 100) -> list:
        """Get contracts by customer"""
        return self.repository.get_by_customer(customer_id, skip=skip, limit=limit)

    def get_contracts_by_status(self, status: str, skip: int = 0, limit: int = 100) -> list:
        """Get contracts by status"""
        return self.repository.get_by_status(status, skip=skip, limit=limit)

    def get_active_contracts(self, skip: int = 0, limit: int = 100) -> list:
        """Get active contracts"""
        return self.repository.get_active_contracts(skip=skip, limit=limit)

    def get_expired_contracts(self, skip: int = 0, limit: int = 100) -> list:
        """Get expired contracts"""
        return self.repository.get_expired_contracts(skip=skip, limit=limit)

    def get_contracts_by_type(self, contract_type: str, skip: int = 0, limit: int = 100) -> list:
        """Get contracts by type"""
        return self.repository.get_by_type(contract_type, skip=skip, limit=limit)

    def update_contract(self, contract_id: int, contract_data: ContractUpdate) -> Contract:
        """Update contract"""
        db_contract = self.repository.get_by_id(contract_id)
        if db_contract:
            return self.repository.update(contract_id, contract_data.dict(exclude_unset=True))
        return None

    def delete_contract(self, contract_id: int) -> bool:
        """Delete contract"""
        return self.repository.delete(contract_id)

    def get_contracts_by_date_range(self, start_date: date, end_date: date, skip: int = 0, limit: int = 100) -> list:
        """Get contracts within date range"""
        return self.repository.get_by_date_range(start_date, end_date, skip=skip, limit=limit)
