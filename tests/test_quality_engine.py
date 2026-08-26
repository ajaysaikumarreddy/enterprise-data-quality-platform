import pandas as pd

from src.quality.quality_engine import run_quality_checks


def test_quality_engine_passes_clean_data():
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

    result = run_quality_checks(
        data,
        ["customer_id", "event_timestamp", "value"],
    )

    assert result["status"] == "PASS"
    assert result["quality_score"] == 100.0
    assert result["duplicate_count"] == 0