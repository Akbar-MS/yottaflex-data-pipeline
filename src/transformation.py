import pandas as pd


def transform_customers(customers: pd.DataFrame) -> pd.DataFrame:
    df = customers.copy()

    df["created_at"] = pd.to_datetime(
        df["created_at"],
        utc=True
    )

    df["customer_created_date"] = (
        df["created_at"].dt.date
    )

    df["customer_name"] = (
        df["customer_name"].str.strip()
    )

    df["email"] = (
        df["email"].str.strip().str.lower()
    )

    df["city"] = df["city"].str.strip()

    return df


def transform_orders(orders: pd.DataFrame) -> pd.DataFrame:
    df = orders.copy()

    df["order_date"] = pd.to_datetime(
        df["order_date"]
    )

    df["amount"] = pd.to_numeric(
        df["amount"]
    )

    df["status"] = df["status"].str.upper()

    df["order_year"] = df["order_date"].dt.year
    df["order_month"] = df["order_date"].dt.month

    return df


def create_customer_order_summary(
    customers: pd.DataFrame,
    orders: pd.DataFrame
) -> pd.DataFrame:

    # Aggregate orders
    order_summary = orders.groupby(
        "customer_id"
    ).agg(
        total_orders=("order_id", "count"),
        completed_orders=(
            "status",
            lambda x: (x == "COMPLETED").sum()
        ),
        completed_revenue=(
            "amount",
            lambda x: x[
                orders.loc[x.index, "status"] == "COMPLETED"
            ].sum()
        )
    ).reset_index()

    # Merge with customers
    summary = customers.merge(
        order_summary,
        on="customer_id",
        how="left"
    )

    # Customers without orders
    summary["total_orders"] = (
        summary["total_orders"].fillna(0).astype(int)
    )

    summary["completed_orders"] = (
        summary["completed_orders"].fillna(0).astype(int)
    )

    summary["completed_revenue"] = (
        summary["completed_revenue"].fillna(0.0)
    )

    summary["average_completed_order_value"] = (
        summary["completed_revenue"] /
        summary["completed_orders"].replace(0, pd.NA)
    )

    return summary