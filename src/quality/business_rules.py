import pandas as pd


def check_non_negative(
    data: pd.DataFrame,
    columns: list[str],
) -> dict:
    invalid_counts = {}

    for column in columns:
        if column not in data.columns:
            continue

        invalid_counts[column] = int(
            (data[column] < 0).sum()
        )

    total_invalid = sum(invalid_counts.values())

    return {
        "invalid_counts": invalid_counts,
        "total_invalid": total_invalid,
        "status": "PASS" if total_invalid == 0 else "FAIL",
    }