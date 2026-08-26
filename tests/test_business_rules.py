import pandas as pd

from src.quality.business_rules import check_non_negative


def test_non_negative_values_pass():
    data = pd.DataFrame(
        {
            "value": [100, 200, 300],
        }
    )

    result = check_non_negative(
        data,
        ["value"],
    )

    assert result["total_invalid"] == 0
    assert result["status"] == "PASS"


def test_negative_values_fail():
    data = pd.DataFrame(
        {
            "value": [100, -50, 300],
        }
    )

    result = check_non_negative(
        data,
        ["value"],
    )

    assert result["total_invalid"] == 1
    assert result["status"] == "FAIL"