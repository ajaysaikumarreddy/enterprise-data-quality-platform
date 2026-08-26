from pathlib import Path

import yaml


CONFIG_FILE = Path("config/quality_rules.yaml")


def load_quality_rules() -> dict:
    with CONFIG_FILE.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file) or {}

    return {
        "required_columns": config.get("required_columns", []),
        "not_null_columns": config.get("not_null_columns", []),
        "unique_columns": config.get("unique_columns", []),
        "email_columns": config.get("email_columns", []),
        "quality_score_threshold": float(
            config.get("quality_score_threshold", 95.0)
        ),
    }