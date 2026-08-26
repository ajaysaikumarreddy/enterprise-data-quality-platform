import json
from pathlib import Path


HISTORY_FILE = Path("data/quality_history.json")


def load_quality_history(
    history_file: Path | None = None,
) -> list[dict]:
    history_file = history_file or HISTORY_FILE

    if not history_file.exists():
        return []

    with history_file.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_quality_result(metrics: dict) -> None:
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)

    history = load_quality_history()

    history.append(metrics)

    with HISTORY_FILE.open("w", encoding="utf-8") as file:
        json.dump(history, file, indent=2)