from sqlalchemy.orm import Session

from api.models import quotation
from api.dependencies import db
from api.repositories import quotation_repository, customer_repository
from api.models.quotation import Quotation, QuotationItem
from api.utils.id_generator import generate_quotation_id


def create_quotation_service(db: Session, quotation_data):

    # 1. Kiểm tra customer tồn tại
    customer = customer_repository.get_customer_by_id(
        db,
        quotation_data.customer_id
    )

    if not customer:
        raise ValueError("Customer does not exist")

    # 2. Generate quotation ID
    quotation_id = generate_quotation_id()

    try :
        # 3. Tạo quotation object
        quotation = Quotation(
            quotation_id=quotation_id,
            customer_id=quotation_data.customer_id,
            staff_id=quotation_data.staff_id,
            quotation_date=quotation_data.quotation_date,
            expiry_date=quotation_data.expiry_date,
            incoterm_id=quotation_data.incoterm_id,
            payment_term_id=quotation_data.payment_term_id
        )

        # 4. Save quotation
        quotation_repository.create_quotation(db, quotation)

        # 5. Save quotation items
        items = []

        for item in quotation_data.items:
            items.append(
                QuotationItem(
                    quotation_id=quotation_id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    unit_price=item.unit_price
                )
            )

        quotation_repository.create_quotation_items(db, items)
        db.commit()

        db.refresh(quotation)

        return quotation
    except Exception as e:
        db.rollback()
        raise e

def get_quotation_service(db: Session, quotation_id: str):

    quotation = quotation_repository.get_quotation_by_id(db, quotation_id)

    if not quotation:
        raise ValueError("Quotation not found")

    return quotation