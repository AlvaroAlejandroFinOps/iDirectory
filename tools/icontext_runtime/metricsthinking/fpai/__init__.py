"""
FPIA Context Engine & MemoryOps Subpackage for MetricsThinking™ v4.0.
"""

from .spectral_engine import compute_spectral_vector
from .confidence import calculate_confidence_envelope
from .gatekeeper import (
    calculate_shannon_entropy,
    scan_file_security,
    scan_repository_security,
)
from .drift_auditor import audit_seed_to_code_drift
from .compensation import (
    generate_pruning_plan,
    apply_pruning_plan,
    PRUNE_START_MARKER,
    PRUNE_END_MARKER,
)
from .medallion import run_local_medallion_pipeline
from .ablation import run_ablation_sampling
from .attribution import resolve_context_attribution

__all__ = [
    "compute_spectral_vector",
    "calculate_confidence_envelope",
    "calculate_shannon_entropy",
    "scan_file_security",
    "scan_repository_security",
    "audit_seed_to_code_drift",
    "generate_pruning_plan",
    "apply_pruning_plan",
    "PRUNE_START_MARKER",
    "PRUNE_END_MARKER",
    "run_local_medallion_pipeline",
    "run_ablation_sampling",
    "resolve_context_attribution",
]
