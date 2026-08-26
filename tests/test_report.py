from src.quality.report import build_quality_report


def test_build_quality_report():
    profile = {
        "row_count": 3,
        "column_count": 2,
        "columns": ["customer_id", "value"],
        "null_counts": {"customer_id": 0, "value": 0},
        "duplicate_count": 0,
    }

    quality_result = {
        "total_records": 3,
        "duplicate_count": 0,
        "quality_score": 100.0,
        "status": "PASS",
        "missing_columns": [],
    }

    report = build_quality_report(profile, quality_result)

    assert report["status"] == "PASS"
    assert report["quality_score"] == 100.0
    assert report["total_records"] == 3