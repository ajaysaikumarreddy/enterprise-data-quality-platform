def record_quality_metrics(total_records, failed_records):
    pass_rate = 0 if total_records == 0 else (
        (total_records - failed_records) / total_records
    ) * 100

    return {
        "total_records": total_records,
        "failed_records": failed_records,
        "pass_rate": pass_rate,
    }