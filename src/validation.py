import pandas as pd
import re


CUSTOMER_COLUMNS = [
    "customer_id",
    "customer_name",
    "email",
    "city",
    "created_at"
]

ORDER_COLUMNS = [
    "order_id",
    "customer_id",
    "order_date",
    "amount",
    "status"
]

ALLOWED_STATUSES = {
    "COMPLETED",
    "PENDING",
    "CANCELLED"
}


def validate_schema(df, required_columns):
    missing = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            f"SCHEMA_MISMATCH: Missing columns {missing}"
        )


def validate_customers(customers):

    df = customers.copy()

    validate_schema(df, CUSTOMER_COLUMNS)

    # Preserve source row numbers
    if "source_row" not in df.columns:
        df["source_row"] = df.index + 2

    reasons = [[] for _ in range(len(df))]

    def add_reason(mask, reason):
        for position, invalid in enumerate(mask):
            if invalid:
                reasons[position].append(reason)

    # Required fields
    for column in CUSTOMER_COLUMNS:

        missing = (
            df[column].isna()
            | df[column].astype(str).str.strip().eq("")
        )

        add_reason(
            missing.to_numpy(),
            f"MISSING_{column.upper()}"
        )

    # Duplicate customer IDs
    duplicate_ids = (
        df["customer_id"].duplicated(keep="first")
        & df["customer_id"].notna()
    )

    add_reason(
        duplicate_ids.to_numpy(),
        "DUPLICATE_CUSTOMER_ID"
    )

    # Email validation
    email_pattern = r"^[\w.+-]+@[\w-]+\.[\w.-]+$"

    invalid_email = ~df["email"].astype(str).str.match(
        email_pattern,
        na=False
    )

    add_reason(
        invalid_email.to_numpy(),
        "INVALID_EMAIL"
    )

    # Date validation
    parsed_dates = pd.to_datetime(
        df["created_at"],
        errors="coerce"
    )

    invalid_dates = parsed_dates.isna()

    add_reason(
        invalid_dates.to_numpy(),
        "INVALID_CREATED_AT"
    )

    # Construct rejects
    reject_mask = [
        len(record_reasons) > 0
        for record_reasons in reasons
    ]

    rejects = df.loc[reject_mask].copy()

    rejects["reject_reason"] = [
        ";".join(reasons[position])
        for position, rejected in enumerate(reject_mask)
        if rejected
    ]

    rejects["reject_code"] = "VALIDATION_FAILED"

    # Valid records
    valid = df.loc[
        [not rejected for rejected in reject_mask]
    ].copy()

    valid["created_at"] = parsed_dates.loc[valid.index]

    return valid, rejects


def validate_orders(orders, customers):

    df = orders.copy()

    validate_schema(df, ORDER_COLUMNS)

    if "source_row" not in df.columns:
        df["source_row"] = df.index + 2

    reasons = [[] for _ in range(len(df))]

    def add_reason(mask, reason):
        for position, invalid in enumerate(mask):
            if invalid:
                reasons[position].append(reason)

    # Required fields
    for column in ORDER_COLUMNS:

        missing = (
            df[column].isna()
            | df[column].astype(str).str.strip().eq("")
        )

        add_reason(
            missing.to_numpy(),
            f"MISSING_{column.upper()}"
        )

    # Duplicate order IDs
    duplicate_ids = (
        df["order_id"].duplicated(keep="first")
        & df["order_id"].notna()
    )

    add_reason(
        duplicate_ids.to_numpy(),
        "DUPLICATE_ORDER_ID"
    )

    # Amount validation
    parsed_amount = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    invalid_amount = (
        parsed_amount.isna()
        | (parsed_amount <= 0)
    )

    add_reason(
        invalid_amount.to_numpy(),
        "INVALID_AMOUNT"
    )

    # Order date validation
    parsed_dates = pd.to_datetime(
        df["order_date"],
        errors="coerce"
    )

    invalid_dates = parsed_dates.isna()

    add_reason(
        invalid_dates.to_numpy(),
        "INVALID_ORDER_DATE"
    )

    # Status validation
    normalized_status = (
        df["status"].astype(str).str.upper().str.strip()
    )

    invalid_status = ~normalized_status.isin(
        ALLOWED_STATUSES
    )

    add_reason(
        invalid_status.to_numpy(),
        "INVALID_ORDER_STATUS"
    )

    # Customer referential integrity
    valid_customer_ids = set(
        customers["customer_id"].dropna()
    )

    invalid_reference = (
        ~df["customer_id"].isin(valid_customer_ids)
    )

    add_reason(
        invalid_reference.to_numpy(),
        "INVALID_CUSTOMER_REFERENCE"
    )

    # Construct rejects
    reject_mask = [
        len(record_reasons) > 0
        for record_reasons in reasons
    ]

    rejects = df.loc[reject_mask].copy()

    rejects["reject_reason"] = [
        ";".join(reasons[position])
        for position, rejected in enumerate(reject_mask)
        if rejected
    ]

    rejects["reject_code"] = "VALIDATION_FAILED"

    # Valid records
    valid = df.loc[
        [not rejected for rejected in reject_mask]
    ].copy()

    valid["amount"] = parsed_amount.loc[valid.index]
    valid["order_date"] = parsed_dates.loc[valid.index]
    valid["status"] = normalized_status.loc[valid.index]

    return valid, rejects