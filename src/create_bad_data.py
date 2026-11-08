import pandas as pd
from pathlib import Path

OUTPUT_DIR = Path("data/quality_test")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

customers = pd.DataFrame([
    ["C001", "Alice", "alice@example.com", "Hyderabad", "2026-01-01"],
    ["C002", "Bob", "bob@example.com", "Chennai", "2026-01-02"],
    ["C002", "Duplicate Bob", "bob2@example.com", "Chennai", "2026-01-03"],
    ["", "Missing ID", "missing@example.com", "Bengaluru", "2026-01-04"],
    ["C003", "Invalid Email", "not-an-email", "Delhi", "2026-01-05"],
    ["C004", "Invalid Date", "date@example.com", "Mumbai", "not-a-date"],
], columns=[
    "customer_id", "customer_name", "email", "city", "created_at"
])

orders = pd.DataFrame([
    ["O001", "C001", "2026-01-01", "100", "COMPLETED"],
    ["O002", "C002", "2026-01-02", "200", "PENDING"],
    ["O002", "C002", "2026-01-03", "300", "COMPLETED"],
    ["O003", "C001", "2026-01-04", "-50", "COMPLETED"],
    ["O004", "C999", "2026-01-05", "150", "COMPLETED"],
    ["O005", "C001", "2026-01-06", "100", "INVALID_STATUS"],
    ["", "C001", "2026-01-07", "100", "PENDING"],
    ["O006", "C001", "invalid-date", "100", "COMPLETED"],
], columns=[
    "order_id", "customer_id", "order_date", "amount", "status"
])

customers.to_csv(OUTPUT_DIR / "customers_bad.csv", index=False)
orders.to_csv(OUTPUT_DIR / "orders_bad.csv", index=False)

print("Data quality test datasets generated.")
print(f"Customers: {len(customers)}")
print(f"Orders: {len(orders)}")