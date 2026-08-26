import json
from pathlib import Path


def load_quality_history(
    history_file: Path = Path("data/quality_history.json"),
) -> list[dict]:
    if not history_file.exists():
        return []

    with history_file.open("r", encoding="utf-8") as file:
        return json.load(file)


def build_quality_trend(
    history: list[dict],
) -> dict:
    if not history:
        return {
            "run_count": 0,
            "latest_score": None,
            "average_score": None,
            "trend": "NO_DATA",
        }

    scores = [
        float(item["quality_score"])
        for item in history
    ]

    latest_score = scores[-1]
    average_score = sum(scores) / len(scores)

    if len(scores) == 1:
        trend = "STABLE"
    elif scores[-1] > scores[-2]:
        trend = "IMPROVING"
    elif scores[-1] < scores[-2]:
        trend = "DECLINING"
    else:
        trend = "STABLE"

    return {
        "run_count": len(scores),
        "latest_score": latest_score,
        "average_score": round(average_score, 2),
        "trend": trend,
    }