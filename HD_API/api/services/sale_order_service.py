from sqlalchemy.orm import Session
from api.repositories import sale_order_repository, contract_repository
from api.models.sale_order import SaleOrder
from api.utils.id_generator import generate_sale_order_id


def create_sale_order_service(db: Session, order_data):

    contract = contract_repository.get_contract_by_id(
        db,
        order_data.contract_id
    )

    if not contract:
        raise ValueError("Contract not found")

    order_id = generate_sale_order_id()

    order = SaleOrder(
        sale_order_id=order_id,
        **order_data.dict()
    )

    return sale_order_repository.create_sale_order(db, order)