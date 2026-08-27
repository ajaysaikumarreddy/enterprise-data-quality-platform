import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import json

import pandas as pd
import streamlit as st

from src.quality.alerts import evaluate_quality_alert
from src.quality.config_loader import load_quality_rules
from src.quality.trend import build_quality_trend
from src.quality.issue_registry import (
    load_issues,
    update_issue_status,
)

HISTORY_FILE = PROJECT_ROOT / "data" / "quality_history.json"
ISSUE_FILE = PROJECT_ROOT / "data" / "dq_issues.json"


st.set_page_config(
    page_title="Enterprise Data Quality Platform",
    page_icon="DQ",
    layout="wide",
)


# ---------------------------------------------------------
# Data Loading
# ---------------------------------------------------------

def load_history() -> list[dict]:
    if not HISTORY_FILE.exists():
        return []

    with HISTORY_FILE.open(
        "r",
        encoding="utf-8-sig",
    ) as file:
        return json.load(file)


def load_issues() -> list[dict]:
    if not ISSUE_FILE.exists():
        return []

    with ISSUE_FILE.open(
        "r",
        encoding="utf-8-sig",
    ) as file:
        return json.load(file)


# ---------------------------------------------------------
# Dashboard Header
# ---------------------------------------------------------

st.title("Enterprise Data Quality Platform")
st.caption("Enterprise Data Quality Monitoring & Observability")


history = load_history()

if not history:
    st.warning("No quality history available.")
    st.stop()


latest = history[-1]

rules = load_quality_rules()

quality_score = float(
    latest.get("quality_score", 0.0)
)

status = latest.get(
    "status",
    "UNKNOWN",
)

total_records = latest.get(
    "total_records",
    0,
)

failed_records = latest.get(
    "failed_records",
    0,
)

duplicate_records = latest.get(
    "duplicate_records",
    0,
)

null_violations = latest.get(
    "null_violations",
    0,
)

invalid_email_records = latest.get(
    "invalid_email_records",
    0,
)

threshold = rules[
    "quality_score_threshold"
]


# ---------------------------------------------------------
# Alert and Trend
# ---------------------------------------------------------

alert = evaluate_quality_alert(
    quality_score,
    threshold=threshold,
)

trend = build_quality_trend(history)


# ---------------------------------------------------------
# Executive Summary
# ---------------------------------------------------------

st.subheader("Quality Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Quality Score",
    f"{quality_score:.1f}%",
)

col2.metric(
    "Status",
    status,
)

col3.metric(
    "Trend",
    trend["trend"],
)

col4.metric(
    "Threshold",
    f"{threshold:.1f}%",
)


st.divider()


# ---------------------------------------------------------
# Data Quality Metrics
# ---------------------------------------------------------

st.subheader("Data Quality Metrics")

col5, col6, col7, col8 = st.columns(4)

col5.metric(
    "Total Records",
    total_records,
)

col6.metric(
    "Failed Records",
    failed_records,
)

col7.metric(
    "Duplicate Records",
    duplicate_records,
)

col8.metric(
    "Null Violations",
    null_violations,
)


col9, col10 = st.columns(2)

col9.metric(
    "Invalid Email Records",
    invalid_email_records,
)

col10.metric(
    "Historical Runs",
    trend["run_count"],
)


st.divider()


# ---------------------------------------------------------
# Quality Alert
# ---------------------------------------------------------

st.subheader("Quality Alert")

if alert.status == "PASS":
    st.success(alert.message)
else:
    st.error(alert.message)


st.divider()


# ---------------------------------------------------------
# DQ Issue Registry
# ---------------------------------------------------------

st.subheader("DQ Issue Registry")

issues = load_issues()

if not issues:

    st.success(
        "No data quality issues have been registered."
    )

