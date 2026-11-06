"""
Spectral Context Efficiency Engine for MetricsThinking™ v4.0.

Implements the multi-dimensional spectral and linear power models:
    S_spectral = sqrt(P^2 + Q_total^2 + D^2)
    S_linear = P + Q_total + D
    where Q_total = Q_dead + Q_dup
    PF_spectral = min(1.0, (P / S_spectral) * G)
    PF_linear = min(1.0, (P / S_linear) * G)
"""

import math
from metricsthinking.models import FPAISpectralVector


def compute_spectral_vector(
    p_active: float,
    q_dead: float,
    q_dup: float,
    d_structural: float,
    gain_coefficient: float = 1.0,
) -> FPAISpectralVector:
    """
    Computes bimodal S_spectral and S_linear, divergence ratio, and decoupled gain.

    Invariant: S_spectral = sqrt(P^2 + (Q_dead + Q_dup)^2 + D_structural^2)
    Invariant: S_linear = P + Q_dead + Q_dup + D_structural
    Invariant: PF_spectral = min(1.0, (P / S_spectral) * gain_coefficient) if S_spectral > 0 else 1.0
    """
    p = max(0.0, float(p_active))
    qd = max(0.0, float(q_dead))
    qr = max(0.0, float(q_dup))
    d = max(0.0, float(d_structural))
    g = max(0.0, float(gain_coefficient))

    q_total = qd + qr

    s_spectral = math.sqrt(p ** 2 + q_total ** 2 + d ** 2)
    s_linear = p + q_total + d

    if s_spectral > 0.0:
        pf_spectral = min(1.0, (p / s_spectral) * g)
    else:
        pf_spectral = 1.0

    if s_linear > 0.0:
        pf_linear = min(1.0, (p / s_linear) * g)
        div_ratio = abs(s_linear - s_spectral) / s_linear
        active_ratio = p / s_linear
        dead_ratio = qd / s_linear
        redundant_ratio = qr / s_linear
        distortion_ratio = d / s_linear
    else:
        pf_linear = 1.0
        div_ratio = 0.0
        active_ratio = 1.0
        dead_ratio = 0.0
        redundant_ratio = 0.0
        distortion_ratio = 0.0

    cal_state = "CALIBRATED" if abs(g - 1.0) > 1e-4 else "DETERMINISTIC"

    return FPAISpectralVector(
        p_active=round(p, 4),
        q_dead=round(qd, 4),
        q_dup=round(qr, 4),
        d_structural=round(d, 4),
        s_spectral=round(s_spectral, 4),
        s_linear=round(s_linear, 4),
        divergence_ratio=round(div_ratio, 4),
        power_factor_spectral=round(pf_spectral, 4),
        power_factor_linear=round(pf_linear, 4),
        active_ratio=round(active_ratio, 4),
        dead_ratio=round(dead_ratio, 4),
        redundant_ratio=round(redundant_ratio, 4),
        distortion_ratio=round(distortion_ratio, 4),
        calibration_state=cal_state,
        gain_coefficient=round(g, 4),
    )
