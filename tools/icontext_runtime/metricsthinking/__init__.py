"""
MetricsThinking™: Universal Project Evaluation Engine & Forensic Auditor.
"""

__version__ = "6.0.0"

from .collector import ProjectCollector, ProjectEvidence
from .engine import run_audit
from .evaluator import CriteriaEvaluator
from .models import (
    AuditCriterion,
    CanonicalModuleEvaluation,
    ContextPruningPlan,
    DomainArchetype,
    EvidencePrimitiveSummary,
    FPAISpectralVector,
    InspectionMode,
    MaturityBand,
    ModuleStatus,
    ProjectAuditReport,
    PruningActionItem,
    RemediationItem,
    SecurityVulnerabilityReport,
    SystemsResilienceReport,
)
from .renderer import ReportRenderer
from .scorer import AuditScorer

__all__ = [
    "ModuleStatus",
    "MaturityBand",
    "DomainArchetype",
    "InspectionMode",
    "EvidencePrimitiveSummary",
    "AuditCriterion",
    "CanonicalModuleEvaluation",
    "RemediationItem",
    "FPAISpectralVector",
    "SecurityVulnerabilityReport",
    "SystemsResilienceReport",
    "PruningActionItem",
    "ContextPruningPlan",
    "ProjectAuditReport",
    "ProjectCollector",
    "ProjectEvidence",
    "CriteriaEvaluator",
    "AuditScorer",
    "ReportRenderer",
    "run_audit",
]
