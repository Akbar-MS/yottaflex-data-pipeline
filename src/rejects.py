import pandas as pd


def create_reject_records(
    rejected_df: pd.DataFrame,
    source_file: str,
    run_id: str
) -> pd.DataFrame:

    if rejected_df.empty:
        return pd.DataFrame()

    rejects = rejected_df.copy()

    rejects["source_file"] = source_file
    rejects["run_id"] = run_id

    if "source_row" not in rejects.columns:
        rejects["source_row"] = rejects.index + 2

    if "reject_reason" not in rejects.columns:
        rejects["reject_reason"] = "VALIDATION_FAILED"

    return rejects


def combine_rejects(*reject_datasets):
    non_empty = [
        df for df in reject_datasets
        if df is not None and not df.empty
    ]

    if not non_empty:
        return pd.DataFrame()

    return pd.concat(
        non_empty,
        ignore_index=True
    )