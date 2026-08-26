import pandas as pd

from src.pipeline import run_data_quality_pipeline


def test_data_quality_pipeline():
    data = pd.DataFrame(
        {
            "customer_id": [1, 2, 3],
            "event_timestamp": [
                "2026-01-01",
                "2026-01-02",
                "2026-01-03",
            ],
            "value": [100, 200, 300],
        }
    )

    report = run_data_quality_pipeline(
        data,
        ["customer_id", "event_timestamp", "value"],
    )

    assert report["status"] == "PASS"
    assert report["quality_score"] == 100.0
    assert report["total_records"] == 3