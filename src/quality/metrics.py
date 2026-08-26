from datetime import datetime, timezone


def build_quality_metrics(report: dict) -> dict:
    """
    Build standardized metrics from a data-quality report.
    """

    null_counts = report.get("null_counts", {})
    invalid_email_counts = report.get("invalid_email_counts", {})

    null_violations = sum(null_counts.values())
    invalid_email_records = sum(invalid_email_counts.values())

    total_records = report.get("total_records", 0)

    duplicate_records = report.get("duplicate_count", 0)

    failed_records = max(
        null_violations,
        duplicate_records,
        invalid_email_records,
    )

    return {
        "run_timestamp": datetime.now(timezone.utc).isoformat(),
        "status": report.get("status", "UNKNOWN"),
        "quality_score": report.get("quality_score", 0),
        "total_records": total_records,
        "failed_records": failed_records,
        "duplicate_records": duplicate_records,
        "null_violations": null_violations,
        "invalid_email_records": invalid_email_records,
        "missing_columns": report.get("missing_columns", []),
    }