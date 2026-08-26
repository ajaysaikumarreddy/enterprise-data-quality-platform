from src.quality.metrics import build_quality_metrics


def test_build_quality_metrics():
    report = {
        "status": "PASS",
        "quality_score": 100.0,
        "total_records": 5,
        "duplicate_count": 0,
        "missing_columns": [],
        "null_counts": {
            "customer_id": 0,
            "customer_name": 0,
            "email": 0,
        },
        "invalid_email_counts": {
            "email": 0,
        },
    }

    metrics = build_quality_metrics(report)

    assert metrics["status"] == "PASS"
    assert metrics["quality_score"] == 100.0
    assert metrics["total_records"] == 5
    assert metrics["failed_records"] == 0
    assert metrics["duplicate_records"] == 0
    assert metrics["null_violations"] == 0
    assert metrics["invalid_email_records"] == 0
    assert metrics["missing_columns"] == []
    assert "run_timestamp" in metrics