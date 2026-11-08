import pandas as pd
from src.publishing import publish_parquet


def test_publish_is_idempotent(tmp_path):
    df = pd.DataFrame({
        "order_id": ["O1", "O2"],
        "amount": [100, 200]
    })

    output_path = tmp_path / "orders.parquet"

    # First publish
    publish_parquet(df, output_path)

    first_output = pd.read_parquet(output_path)

    # Second publish with same data
    publish_parquet(df, output_path)

    second_output = pd.read_parquet(output_path)

    # Outputs must remain identical
    pd.testing.assert_frame_equal(
        first_output,
        second_output
    )

    # No duplicate records
    assert len(second_output) == 2

def test_failed_publish_preserves_existing_output(tmp_path, monkeypatch):
    import pandas as pd
    from src.publishing import publish_parquet

    output_path = tmp_path / "orders.parquet"

    original_df = pd.DataFrame({
        "order_id": ["O1"],
        "amount": [100]
    })

    publish_parquet(original_df, output_path)

    original_output = pd.read_parquet(output_path)

    new_df = pd.DataFrame({
        "order_id": ["O2"],
        "amount": [200]
    })

    def simulate_failure(*args, **kwargs):
        raise RuntimeError("Simulated write failure")

    monkeypatch.setattr(pd.DataFrame, "to_parquet", simulate_failure)

    try:
        publish_parquet(new_df, output_path)
    except RuntimeError:
        pass

    recovered_output = pd.read_parquet(output_path)

    pd.testing.assert_frame_equal(
        original_output,
        recovered_output
    )