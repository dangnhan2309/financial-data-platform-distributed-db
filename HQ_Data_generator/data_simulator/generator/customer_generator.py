import random
import uuid

def generate_customer():

    return {
        "customer_code": f"CUS-{uuid.uuid4().hex[:6]}",
        "company_name": f"Company {random.randint(100,999)}",
        "country": random.choice(["USA","Japan","Germany"]),
        "city": "City",
        "address": "Address",
        "phone": "123456",
        "email": "test@email.com",
        "status": "ACTIVE",
        "preferred_currency": "USD"
    }