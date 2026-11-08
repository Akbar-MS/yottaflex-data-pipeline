from src.ingestion import ingest_orders


def test_ingestion_quarantines_malformed_rows(tmp_path):

    input_file = tmp_path / "orders.csv"

    input_file.write_text(
        "order_id,customer_id,order_date,amount,status\n"
        "O001,C001,2026-01-01,100,COMPLETED\n"
        "O002,C002,2026-01-02,200\n"
        "O003,C003,2026-01-03,300,COMPLETED\n",
        encoding="utf-8"
    )

    reject_dir = tmp_path / "rejects"

    valid = ingest_orders(
        input_file,
        reject_dir
    )

    assert len(valid) == 2

    assert list(valid["order_id"]) == [
        "O001",
        "O003"
    ]

    assert list(valid["source_row"]) == [
        2,
        4
    ]

    malformed_file = (
        reject_dir / "orders_malformed.csv"
    )

    assert malformed_file.exists()