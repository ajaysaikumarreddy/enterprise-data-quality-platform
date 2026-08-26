import pandas as pd


def check_referential_integrity(
    child_data: pd.DataFrame,
    parent_data: pd.DataFrame,
    child_key: str,
    parent_key: str,
) -> dict:
    if child_key not in child_data.columns:
        raise ValueError(f"Child key not found: {child_key}")

    if parent_key not in parent_data.columns:
        raise ValueError(f"Parent key not found: {parent_key}")

    parent_keys = set(parent_data[parent_key].dropna())

    orphan_count = int(
        (~child_data[child_key].isin(parent_keys)).sum()
    )

    return {
        "child_key": child_key,
        "parent_key": parent_key,
        "orphan_count": orphan_count,
        "status": "PASS" if orphan_count == 0 else "FAIL",
    }