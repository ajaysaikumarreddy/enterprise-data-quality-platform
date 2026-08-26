def check_required_columns(data, required_columns):
    missing = [column for column in required_columns if column not in data.columns]
    return missing