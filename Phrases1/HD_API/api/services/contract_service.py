from sqlalchemy.orm import Session
from api.repositories import contract_repository, proforma_repository
from api.models.contract import Contract
from api.utils.id_generator import generate_contract_id


def create_contract_service(db: Session, contract_data):

    proforma = proforma_repository.get_proforma_by_id(
        db,
        contract_data.proforma_invoice_id
    )

    if not proforma:
        raise ValueError("Proforma invoice not found")

    contract_id = generate_contract_id()

    contract = Contract(
        contract_id=contract_id,
        **contract_data.dict()
    )

    return contract_repository.create_contract(db, contract)