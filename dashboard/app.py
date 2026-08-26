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


HISTORY_FILE = PROJECT_ROOT / "data" / "quality_history.json"

st.set_page_config(
    page_title="Enterprise Data Quality Platform",
    page_icon="📊",
    layout="wide",
)


def load_history() -> list[dict]:
    if not HISTORY_FILE.exists():
        return []

    with HISTORY_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


st.title("Enterprise Data Quality Platform")
st.caption("Enterprise Data Quality Monitoring & Observability")


history = load_history()

if not history:
    st.warning("No quality history available.")
    st.stop()


latest = history[-1]

rules = load_quality_rules()

quality_score = float(latest.get("quality_score", 0.0))
status = latest.get("status", "UNKNOWN")
total_records = latest.get("total_records", 0)
failed_records = latest.get("failed_records", 0)
duplicate_records = latest.get("duplicate_records", 0)
null_violations = latest.get("null_violations", 0)
invalid_email_records = latest.get("invalid_email_records", 0)

threshold = rules["quality_score_threshold"]

alert = evaluate_quality_alert(
    quality_score,
    threshold=threshold,
)

trend = build_quality_trend(history)


# Executive summary
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


# Data quality metrics
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


# Alert section
st.subheader("Quality Alert")

if alert.status == "PASS":
    st.success(alert.message)
else:
    st.error(alert.message)


st.divider()


# Quality history
st.subheader("Quality History")

history_df = pd.DataFrame(history)

if "run_timestamp" in history_df.columns:
    history_df["run_timestamp"] = pd.to_datetime(
        history_df["run_timestamp"]
    )

if not history_df.empty:

    chart_data = history_df[
        ["run_timestamp", "quality_score"]
    ].set_index("run_timestamp")

    st.line_chart(chart_data)


st.divider()


# Historical run details
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


# Latest run details
with st.expander("Latest Run Details"):
    st.json(latest)