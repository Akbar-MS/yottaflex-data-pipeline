from pathlib import Path

from ingestion import ingest_customers, ingest_orders
from validation import validate_customers, validate_orders
from transformation import (
    transform_customers,
    transform_orders,
    create_customer_order_summary
)
from publishing import publish_curated_datasets
from metrics import start_run, finish_run, save_run_report
from reconciliation import (
    build_reconciliation,
    save_reconciliation
)
from rejects import create_reject_records, combine_rejects
from malformed_handler import quarantine_malformed_csv

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_DIR = BASE_DIR / "data" / "input"


def main():
    run = start_run()
    malformed_customer_records = quarantine_malformed_csv(
    INPUT_DIR / "customers.csv",
    [
        "customer_id",
        "customer_name",
        "email",
        "city",
        "created_at"
    ],
    BASE_DIR / "data" / "rejects"
    )

    malformed_order_records = quarantine_malformed_csv(
    INPUT_DIR / "orders.csv",
    [
        "order_id",
        "customer_id",
        "order_date",
        "amount",
        "status"
    ],
    BASE_DIR / "data" / "rejects"
    )

    print(
    f"Malformed customer records: "
    f"{len(malformed_customer_records)}"
    )

    print(
    f"Malformed order records: "
    f"{len(malformed_order_records)}"
    )
    # Ingestion
    customers_raw = ingest_customers(
        INPUT_DIR / "customers.csv"
    )

    orders_raw = ingest_orders(
        INPUT_DIR / "orders.csv"
    )

    # Customer validation
    customers_valid, customer_rejects = validate_customers(
        customers_raw
    )

    # Order validation
    orders_valid, order_rejects = validate_orders(
        orders_raw,
        customers_valid
    )

    print("\n--- VALIDATION RESULTS ---")

    print(f"Customers input: {len(customers_raw)}")
    print(f"Customers valid: {len(customers_valid)}")
    print(f"Customers rejected: {len(customer_rejects)}")

    print(f"\nOrders input: {len(orders_raw)}")
    print(f"Orders valid: {len(orders_valid)}")
    print(f"Orders rejected: {len(order_rejects)}")

    # Transformations
    customers_curated = transform_customers(
    customers_valid
    )

    orders_curated = transform_orders(
    orders_valid
    )

    customer_summary = create_customer_order_summary(
    customers_curated,
    orders_curated
    )

    print("\n--- TRANSFORMATION RESULTS ---")
  
    print(f"Curated customers: {len(customers_curated)}")
    print(f"Curated orders: {len(orders_curated)}")
    print(f"Customer summary: {len(customer_summary)}")

    print("\nCustomer summary sample:")
    print(customer_summary.head())

    # Publishing
    OUTPUT_DIR = BASE_DIR / "data" / "output"

    publish_curated_datasets(
    customers_curated,
    orders_curated,
    customer_summary,
    OUTPUT_DIR
    )

    print("\n--- PUBLISHING RESULTS ---")
    print("Curated datasets published successfully.")

    metrics = {
    "customers_input": len(customers_raw),
    "customers_valid": len(customers_valid),
    "customers_rejected": len(customer_rejects),
    "orders_input": len(orders_raw),
    "orders_valid": len(orders_valid),
    "orders_rejected": len(order_rejects),
    "customers_published": len(customers_curated),
    "orders_published": len(orders_curated),
    "summary_published": len(customer_summary)
    }

    run_report = finish_run(
    run,
    metrics,
    status="SUCCESS"
    )

    report_path = save_run_report(
    run_report,
    BASE_DIR / "reports"
    )

    print(f"\nRun ID: {run_report['run_id']}")
    print(f"Duration: {run_report['duration_seconds']} seconds")
    print(f"Status: {run_report['status']}")
    print(f"Run report: {report_path}")

    reconciliation = build_reconciliation(
    customers_raw,
    customers_valid,
    customer_rejects,
    orders_raw,
    orders_valid,
    order_rejects,
    customers_curated,
    orders_curated
    )

    reconciliation_path = save_reconciliation(
    reconciliation,
    BASE_DIR / "reports"
    )

    print("\n--- RECONCILIATION ---")
    print(reconciliation)
    print(f"Report saved: {reconciliation_path}")

    customer_rejects = create_reject_records(
    customer_rejects,
    "customers.csv",
    run["run_id"]
    )

    order_rejects = create_reject_records(
    order_rejects,
    "orders.csv",
    run["run_id"]
    )

    all_rejects = combine_rejects(
    customer_rejects,
    order_rejects
    )

    # Save rejects
    reject_dir = BASE_DIR / "data" / "rejects"
    reject_dir.mkdir(parents=True, exist_ok=True)

    customer_rejects.to_csv(
        reject_dir / "customer_rejects.csv",
        index=False
    )

    order_rejects.to_csv(
        reject_dir / "order_rejects.csv",
        index=False
    )

    all_rejects.to_csv(
    reject_dir / "all_rejects.csv",
    index=False
   )

    print("\nReject datasets saved successfully.")



if __name__ == "__main__":
    main()