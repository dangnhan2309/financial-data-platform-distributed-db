from sqlalchemy.orm import Session
from api.models.quotation import Quotation, QuotationItem


def create_quotation(db: Session, quotation: Quotation):

    db.add(quotation)
  

    return quotation


def create_quotation_items(db: Session, items):

    db.add_all(items)

    return items


def get_quotation_by_id(db: Session, quotation_id: str):

    return db.query(Quotation).filter(
        Quotation.quotation_id == quotation_id
    ).first()