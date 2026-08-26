import pandas as pd


def run_quality_checks(data: pd.DataFrame, required_columns: list[str]) -> dict:
    missing_columns = [
        column for column in required_columns
        if column not in data.columns
    ]

    null_counts = data.isnull().sum().to_dict()
    duplicate_count = int(data.duplicated().sum())

    total_records = len(data)

    if total_records == 0:
        quality_score = 0
    else:
        null_records = int(data.isnull().any(axis=1).sum())
        failed_records = max(null_records, duplicate_count)
        quality_score = (
            (total_records - failed_records) / total_records
        ) * 100

    return {
        "total_records": total_records,
        "missing_columns": missing_columns,
        "null_counts": null_counts,
        "duplicate_count": duplicate_count,
        "quality_score": round(quality_score, 2),
        "status": "PASS" if (
            not missing_columns and quality_score >= 95
        ) else "FAIL",
    }