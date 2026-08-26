import pandas as pd

from src.quality.quality_checks import check_required_columns


def test_required_columns():
    data = pd.DataFrame(
        {
            "customer_id": [1],
            "event_timestamp": ["2026-01-01"],
            "value": [100],
        }
    )

    required = ["customer_id", "event_timestamp", "value"]

    assert check_required_columns(data, required) == []