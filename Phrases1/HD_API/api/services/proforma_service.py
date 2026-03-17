from sqlalchemy.orm import Session
from api.repositories import proforma_repository, quotation_repository
from api.models.proforma import ProformaInvoice
from api.utils.id_generator import generate_proforma_id


def create_proforma_service(db: Session, proforma_data):

    quotation = quotation_repository.get_quotation_by_id(
        db,
        proforma_data.quotation_id
    )

    if not quotation:
        raise ValueError("Quotation not found")

    existing = proforma_repository.get_proforma_by_quotation(
        db,
        proforma_data.quotation_id
    )

    if existing:
        raise ValueError("Proforma already exists for this quotation")

    proforma_id = generate_proforma_id()

    proforma = ProformaInvoice(
        proforma_invoice_id=proforma_id,
        **proforma_data.dict()
    )

    return proforma_repository.create_proforma(db, proforma)