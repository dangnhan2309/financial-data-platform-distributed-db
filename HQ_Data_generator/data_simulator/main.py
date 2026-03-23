import time
from api_client import *
from generator.customer_generator import generate_customer
from generator.quotation_generator import generate_quotation


while True:

    customer = create_customer(generate_customer())

    quotation = create_quotation(
        generate_quotation(customer["customer_id"])
    )

    print("Flow created")

    time.sleep(10)