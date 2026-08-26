import pandas as pd

from src.quality.profiler import profile_dataset


def test_profile_dataset():
    data = pd.DataFrame(
        {
            "customer_id": [1, 2, 3],
            "value": [100, 200, 300],
        }
    )

    profile = profile_dataset(data)

    assert profile["row_count"] == 3
    assert profile["column_count"] == 2
    assert profile["duplicate_count"] == 0