import uuid
from datetime import date


def generate_contract(customer_id, proforma_id):

    return {
        "contract_id": f"CT-{uuid.uuid4().hex[:6]}",
        "customer_id": customer_id,
        "proforma_invoice_id": proforma_id,
        "staff_id": "EMP002",
        "contract_date": str(date.today()),
        "currency": "USD",
        "status": "DRAFT"
    }