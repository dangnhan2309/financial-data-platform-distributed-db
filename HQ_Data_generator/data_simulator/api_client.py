import requests

BASE_URL = "http://localhost:8000"


def create_customer(data):
    return requests.post(f"{BASE_URL}/customers", json=data).json()


def create_quotation(data):
    return requests.post(f"{BASE_URL}/quotation", json=data).json()


def create_contract(data):
    return requests.post(f"{BASE_URL}/contract", json=data).json()


def create_sale_order(data):
    return requests.post(f"{BASE_URL}/sale-order", json=data).json()