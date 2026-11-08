import csv
import random
from pathlib import Path
from datetime import datetime, timedelta

random.seed(42)

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_DIR = BASE_DIR / "data" / "input"
INPUT_DIR.mkdir(parents=True, exist_ok=True)

CUSTOMERS_FILE = INPUT_DIR / "customers.csv"
ORDERS_FILE = INPUT_DIR / "orders.csv"


def generate_customers(count=1000):
    customers = []

    for i in range(1, count + 1):
        customers.append({
            "customer_id": f"C{i:06d}",
            "customer_name": f"Customer_{i}",
            "email": f"customer{i}@example.com",
            "city": random.choice(
                ["Hyderabad", "Bengaluru", "Chennai", "Mumbai"]
            ),
            "created_at": (
                datetime(2026, 1, 1) +
                timedelta(days=random.randint(0, 300))
            ).isoformat()
        })

    return customers


def generate_orders(count=10000, customer_count=1000):
    orders = []

    for i in range(1, count + 1):
        orders.append({
            "order_id": f"O{i:08d}",
            "customer_id": f"C{random.randint(1, customer_count):06d}",
            "order_date": (
                datetime(2026, 1, 1) +
                timedelta(days=random.randint(0, 300))
            ).date().isoformat(),
            "amount": round(random.uniform(100, 10000), 2),
            "status": random.choice(
                ["COMPLETED", "PENDING", "CANCELLED"]
            )
        })

    return orders


def write_csv(path, records):
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)


def main():
    customers = generate_customers(10000)
    orders = generate_orders(100000, 10000)
    write_csv(CUSTOMERS_FILE, customers)
    write_csv(ORDERS_FILE, orders)

    print(f"Customers generated: {len(customers)}")
    print(f"Orders generated: {len(orders)}")
    print("Sample data generated successfully!")


if __name__ == "__main__":
    main()