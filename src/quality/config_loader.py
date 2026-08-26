from pathlib import Path
import yaml


def load_quality_rules(config_path: str = "config/quality_rules.yaml") -> dict:
    """Load data quality rules from YAML configuration."""

    path = Path(config_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Quality rules configuration not found: {path}"
        )

    with path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if not config or "quality_rules" not in config:
        raise ValueError(
            "Configuration must contain a 'quality_rules' section."
        )

    return config["quality_rules"]