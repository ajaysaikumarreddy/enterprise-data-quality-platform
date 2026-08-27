import json

from src.quality.issue_registry import (
    create_issue,
    load_issues,
    save_issue,
    update_issue_status,
)


def test_create_issue():
    issue = create_issue(
        check_name="duplicate_customer_id",
        message="Duplicate customer IDs detected.",
    )

    assert issue["check_name"] == "duplicate_customer_id"
    assert issue["severity"] == "HIGH"
    assert issue["status"] == "OPEN"
    assert "issue_id" in issue
    assert "created_at" in issue


def test_save_and_load_issue(tmp_path, monkeypatch):
    issue_file = tmp_path / "dq_issues.json"

    monkeypatch.setattr(
        "src.quality.issue_registry.ISSUE_FILE",
        issue_file,
    )

    issue = create_issue(
        check_name="null_email",
        message="Null email values detected.",
        severity="MEDIUM",
    )

    save_issue(issue)

    issues = load_issues()

    assert len(issues) == 1
    assert issues[0]["check_name"] == "null_email"
    assert issues[0]["severity"] == "MEDIUM"

def test_update_issue_status(tmp_path, monkeypatch):
    issue_file = tmp_path / "dq_issues.json"

    monkeypatch.setattr(
        "src.quality.issue_registry.ISSUE_FILE",
        issue_file,
    )

    issue = create_issue(
        check_name="duplicate_customer_id",
        message="Duplicate customer IDs detected.",
    )

    save_issue(issue)

    updated_issue = update_issue_status(
        issue["issue_id"],
        "ACKNOWLEDGED",
    )

    assert updated_issue["status"] == "ACKNOWLEDGED"
    assert "updated_at" in updated_issue

    issues = load_issues()

    assert len(issues) == 1
    assert issues[0]["status"] == "ACKNOWLEDGED"


def test_resolve_issue(tmp_path, monkeypatch):
    issue_file = tmp_path / "dq_issues.json"

    monkeypatch.setattr(
        "src.quality.issue_registry.ISSUE_FILE",
        issue_file,
    )

    issue = create_issue(
        check_name="invalid_email",
        message="Invalid email detected.",
        severity="MEDIUM",
    )

    save_issue(issue)

    updated_issue = update_issue_status(
        issue["issue_id"],
        "RESOLVED",
    )

    assert updated_issue["status"] == "RESOLVED"


def test_invalid_issue_status(tmp_path, monkeypatch):
    issue_file = tmp_path / "dq_issues.json"

    monkeypatch.setattr(
        "src.quality.issue_registry.ISSUE_FILE",
        issue_file,
    )

    issue = create_issue(
        check_name="test_check",
        message="Test issue.",
    )

    save_issue(issue)

    try:
        update_issue_status(
            issue["issue_id"],
            "INVALID",
        )
        assert False
    except ValueError:
        assert True
