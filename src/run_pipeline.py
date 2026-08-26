import pandas as pd

from src.pipeline import run_data_quality_pipeline


def main():
    data = pd.read_csv("data/customers.csv")

    required_columns = [
        "customer_id",
        "event_timestamp",
        "value",
    ]

    report = run_data_quality_pipeline(
        data,
        required_columns,
    )

    print("Data Quality Report")
    print("--------------------")
    print(f"Status: {report['status']}")
    print(f"Quality Score: {report['quality_score']}%")
    print(f"Total Records: {report['total_records']}")
    print(f"Duplicate Records: {report['duplicate_count']}")
    print(f"Missing Columns: {report['missing_columns']}")


if __name__ == "__main__":
    main()