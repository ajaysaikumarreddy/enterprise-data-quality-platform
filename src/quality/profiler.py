import pandas as pd


def profile_dataset(data: pd.DataFrame) -> dict:
    return {
        "row_count": len(data),
        "column_count": len(data.columns),
        "columns": list(data.columns),
        "null_counts": data.isnull().sum().to_dict(),
        "duplicate_count": int(data.duplicated().sum()),
    }