from src.quality.trend import build_quality_trend


def test_quality_trend_improving():
    history = [
        {
            "quality_score": 90.0,
        },
        {
            "quality_score": 100.0,
        },
    ]

    result = build_quality_trend(history)

    assert result["run_count"] == 2
    assert result["latest_score"] == 100.0
    assert result["average_score"] == 95.0
    assert result["trend"] == "IMPROVING"


def test_quality_trend_declining():
    history = [
        {
            "quality_score": 100.0,
        },
        {
            "quality_score": 90.0,
        },
    ]

    result = build_quality_trend(history)

    assert result["trend"] == "DECLINING"


def test_quality_trend_stable():
    history = [
        {
            "quality_score": 100.0,
        },
        {
            "quality_score": 100.0,
        },
    ]

    result = build_quality_trend(history)

    assert result["trend"] == "STABLE"