else:

    # -----------------------------------------------------
    # Issue summary
    # -----------------------------------------------------

    open_issues = [
        issue
        for issue in issues
        if issue.get("status") == "OPEN"
    ]

    acknowledged_issues = [
        issue
        for issue in issues
        if issue.get("status") == "ACKNOWLEDGED"
    ]

    resolved_issues = [
        issue
        for issue in issues
        if issue.get("status") == "RESOLVED"
    ]

    high_issues = [
        issue
        for issue in issues
        if issue.get("severity") == "HIGH"
    ]

    medium_issues = [
        issue
        for issue in issues
        if issue.get("severity") == "MEDIUM"
    ]

    low_issues = [
        issue
        for issue in issues
        if issue.get("severity") == "LOW"
    ]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Open",
        len(open_issues),
    )

    col2.metric(
        "Acknowledged",
        len(acknowledged_issues),
    )

    col3.metric(
        "Resolved",
        len(resolved_issues),
    )

    col4.metric(
        "High Severity",
        len(high_issues),
    )

    st.divider()

    # -----------------------------------------------------
    # Filters
    # -----------------------------------------------------

    filter_col1, filter_col2 = st.columns(2)

    status_filter = filter_col1.selectbox(
        "Filter by Status",
        [
            "ALL",
            "OPEN",
            "ACKNOWLEDGED",
            "RESOLVED",
        ],
    )

    severity_filter = filter_col2.selectbox(
        "Filter by Severity",
        [
            "ALL",
            "HIGH",
            "MEDIUM",
            "LOW",
        ],
    )

    # -----------------------------------------------------
    # Apply filters
    # -----------------------------------------------------

    filtered_issues = issues

    if status_filter != "ALL":

        filtered_issues = [
            issue
            for issue in filtered_issues
            if issue.get("status") == status_filter
        ]

    if severity_filter != "ALL":

        filtered_issues = [
            issue
            for issue in filtered_issues
            if issue.get("severity") == severity_filter
        ]

    st.caption(
        f"Showing {len(filtered_issues)} of {len(issues)} issues"
    )

    st.divider()

    # -----------------------------------------------------
    # Display issues
    # -----------------------------------------------------

    if not filtered_issues:

        st.info(
            "No issues match the selected filters."
        )

    else:

        for issue in filtered_issues:

            issue_id = issue.get(
                "issue_id",
                "",
            )

            status = issue.get(
                "status",
                "OPEN",
            )

            severity = issue.get(
                "severity",
                "HIGH",
            )

            check_name = issue.get(
                "check_name",
                "",
            )

            message = issue.get(
                "message",
                "",
            )

            created_at = issue.get(
                "created_at",
                "",
            )

            updated_at = issue.get(
                "updated_at",
                "",
            )

            # -------------------------------------------------
            # Issue card
            # -------------------------------------------------

            with st.container(border=True):

                header_col1, header_col2 = st.columns(
                    [3, 1]
                )

                header_col1.markdown(
                    f"### {check_name}"
                )

                header_col2.markdown(
                    f"**{severity}**"
                )

                st.write(message)

                st.caption(
                    f"Issue ID: {issue_id}"
                )

                st.caption(
                    f"Created: {created_at}"
                )

                if updated_at:

                    st.caption(
                        f"Updated: {updated_at}"
                    )

                status_col, action_col1, action_col2 = st.columns(
                    [2, 1, 1]
                )

                status_col.markdown(
                    f"**Status:** `{status}`"
                )

                # ---------------------------------------------
                # Acknowledge
                # ---------------------------------------------

                if status == "OPEN":

                    if action_col1.button(
                        "Acknowledge",
                        key=f"ack_{issue_id}",
                        use_container_width=True,
                    ):

                        update_issue_status(
                            issue_id,
                            "ACKNOWLEDGED",
                        )

                        st.rerun()

                # ---------------------------------------------
                # Resolve
                # ---------------------------------------------

                if status == "ACKNOWLEDGED":

                    if action_col2.button(
                        "Resolve",
                        key=f"resolve_{issue_id}",
                        use_container_width=True,
                    ):

                        update_issue_status(
                            issue_id,
                            "RESOLVED",
                        )

                        st.rerun()
# ---------------------------------------------------------
# Quality History
# ---------------------------------------------------------

st.subheader("Quality History")

history_df = pd.DataFrame(history)

if "run_timestamp" in history_df.columns:

    history_df["run_timestamp"] = pd.to_datetime(
        history_df["run_timestamp"]
    )


if not history_df.empty:

    chart_data = history_df[
        [
            "run_timestamp",
            "quality_score",
        ]
    ].set_index(
        "run_timestamp"
    )

    st.line_chart(chart_data)


st.divider()


# ---------------------------------------------------------
# Historical Run Details
# ---------------------------------------------------------

st.subheader("Historical Runs")

display_columns = [
    column
    for column in [
        "run_timestamp",
        "status",
        "quality_score",
        "total_records",
        "failed_records",
        "duplicate_records",
        "null_violations",
        "invalid_email_records",
    ]
    if column in history_df.columns
]

st.dataframe(
    history_df[display_columns],
    use_container_width=True,
    hide_index=True,
)


st.divider()


# ---------------------------------------------------------
# Latest Run Details
# ---------------------------------------------------------

with st.expander(
    "Latest Run Details"
):
    st.json(latest)