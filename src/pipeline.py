import pandas as pd

from src.quality.alerts import evaluate_quality_alert
from src.quality.config_loader import load_quality_rules
from src.quality.history import load_quality_history, save_quality_result
from src.quality.metrics import build_quality_metrics
from src.quality.profiler import profile_dataset
from src.quality.quality_engine import run_quality_checks
from src.quality.report import build_quality_report
from src.quality.trend import build_quality_trend


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

    report = build_quality_report(
        profile,
        quality_result,
    )

    metrics = build_quality_metrics(report)

    report["metrics"] = metrics

    save_quality_result(metrics)

    history = load_quality_history()

    report["trend"] = build_quality_trend(history)

    report["alert"] = evaluate_quality_alert(
    metrics["quality_score"],
    threshold=rules["quality_score_threshold"],
)

    return report