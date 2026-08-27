import json
import uuid
from datetime import UTC, datetime
from pathlib import Path


ISSUE_FILE = Path("data/dq_issues.json")

VALID_STATUSES = {
    "OPEN",
    "ACKNOWLEDGED",
    "RESOLVED",
}


def create_issue(
    check_name: str,
    message: str,
    severity: str = "HIGH",
) -> dict:
    return {
        "issue_id": str(uuid.uuid4()),
        "created_at": datetime.now(UTC).isoformat(),
        "updated_at": datetime.now(UTC).isoformat(),
        "check_name": check_name,
        "severity": severity,
        "message": message,
        "status": "OPEN",
    }


def save_issue(issue: dict) -> None:
    ISSUE_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    issues = []

    if ISSUE_FILE.exists():
        with ISSUE_FILE.open(
            "r",
            encoding="utf-8-sig",
        ) as file:
            issues = json.load(file)

    issues.append(issue)

    with ISSUE_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            issues,
            file,
            indent=2,
        )


def load_issues() -> list[dict]:
    if not ISSUE_FILE.exists():
        return []

    with ISSUE_FILE.open(
        "r",
        encoding="utf-8-sig",
    ) as file:
        return json.load(file)


def update_issue_status(
    issue_id: str,
    status: str,
) -> dict:
    if status not in VALID_STATUSES:
        raise ValueError(
            f"Invalid issue status: {status}"
        )

    issues = load_issues()

    for issue in issues:
        if issue.get("issue_id") == issue_id:

            issue["status"] = status

            issue["updated_at"] = (
                datetime.now(UTC).isoformat()
            )

            with ISSUE_FILE.open(
                "w",
                encoding="utf-8",
            ) as file:
                json.dump(
                    issues,
                    file,
                    indent=2,
                )

            return issue

    raise ValueError(
        f"Issue not found: {issue_id}"
    )