from sqlalchemy.orm import Session
from api.models.sale_order import SaleOrder


def create_sale_order(db: Session, sale_order: SaleOrder):
    db.add(sale_order)
    db.commit()
    db.refresh(sale_order)
    return sale_order


def get_sale_order_by_id(db: Session, sale_order_id: str):
    return db.query(SaleOrder).filter(
        SaleOrder.sale_order_id == sale_order_id
    ).first()


def get_orders_by_contract(db: Session, contract_id: str):
    return db.query(SaleOrder).filter(
        SaleOrder.contract_id == contract_id
    ).all()


def get_all_orders(db: Session):
    return db.query(SaleOrder).all()