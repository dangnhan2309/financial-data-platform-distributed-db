from sqlalchemy.orm import Session
from api.models.proforma import ProformaInvoice


def create_proforma(db: Session, proforma: ProformaInvoice):
    db.add(proforma)
    db.commit()
    db.refresh(proforma)
    return proforma


def get_proforma_by_id(db: Session, proforma_id: str):
    return db.query(ProformaInvoice).filter(
        ProformaInvoice.proforma_invoice_id == proforma_id
    ).first()


def get_proforma_by_quotation(db: Session, quotation_id: str):
    return db.query(ProformaInvoice).filter(
        ProformaInvoice.quotation_id == quotation_id
    ).first()


def get_all_proformas(db: Session):
    return db.query(ProformaInvoice).all()