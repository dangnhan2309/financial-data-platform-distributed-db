import uuid
from datetime import date


def generate_sale_order(contract_id):

    return {
        "sale_order_id": f"SO-{uuid.uuid4().hex[:6]}",
        "contract_id": contract_id,
        "order_date": str(date.today()),
        "delivery_date": str(date.today()),
        "total_amount": 10000
    }