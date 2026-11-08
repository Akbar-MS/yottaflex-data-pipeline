import pandas as pd
from src.validation import validate_customers, validate_orders


def test_bad_customer_records_are_rejected():
    customers = pd.read_csv(
        "data/quality_test/customers_bad.csv",
        dtype="string"
    )

    valid, rejected = validate_customers(customers)

    assert len(rejected) > 0
    assert len(valid) + len(rejected) == len(customers)

    print("\nCustomer rejects:")
    print(rejected[["customer_id", "reject_reason"]])


def test_bad_order_records_are_rejected():
    customers = pd.DataFrame({
        "customer_id": ["C001", "C002"]
    })

    orders = pd.read_csv(
        "data/quality_test/orders_bad.csv",
        dtype="string"
    )

    valid, rejected = validate_orders(orders, customers)

    assert len(rejected) > 0
    assert len(valid) + len(rejected) == len(orders)

    print("\nOrder rejects:")
    print(rejected[["order_id", "reject_reason"]])