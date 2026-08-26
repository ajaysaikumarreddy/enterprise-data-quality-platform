import pandas as pd

from src.quality.referential_integrity import (
    check_referential_integrity,
)


def test_referential_integrity_passes():
    parent_data = pd.DataFrame(
        {
            "customer_id": [1, 2, 3],
        }
    )

    child_data = pd.DataFrame(
        {
            "customer_id": [1, 2, 3],
        }
    )

    result = check_referential_integrity(
        child_data,
        parent_data,
        "customer_id",
        "customer_id",
    )

    assert result["orphan_count"] == 0
    assert result["status"] == "PASS"


def test_referential_integrity_detects_orphans():
    parent_data = pd.DataFrame(
        {
            "customer_id": [1, 2, 3],
        }
    )

    child_data = pd.DataFrame(
        {
            "customer_id": [1, 2, 99],
        }
    )

    result = check_referential_integrity(
        child_data,
        parent_data,
        "customer_id",
        "customer_id",
    )

    assert result["orphan_count"] == 1
    assert result["status"] == "FAIL"