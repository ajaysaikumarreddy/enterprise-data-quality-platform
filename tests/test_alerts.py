from src.quality.alerts import evaluate_quality_alert


def test_quality_alert_pass():
    alert = evaluate_quality_alert(100.0)

    assert alert.status == "PASS"
    assert alert.severity == "NONE"
    assert alert.quality_score == 100.0


def test_quality_alert_failure():
    alert = evaluate_quality_alert(90.0)

    assert alert.status == "ALERT"
    assert alert.severity == "HIGH"
    assert alert.quality_score == 90.0


def test_quality_alert_threshold():
    alert = evaluate_quality_alert(95.0)

    assert alert.status == "PASS"
    assert alert.severity == "NONE"