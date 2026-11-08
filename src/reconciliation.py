import pandas as pd
from pathlib import Path
import json


def build_reconciliation(
    customers_raw,
    customers_valid,
    customer_rejects,
    orders_raw,
    orders_valid,
    order_rejects,
    customers_published,
    orders_published
):
    report = {
        "customers": {
            "input_count": len(customers_raw),
            "valid_count": len(customers_valid),
            "reject_count": len(customer_rejects),
            "published_count": len(customers_published),
            "reconciled": (
                len(customers_raw)
                == len(customers_valid) + len(customer_rejects)
            )
        },
        "orders": {
            "input_count": len(orders_raw),
            "valid_count": len(orders_valid),
            "reject_count": len(order_rejects),
            "published_count": len(orders_published),
            "input_amount": float(
                pd.to_numeric(
                    orders_raw["amount"],
                    errors="coerce"
                ).sum()
            ),
            "valid_amount": float(orders_valid["amount"].sum()),
            "reconciled": (
                len(orders_raw)
                == len(orders_valid) + len(order_rejects)
            )
        }
    }

    report["customers"]["publish_match"] = (
        len(customers_valid) == len(customers_published)
    )

    report["orders"]["publish_match"] = (
        len(orders_valid) == len(orders_published)
    )

    return report


def save_reconciliation(report, reports_dir: Path):
    reports_dir.mkdir(parents=True, exist_ok=True)

    path = reports_dir / "reconciliation.json"

    with open(path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    return path