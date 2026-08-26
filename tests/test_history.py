import json

from src.quality.history import save_quality_result


def test_save_quality_result(tmp_path, monkeypatch):
    history_file = tmp_path / "quality_history.json"

    monkeypatch.setattr(
        "src.quality.history.HISTORY_FILE",
        history_file,
    )

    metrics = {
        "status": "PASS",
        "quality_score": 100.0,
        "total_records": 5,
        "failed_records": 0,
    }

    save_quality_result(metrics)

    with history_file.open("r", encoding="utf-8") as file:
        history = json.load(file)

    assert len(history) == 1
    assert history[0]["status"] == "PASS"
    assert history[0]["quality_score"] == 100.0