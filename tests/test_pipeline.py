import pandas as pd

from src.validation import (
    validate_customers,
    validate_orders
)


def test_valid_customers():
    customers = pd.DataFrame([
        {
            "customer_id": "C001",
            "customer_name": "Rahul",
            "email": "rahul@example.com",
            "city": "Hyderabad",
            "created_at": "2026-01-01T10:00:00"
        }
    ])

    valid, rejects = validate_customers(customers)

    assert len(valid) == 1
    assert len(rejects) == 0


def test_customer_null_key():
    customers = pd.DataFrame([
        {
            "customer_id": "",
            "customer_name": "Rahul",
            "email": "rahul@example.com",
            "city": "Hyderabad",
            "created_at": "2026-01-01T10:00:00"
        }
    ])

    valid, rejects = validate_customers(customers)

    assert len(valid) == 0
    assert len(rejects) == 1


def test_duplicate_customer():
    customers = pd.DataFrame([
        {
            "customer_id": "C001",
            "customer_name": "Rahul",
            "email": "rahul@example.com",
            "city": "Hyderabad",
            "created_at": "2026-01-01T10:00:00"
        },
        {
            "customer_id": "C001",
            "customer_name": "Rahul Duplicate",
            "email": "duplicate@example.com",
            "city": "Hyderabad",
            "created_at": "2026-01-02T10:00:00"
        }
    ])

    valid, rejects = validate_customers(customers)

    assert len(valid) == 1
    assert len(rejects) == 1


def test_invalid_email():
    customers = pd.DataFrame([
        {
            "customer_id": "C001",
            "customer_name": "Rahul",
            "email": "invalid-email",
            "city": "Hyderabad",
            "created_at": "2026-01-01T10:00:00"
        }
    ])

    valid, rejects = validate_customers(customers)

    assert len(valid) == 0
    assert len(rejects) == 1


def test_invalid_order_amount():
    orders = pd.DataFrame([
        {
            "order_id": "O001",
            "customer_id": "C001",
            "order_date": "2026-02-01",
            "amount": "-100",
            "status": "COMPLETED"
        }
    ])

    customers = pd.DataFrame([
        {"customer_id": "C001"}
    ])

    valid, rejects = validate_orders(orders, customers)

    assert len(valid) == 0
    assert len(rejects) == 1


def test_invalid_customer_reference():
    orders = pd.DataFrame([
        {
            "order_id": "O001",
            "customer_id": "C999",
            "order_date": "2026-02-01",
            "amount": "100",
            "status": "COMPLETED"
        }
    ])

    customers = pd.DataFrame([
        {"customer_id": "C001"}
    ])

    valid, rejects = validate_orders(orders, customers)

    assert len(valid) == 0
    assert len(rejects) == 1
    
def test_duplicate_order():
    orders = pd.DataFrame([
        {
            "order_id": "O001",
            "customer_id": "C001",
            "order_date": "2026-02-01",
            "amount": "100",
            "status": "COMPLETED"
        },
        {
            "order_id": "O001",
            "customer_id": "C001",
            "order_date": "2026-02-02",
            "amount": "200",
            "status": "COMPLETED"
        }
    ])

    customers = pd.DataFrame([
        {"customer_id": "C001"}
    ])

    valid, rejects = validate_orders(orders, customers)

    assert len(valid) == 1
    assert len(rejects) == 1


def test_null_order_id():
    orders = pd.DataFrame([
        {
            "order_id": "",
            "customer_id": "C001",
            "order_date": "2026-02-01",
            "amount": "100",
            "status": "COMPLETED"
        }
    ])

    customers = pd.DataFrame([
        {"customer_id": "C001"}
    ])

    valid, rejects = validate_orders(orders, customers)

    assert len(valid) == 0
    assert len(rejects) == 1


def test_invalid_order_date():
    orders = pd.DataFrame([
        {
            "order_id": "O001",
            "customer_id": "C001",
            "order_date": "not-a-date",
            "amount": "100",
            "status": "COMPLETED"
        }
    ])

    customers = pd.DataFrame([
        {"customer_id": "C001"}
    ])

    valid, rejects = validate_orders(orders, customers)

    assert len(valid) == 0
    assert len(rejects) == 1


def test_invalid_order_status():
    orders = pd.DataFrame([
        {
            "order_id": "O001",
            "customer_id": "C001",
            "order_date": "2026-02-01",
            "amount": "100",
            "status": "UNKNOWN"
        }
    ])

    customers = pd.DataFrame([
        {"customer_id": "C001"}
    ])

    valid, rejects = validate_orders(orders, customers)

    assert len(valid) == 0
    assert len(rejects) == 1


def test_empty_customers():
    customers = pd.DataFrame(columns=[
        "customer_id",
        "customer_name",
        "email",
        "city",
        "created_at"
    ])

    valid, rejects = validate_customers(customers)

    assert len(valid) == 0
    assert len(rejects) == 0