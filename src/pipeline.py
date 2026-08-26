import pandas as pd

from src.quality.profiler import profile_dataset
from src.quality.quality_engine import run_quality_checks
from src.quality.report import build_quality_report


def run_data_quality_pipeline(
    data: pd.DataFrame,
    required_columns: list[str],
) -> dict:
    profile = profile_dataset(data)

    quality_result = run_quality_checks(
        data,
        required_columns,
    )

    return build_quality_report(
        profile,
        quality_result,
    )