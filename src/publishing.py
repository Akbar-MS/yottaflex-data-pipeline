import pandas as pd
from pathlib import Path


def publish_parquet(
    df: pd.DataFrame,
    output_path: Path
):
    """
    Publish a curated dataset atomically using a temporary file.
    """
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    temp_path = output_path.with_suffix(".tmp.parquet")

    df.to_parquet(
        temp_path,
        index=False
    )

    # Replace previous output only after successful write
    temp_path.replace(output_path)


def publish_curated_datasets(
    customers: pd.DataFrame,
    orders: pd.DataFrame,
    summary: pd.DataFrame,
    output_dir: Path
):
    publish_parquet(
        customers,
        output_dir / "customers_curated.parquet"
    )

    publish_parquet(
        orders,
        output_dir / "orders_curated.parquet"
    )

    publish_parquet(
        summary,
        output_dir / "customer_order_summary.parquet"
    )
