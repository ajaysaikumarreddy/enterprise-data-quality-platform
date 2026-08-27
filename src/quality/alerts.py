from dataclasses import dataclass


@dataclass
class QualityAlert:
    status: str
    severity: str
    message: str
    quality_score: float


def evaluate_quality_alert(
    quality_score: float,
    threshold: float = 95.0,
) -> QualityAlert:
    if quality_score < threshold:
        return QualityAlert(
            status="ALERT",
            severity="HIGH",
            message=(
                f"Data quality score {quality_score:.1f}% "
                f"is below the threshold of {threshold:.1f}%."
            ),
            quality_score=quality_score,
        )

    return QualityAlert(
        status="PASS",
        severity="NONE",
        message=(
            f"Data quality score {quality_score:.1f}% "
            f"meets the threshold of {threshold:.1f}%."
        ),
        quality_score=quality_score,
    )