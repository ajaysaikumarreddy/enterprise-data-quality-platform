from src.quality.config_loader import load_quality_rules


def test_load_quality_rules():
    rules = load_quality_rules()

    assert "required_columns" in rules
    assert "not_null_columns" in rules
    assert "unique_columns" in rules
    assert "email_columns" in rules

    assert "customer_id" in rules["required_columns"]
    assert "email" in rules["email_columns"]