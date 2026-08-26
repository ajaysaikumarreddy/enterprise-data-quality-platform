from datetime import UTC, datetime


def build_quality_report(profile: dict, quality_result: dict) -> dict:
    return {
        "run_timestamp": datetime.now(UTC).isoformat(),
        "total_records": quality_result["total_records"],
        "duplicate_count": quality_result["duplicate_count"],
        "quality_score": quality_result["quality_score"],
        "status": quality_result["status"],
        "missing_columns": quality_result["missing_columns"],
        "profile": profile,
    }