import uuid

def generate_contract_id():
    return "CON-" + uuid.uuid4().hex[:8]
def generate_customer_id():
    return "CUS-" + uuid.uuid4().hex[:8]
def generate_quotation_id():
    return "QTN-" + uuid.uuid4().hex[:8]
def generate_proforma_id():
    return "PRO-" + uuid.uuid4().hex[:8]
def generate_sale_order_id():
    return "SAL-" + uuid.uuid4().hex[:8]
def generate_staff_id():
    return "STF-" + uuid.uuid4().hex[:8]