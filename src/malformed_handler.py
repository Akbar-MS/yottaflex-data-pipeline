import csv
from pathlib import Path
import pandas as pd


def quarantine_malformed_csv(
    file_path: str | Path,
    expected_columns: list[str],
    reject_dir: str | Path
) -> tuple[pd.DataFrame, pd.DataFrame]:

    file_path = Path(file_path)
    reject_dir = Path(reject_dir)

    reject_dir.mkdir(parents=True, exist_ok=True)

    valid_records = []
    valid_source_rows = []
    rejects = []

    with file_path.open("r", encoding="utf-8", newline="") as file:

        reader = csv.reader(file, strict=True)

        try:
            header = next(reader)
        except StopIteration:
            raise ValueError(f"Empty CSV file: {file_path.name}")

        if header != expected_columns:
            raise ValueError(
                f"Schema mismatch in {file_path.name}. "
                f"Expected {expected_columns}, received {header}"
            )

        row_number = 1

        while True:
            try:
                row = next(reader)
                row_number += 1

                # Validate record field count
                if len(row) != len(expected_columns):

                    rejects.append({
                        "source_file": file_path.name,
                        "source_row": row_number,
                        "raw_record": repr(row),
                        "reject_reason": (
                            f"Expected {len(expected_columns)} fields, "
                            f"received {len(row)}"
                        ),
                        "reject_code": "MALFORMED_RECORD"
                    })

                    continue

                # Valid CSV structure
                valid_records.append(row)

                # Preserve original source row number
                valid_source_rows.append(row_number)

            except StopIteration:
                break

            except csv.Error as exc:

                row_number += 1

                rejects.append({
                    "source_file": file_path.name,
                    "source_row": row_number,
                    "raw_record": "UNPARSABLE_CSV_RECORD",
                    "reject_reason": f"MALFORMED_CSV: {exc}",
                    "reject_code": "CSV_PARSE_ERROR"
                })

                # Stop processing after an unrecoverable CSV parsing error
                break

    # Create valid DataFrame
    valid_df = pd.DataFrame(
        valid_records,
        columns=expected_columns
    )

    # Correct original source row tracking
    valid_df["source_row"] = valid_source_rows

    # Create rejects DataFrame
    reject_df = pd.DataFrame(
        rejects,
        columns=[
            "source_file",
            "source_row",
            "raw_record",
            "reject_reason",
            "reject_code"
        ]
    )

    # Save malformed records separately
    if not reject_df.empty:

        malformed_output = (
            reject_dir / f"{file_path.stem}_malformed.csv"
        )

        reject_df.to_csv(
            malformed_output,
            index=False
        )

    return valid_df, reject_df