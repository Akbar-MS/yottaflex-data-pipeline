import time
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from ingestion import ingest_customers, ingest_orders # type: ignore
from validation import validate_customers, validate_orders # type: ignore
from transformation import ( # type: ignore
    transform_customers,
    transform_orders,
    create_customer_order_summary
)


INPUT_DIR = PROJECT_ROOT / "data" / "input"


def main():
    start = time.perf_counter()

    customers_raw = ingest_customers(
        INPUT_DIR / "customers.csv"
    )

    orders_raw = ingest_orders(
        INPUT_DIR / "orders.csv"
    )

    customers_valid, _ = validate_customers(
        customers_raw
    )

    orders_valid, _ = validate_orders(
        orders_raw,
        customers_valid
    )

    customers = transform_customers(
        customers_valid
    )

    orders = transform_orders(
        orders_valid
    )

    summary = create_customer_order_summary(
        customers,
        orders
    )

    elapsed = time.perf_counter() - start

    print("\n--- PERFORMANCE BENCHMARK ---")
    print(f"Customers processed: {len(customers)}")
    print(f"Orders processed: {len(orders)}")
    print(f"Summary records: {len(summary)}")
    print(f"Execution time: {elapsed:.3f} seconds")
    print(
        f"Orders per second: "
        f"{len(orders) / elapsed:.2f}"
    )


if __name__ == "__main__":
    main()