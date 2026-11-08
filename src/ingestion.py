import pandas as pd
from pathlib import Path

from malformed_handler import quarantine_malformed_csv


class SchemaMismatchError(Exception):
    pass


class MalformedCSVError(Exception):
    pass


def ingest_csv(
    file_path: str,
    expected_columns: list[str],
    reject_dir: str | Path = "data/rejects"
) -> pd.DataFrame:

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Input file not found: {path}"
        )

    try:
        df, malformed_rejects = quarantine_malformed_csv(
            file_path=path,
            expected_columns=expected_columns,
            reject_dir=reject_dir
        )

    except ValueError as exc:
        raise SchemaMismatchError(
            f"Schema mismatch in {path.name}: {exc}"
        ) from exc

    except Exception as exc:
        raise MalformedCSVError(
            f"Malformed CSV in {path.name}: {exc}"
        ) from exc

    if not malformed_rejects.empty:
        print(
            f"Malformed records quarantined in "
            f"{path.name}: {len(malformed_rejects)}"
        )

    return df


def ingest_customers(
    file_path: str,
    reject_dir: str | Path = "data/rejects"
) -> pd.DataFrame:

    expected_columns = [
        "customer_id",
        "customer_name",
        "email",
        "city",
        "created_at"
    ]

    return ingest_csv(
        file_path,
        expected_columns,
        reject_dir
    )


def ingest_orders(
    file_path: str,
    reject_dir: str | Path = "data/rejects"
) -> pd.DataFrame:

    expected_columns = [
        "order_id",
        "customer_id",
        "order_date",
        "amount",
        "status"
    ]

    return ingest_csv(
        file_path,
        expected_columns,
        reject_dir
    )