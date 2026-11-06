"""
Confidence Envelope and Statistical Calibration Module for MetricsThinking™ v4.0.

Provides rigorous CI95% bounds and error envelopes for continuous evaluation metrics.
"""

import math
from typing import Any


def calculate_confidence_envelope(
    sample_values: list[float],
    confidence_level: float = 0.95,
) -> dict[str, float | int]:
    """
    Computes statistical confidence envelope for continuous evaluation metrics.

    Returns:
        {
            "mean": float,
            "ci_lower": float,
            "ci_upper": float,
            "margin_of_error": float,
            "sample_size": int,
        }
    """
    n = len(sample_values)
    if n == 0:
        return {
            "mean": 0.0,
            "ci_lower": 0.0,
            "ci_upper": 0.0,
            "margin_of_error": 0.0,
            "sample_size": 0,
        }

    mean = sum(sample_values) / n

    if n == 1:
        return {
            "mean": round(mean, 4),
            "ci_lower": round(mean, 4),
            "ci_upper": round(mean, 4),
            "margin_of_error": 0.0,
            "sample_size": 1,
        }

    variance = sum((x - mean) ** 2 for x in sample_values) / (n - 1)
    std_dev = math.sqrt(variance)
    std_err = std_dev / math.sqrt(n)

    # Standard critical z-score mapping
    if confidence_level >= 0.99:
        z = 2.576
    elif confidence_level >= 0.95:
        z = 1.960
    elif confidence_level >= 0.90:
        z = 1.645
    else:
        z = 1.960

    margin = z * std_err
    ci_lower = max(0.0, mean - margin)
    ci_upper = min(1.0, mean + margin) if mean <= 1.0 else mean + margin

    return {
        "mean": round(mean, 4),
        "ci_lower": round(ci_lower, 4),
        "ci_upper": round(ci_upper, 4),
        "margin_of_error": round(margin, 4),
        "sample_size": n,
    }
