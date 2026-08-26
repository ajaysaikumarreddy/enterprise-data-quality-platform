import pandas as pd

from src.quality.config_loader import load_quality_rules
from src.quality.profiler import profile_dataset
from src.quality.quality_engine import run_quality_checks
from src.quality.report import build_quality_report


def run_data_quality_pipeline(
    data: pd.DataFrame,
    required_columns: list[str] | None = None,
) -> dict:
    rules = load_quality_rules()

    required_columns = required_columns or rules["required_columns"]

    profile = profile_dataset(data)

    quality_result = run_quality_checks(
        data=data,
        required_columns=required_columns,
        not_null_columns=rules["not_null_columns"],
        unique_columns=rules["unique_columns"],
        email_columns=rules["email_columns"],
    )

    return build_quality_report(
        profile,
        quality_result,
    )