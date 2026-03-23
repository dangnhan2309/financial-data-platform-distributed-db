import uuid
import random
from datetime import date


def generate_quotation(customer_id):

    return {
        "quotation_id": f"QT-{uuid.uuid4().hex[:6]}",
        "customer_id": customer_id,
        "staff_id": "EMP001",
        "quotation_date": str(date.today()),
        "incoterm_id": "INC001",
        "payment_term_id": "PT001"
    }