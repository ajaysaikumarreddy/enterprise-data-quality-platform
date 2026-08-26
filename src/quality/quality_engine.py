import re

import pandas as pd


def run_quality_checks(
    data: pd.DataFrame,
    required_columns: list[str],
    not_null_columns: list[str] | None = None,
    unique_columns: list[str] | None = None,
    email_columns: list[str] | None = None,
) -> dict:
    not_null_columns = not_null_columns or []
    unique_columns = unique_columns or []
    email_columns = email_columns or []

    missing_columns = [
        column
        for column in required_columns
        if column not in data.columns
    ]

    null_counts = {
        column: int(data[column].isnull().sum())
        for column in not_null_columns
        if column in data.columns
    }

    duplicate_count = 0

    for column in unique_columns:
        if column in data.columns:
            duplicate_count += int(data[column].duplicated().sum())

    invalid_email_counts = {}

    email_pattern = re.compile(
        r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    )

    for column in email_columns:
        if column in data.columns:
            invalid_count = int(
                data[column]
                .fillna("")
                .astype(str)
                .apply(lambda value: not bool(email_pattern.match(value)))
                .sum()
            )

            invalid_email_counts[column] = invalid_count

    total_records = len(data)

    null_failed_records = sum(null_counts.values())
    failed_records = max(
        null_failed_records,
        duplicate_count,
        sum(invalid_email_counts.values()),
    )

    if total_records == 0:
        quality_score = 0
    else:
        quality_score = max(
            0,
            ((total_records - failed_records) / total_records) * 100,
        )

    status = (
        "PASS"
        if not missing_columns and quality_score >= 95
        else "FAIL"
    )

    return {
        "total_records": total_records,
        "missing_columns": missing_columns,
        "null_counts": null_counts,
        "duplicate_count": duplicate_count,
        "invalid_email_counts": invalid_email_counts,
        "quality_score": round(quality_score, 2),
        "status": status,
    }