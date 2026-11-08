from src.malformed_handler import quarantine_malformed_csv


def test_malformed_csv_quarantine(tmp_path):

    input_file = tmp_path / "orders.csv"

    input_file.write_text(
        "order_id,customer_id,order_date,amount,status\n"
        "O001,C001,2026-01-01,100,COMPLETED\n"
        "O002,C002,2026-01-02,200\n"
        "O003,C003,2026-01-03,300,COMPLETED\n",
        encoding="utf-8"
    )
    expected_columns = [
    "order_id",
    "customer_id",
    "order_date",
    "amount",
    "status"
    ]

    valid, rejects = quarantine_malformed_csv(
    input_file,
    expected_columns,
    tmp_path / "rejects"
)   
    assert len(valid) ==2
    assert len(rejects) == 1
    assert rejects.iloc[0]["source_row"] == 3