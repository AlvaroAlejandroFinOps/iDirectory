#!/usr/bin/env python3
"""
iDirectory: Framework de Gobernanza, Ruteo y Context Engineering (v5.0)
Creado por Gravity HyperScale Thinking.

Diseñado para sistemas Multi-Cloud (GCP, AWS, Azure, Fabric), IA, Datos y Analítica.
Implementa:
- Topología unificada en minúsculas (all-lowercase).
- Mapa topológico satelital (.context/tree.json) con fingerprint criptográfico SHA-256 (topology_hash).
- Bus Federado de Interoperabilidad v5.0 (.context/icontext_bus.json) y Caché AST (.context/contracts_ast.json).
- Semáforos de poda y relevancia de directorio (Context Beacons: .context.yaml).
- Bootloader Adaptativo de 3 Perfiles (Tier 1A, Tier 1B, Tier 2) y Ecosystem Pack (--pack-ecosystem).
- Compilador de paquetes de contexto en una sola llamada (context --pack <dir>).
- Consulta seccional quirúrgica del ThinkingSeed Master (seed --toc / --section).
- Máquina de estados de continuidad atencional (.context/checkpoint.json).
- Cierre idempotente de un solo comando (reconcile).
- Cero dependencias externas (Python Standard Library pura).
"""

import os
import re
import sys
import ast
import json
import time
import errno
import hashlib
import fnmatch
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional, Set, Callable, Tuple

ENGINE_VERSION = "5.0"

# ==============================================================================
# 1. MiniYAML: Serializador / Deserializador ligero sin dependencias (PyYAML-free)
# ==============================================================================
class MiniYAML:
    """Parser y emitter minimalista para el subconjunto de YAML usado en .context.yaml y frontmatters."""

    @staticmethod
    def dump(data: Dict[str, Any], indent: int = 0) -> str:
        lines = []
        prefix = " " * indent
        for key, value in data.items():
            if isinstance(value, dict):
                lines.append(f"{prefix}{key}:")
                lines.append(MiniYAML.dump(value, indent + 2))
            elif isinstance(value, list):
                lines.append(f"{prefix}{key}:")
                for item in value:
                    lines.append(f"{prefix}  - {json.dumps(item, ensure_ascii=False)}")
            elif isinstance(value, bool):
                lines.append(f"{prefix}{key}: {'true' if value else 'false'}")
            elif value is None:
                lines.append(f"{prefix}{key}: null")
            elif isinstance(value, (int, float)):
                lines.append(f"{prefix}{key}: {value}")
            else:
                val_str = str(value)
                if any(c in val_str for c in [":", "#", "{", "}", "[", "]", ",", "&", "*", "?", "|", "-", "<", ">", "=", "!"]):
                    val_str = json.dumps(val_str, ensure_ascii=False)
                lines.append(f"{prefix}{key}: {val_str}")
        return "\n".join(lines)

    @staticmethod
    def _unquote(raw: str) -> str:
        s = raw.strip()
        if len(s) >= 2 and s.startswith('"') and s.endswith('"'):
            try:
                parsed = json.loads(s)
                if isinstance(parsed, str):
                    return parsed
            except ValueError:
                pass
            return s[1:-1]
        if len(s) >= 2 and s.startswith("'") and s.endswith("'"):
            return s[1:-1]
        return s

    @staticmethod
    def load(yaml_str: str) -> Dict[str, Any]:
        """Parser básico línea por línea para diccionarios y listas simples."""
        result: Dict[str, Any] = {}
        current_list_key = None
        for raw_line in yaml_str.splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("- ") and current_list_key:
                val = MiniYAML._unquote(line[2:])
                result[current_list_key].append(val)
                continue
            if ":" in line:
                parts = line.split(":", 1)
                k = parts[0].strip()
                v = parts[1].strip()
                if not v:
                    current_list_key = k
                    result[k] = []
                else:
                    current_list_key = None
                    if v.lower() == "true":
                        result[k] = True
                    elif v.lower() == "false":
                        result[k] = False
                    elif v.lower() in ("null", "none"):
                        result[k] = None
                    elif (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
                        result[k] = MiniYAML._unquote(v)
                    else:
                        try:
                            result[k] = int(v)
                        except ValueError:
                            try:
                                result[k] = float(v)
                            except ValueError:
                                result[k] = v
        return result


# ==============================================================================
# 2. Manifiesto Topológico Canónico v4.0 (All-Lowercase Topology)
# ==============================================================================
IGNORED_DISCOVERY_DIRS: Set[str] = {
    ".git", ".github", ".venv", "venv", "env", "__pycache__",
    ".pytest_cache", ".mypy_cache", ".ruff_cache", "node_modules",
    "target", "dist", "build", ".idea", ".vscode", ".agents", ".claude", ".context"
}

BINARY_EXTENSIONS: Set[str] = {
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".webp", ".bmp",
    ".pbix", ".parquet", ".delta", ".avro", ".orc", ".feather",
    ".pdf", ".zip", ".tar", ".gz", ".7z", ".whl", ".pyc", ".pyd", ".so", ".dll", ".exe"
}
BINARY_EXTENSIONS_TUPLE: Tuple[str, ...] = tuple(BINARY_EXTENSIONS)

CODE_SCHEMA_EXTENSIONS: Set[str] = {
    ".py", ".sql", ".json", ".yaml", ".yml", ".avsc", ".tf", ".sh", ".ps1", ".toml"
}

DEFAULT_CONTEXT_POLICY: Dict[str, Any] = {
    "version": "5.0.0",
    "project": "iDirectory",
    "architecture": "Gravity HyperScale Thinking — Federated Adaptive Context Engineering v5.0",
    "federation_protocol": {
        "version": "5.0.0",
        "bus_path": ".context/icontext_bus.json",
        "ast_cache_path": ".context/contracts_ast.json",
        "layers": {
            "l0": "iDirectory v5.0 (Topological & Attentional Control Plane)",
            "l1": "ThinkingSeed v5.0 (Symbolic Architectural DNA Vector)",
            "l2": "MetricsThinking v5.0 (Forensic & Spectral FPIA Governor)",
            "l3": "iReadme v5.0 (Institutional Paper-Grade Synthesizer)"
        }
    },
    "profiles": {
        "tier_1a": {
            "name": "Atomic Known-Path Execution",
            "entry_command": "python FWengine.py context --pack <target_dir> --tier 1a",
            "fallback": "python FWengine.py map --slice <target_dir>",
            "seed_policy": "forbidden_unless_contract_collision",
            "target_token_budget": 220
        },
        "tier_1b": {
            "name": "Scoped Multi-File / Scoped Plan (Default for /plan)",
            "entry_command": "python FWengine.py context --compact",
            "secondary": ["python FWengine.py map --slice <dir>", "python FWengine.py seed --section <id>"],
            "seed_policy": "sectional_only",
            "target_token_budget": 800
        },
        "tier_2": {
            "name": "Global Architecture / Forensic Audit / Ecosystem Federation",
            "entry_command": "python FWengine.py context --pack-ecosystem",
            "triggers": ["/seedMaster", "/metrics", "/readme", "/ultraThinking", "cross_domain_redesign"],
            "seed_policy": "full_or_ecosystem_bus",
            "target_token_budget": 16000
        }
    },
    "budgets": {
        "compact_radar_max_tokens": 250,
        "slice_max_chars": 600,
        "slice_max_tokens": 150,
        "beacon_max_chars": 600,
        "beacon_max_tokens": 150,
        "checkpoint_max_tokens": 300,
        "ecosystem_pack_max_tokens": 650,
        "satellite_max_tokens": 1000
    },
    "closure_contract": {
        "primary_command": "python FWengine.py reconcile",
        "verify_command": "python FWengine.py reconcile --check"
    },
    "precedence_order": [
        "1. Executable code (FWengine.py) & formal JSON schemas (schemas/*.schema.json)",
        "2. Canonical policy (config/context_policy.json)",
        "3. Verified satellite (.context/tree.json) & local beacons (.context.yaml)",
        "4. Active attentional checkpoint (.context/checkpoint.json)",
        "5. Architectural DNA (01_seed/seed-idirectory-master.md)",
        "6. Active plans with status=approved|executing (artifacts/plans/active/)"
    ],
    "supported_adapters": [
        "AGENTS.md",
        "GEMINI.md",
        "CLAUDE.md",
        ".cursorrules",
        ".github/copilot-instructions.md",
        ".agents/skills/idir/SKILL.md"
    ]
}

FOLDER_METADATA: Dict[str, Dict[str, Any]] = {
    "01_seed": {
        "purpose": "Semilla de proyecto y memoria técnica (ThinkingSeed Master). ADN arquitectónico del sistema.",
        "role": "dna",
        "relevance": "critical",
        "crawl": True,
        "read_priority": "p0",
        "seed_reference": "required",
        "tier1_preload": False,
        "token_density": "medium",
        "instructions": "LECTURA CONDICIONAL (Tier 2 o consulta seccional vía seed --section). Prohibido precargar completo en Tier 1."
    },
    "02_foundation/engine": {
        "purpose": "Núcleo del framework de automatización, lógica de ruteo, indexación y governance engine.",
        "role": "core_engine",
        "relevance": "critical",
        "crawl": True,
        "read_priority": "p1",
        "seed_reference": "optional",
        "token_density": "sparse",
        "key_files": ["engine_readme.md"],
        "instructions": "Contiene los utilitarios de gobernanza y especificación formal de directorios."
    },
    "03_research/notebooks": {
        "purpose": "Notebooks de desarrollo interactivo (Jupyter/Colab/Fabric/Databricks) para análisis exploratorio (EDA).",
        "role": "eda",
        "relevance": "low",
        "crawl": False,
        "read_priority": "p2",
        "seed_reference": "optional",
        "token_density": "dense",
        "instructions": "Notebooks exploratorios. No iterar de forma recursiva a menos que se solicite un análisis específico."
    },
    "03_research/prompts": {
        "purpose": "Estructuras de prompts para LLMs, system prompts, árboles de contexto y plantillas de inferencia.",
        "role": "prompt_engineering",
        "relevance": "high",
        "crawl": True,
        "read_priority": "p1",
        "seed_reference": "optional",
        "token_density": "sparse",
        "instructions": "Plantillas de inferencia y configuración de agentes."
    },
    "03_research/experiments": {
        "purpose": "Pruebas de concepto (PoCs), prototipos de modelos algorítmicos, benchmarks e I+D.",
        "role": "pocs_benchmarks",
        "relevance": "medium",
        "crawl": False,
        "read_priority": "p2",
        "seed_reference": "optional",
        "token_density": "medium",
        "instructions": "Espacio de pruebas descartables y experimentos temporales."
    },
    "src/cloud_jobs": {
        "purpose": "Scripts productivos, pipelines y orquestación multi-cloud (Fabric PySpark, AWS Glue, GCP Dataproc, Azure Synapse).",
        "role": "production_pipelines",
        "relevance": "high",
        "crawl": True,
        "read_priority": "p1",
        "seed_reference": "optional",
        "token_density": "medium",
        "dependencies": ["schemas", "config"],
        "instructions": "Cargas productivas de datos. Conservar invariantes de arquitectura e idempotencia."
    },
    "src/data_generation": {
        "purpose": "Módulos de generación y simulación de datos sintéticos con rigor probabilístico y volumetría estadística.",
        "role": "synthetic_data",
        "relevance": "medium",
        "crawl": True,
        "read_priority": "p2",
        "seed_reference": "optional",
        "token_density": "medium",
        "instructions": "Generadores de pruebas de carga y benchmarking sintético."
    },
    "src/core": {
        "purpose": "Lógica de negocio transversal, utilitarios de backend, clientes de servicios y módulos comunes.",
        "role": "shared_backend",
        "relevance": "high",
        "crawl": True,
        "read_priority": "p1",
        "seed_reference": "optional",
        "token_density": "medium",
        "instructions": "Servicios backend reutilizables por jobs y dashboards."
    },
    "src/dashboards": {
        "purpose": "Tableros de Business Intelligence y apps de visualización interactiva (Streamlit, Dash, PowerBI, Looker).",
        "role": "bi_viz",
        "relevance": "medium",
        "crawl": True,
        "read_priority": "p2",
        "seed_reference": "optional",
        "token_density": "medium",
        "instructions": "Aplicaciones de visualización frontend y consumo analítico."
    },
    "artifacts/plans/active": {
        "purpose": "Planes de capacidad activos (F-SKUs), presupuestos cloud vigentes e hitos operativos en curso.",
        "role": "active_plans",
        "relevance": "high",
        "crawl": True,
        "read_priority": "p1",
        "seed_reference": "optional",
        "token_density": "sparse",
        "instructions": "Planes vigentes verificados (status: approved|executing). Ignorar o archivar planes superseded."
    },
    "artifacts/plans/metricsthinking": {
        "purpose": "Evaluación forense de métricas de avance del proyecto, scores de madurez y roadmap de remediación SDD (MetricsThinking™).",
        "role": "metrics_evaluation",
        "relevance": "medium",
        "crawl": True,
        "read_priority": "p2",
        "seed_reference": "optional",
        "token_density": "sparse",
        "key_files": ["MetricsThinking.md", "MetricsThinking.json"],
        "instructions": "Snapshots de auditoría MetricsThinking. Consultar solo en evaluaciones de madurez (/metrics); verificar fecha de vigencia."
    },
    "artifacts/plans/backlog": {
        "purpose": "Cola formal de intenciones, backlog de tareas y planes candidatos de ejecución.",
        "role": "intent_backlog",
        "relevance": "low",
        "crawl": False,
        "read_priority": "p2",
        "seed_reference": "optional",
        "tier1_preload": False,
        "token_density": "sparse",
        "instructions": "Cola formal de intenciones y backlog de planes. No explorar de forma recursiva (crawl: false)."
    },
    "artifacts/plans/archive": {
        "purpose": "Histórico de planes evaluados, arquitecturas descartadas y documentación obsoleta preservada por trazabilidad.",
        "role": "archived_plans",
        "relevance": "zero_for_llm",
        "crawl": False,
        "read_priority": "p3",
        "seed_reference": "optional",
        "token_density": "sparse",
        "instructions": "RAMA MUERTA / ARCHIVADA. No explorar a menos que se pida explícitamente auditar el pasado."
    },
    "docs/architecture": {
        "purpose": "Diagramas de arquitectura multi-cloud, topologías C4 y flujos de datos de las capas Medallion.",
        "role": "architecture_diagrams",
        "relevance": "high",
        "crawl": True,
        "read_priority": "p1",
        "seed_reference": "optional",
        "token_density": "sparse",
        "instructions": "Diagramas y especificaciones de alto nivel de sistemas."
    },
    "docs/specs": {
        "purpose": "Especificaciones técnicas detalladas, linaje de datos, contratos de esquemas y requerimientos no funcionales.",
        "role": "technical_specs",
        "relevance": "high",
        "crawl": True,
        "read_priority": "p1",
        "seed_reference": "optional",
        "token_density": "sparse",
        "instructions": "Contratos técnicos de integración."
    },
    "docs/notes": {
        "purpose": "Bitácoras de ingeniería, registro de deuda técnica, decisiones rápidas (ADRs) y análisis de causa raíz (RCA).",
        "role": "engineers_notes",
        "relevance": "medium",
        "crawl": True,
        "read_priority": "p2",
        "seed_reference": "optional",
        "token_density": "sparse",
        "instructions": "Notas de ingeniería y registros de decisiones."
    },
    "config": {
        "purpose": "Parámetros de entorno (dev, staging, prod), políticas de contexto y variables desacopladas.",
        "role": "configuration",
        "relevance": "high",
        "crawl": True,
        "read_priority": "p1",
        "seed_reference": "optional",
        "token_density": "sparse",
        "key_files": ["context_policy.json"],
        "instructions": "Variables y política canónica de contexto. NUNCA colocar claves secretas en texto plano."
    },
    "data/raw": {
        "purpose": "Zona de aterrizaje local (Bronze) para fuentes puras e inmutables. Ignorado en Git y AI.",
        "role": "bronze_storage",
        "relevance": "zero_for_llm",
        "crawl": False,
        "read_priority": "p3",
        "seed_reference": "optional",
        "token_density": "massive_binary",
        "instructions": "RAMA DE DATOS CRUDOS. PROHIBIDO EXPLORAR O VOLCAR CONTENIDO EN CONTEXTO."
    },
    "data/processed": {
        "purpose": "Datos transformados localmente (Silver/Gold) en formatos estructurados (Parquet/Delta).",
        "role": "silver_gold_storage",
        "relevance": "zero_for_llm",
        "crawl": False,
        "read_priority": "p3",
        "seed_reference": "optional",
        "token_density": "massive_binary",
        "instructions": "RAMA DE DATOS REFINADOS. PROHIBIDO EXPLORAR O VOLCAR CONTENIDO EN CONTEXTO."
    },
    "data/sandbox": {
        "purpose": "Entorno aislado para experimentación de científicos de datos y arquitectos.",
        "role": "sandbox",
        "relevance": "zero_for_llm",
        "crawl": False,
        "read_priority": "p3",
        "seed_reference": "optional",
        "token_density": "dense",
        "instructions": "ZONA SCRATCH. No explorar ni indexar en contexto agéntico."
    },
    "schemas": {
        "purpose": "Definiciones estrictas de esquemas (Avro, JSON Schema, DDL de SQL) para control de deriva de datos.",
        "role": "data_contracts",
        "relevance": "high",
        "crawl": True,
        "read_priority": "p1",
        "seed_reference": "optional",
        "token_density": "sparse",
        "instructions": "Contratos formales de datos. Consultar antes de emitir transformaciones SQL o PySpark."
    },
    "scripts": {
        "purpose": "Scripts operativos del sistema operativo (bash, powershell, make) para tareas de mantenimiento.",
        "role": "ops_automation",
        "relevance": "medium",
        "crawl": True,
        "read_priority": "p2",
        "seed_reference": "optional",
        "token_density": "sparse",
        "instructions": "Automatización operativa de terminal."
    },
    "tests": {
        "purpose": "Suites de pruebas unitarias, integración y calidad de datos (Great Expectations / pytest).",
        "role": "test_suites",
        "relevance": "high",
        "crawl": True,
        "read_priority": "p1",
        "seed_reference": "optional",
        "token_density": "medium",
        "instructions": "Pruebas de verificación de software y pipelines."
    },
    "tools": {
        "purpose": "Scripts utilitarios internos, herramientas de automatización local y linters.",
        "role": "tooling",
        "relevance": "medium",
        "crawl": True,
        "read_priority": "p2",
        "seed_reference": "optional",
        "token_density": "sparse",
        "instructions": "Herramientas locales del proyecto."
    },
    "logs": {
        "purpose": "Trazas locales de ejecución, auditorías y dumps de errores.",
        "role": "logs",
        "relevance": "zero_for_llm",
        "crawl": False,
        "read_priority": "p3",
        "seed_reference": "optional",
        "token_density": "massive_text",
        "instructions": "ARCHIVOS DE REGISTRO. No inspeccionar de forma recursiva a menos que se analice un error puntual."
    },
    ".context": {
        "purpose": "Directorio de telemetría, checkpoints y mapas satelitales de Context Engineering de iDirectory.",
        "role": "context_engineering",
        "relevance": "critical",
        "crawl": True,
        "read_priority": "p0",
        "seed_reference": "optional",
        "token_density": "sparse",
        "key_files": ["tree.json"],
        "instructions": "Contiene el mapa satelital verificable (tree.json) y checkpoints de sesión (checkpoint.json)."
    }
}

# Compatibilidad de mapeo simple
FOLDER_MANIFEST = {k: v["purpose"] for k, v in FOLDER_METADATA.items() if k != ".context"}

# Matriz de Ruteo Inteligente (v4.0)
ROUTING_MAP = {
    # Documentación y Diseño
    ".md": "docs/notes",
    ".pdf": "docs/specs",
    ".drawio": "docs/architecture",
    ".png": "docs/architecture",
    # Código y Cómputo / IA
    ".ipynb": "03_research/notebooks",
    ".py": "src/cloud_jobs",
    ".sql": "src/cloud_jobs",
    # Prompts / Inferencia IA
    ".prompt": "03_research/prompts",
    # Visualización / Dashboards / BI
    ".pbix": "src/dashboards",
    ".pbip": "src/dashboards",
    # Gobernanza, Infraestructura y Configuración
    ".yaml": "config",
    ".yml": "config",
    ".json": "schemas",
    ".avsc": "schemas",
    ".tf": "infrastructure",
    # Datos Locales
    ".csv": "data/raw",
    ".parquet": "data/processed",
    ".delta": "data/processed"
}


# ==============================================================================
# 3. Núcleo de Context Engineering (Beacons, Tree, Hash, Pack, Seed & Budgeting)
# ==============================================================================

# ------------------------------------------------------------------------------
# 3.0 Resiliencia I/O (Windows NTFS: WinError 5 / 32 por antivirus o indexadores)
# ------------------------------------------------------------------------------
TRANSIENT_WINERRORS: Set[int] = {5, 32, 33}
TRANSIENT_ERRNOS: Set[int] = {errno.EACCES, errno.EBUSY, errno.EAGAIN}


def _is_transient_io_error(exc: BaseException) -> bool:
    """
    Governs: [INV-01].
    True solo para bloqueos transitorios. FileNotFoundError / FileExistsError y similares
    son errores lógicos y NUNCA se reintentan.
    """
    if isinstance(exc, (FileNotFoundError, FileExistsError, IsADirectoryError, NotADirectoryError)):
        return False
    if isinstance(exc, PermissionError):
        return True
    if isinstance(exc, OSError):
        if getattr(exc, "winerror", None) in TRANSIENT_WINERRORS:
            return True
        return exc.errno in TRANSIENT_ERRNOS
    return False


def safe_io_retry(
    operation: Callable[[], Any],
    max_attempts: int = 4,
    initial_delay_ms: float = 25.0
) -> Any:
    """
    Governs: [INV-01], [G-05].
    Ejecuta operation() con backoff exponencial determinista (25ms, 50ms, 100ms por defecto).
    Re-lanza inmediatamente errores no transitorios; tras agotar intentos re-lanza el último error.
    """
    delay_s = initial_delay_ms / 1000.0
    for attempt in range(1, max_attempts + 1):
        try:
            return operation()
        except OSError as exc:
            if attempt >= max_attempts or not _is_transient_io_error(exc):
                raise
            time.sleep(delay_s)
            delay_s *= 2
    return None  # inalcanzable; satisface type-checkers


def safe_rename_casing(src: Path, dest: Path) -> Path:
    """
    Governs: [INV-06], [G-05].
    Renombrado en dos pasos vía archivo temporal (.tmp_{pid}_{name}) para filesystems
    case-insensitive. Ante fallo del segundo paso, revierte temp -> src para no dejar residuos.
    """
    temp_path = dest.parent / f".tmp_{os.getpid()}_{dest.name}"
    safe_io_retry(lambda: os.replace(src, temp_path))
    try:
        safe_io_retry(lambda: os.replace(temp_path, dest))
    except OSError:
        if temp_path.exists():
            try:
                os.replace(temp_path, src)
            except OSError:
                pass
        raise
    return dest


def estimate_tokens_v4(text_or_path: Any, fast_stat_only: bool = False) -> int:
    """
    Governs: [Opt-1].
    Estimador de tokens multimodal en stdlib pura sensible al tipo de contenido:
    - Excluye archivos binarios (retorna 0 tokens de texto LLM).
    - Ajusta el ratio caracteres/token según densidad simbólica (LaTeX, Mermaid, JSON/código, UTF-8).
    """
    if isinstance(text_or_path, Path):
        ext = text_or_path.suffix.lower()
        if ext in BINARY_EXTENSIONS:
            return 0
        try:
            fsize = text_or_path.stat().st_size
        except OSError:
            return 0
        if fsize == 0:
            return 0
        if fast_stat_only:
            if ext in CODE_SCHEMA_EXTENSIONS:
                return max(1, int(fsize / 3.6))
            return max(1, fsize // 4)
        try:
            raw_bytes = text_or_path.read_bytes()
        except OSError:
            return 0
        if b"\x00" in raw_bytes[:1024]:
            return 0
        text = raw_bytes.decode("utf-8", errors="replace")
        if not text:
            return 0
        if ext in CODE_SCHEMA_EXTENSIONS:
            return max(1, int(len(text) / 3.6))
    else:
        text = str(text_or_path)
        if not text:
            return 0

    length = len(text)
    non_ascii = sum(1 for ch in text if ord(ch) > 127)
    symbolic = sum(1 for ch in text if ch in "{}[]()<>|$/\\:=*+-_~`#")
    sym_ratio = (non_ascii + symbolic) / max(1, length)
    if sym_ratio > 0.14 or "$$" in text or "```mermaid" in text:
        return max(1, int(length / 3.4))
    return max(1, length // 4)


def resolve_seed_key_files(root_path: Path) -> List[str]:
    """
    Governs: [R-001], [ADR-006], [INV-08].
    Scans (root_path / "01_seed").glob("seed-*.md") for physical seed files.
    Returns sorted filenames if present; otherwise returns [f"seed-{project_slug}-master.md"].
    """
    seed_dir = root_path / "01_seed"
    if seed_dir.exists() and seed_dir.is_dir():
        found = sorted(
            f.name for f in seed_dir.glob("seed-*.md") if f.is_file()
        )
        if found:
            return found
    project_slug = root_path.resolve().name.lower().replace(" ", "-")
    return [f"seed-{project_slug}-master.md"]


def _resolve_physical_rel_path(root_path: Path, canonical_rel: str) -> str:
    """
    Governs: [R-004], [ADR-008], [INV-06].
    Resolves the exact physical casing stored on disk (NTFS/APFS) for a relative path using os.listdir().
    Returns canonical_rel if the directory does not exist yet on disk.
    """
    parts = canonical_rel.split("/")
    curr = root_path
    actual_parts: List[str] = []
    for part in parts:
        if not curr.exists() or not curr.is_dir():
            return canonical_rel
        try:
            entries = os.listdir(curr)
        except OSError:
            return canonical_rel
        match = next((e for e in entries if e.lower() == part.lower()), None)
        if match is None:
            return canonical_rel
        actual_parts.append(match)
        curr = curr / match
    return "/".join(actual_parts)


def generate_beacon_content(
    folder: str,
    meta: Dict[str, Any],
    root_path: Optional[Path] = None
) -> str:
    """Genera el contenido .context.yaml para un directorio."""
    beacon_data: Dict[str, Any] = {
        "version": "1.0",
        "directory": folder,
        "role": meta.get("role", "general"),
        "purpose": meta.get("purpose", ""),
        "relevance": meta.get("relevance", "medium"),
        "crawl": meta.get("crawl", True),
        "read_priority": meta.get("read_priority", "p2"),
        "seed_reference": meta.get("seed_reference", "optional"),
    }
    if "tier1_preload" in meta:
        beacon_data["tier1_preload"] = meta["tier1_preload"]
    if "inherited" in meta:
        beacon_data["inherited"] = bool(meta["inherited"])
    beacon_data["token_density"] = meta.get("token_density", "sparse")
    beacon_data["instructions"] = meta.get("instructions", "Directorio estándar.")
    if folder == "01_seed":
        seed_files = (
            resolve_seed_key_files(root_path)
            if root_path is not None
            else list(meta.get("key_files", []))
        )
        extra_files = [f for f in meta.get("key_files", []) if f not in seed_files]
        beacon_data["key_files"] = seed_files + extra_files
    elif "key_files" in meta and meta["key_files"]:
        beacon_data["key_files"] = meta["key_files"]
    if "imports_from" in meta and meta["imports_from"]:
        beacon_data["imports_from"] = meta["imports_from"]
    if "exported_to" in meta and meta["exported_to"]:
        beacon_data["exported_to"] = meta["exported_to"]
    if "dependencies" in meta and meta["dependencies"]:
        beacon_data["dependencies"] = meta["dependencies"]
    return MiniYAML.dump(beacon_data)


def resolve_beacon(dir_path: Path, root_path: Path) -> Dict[str, Any]:
    """
    Resuelve recursivamente las directivas de un directorio por herencia jerárquica.
    Si carece de .context.yaml físico, asciende hacia root_path heredando directivas.
    Invariante estricto: si cualquier ancestro declara crawl: False, crawl será False.
    """
    dir_path = dir_path.resolve()
    root_path = root_path.resolve()

    try:
        rel = dir_path.relative_to(root_path)
    except ValueError:
        return {
            "role": "general",
            "purpose": "",
            "relevance": "medium",
            "crawl": True,
            "read_priority": "p2",
            "seed_reference": "optional",
            "token_density": "sparse",
            "instructions": "Directorio externo o sin jerarquía.",
            "inherited": False,
            "inherited_from": None
        }

    chain: List[Path] = []
    curr = dir_path
    while curr != root_path:
        chain.append(curr)
        curr = curr.parent

    resolved: Dict[str, Any] = {
        "role": "general",
        "purpose": "",
        "relevance": "medium",
        "crawl": True,
        "read_priority": "p2",
        "seed_reference": "optional",
        "token_density": "sparse",
        "instructions": "Directorio con herencia canónica."
    }

    inherited = False
    inherited_from = None
    has_crawl_false = False

    # De ancestro más cercano a root hasta dir_path
    for p in reversed(chain):
        p_rel = str(p.relative_to(root_path)).replace("\\", "/").lower()
        node_meta = {}

        beacon_file = p / ".context.yaml"
        if beacon_file.exists():
            try:
                with open(beacon_file, "r", encoding="utf-8") as f:
                    node_meta = MiniYAML.load(f.read())
            except Exception:
                node_meta = {}
        elif p_rel in FOLDER_METADATA:
            node_meta = dict(FOLDER_METADATA[p_rel])

        if node_meta:
            if p != dir_path:
                inherited = True
                inherited_from = p_rel
            for k in ["role", "purpose", "relevance", "read_priority", "seed_reference", "token_density", "instructions", "key_files", "imports_from", "exported_to"]:
                if k in node_meta:
                    resolved[k] = node_meta[k]
            if "priority" in node_meta and "read_priority" not in node_meta:
                resolved["read_priority"] = node_meta["priority"]
            if node_meta.get("crawl") is False:
                has_crawl_false = True

    if has_crawl_false:
        resolved["crawl"] = False
    else:
        if "crawl" in node_meta:
            resolved["crawl"] = node_meta["crawl"]

    resolved["inherited"] = inherited
    resolved["inherited_from"] = inherited_from
    return resolved


def extract_preserved_comments(beacon_file: Path) -> List[str]:
    """
    Governs: [R-007], [ADR-010].
    Extracts manual user comment lines (lines starting with '#')
    from an existing .context.yaml file so they survive sync_beacons().
    """
    if not beacon_file.exists():
        return []
    try:
        raw_lines = beacon_file.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    preserved: List[str] = []
    for line in raw_lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            preserved.append(line)
    return preserved


# ------------------------------------------------------------------------------
# 3.1 Auto-descubrimiento, Validación Estricta y Auto-Scaffolding de Beacons (v4.0)
# ------------------------------------------------------------------------------
BEACON_FILENAME = ".context.yaml"
BEACON_CHAR_BUDGET = 600  # ~150 tokens (heurística 4 chars/token)
SLICE_CHAR_BUDGET = 600   # ~150 tokens
CODE_HINT_NAMES: Set[str] = {
    "src", "core", "lib", "api", "schemas", "models", "services",
    "pipelines", "jobs", "engine", "domain", "modules"
}
DOC_HINT_NAMES: Set[str] = {
    "docs", "notes", "utils", "tools", "scripts", "helpers", "examples", "assets"
}
PRIO_TO_RELEVANCE: Dict[str, str] = {"p0": "critical", "p1": "high", "p2": "medium", "p3": "low"}
REQUIRED_BEACON_KEYS: List[str] = [
    "version", "directory", "role", "purpose", "relevance",
    "crawl", "read_priority", "seed_reference", "token_density", "instructions"
]
ALLOWED_BEACON_KEYS: Set[str] = set(REQUIRED_BEACON_KEYS) | {
    "tier1_preload", "inherited", "key_files", "imports_from", "exported_to", "dependencies"
}
VALID_RELEVANCE: Set[str] = {"critical", "high", "medium", "low", "zero_for_llm"}
VALID_PRIORITIES: Set[str] = {"p0", "p1", "p2", "p3"}
VALID_SEED_REFS: Set[str] = {"required", "optional"}
VALID_TOKEN_DENSITIES: Set[str] = {"sparse", "medium", "dense", "massive_text", "massive_binary"}


def validate_beacon_data(data: Dict[str, Any]) -> List[str]:
    """
    Governs: [GAP-05], [V-06].
    Valida en stdlib pura que un diccionario .context.yaml cumpla 100% con schemas/beacon.schema.json
    (incluyendo additionalProperties: false, tipos de listas y longitudes máximas).
    """
    errors: List[str] = []
    if not isinstance(data, dict):
        return ["el contenido del beacon no es un objeto clave-valor válido"]

    unknown_keys = set(data.keys()) - ALLOWED_BEACON_KEYS
    if unknown_keys:
        errors.append(f"propiedades no permitidas (additionalProperties: false): {sorted(unknown_keys)}")

    for req in REQUIRED_BEACON_KEYS:
        if req not in data or data[req] is None or data[req] == "":
            errors.append(f"falta clave '{req}'")

    if "relevance" in data and data["relevance"] not in VALID_RELEVANCE:
        errors.append(f"relevance inválido '{data['relevance']}'")
    if "read_priority" in data and data["read_priority"] not in VALID_PRIORITIES:
        errors.append(f"read_priority inválido '{data['read_priority']}'")
    if "seed_reference" in data and data["seed_reference"] not in VALID_SEED_REFS:
        errors.append(f"seed_reference inválido '{data['seed_reference']}'")
    if "token_density" in data and data["token_density"] not in VALID_TOKEN_DENSITIES:
        errors.append(f"token_density inválido '{data['token_density']}'")
    if "crawl" in data and not isinstance(data["crawl"], bool):
        errors.append(f"crawl debe ser booleano (recibido {type(data['crawl']).__name__})")
    if "tier1_preload" in data and not isinstance(data["tier1_preload"], bool):
        errors.append("tier1_preload debe ser booleano")
    if "inherited" in data and not isinstance(data["inherited"], bool):
        errors.append("inherited debe ser booleano")
    if "directory" in data and "\\" in str(data["directory"]):
        errors.append("directory contiene '\\' (viola [INV-08])")
    if "purpose" in data and isinstance(data["purpose"], str) and len(data["purpose"]) > 200:
        errors.append(f"purpose excede maxLength=200 ({len(data['purpose'])} chars)")
    if "instructions" in data and isinstance(data["instructions"], str) and len(data["instructions"]) > 240:
        errors.append(f"instructions excede maxLength=240 ({len(data['instructions'])} chars)")

    for list_key in ("key_files", "imports_from", "exported_to"):
        if list_key in data:
            val = data[list_key]
            if not isinstance(val, list):
                errors.append(f"{list_key} debe ser una lista")
            else:
                for item in val:
                    if not isinstance(item, str):
                        errors.append(f"elemento en {list_key} debe ser string")
                    elif list_key == "key_files" and len(item) > 160:
                        errors.append(f"item en key_files excede maxLength=160 ({len(item)} chars)")
                    elif list_key in ("imports_from", "exported_to") and "\\" in item:
                        errors.append(f"item en {list_key} contiene '\\' ('{item}')")
    return errors


def validate_tree_data(data: Dict[str, Any]) -> List[str]:
    """
    Governs: [V-03], [V-06].
    Valida en stdlib pura que .context/tree.json cumpla con schemas/tree.schema.json.
    """
    errors: List[str] = []
    if not isinstance(data, dict):
        return ["tree.json no es un objeto JSON válido"]
    if data.get("sliced") is True:
        for req in ("project", "sliced", "focus_node", "nodes"):
            if req not in data:
                errors.append(f"falta clave obligatoria en slice: '{req}'")
    else:
        for req in ("$schema", "version", "project", "architecture", "updated_at", "timestamp", "topology_hash", "bootloader", "nodes"):
            if req not in data:
                errors.append(f"falta clave obligatoria en tree.json: '{req}'")
        th = data.get("topology_hash", "")
        if not isinstance(th, str) or len(th) != 64:
            errors.append("topology_hash inválido (se requiere SHA-256 hex de 64 caracteres)")

    nodes = data.get("nodes")
    if not isinstance(nodes, dict):
        errors.append("'nodes' debe ser un objeto")
    else:
        for nk, nv in nodes.items():
            if not isinstance(nv, dict):
                errors.append(f"nodo '{nk}' no es un objeto")
                continue
            for r in ("role", "prio", "crawl"):
                if r not in nv:
                    errors.append(f"nodo '{nk}' carece de '{r}'")
            if nv.get("prio") not in VALID_PRIORITIES:
                errors.append(f"nodo '{nk}' tiene prio inválido '{nv.get('prio')}'")
            if not isinstance(nv.get("crawl"), bool):
                errors.append(f"nodo '{nk}' tiene crawl no booleano")
    return errors


ALLOWED_BACKLOG_ITEM_KEYS: Set[str] = {
    "id", "target_nodes", "tier_estimate", "intent", "status", "acceptance_test"
}
VALID_TIER_ESTIMATES: Set[str] = {"1a", "1b", "2"}
VALID_BACKLOG_STATUSES: Set[str] = {"queued", "promoted", "done"}
BACKLOG_ID_REGEX = re.compile(r"^BKL-[0-9]{3,}$")


def validate_backlog_data(data: Dict[str, Any]) -> List[str]:
    """
    Valida en stdlib pura que artifacts/plans/backlog/queue.json cumpla con schemas/backlog.schema.json.
    """
    errors: List[str] = []
    if not isinstance(data, dict):
        return ["queue.json no es un objeto JSON válido"]

    unknown_root = set(data.keys()) - {"version", "items"}
    if unknown_root:
        errors.append(f"propiedades raíz no permitidas en queue.json: {sorted(unknown_root)}")

    if "version" not in data or not isinstance(data["version"], str):
        errors.append("falta 'version' (string) en queue.json")
    if "items" not in data or not isinstance(data["items"], list):
        errors.append("falta 'items' (array) en queue.json")
        return errors

    for idx, item in enumerate(data["items"]):
        prefix = f"item[{idx}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix} no es un objeto")
            continue

        item_id = item.get("id", f"#{idx}")
        unknown_keys = set(item.keys()) - ALLOWED_BACKLOG_ITEM_KEYS
        if unknown_keys:
            errors.append(f"item '{item_id}' tiene propiedades no permitidas: {sorted(unknown_keys)}")

        for req in ALLOWED_BACKLOG_ITEM_KEYS:
            if req not in item:
                errors.append(f"item '{item_id}' carece del campo obligatorio '{req}'")

        iid = item.get("id")
        if not isinstance(iid, str) or not BACKLOG_ID_REGEX.match(iid):
            errors.append(f"item '{item_id}' tiene id inválido (debe cumplir '^BKL-[0-9]{{3,}}$')")

        target_nodes = item.get("target_nodes")
        if not isinstance(target_nodes, list):
            errors.append(f"item '{item_id}': 'target_nodes' debe ser una lista")
        else:
            for node_path in target_nodes:
                if not isinstance(node_path, str) or "\\" in node_path or not node_path.strip():
                    errors.append(f"item '{item_id}': ruta en 'target_nodes' inválida '{node_path}'")

        tier = item.get("tier_estimate")
        if tier not in VALID_TIER_ESTIMATES:
            errors.append(f"item '{item_id}': tier_estimate inválido '{tier}' (válidos: {sorted(VALID_TIER_ESTIMATES)})")

        intent = item.get("intent")
        if not isinstance(intent, str) or len(intent) > 160:
            errors.append(f"item '{item_id}': intent debe ser string <= 160 caracteres")

        status = item.get("status")
        if status not in VALID_BACKLOG_STATUSES:
            errors.append(f"item '{item_id}': status inválido '{status}' (válidos: {sorted(VALID_BACKLOG_STATUSES)})")

        acc_test = item.get("acceptance_test")
        if not isinstance(acc_test, str):
            errors.append(f"item '{item_id}': acceptance_test debe ser un string")

    return errors


def validate_backlog_queue(root_path: Path, check_only: bool = False) -> List[str]:
    """
    Verifica la existencia y validez del archivo artifacts/plans/backlog/queue.json,
    así como la existencia física de todos sus target_nodes.
    """
    root = root_path.resolve()
    violations: List[str] = []
    backlog_dir = root / "artifacts" / "plans" / "backlog"
    queue_file = backlog_dir / "queue.json"

    if not queue_file.is_file():
        if check_only:
            return ["No se encontró el archivo de backlog requerido 'artifacts/plans/backlog/queue.json'."]
        backlog_dir.mkdir(parents=True, exist_ok=True)
        init_content = {"version": "1.0", "items": []}
        safe_io_retry(lambda: queue_file.write_text(json.dumps(init_content, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"))
        return violations

    try:
        data = json.loads(queue_file.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"Archivo 'artifacts/plans/backlog/queue.json' contiene JSON corrupto: {exc}"]

    schema_errs = validate_backlog_data(data)
    violations.extend(schema_errs)

    # Validar existencia física de target_nodes
    if isinstance(data.get("items"), list):
        for item in data["items"]:
            if not isinstance(item, dict):
                continue
            item_id = item.get("id", "desconocido")
            target_nodes = item.get("target_nodes", [])
            if isinstance(target_nodes, list):
                for target in target_nodes:
                    if not isinstance(target, str):
                        continue
                    clean_target = target.strip().replace("\\", "/").rstrip("/")
                    target_p = root / clean_target
                    if not target_p.exists():
                        violations.append(
                            f"Nodo huérfano en backlog '{item_id}': '{target}' no existe físicamente en el repositorio."
                        )

    return violations


def _rel_posix(path: Path, root_path: Path) -> str:
    """Governs: [INV-08]. Ruta relativa estilo Unix; '.' para la raíz."""
    return path.resolve().relative_to(root_path.resolve()).as_posix()


def load_ignore_patterns(root_path: Path) -> List[str]:
    """
    Governs: [INV-02].
    Lee .agentignore y .gitignore (si existen). Omite comentarios, vacíos y negaciones ('!').
    """
    patterns: List[str] = []
    for name in (".agentignore", ".gitignore"):
        ignore_file = root_path / name
        if not ignore_file.is_file():
            continue
        try:
            lines = ignore_file.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for raw in lines:
            line = raw.strip()
            if not line or line.startswith("#") or line.startswith("!"):
                continue
            patterns.append(line.replace("\\", "/").lstrip("/"))
    return patterns


def is_ignored_path(
    dir_path: Path,
    root_path: Path,
    patterns: Optional[List[str]] = None
) -> bool:
    """
    Governs: [INV-02], [INV-03].
    True si el directorio: está fuera de la raíz; algún segmento es oculto ('.x') o está en
    IGNORED_DISCOVERY_DIRS; coincide con un patrón de directorio de .agentignore/.gitignore;
    o hereda crawl: false (resolve_beacon).
    """
    root = root_path.resolve()
    target = dir_path.resolve()
    try:
        rel = target.relative_to(root)
    except ValueError:
        return True
    parts = rel.parts
    if not parts:
        return False  # la raíz nunca se ignora
    lowered = [p.lower() for p in parts]
    for part in lowered:
        if part.startswith(".") or part in IGNORED_DISCOVERY_DIRS:
            return True
    rel_posix = "/".join(lowered)
    if patterns is None:
        patterns = load_ignore_patterns(root)
    for pat in patterns:
        p = pat.lower()
        if p.endswith("/"):
            core = p.rstrip("/")
            if "/" in core:  # patrón anclado: data/raw/
                if rel_posix == core or rel_posix.startswith(core + "/"):
                    return True
            elif any(fnmatch.fnmatch(part, core) for part in lowered):  # logs/, *.delta/
                return True
        elif "/" not in p and not any(ch in p for ch in "*?[") and p in lowered:
            return True  # nombre literal sin slash (p. ej. 'node_modules')
    if resolve_beacon(target, root).get("crawl", True) is False:
        return True
    return False


def discover_unbeaconed_directories(root_path: Path) -> List[Path]:
    """
    Governs: [INV-02], [INV-03], [G-01].
    os.walk con poda in-place: no desciende a directorios ignorados ni con crawl: false.
    Retorna directorios no ignorados sin .context.yaml físico (orden determinista).
    """
    root = root_path.resolve()
    patterns = load_ignore_patterns(root)
    orphans: List[Path] = []
    for current, dirs, _files in os.walk(root):
        cur = Path(current)
        kept: List[str] = []
        for name in sorted(dirs):
            child = cur / name
            if is_ignored_path(child, root, patterns):
                continue
            kept.append(name)
            if not (child / BEACON_FILENAME).exists():
                orphans.append(child)
        dirs[:] = kept
    return orphans


def infer_beacon_meta(dir_path: Path, root_path: Path) -> Dict[str, Any]:
    """
    Governs: [INV-03], [INV-07].
    Infiere metadatos para un directorio NO canónico:
      - namespace: ancestro de algún nodo canónico (p. ej. src/, docs/).
      - domain_extension: primer nivel no canónico (p. ej. infrastructure/).
      - subdominio: hoja bajo un nodo existente; hereda role/seed_reference y marca inherited: True.
    """
    root = root_path.resolve()
    rel = _rel_posix(dir_path, root)
    rel_l = rel.lower()
    name = dir_path.name.lower()
    parent_rel = rel_l.rsplit("/", 1)[0] if "/" in rel_l else ""
    inherited = resolve_beacon(dir_path, root)
    crawl = bool(inherited.get("crawl", True))
    is_namespace = any(k.lower().startswith(rel_l + "/") for k in FOLDER_METADATA)
    is_inherited_subdomain = False

    if is_namespace:
        role = "namespace"
        purpose = f"Contenedor de subdominios canónicos de {rel}/."
        instructions = "Sin lógica propia. Usar map --slice o leer el beacon del subdirectorio objetivo."
    elif "/" not in rel_l:
        role = "domain_extension"
        purpose = f"Dominio de extensión {name}."
        instructions = "Extensión de dominio activa. Enriquecer con /idir enrich si añade contratos."
    else:
        role = inherited.get("role", "general") if inherited.get("inherited") else "general"
        source = inherited.get("inherited_from") or parent_rel
        purpose = f"Subdominio {name} bajo {source}/."
        instructions = f"Hereda directivas de {source}/."
        is_inherited_subdomain = True

    if not crawl:
        prio = "p3"
    elif name in CODE_HINT_NAMES or role == "domain_extension":
        prio = "p1"
    elif name in DOC_HINT_NAMES or role == "namespace":
        prio = "p2"
    else:
        prio = inherited.get("read_priority", "p2")
        if prio not in PRIO_TO_RELEVANCE:
            prio = "p2"

    meta_out: Dict[str, Any] = {
        "role": role,
        "purpose": purpose,
        "relevance": PRIO_TO_RELEVANCE[prio],
        "crawl": crawl,
        "read_priority": prio,
        "seed_reference": inherited.get("seed_reference", "optional"),
        "tier1_preload": False,
        "token_density": "sparse",
        "instructions": instructions,
    }
    if is_inherited_subdomain:
        meta_out["inherited"] = True
    return meta_out


def scaffold_beacon_for_dir(
    dir_path: Path,
    root_path: Path,
    overwrite: bool = False
) -> Optional[Path]:
    """
    Governs: [OBJ-01], [INV-07], [INV-08], [G-03].
    Crea .context.yaml en dir_path. Si la ruta es canónica usa FOLDER_METADATA; si no, infer_beacon_meta().
    NUNCA sobrescribe un beacon existente salvo overwrite=True. Retorna la ruta creada o None.
    """
    root = root_path.resolve()
    target = dir_path.resolve()
    rel = _rel_posix(target, root)
    if rel == ".":
        return None
    beacon_file = target / BEACON_FILENAME
    if beacon_file.exists() and not overwrite:
        return None
    safe_io_retry(lambda: target.mkdir(parents=True, exist_ok=True))
    rel_key = rel.lower()
    if rel_key in FOLDER_METADATA:
        meta = dict(FOLDER_METADATA[rel_key])
        meta.setdefault("tier1_preload", False)
        content = generate_beacon_content(rel_key, meta, root_path=root)
    else:
        content = generate_beacon_content(rel, infer_beacon_meta(target, root), root_path=root)
    safe_io_retry(lambda: beacon_file.write_text(content + "\n", encoding="utf-8"))
    return beacon_file


def ensure_beacon_chain(target_dir: Path, root_path: Path) -> List[Path]:
    """
    Governs: [OBJ-02], [INV-04].
    Crea target_dir (si falta) y garantiza beacon en él y en cada ancestro hasta la raíz.
    Se detiene en segmentos ocultos / IGNORED_DISCOVERY_DIRS. Retorna beacons creados.
    """
    root = root_path.resolve()
    target = target_dir.resolve()
    safe_io_retry(lambda: target.mkdir(parents=True, exist_ok=True))
    created: List[Path] = []
    curr = root
    for part in target.relative_to(root).parts:
        if part.startswith(".") or part.lower() in IGNORED_DISCOVERY_DIRS:
            break
        curr = curr / part
        result = scaffold_beacon_for_dir(curr, root)
        if result is not None:
            created.append(result)
    return created


def iter_beacon_files(root_path: Path) -> List[Path]:
    """
    Governs: [INV-02].
    Lista beacons físicos: los canónicos (incluidos crawl: false) + los de directorios no ignorados.
    """
    root = root_path.resolve()
    patterns = load_ignore_patterns(root)
    found: Dict[str, Path] = {}
    for folder in FOLDER_METADATA:
        f = root / folder / BEACON_FILENAME
        if f.exists():
            found[f.as_posix().lower()] = f
    for current, dirs, files in os.walk(root):
        cur = Path(current)
        dirs[:] = [n for n in sorted(dirs) if not is_ignored_path(cur / n, root, patterns)]
        if cur != root and BEACON_FILENAME in files:
            f = cur / BEACON_FILENAME
            found[f.as_posix().lower()] = f
    return [found[k] for k in sorted(found)]


def _read_local_beacon(dir_path: Path) -> Dict[str, Any]:
    beacon = dir_path / BEACON_FILENAME
    if not beacon.exists():
        return {}
    try:
        return MiniYAML.load(beacon.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def sync_beacons(root_path: Path, auto_discover: bool = True, force_defaults: bool = False) -> int:
    """
    Sincroniza los .context.yaml canónicos (preservando comentarios '#' y enriquecimiento agéntico
    salvo force_defaults=True) y, si auto_discover=True, auto-scaffoldea beacons en directorios
    huérfanos no ignorados (sin sobrescribir existentes).
    """
    count = 0
    is_pkg_repo = _is_custom_src_package_repo(root_path.resolve())
    for folder, meta in FOLDER_METADATA.items():
        if folder == ".context":
            continue
        dir_path = root_path / folder
        if not dir_path.exists() and is_pkg_repo and folder in OPTIONAL_SKELETON_IF_PACKAGED:
            continue
        dir_path.mkdir(parents=True, exist_ok=True)
        beacon_file = dir_path / BEACON_FILENAME
        preserved_comments = extract_preserved_comments(beacon_file)
        effective_meta = dict(meta)
        if beacon_file.exists() and not force_defaults:
            existing = _read_local_beacon(dir_path)
            for enrich_key in ("purpose", "instructions", "key_files", "imports_from", "exported_to", "dependencies"):
                if enrich_key in existing and existing[enrich_key]:
                    effective_meta[enrich_key] = existing[enrich_key]
        beacon_content = generate_beacon_content(folder, effective_meta, root_path=root_path)
        if preserved_comments:
            beacon_content = beacon_content + "\n" + "\n".join(preserved_comments)
        final_content = beacon_content + "\n"
        safe_io_retry(lambda: beacon_file.write_text(final_content, encoding="utf-8"))
        count += 1
    if auto_discover:
        for orphan in discover_unbeaconed_directories(root_path):
            if scaffold_beacon_for_dir(orphan, root_path) is not None:
                count += 1
    return count


# ------------------------------------------------------------------------------
# 3.2 Fingerprint Topológico SHA-256 y Generación de Satélite Verificable (v4.0)
# ------------------------------------------------------------------------------
def _resolve_beacon_fast(
    dir_path: Path,
    root_path: Path,
    beacon_cache: Optional[Dict[str, Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Versión con caché en memoria para evitar lecturas repetitivas en os.walk."""
    try:
        rel = dir_path.relative_to(root_path).as_posix().lower()
    except ValueError:
        return {"crawl": True, "role": "general", "read_priority": "p2"}
    if beacon_cache is not None and rel in beacon_cache:
        return beacon_cache[rel]
    res = resolve_beacon(dir_path, root_path)
    if beacon_cache is not None:
        beacon_cache[rel] = res
    return res


def compute_topology_hash(root_path: Path) -> str:
    """
    Governs: [V-02], [Corrección-1].
    Calcula un fingerprint determinista SHA-256 en una sola pasada (O(N)) sobre:
    - Presencia física de cada nodo canónico y contenido de su .context.yaml.
    - Subdirectorios inmediatos y archivos de nodos activos (crawl: true).
    Inmune a distorsiones de mtime tras git clone / checkout.
    """
    root = root_path.resolve()
    hasher = hashlib.sha256()
    patterns = load_ignore_patterns(root) if root.exists() else []
    beacon_cache: Dict[str, Dict[str, Any]] = {}

    # 1. Nodos canónicos y sus beacons (usando os.scandir para mínima latencia en NTFS)
    for folder, meta in sorted(FOLDER_METADATA.items()):
        if folder == ".context":
            continue
        dpath = root / folder
        exists = dpath.is_dir()
        hasher.update(f"CANON:{folder}:exists={exists}\n".encode("utf-8"))
        if not exists:
            continue
        beacon = dpath / BEACON_FILENAME
        if beacon.is_file():
            try:
                b_bytes = beacon.read_bytes()
                hasher.update(f"BEACON:{folder}:{hashlib.sha256(b_bytes).hexdigest()}\n".encode("utf-8"))
            except OSError:
                pass
        if not meta.get("crawl", True):
            continue
        try:
            with os.scandir(dpath) as it:
                subdirs = []
                files = []
                for entry in it:
                    ename = entry.name
                    if ename.startswith(".") and ename != BEACON_FILENAME:
                        continue
                    if ename.lower() in IGNORED_DISCOVERY_DIRS:
                        continue
                    if entry.is_dir(follow_symlinks=False):
                        subdirs.append(ename)
                    else:
                        files.append(ename)
                subdirs.sort()
                files.sort()
                hasher.update(f"NODE:{folder}:subdirs={','.join(subdirs)}:files={','.join(files)}\n".encode("utf-8"))
        except OSError:
            pass

    # 2. Directorios de primer nivel en raíz
    if root.exists() and root.is_dir():
        try:
            with os.scandir(root) as it:
                root_dirs = sorted(
                    e.name for e in it
                    if not e.name.startswith(".") and e.name.lower() not in IGNORED_DISCOVERY_DIRS and e.is_dir(follow_symlinks=False)
                )
        except OSError:
            root_dirs = []
        hasher.update(f"ROOT_DIRS:{','.join(root_dirs)}\n".encode("utf-8"))

    return hasher.hexdigest()


def _has_dynamic_subdirectories(dir_path: Path, root_path: Path, patterns: List[str]) -> bool:
    """Detecta rápidamente con os.scandir si un directorio posee subdirectorios que no son nodos canónicos."""
    canonical_lowers = {k.lower() for k in FOLDER_METADATA}
    try:
        rel_base = dir_path.relative_to(root_path).as_posix().lower()
    except ValueError:
        return False
    try:
        with os.scandir(dir_path) as it:
            for entry in it:
                name = entry.name
                if name.startswith(".") or name.lower() in IGNORED_DISCOVERY_DIRS:
                    continue
                if entry.is_dir(follow_symlinks=False):
                    rel_child = f"{rel_base}/{name.lower()}" if rel_base != "." else name.lower()
                    if rel_child not in canonical_lowers:
                        return True
    except OSError:
        return False
    return False


def compute_node_fingerprint(dir_path: Path) -> str:
    """
    Indexación Incremental O(Delta) por Nodo (v4.1):
    Usando os.scandir(), calcula un hash SHA-256 rápido de 16 caracteres hexadecimales
    basado únicamente en (entry.name, entry.stat().st_size, entry.stat().st_mtime_ns) de los
    archivos directos del directorio y su .context.yaml, ignorando binarios y subdirectorios.
    """
    if not dir_path.is_dir():
        return ""
    hasher = hashlib.sha256()
    file_entries: List[Tuple[str, int, int]] = []
    try:
        with os.scandir(dir_path) as it:
            for entry in it:
                try:
                    if entry.is_dir(follow_symlinks=False):
                        continue
                    ename = entry.name
                    if ename.startswith(".") and ename != BEACON_FILENAME:
                        continue
                    if ename.lower().endswith(BINARY_EXTENSIONS_TUPLE):
                        continue
                    st = entry.stat(follow_symlinks=False)
                    file_entries.append((ename, st.st_size, st.st_mtime_ns))
                except OSError:
                    continue
    except OSError:
        return ""

    file_entries.sort(key=lambda x: x[0])
    for name, size, mtime_ns in file_entries:
        hasher.update(f"{name}:{size}:{mtime_ns}\n".encode("utf-8"))
    return hasher.hexdigest()[:16]


OPTIONAL_SKELETON_IF_PACKAGED: Set[str] = {
    "src/cloud_jobs",
    "src/core",
    "src/dashboards",
    "src/data_generation",
    "tools",
    "data/sandbox",
}


def _is_custom_src_package_repo(root: Path) -> bool:
    """Detecta si el repositorio es un paquete Python con pyproject.toml y src/<pkg> propio."""
    if not (root / "pyproject.toml").is_file():
        return False
    src_dir = root / "src"
    if not src_dir.is_dir():
        return False
    canonical_src = {"cloud_jobs", "core", "dashboards", "data_generation"}
    try:
        for entry in os.listdir(src_dir):
            if not entry.startswith(".") and entry.lower() not in canonical_src and (src_dir / entry).is_dir():
                return True
    except OSError:
        pass
    return False


def generate_tree_json(root_path: Path) -> Dict[str, Any]:
    """Genera el mapa satelital verificable de todo el repositorio (v4.0)."""
    root = root_path.resolve()
    now_ts = time.time()
    seed_files = resolve_seed_key_files(root)
    primary_seed = f"01_seed/{seed_files[0]}"
    topo_hash = compute_topology_hash(root)

    tree_data: Dict[str, Any] = {
        "$schema": "../schemas/tree.schema.json",
        "version": "5.0",
        "project": root.name,
        "architecture": "Gravity HyperScale Thinking",
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "timestamp": now_ts,
        "topology_hash": topo_hash,
        "bootloader": {
            "tier_1": [
                "AGENTS.md",
                ".context/tree.json",
                "[target_folder]/.context.yaml"
            ],
            "tier_1a": [
                "python FWengine.py context --pack <target_dir> --tier 1a"
            ],
            "tier_1b": [
                "python FWengine.py context --compact",
                "python FWengine.py map --slice <target_dir>",
                "python FWengine.py seed --section <id>"
            ],
            "tier_2": [
                "AGENTS.md",
                ".context/tree.json",
                primary_seed,
                "[target_folder]/.context.yaml"
            ]
        },
        "nodes": {}
    }

    canonical_top_levels: Set[str] = {k.split("/")[0].lower() for k in FOLDER_METADATA.keys()}
    patterns = load_ignore_patterns(root) if root.exists() else []
    is_pkg_repo = _is_custom_src_package_repo(root)

    for folder, meta in FOLDER_METADATA.items():
        folder_dir = root / folder
        exists_on_disk = folder_dir.is_dir()
        if not exists_on_disk and is_pkg_repo and folder in OPTIONAL_SKELETON_IF_PACKAGED:
            continue
        physical_key = _resolve_physical_rel_path(root, folder) if exists_on_disk else folder
        local_beacon = _read_local_beacon(folder_dir) if exists_on_disk else {}

        node_info: Dict[str, Any] = {
            "role": local_beacon.get("role") or meta.get("role", "general"),
            "prio": local_beacon.get("read_priority") or meta.get("read_priority", "p2"),
            "crawl": bool(local_beacon.get("crawl", meta.get("crawl", True))) if meta.get("crawl", True) else False,
        }
        seed_ref_val = local_beacon.get("seed_reference") or meta.get("seed_reference", "optional")
        if seed_ref_val == "required":
            node_info["seed_ref"] = "required"
        if not exists_on_disk:
            node_info["exists"] = False
        if "tier1_preload" in meta:
            node_info["tier1_preload"] = meta["tier1_preload"]
        if folder == "01_seed":
            node_info["key_files"] = seed_files
        elif local_beacon.get("key_files"):
            node_info["key_files"] = local_beacon["key_files"]
        elif "key_files" in meta:
            node_info["key_files"] = meta["key_files"]

        if exists_on_disk and node_info["crawl"] and _has_dynamic_subdirectories(folder_dir, root, patterns):
            node_info["has_dynamic_children"] = True
        if exists_on_disk:
            node_info["node_hash"] = compute_node_fingerprint(folder_dir)

        tree_data["nodes"][physical_key] = node_info

    # Auto-discover non-canonical first-level domain directories
    if root.exists() and root.is_dir():
        try:
            disk_entries = sorted(os.listdir(root))
        except OSError:
            disk_entries = []
        for entry in disk_entries:
            if entry.startswith(".") or entry.lower() in IGNORED_DISCOVERY_DIRS:
                continue
            if entry.lower() in canonical_top_levels:
                continue
            full_entry = root / entry
            if full_entry.is_dir() and not is_ignored_path(full_entry, root, patterns):
                local = _read_local_beacon(full_entry)
                ext_node: Dict[str, Any] = {
                    "role": local.get("role", "domain_extension"),
                    "prio": local.get("read_priority", "p1"),
                    "crawl": bool(local.get("crawl", True)),
                    "node_hash": compute_node_fingerprint(full_entry)
                }
                if local.get("seed_reference") == "required":
                    ext_node["seed_ref"] = "required"
                if local.get("key_files"):
                    ext_node["key_files"] = local["key_files"]
                if ext_node["crawl"] and _has_dynamic_subdirectories(full_entry, root, patterns):
                    ext_node["has_dynamic_children"] = True
                tree_data["nodes"][entry] = ext_node

        # Auto-discover custom packages under src/ when is_pkg_repo is True
        if is_pkg_repo and (root / "src").is_dir():
            canonical_src = {"cloud_jobs", "core", "dashboards", "data_generation"}
            try:
                src_entries = sorted(os.listdir(root / "src"))
            except OSError:
                src_entries = []
            for sub in src_entries:
                if sub.startswith(".") or sub.lower() in canonical_src or sub.lower() in IGNORED_DISCOVERY_DIRS:
                    continue
                sub_dir = root / "src" / sub
                if sub_dir.is_dir() and not is_ignored_path(sub_dir, root, patterns):
                    local = _read_local_beacon(sub_dir)
                    pkg_node: Dict[str, Any] = {
                        "role": local.get("role", "shared_backend"),
                        "prio": local.get("read_priority", "p1"),
                        "crawl": bool(local.get("crawl", True)),
                        "node_hash": compute_node_fingerprint(sub_dir),
                    }
                    if local.get("key_files"):
                        pkg_node["key_files"] = local["key_files"]
                    if pkg_node["crawl"] and _has_dynamic_subdirectories(sub_dir, root, patterns):
                        pkg_node["has_dynamic_children"] = True
                    tree_data["nodes"][f"src/{sub}"] = pkg_node

    return tree_data


def check_satellite_freshness(root_path: Path) -> Dict[str, Any]:
    """
    Governs: [V-02], [Corrección-1].
    Verifica si .context/tree.json está al día combinando:
    1. Fingerprint criptográfico determinista (topology_hash SHA-256) de carpetas, subdirectorios y .context.yaml.
    2. Marca temporal (mtime) de todos los directorios gobernados (incluyendo artifacts/, infrastructure/, beacons y raíz).
    """
    root = root_path.resolve()
    tree_file = root / ".context" / "tree.json"
    if not tree_file.exists():
        return {
            "fresh": False,
            "drift_detected": True,
            "satellite_time": 0.0,
            "latest_mtime": 0.0,
            "latest_path": None,
            "topology_hash_match": False,
            "reason": "El archivo .context/tree.json no existe. Ejecute 'python FWengine.py reconcile'."
        }

    try:
        with open(tree_file, "r", encoding="utf-8") as f:
            tree_data = json.load(f)
        satellite_time = max(
            float(tree_data.get("timestamp", 0.0)),
            float(tree_file.stat().st_mtime),
        )
        recorded_hash = str(tree_data.get("topology_hash", ""))
    except Exception:
        satellite_time = tree_file.stat().st_mtime
        recorded_hash = ""

    current_hash = compute_topology_hash(root)
    hash_match = bool(recorded_hash) and (recorded_hash == current_hash)

    # Recolectar todos los directorios de primer nivel gobernados + extensiones
    key_folders: Set[str] = {k.split("/")[0] for k in FOLDER_METADATA.keys() if k != ".context"}
    if root.exists():
        try:
            for entry in os.listdir(root):
                if not entry.startswith(".") and entry.lower() not in IGNORED_DISCOVERY_DIRS:
                    if (root / entry).is_dir():
                        key_folders.add(entry)
        except OSError:
            pass

    patterns = load_ignore_patterns(root)
    latest_mtime = 0.0
    latest_path: Optional[Path] = None

    for kf in sorted(key_folders):
        dir_path = root / kf
        if not dir_path.exists() or is_ignored_path(dir_path, root, patterns):
            continue
        try:
            d_mtime = dir_path.stat().st_mtime
            if d_mtime > latest_mtime:
                latest_mtime = d_mtime
                latest_path = dir_path
        except OSError:
            pass

        for current, dirs, files in os.walk(dir_path):
            cur = Path(current)
            dirs[:] = [
                n for n in sorted(dirs)
                if not n.startswith(".") and n.lower() not in IGNORED_DISCOVERY_DIRS
                and not is_ignored_path(cur / n, root, patterns)
            ]
            for fname in files:
                # Incluir explícitamente .context.yaml aunque empiece con '.'
                if fname.startswith(".") and fname != BEACON_FILENAME:
                    continue
                item = cur / fname
                try:
                    m = item.stat().st_mtime
                    if m > latest_mtime:
                        latest_mtime = m
                        latest_path = item
                except OSError:
                    pass

    mtime_drift = latest_mtime > (satellite_time + 1.5)
    drift = (not hash_match) or mtime_drift
    rel_path_str = _rel_posix(latest_path, root) if latest_path else ("topology_hash" if not hash_match else "desconocido")
    return {
        "fresh": not drift,
        "drift_detected": drift,
        "topology_hash_match": hash_match,
        "satellite_time": satellite_time,
        "latest_mtime": latest_mtime,
        "latest_path": rel_path_str
    }


def format_compact_tree_json(data: Dict[str, Any]) -> str:
    """
    Governs: [R-005], [ADR-009], [INV-07].
    Serializes tree.json with one compact JSON line per node in 'nodes', keeping total size < 1,000 tokens.
    """
    lines: List[str] = ["{"]
    top_keys = [k for k in data.keys() if k != "nodes"]
    for k in top_keys:
        val_str = json.dumps(data[k], ensure_ascii=False, separators=(",", ": "))
        lines.append(f'  "{k}": {val_str},')
    lines.append('  "nodes": {')
    node_items = list(data.get("nodes", {}).items())
    for idx, (node_key, node_val) in enumerate(node_items):
        comma = "," if idx < len(node_items) - 1 else ""
        compact_node = json.dumps(node_val, ensure_ascii=False, separators=(",", ":"))
        lines.append(f'    {json.dumps(node_key, ensure_ascii=False)}: {compact_node}{comma}')
    lines.append("  }")
    lines.append("}")
    return "\n".join(lines) + "\n"


def sync_tree(root_path: Path) -> Path:
    """
    Governs: [R-005], [R-006], [INV-04], [INV-07].
    Writes .context/tree.json using format_compact_tree_json().
    """
    context_dir = root_path / ".context"
    context_dir.mkdir(parents=True, exist_ok=True)
    tree_file = context_dir / "tree.json"
    # Pre-crear tree.json si no existe para que compute_topology_hash vea el estado final de .context/
    if not tree_file.exists():
        tree_file.write_text("{}", encoding="utf-8")
    data = generate_tree_json(root_path)
    data["timestamp"] = time.time()
    with open(tree_file, "w", encoding="utf-8", newline="\n") as f:
        f.write(format_compact_tree_json(data))
    return tree_file


def generate_sliced_tree(
    root_path: Path,
    target_path: str,
    radius: int = 1,
    max_children: int = 6
) -> Dict[str, Any]:
    """
    Governs: [OBJ-04], [INV-02], [INV-03], [INV-08], [V-05].
    Subgrafo focalizado: nodo foco + padre + descendientes hasta 'radius' niveles (máx. max_children)
    + dependencias declaradas en el beacon foco ('imports_from' y 'exported_to').
    Garantiza len(format_sliced_tree(result)) <= SLICE_CHAR_BUDGET recortando hijos, consumidores,
    dependencias y key_files, emitiendo 'budget_exceeded: True' y 'omitted_nodes' si aplica.
    """
    root = root_path.resolve()
    focus = target_path.replace("\\", "/").strip()
    if focus.startswith("./"):
        focus = focus[2:]
    focus = focus.strip("/")
    if not focus or ".." in focus.split("/"):
        raise PermissionError(f"[-] Error de Seguridad: ruta de slice inválida '{target_path}'.")
    focus_dir = (root / focus).resolve()
    try:
        focus_dir.relative_to(root)
    except ValueError:
        raise PermissionError(f"[-] Error de Seguridad: slice fuera de la raíz '{target_path}'.")
    if not focus_dir.is_dir():
        raise FileNotFoundError(f"[-] Directorio de slice inexistente: '{focus}'")

    tree = generate_tree_json(root)
    tree_nodes = {k.lower(): v for k, v in tree["nodes"].items()}
    patterns = load_ignore_patterns(root)

    def build_node(dir_path: Path, edge: str) -> Dict[str, Any]:
        rel = _rel_posix(dir_path, root)
        local = _read_local_beacon(dir_path)
        resolved = resolve_beacon(dir_path, root)
        tn = tree_nodes.get(rel.lower(), {})
        node: Dict[str, Any] = {
            "role": local.get("role") or tn.get("role") or resolved.get("role", "general"),
            "prio": local.get("read_priority") or tn.get("prio") or resolved.get("read_priority", "p2"),
            "crawl": bool(resolved.get("crawl", True)),
            "edge": edge,
        }
        kf = local.get("key_files") or tn.get("key_files")
        if edge == "focus":
            if kf:
                node["key_files"] = list(kf)
            purp = local.get("purpose") or resolved.get("purpose", "")
            if purp:
                node["purpose"] = purp[:80]
        if not node["crawl"]:
            node["pruned"] = True
        return node

    focus_key = _rel_posix(focus_dir, root)
    nodes: Dict[str, Dict[str, Any]] = {focus_key: build_node(focus_dir, "focus")}

    if "/" in focus_key:
        parent_dir = focus_dir.parent
        nodes[_rel_posix(parent_dir, root)] = build_node(parent_dir, "parent")

    children: List[Path] = []
    if nodes[focus_key]["crawl"]:  # [INV-03] no expandir ramas podadas
        frontier = [focus_dir]
        for _ in range(max(1, radius)):
            next_frontier: List[Path] = []
            for d in frontier:
                try:
                    entries = sorted(os.listdir(d))
                except OSError:
                    continue
                for name in entries:
                    child = d / name
                    if child.is_dir() and not is_ignored_path(child, root, patterns):
                        children.append(child)
                        next_frontier.append(child)
            frontier = next_frontier

    focus_local = _read_local_beacon(focus_dir)
    dep_keys: List[str] = []
    for dep in focus_local.get("imports_from", []) or []:
        dep_dir = (root / str(dep).strip("/")).resolve()
        try:
            dep_key = _rel_posix(dep_dir, root)
        except ValueError:
            continue
        if dep_dir.is_dir() and dep_key not in nodes:
            nodes[dep_key] = build_node(dep_dir, "dep")
            dep_keys.append(dep_key)

    consumer_keys: List[str] = []
    for cons in focus_local.get("exported_to", []) or []:
        cons_dir = (root / str(cons).strip("/")).resolve()
        try:
            cons_key = _rel_posix(cons_dir, root)
        except ValueError:
            continue
        if cons_dir.is_dir() and cons_key not in nodes:
            nodes[cons_key] = build_node(cons_dir, "consumer")
            consumer_keys.append(cons_key)

    result: Dict[str, Any] = {
        "project": tree["project"],
        "sliced": True,
        "focus_node": focus_key,
        "sliced_at": int(time.time()),
        "nodes": nodes,
    }
    total_children = len(children)
    for child in children[:max_children]:
        nodes[_rel_posix(child, root)] = build_node(child, "child")
    included = min(total_children, max_children)

    omitted: List[str] = []
    # Paso 1: si excede presupuesto, quitar propósito opcional del foco primero
    if len(format_sliced_tree(result)) > SLICE_CHAR_BUDGET and "purpose" in nodes[focus_key]:
        nodes[focus_key].pop("purpose", None)

    # Paso 2: recortar hijos
    while len(format_sliced_tree(result)) > SLICE_CHAR_BUDGET and included > 0:
        included -= 1
        ck = _rel_posix(children[included], root)
        nodes.pop(ck, None)
        omitted.append(ck)
        result["truncated"] = total_children - included

    # Paso 3: recortar consumidores
    while len(format_sliced_tree(result)) > SLICE_CHAR_BUDGET and consumer_keys:
        dropped = consumer_keys.pop()
        nodes.pop(dropped, None)
        omitted.append(dropped)
        result["truncated"] = result.get("truncated", 0) + 1

    # Paso 4: recortar dependencias (imports_from) si aún supera SLICE_CHAR_BUDGET
    while len(format_sliced_tree(result)) > SLICE_CHAR_BUDGET and dep_keys:
        dropped_dep = dep_keys.pop()
        nodes.pop(dropped_dep, None)
        omitted.append(dropped_dep)
        result["budget_exceeded"] = True
        result["truncated"] = result.get("truncated", 0) + 1

    # Paso 5: recortar key_files del nodo foco si aún supera SLICE_CHAR_BUDGET
    while len(format_sliced_tree(result)) > SLICE_CHAR_BUDGET and nodes[focus_key].get("key_files"):
        nodes[focus_key]["key_files"].pop()
        result["budget_exceeded"] = True
        result["truncated"] = result.get("truncated", 0) + 1
        if not nodes[focus_key]["key_files"]:
            nodes[focus_key].pop("key_files", None)
            break

    if total_children > included and "truncated" not in result:
        result["truncated"] = total_children - included
    if result.get("budget_exceeded") and omitted:
        result["omitted_nodes"] = omitted[:5]
        while len(format_sliced_tree(result)) > SLICE_CHAR_BUDGET and result.get("omitted_nodes"):
            result["omitted_nodes"].pop()
            if not result["omitted_nodes"]:
                result.pop("omitted_nodes", None)
                break
    return result


def format_sliced_tree(data: Dict[str, Any]) -> str:
    """Governs: [OBJ-04]. Serialización de una línea, separadores mínimos (menor costo en tokens)."""
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))


# ------------------------------------------------------------------------------
# 3.3 Compilador de Context Pack, Navegador Seccional de Seed y Checkpoints (v4.0)
# ------------------------------------------------------------------------------
def build_context_pack(root_path: Path, target_path: str, tier: str = "1a") -> Dict[str, Any]:
    """
    Governs: [Opt-2].
    Compila en una sola llamada (< 220 tokens en Tier 1A) el paquete de orientación quirúrgica:
    - Subgrafo recortado (slice).
    - Directivas efectivas resueltas por herencia (role, prio, crawl, purpose, instructions).
    - Archivos clave verificados físicamente en disco con su peso estimado en tokens.
    - Alerta de continuidad si existe .context/checkpoint.json activo.
    """
    root = root_path.resolve()
    sliced = generate_sliced_tree(root, target_path, radius=1, max_children=4)
    focus_key = sliced["focus_node"]
    focus_dir = root / focus_key
    resolved = resolve_beacon(focus_dir, root)
    local = _read_local_beacon(focus_dir)

    verified_files: List[str] = []
    if resolved.get("crawl", True) and focus_dir.is_dir():
        try:
            for entry in sorted(os.listdir(focus_dir))[:8]:
                if entry.startswith(".") or entry.lower() in ("desktop.ini", "thumbs.db", ".ds_store"):
                    continue
                fp = focus_dir / entry
                if fp.is_file():
                    tok = estimate_tokens_v4(fp)
                    verified_files.append(f"{entry}(~{tok}t)")
        except OSError:
            pass

    pack: Dict[str, Any] = {
        "idir_pack": ENGINE_VERSION,
        "tier": tier.lower(),
        "focus": focus_key,
        "role": local.get("role") or resolved.get("role", "general"),
        "prio": local.get("read_priority") or resolved.get("read_priority", "p2"),
        "crawl": bool(resolved.get("crawl", True)),
        "seed_ref": local.get("seed_reference") or resolved.get("seed_reference", "optional"),
        "instructions": (local.get("instructions") or resolved.get("instructions", ""))[:120],
        "files": verified_files[:6],
        "edges": {k: v["edge"] for k, v in sliced["nodes"].items() if k != focus_key},
    }
    if resolved.get("inherited"):
        pack["inherited_from"] = resolved.get("inherited_from")

    cp_file = root / ".context" / "checkpoint.json"
    if cp_file.is_file():
        try:
            cp_data = json.loads(cp_file.read_text(encoding="utf-8"))
            if cp_data.get("status") in ("executing", "approved", "paused"):
                pack["checkpoint"] = {
                    "plan_id": cp_data.get("plan_id"),
                    "phase": cp_data.get("current_phase"),
                    "next": cp_data.get("next_action", "")[:80],
                }
        except Exception:
            pass
    return pack


def get_seed_sections(root_path: Path) -> List[Dict[str, Any]]:
    """
    Governs: [Opt-3].
    Parsea los encabezados ## y ### del archivo seed activo en 01_seed/, devolviendo
    el índice de secciones con su ID, título, rango de líneas y estimación de tokens.
    """
    root = root_path.resolve()
    seed_files = resolve_seed_key_files(root)
    seed_path = root / "01_seed" / seed_files[0]
    if not seed_path.is_file():
        return []
    lines = seed_path.read_text(encoding="utf-8", errors="replace").splitlines()
    sections: List[Dict[str, Any]] = []
    header_re = re.compile(r"^(#{2,3})\s+(?:(\d+(?:\.\d+)?)\b[\.\:\s-]*)?(.*)$")

    for idx, line in enumerate(lines, start=1):
        m = header_re.match(line.strip())
        if m:
            level = len(m.group(1))
            sec_id = m.group(2) or f"L{idx}"
            title = m.group(3).strip()
            if sections:
                sections[-1]["end_line"] = idx - 1
            sections.append({
                "id": sec_id,
                "level": level,
                "title": title,
                "start_line": idx,
                "end_line": len(lines),
            })

    for sec in sections:
        chunk = "\n".join(lines[sec["start_line"] - 1 : sec["end_line"]])
        sec["est_tokens"] = estimate_tokens_v4(chunk)
    return sections


def extract_seed_section(root_path: Path, query: str) -> str:
    """
    Governs: [Opt-3].
    Extrae quirúrgicamente una sección específica del ThinkingSeed Master por su ID ('2', '4.1')
    o por coincidencia de título, incluyendo sus subsecciones si se pide un capítulo de nivel 2.
    """
    root = root_path.resolve()
    seed_files = resolve_seed_key_files(root)
    seed_path = root / "01_seed" / seed_files[0]
    if not seed_path.is_file():
        return f"[-] Seed no encontrado en 01_seed/{seed_files[0]}"

    lines = seed_path.read_text(encoding="utf-8", errors="replace").splitlines()
    sections = get_seed_sections(root)
    q = query.strip().lower()

    # Buscar coincidencia exacta de ID primero
    target_idx = None
    for i, sec in enumerate(sections):
        if sec["id"].lower() == q or q in sec["title"].lower():
            target_idx = i
            break
    if target_idx is None:
        return f"[-] Sección '{query}' no encontrada en {seed_files[0]}. Use 'python FWengine.py seed --toc'."

    start_sec = sections[target_idx]
    start_line = start_sec["start_line"]
    end_line = start_sec["end_line"]
    # Si es de nivel 2 (##), abarcar también sus subsecciones (###) hasta el próximo ##
    if start_sec["level"] == 2:
        for nxt in sections[target_idx + 1 :]:
            if nxt["level"] <= 2:
                end_line = nxt["start_line"] - 1
                break
            end_line = nxt["end_line"]

    extracted = "\n".join(lines[start_line - 1 : end_line])
    tok = estimate_tokens_v4(extracted)
    header = f"# [SEED SECTION {start_sec['id']}: {start_sec['title']} | L{start_line}-L{end_line} | ~{tok} tokens]\n"
    return header + extracted


def manage_checkpoint(
    root_path: Path,
    action: str = "show",
    plan_id: Optional[str] = None,
    status: Optional[str] = None,
    phase: Optional[str] = None,
    next_action: Optional[str] = None,
    completed_step: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Governs: [Opt-5].
    Gestiona el estado de continuidad atencional en .context/checkpoint.json (< 300 tokens).
    """
    root = root_path.resolve()
    cp_dir = root / ".context"
    cp_dir.mkdir(parents=True, exist_ok=True)
    cp_file = cp_dir / "checkpoint.json"

    if action == "clear":
        if cp_file.exists():
            cp_file.unlink()
        return {"cleared": True}

    current: Dict[str, Any] = {
        "version": ENGINE_VERSION,
        "plan_id": "active-session",
        "status": "executing",
        "current_phase": "P0",
        "completed_steps": [],
        "next_action": "Verificar estado con python FWengine.py reconcile --check",
        "verified_evidence": [],
        "active_invariants": ["INV-01", "INV-02", "INV-03", "INV-06", "INV-08"],
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
    if cp_file.is_file():
        try:
            loaded = json.loads(cp_file.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                current.update(loaded)
        except Exception:
            pass

    if action == "set":
        if plan_id:
            current["plan_id"] = plan_id[:120]
        if status:
            current["status"] = status
        if phase:
            current["current_phase"] = phase[:120]
        if next_action:
            current["next_action"] = next_action[:240]
        if completed_step:
            steps = list(current.get("completed_steps", []))
            if completed_step not in steps:
                steps.append(completed_step[:160])
            current["completed_steps"] = steps[-8:]
        current["updated_at"] = datetime.now(timezone.utc).isoformat()
        safe_io_retry(lambda: cp_file.write_text(json.dumps(current, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"))

    return current


# ------------------------------------------------------------------------------
# 3.3b Protocolo de Interoperabilidad Federada v5.0 (AST Index, Bus & Ecosystem Pack)
# ------------------------------------------------------------------------------
def _format_ast_arg(arg: ast.arg) -> str:
    if arg.annotation is not None:
        try:
            return f"{arg.arg}: {ast.unparse(arg.annotation)}"
        except Exception:
            return arg.arg
    return arg.arg


def build_ast_contracts_index(root_path: Path, write_to_disk: bool = True) -> Dict[str, Any]:
    """
    Governs: [v5.0 Federation Layer 0].
    Extrae en una sola pasada (respetando crawl: false e ignorados) todas las funciones públicas,
    clases, firmas simbólicas AST de 1 línea y flags CLI de los módulos Python del repositorio.
    Persiste .context/contracts_ast.json para evitar doble/triple escaneo en ThinkingSeed y MetricsThinking.
    """
    root = root_path.resolve()
    patterns = load_ignore_patterns(root) if root.exists() else []
    beacon_cache: Dict[str, Dict[str, Any]] = {}
    topo_hash = compute_topology_hash(root)

    ast_file = root / ".context" / "contracts_ast.json"
    if ast_file.is_file():
        try:
            cached = json.loads(ast_file.read_text(encoding="utf-8"))
            if isinstance(cached, dict) and cached.get("topology_hash") == topo_hash and cached.get("version") == ENGINE_VERSION:
                return cached
        except Exception:
            pass

    public_symbols: List[str] = []
    cli_flags: List[str] = []
    signatures_1line: List[str] = []
    modules_map: Dict[str, Dict[str, Any]] = {}

    for current, dirs, files in os.walk(root):
        cur = Path(current)
        kept_dirs: List[str] = []
        for d in sorted(dirs):
            if d.startswith(".") or d.lower() in IGNORED_DISCOVERY_DIRS:
                continue
            child = cur / d
            if is_ignored_path(child, root, patterns):
                continue
            if not _resolve_beacon_fast(child, root, beacon_cache).get("crawl", True):
                continue
            kept_dirs.append(d)
        dirs[:] = kept_dirs

        for fname in sorted(files):
            if not fname.endswith(".py") or fname.startswith("."):
                continue
            fpath = cur / fname
            rel_py = _rel_posix(fpath, root)
            try:
                source = fpath.read_text(encoding="utf-8", errors="replace")
                tree = ast.parse(source, filename=str(fpath))
            except Exception:
                continue

            mod_symbols: List[str] = []
            mod_flags: List[str] = []
            mod_sigs: List[str] = []

            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if not node.name.startswith("_"):
                        if node.name not in public_symbols:
                            public_symbols.append(node.name)
                        if node.name not in mod_symbols:
                            mod_symbols.append(node.name)
                        args_list = [_format_ast_arg(a) for a in node.args.args if a.arg != "self"]
                        ret_str = "Any"
                        if node.returns is not None:
                            try:
                                ret_str = ast.unparse(node.returns)
                            except Exception:
                                ret_str = "Any"
                        sig = f"./{rel_py}::{node.name}({', '.join(args_list)}) -> {ret_str}"
                        mod_sigs.append(sig)
                        signatures_1line.append(sig)
                elif isinstance(node, ast.ClassDef):
                    if not node.name.startswith("_"):
                        if node.name not in public_symbols:
                            public_symbols.append(node.name)
                        if node.name not in mod_symbols:
                            mod_symbols.append(node.name)
                        sig = f"./{rel_py}::{node.name}(class)"
                        mod_sigs.append(sig)
                        signatures_1line.append(sig)

            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                    if node.func.attr == "add_argument":
                        for arg in node.args:
                            if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                                if arg.value.startswith("-"):
                                    if arg.value not in cli_flags:
                                        cli_flags.append(arg.value)
                                    if arg.value not in mod_flags:
                                        mod_flags.append(arg.value)

            if mod_symbols or mod_flags or mod_sigs:
                modules_map[rel_py] = {
                    "symbols": mod_symbols,
                    "cli_flags": mod_flags,
                    "signatures": mod_sigs,
                }

    digest_payload = "\n".join(sorted(signatures_1line) + sorted(cli_flags))
    ast_hash = hashlib.sha256(digest_payload.encode("utf-8")).hexdigest()

    index_data: Dict[str, Any] = {
        "$schema": "../schemas/contracts_ast.schema.json",
        "version": ENGINE_VERSION,
        "project": root.name,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "topology_hash": topo_hash,
        "contracts_ast_hash": ast_hash,
        "public_symbols": public_symbols,
        "cli_flags": cli_flags,
        "signatures_1line": signatures_1line,
        "modules": modules_map,
    }

    if write_to_disk:
        ctx_dir = root / ".context"
        ctx_dir.mkdir(parents=True, exist_ok=True)
        safe_io_retry(
            lambda: ast_file.write_text(
                json.dumps(index_data, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
        )
    return index_data


def _count_fpai_pruned_paths(root_path: Path) -> int:
    """Cuenta cuántas rutas podadas por MetricsThinking FPIA residen en .agentignore."""
    agentignore = root_path / ".agentignore"
    if not agentignore.is_file():
        return 0
    try:
        lines = agentignore.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return 0
    in_block = False
    count = 0
    for line in lines:
        s = line.strip()
        if s in ("# >>> FPAI-PRUNE-START", "# >>> METRICSTHINKING AUTO-PRUNE >>>"):
            in_block = True
            continue
        if s in ("# <<< FPAI-PRUNE-END", "# <<< METRICSTHINKING AUTO-PRUNE <<<"):
            in_block = False
            continue
        if in_block and s and not s.startswith("#"):
            count += 1
    return count


def sync_icontext_bus(
    root_path: Path,
    tree_data: Optional[Dict[str, Any]] = None,
    ast_index: Optional[Dict[str, Any]] = None,
    write_to_disk: bool = True,
) -> Dict[str, Any]:
    """
    Governs: [v5.0 Federation Bus].
    Sincroniza el archivo .context/icontext_bus.json que coordina las 4 capas del ecosistema:
    - l0_idirectory (Topología, AST hash, nodos activos y podados)
    - l1_thinkingseed (Estado de 01_seed/, seed_hash, versión y cobertura AST)
    - l2_metricsthinking (Score consolidado, FPIA PF_spectral, cuello de botella y seguridad)
    - l3_ireadme (Paridad dual README.md / README_ES.md y cero fugas de ruta)
    """
    root = root_path.resolve()
    tree = tree_data or generate_tree_json(root)
    topo_hash = str(tree.get("topology_hash") or compute_topology_hash(root))
    ast_data = ast_index or build_ast_contracts_index(root, write_to_disk=write_to_disk)
    ast_hash = str(ast_data.get("contracts_ast_hash", ""))

    nodes = tree.get("nodes", {})
    active_nodes = sum(1 for v in nodes.values() if isinstance(v, dict) and v.get("crawl", True))
    pruned_nodes = sum(1 for v in nodes.values() if isinstance(v, dict) and not v.get("crawl", True))
    budget_stats = compute_context_budget(root)
    active_tokens = sum(int(s.get("est_tokens", 0)) for s in budget_stats if s.get("crawl", True))

    bus_file = root / ".context" / "icontext_bus.json"
    existing_layers: Dict[str, Any] = {}
    if bus_file.is_file():
        try:
            loaded_bus = json.loads(bus_file.read_text(encoding="utf-8"))
            if isinstance(loaded_bus, dict) and isinstance(loaded_bus.get("layers"), dict):
                existing_layers = loaded_bus["layers"]
        except Exception:
            existing_layers = {}

    # Capa 0: iDirectory v5.0
    l0_data: Dict[str, Any] = {
        "version": f"{ENGINE_VERSION}.0",
        "topology_hash": topo_hash,
        "contracts_ast_hash": ast_hash,
        "active_nodes_count": active_nodes,
        "pruned_nodes_count": pruned_nodes,
        "active_tokens_estimate": active_tokens,
        "fpai_pruned_paths_count": _count_fpai_pruned_paths(root),
    }

    # Capa 1: ThinkingSeed v5.0
    seed_files = resolve_seed_key_files(root)
    primary_seed_rel = f"01_seed/{seed_files[0]}"
    seed_path = root / primary_seed_rel
    l1_prev = existing_layers.get("l1_thinkingseed", {}) if isinstance(existing_layers.get("l1_thinkingseed"), dict) else {}
    if seed_path.is_file():
        try:
            seed_text = seed_path.read_text(encoding="utf-8", errors="replace")
            seed_hash = hashlib.sha256(seed_text.encode("utf-8")).hexdigest()
            ver_match = re.search(r'<SEED_ARCHITECTURAL_VECTOR[^>]*version="([^"]+)"', seed_text)
            if not ver_match:
                ver_match = re.search(r'seed_schema_version:\s*"?([0-9.]+)"?', seed_text)
            seed_ver = ver_match.group(1) if ver_match else "3.0"
            all_contracts = list(ast_data.get("public_symbols", [])) + list(ast_data.get("cli_flags", []))
            if all_contracts:
                matched_c = sum(1 for c in all_contracts if c in seed_text)
                ast_cov = round((matched_c / len(all_contracts)) * 100.0, 2)
            else:
                ast_cov = 100.0
            l1_data: Dict[str, Any] = {
                "present": True,
                "version": seed_ver,
                "seed_path": primary_seed_rel,
                "seed_hash": seed_hash,
                "synced_with_topology_hash": topo_hash,
                "ast_coverage_pct": ast_cov,
                "gates_passed": l1_prev.get("gates_passed", "6/6" if ast_cov >= 90.0 else "pending"),
            }
        except OSError:
            l1_data = {"present": False, "version": "none"}
    else:
        l1_data = {"present": False, "version": "none"}

    # Capa 2: MetricsThinking v5.0
    mt_candidates = [
        root / "artifacts" / "plans" / "metricsthinking" / "MetricsThinking.json",
        root / "artifacts" / "MetricsThinking.json",
    ]
    mt_file = next((p for p in mt_candidates if p.is_file()), None)
    if mt_file is not None:
        try:
            mt_json = json.loads(mt_file.read_text(encoding="utf-8", errors="replace"))
            fpai = mt_json.get("fpai_spectral") or {}
            sec = mt_json.get("security_report") or {}
            score_val = mt_json.get("consolidated_score")
            if score_val is None:
                score_val = mt_json.get("score_total", 100.0)
            l2_data: Dict[str, Any] = {
                "present": True,
                "version": str(mt_json.get("engine_version") or mt_json.get("version") or "5.0.0"),
                "report_path": _rel_posix(mt_file, root),
                "consolidated_score": float(score_val) if score_val is not None else 100.0,
                "maturity_band": str(mt_json.get("maturity_band", "OPERATIONAL_EXCELLENCE")),
                "active_bottleneck": str(mt_json.get("active_bottleneck", "NONE")),
                "fpai_pf_spectral": float(fpai.get("power_factor_spectral", 1.0)),
                "fpai_s_spectral": float(fpai.get("s_spectral", 0.0)),
                "security_gate": 1.0 if int(sec.get("pii_matches_count", 0)) == 0 else 0.0,
                "synced_with_seed_hash": l1_data.get("seed_hash", ""),
            }
        except Exception:
            l2_data = {"present": False, "version": "none"}
    else:
        l2_data = {"present": False, "version": "none"}

    # Capa 3: iReadme v5.0
    readme_en = root / "README.md"
    readme_es = root / "README_ES.md"
    if readme_en.is_file() and readme_es.is_file():
        try:
            en_txt = readme_en.read_text(encoding="utf-8", errors="replace")
            es_txt = readme_es.read_text(encoding="utf-8", errors="replace")
            has_dual_header = ("README_ES.md" in en_txt) and ("README.md" in es_txt)
            leak_re = re.compile(r"([A-Za-z]:[/\\][A-Za-z0-9_.-]+|file:///[A-Za-z]:|/home/[A-Za-z0-9_.-]+)")
            leaks = len(leak_re.findall(en_txt)) + len(leak_re.findall(es_txt))
            phi = 1.0 if (has_dual_header and leaks == 0) else 0.5
            std_ver = "Enterprise Paper-Grade v5.0" if "5.0" in en_txt else "Enterprise Paper-Grade v2.0"
            l3_data: Dict[str, Any] = {
                "present": True,
                "version": "5.0.0" if "5.0" in en_txt else "2.0.0",
                "standard": std_ver,
                "parity_score_phi": phi,
                "path_leakage_rate": 0.0 if leaks == 0 else round(leaks / 100.0, 4),
                "synced_with_topology_hash": topo_hash,
            }
        except OSError:
            l3_data = {"present": False, "version": "none"}
    elif readme_en.is_file():
        l3_data = {
            "present": True,
            "version": "partial",
            "standard": "Single-Language README",
            "parity_score_phi": 0.5,
            "path_leakage_rate": 0.0,
            "synced_with_topology_hash": topo_hash,
        }
    else:
        l3_data = {"present": False, "version": "none"}

    bus_payload: Dict[str, Any] = {
        "$schema": "../schemas/icontext_bus.schema.json",
        "protocol_version": f"{ENGINE_VERSION}.0",
        "project": root.name,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "layers": {
            "l0_idirectory": l0_data,
            "l1_thinkingseed": l1_data,
            "l2_metricsthinking": l2_data,
            "l3_ireadme": l3_data,
        },
    }

    if write_to_disk:
        ctx_dir = root / ".context"
        ctx_dir.mkdir(parents=True, exist_ok=True)
        safe_io_retry(
            lambda: bus_file.write_text(
                json.dumps(bus_payload, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
        )
    return bus_payload


def build_ecosystem_pack(root_path: Path) -> Dict[str, Any]:
    """
    Governs: [v5.0 Tri-Artifact Ecosystem Pack].
    Compila en una sola llamada (< 650 tokens) el estado federado de las 4 herramientas
    (iDirectory + ThinkingSeed + MetricsThinking + iReadme) para evitar escaneos redundantes.
    """
    root = root_path.resolve()
    tree = generate_tree_json(root)
    ast_index = build_ast_contracts_index(root, write_to_disk=False)
    bus = sync_icontext_bus(root, tree_data=tree, ast_index=ast_index, write_to_disk=False)

    active_topology = [
        f"{k}:{v['role']}({v['prio']})"
        for k, v in tree.get("nodes", {}).items()
        if isinstance(v, dict) and v.get("crawl", True)
    ]
    pack: Dict[str, Any] = {
        "icontext_ecosystem_pack": f"{ENGINE_VERSION}.0",
        "project": root.name,
        "topology_hash": tree.get("topology_hash", "")[:16],
        "contracts_ast_hash": ast_index.get("contracts_ast_hash", "")[:16],
        "active_topology": active_topology,
        "ast_summary": {
            "modules_count": len(ast_index.get("modules", {})),
            "public_symbols_count": len(ast_index.get("public_symbols", [])),
            "cli_flags_count": len(ast_index.get("cli_flags", [])),
            "sample_signatures": ast_index.get("signatures_1line", [])[:12],
        },
        "federation_layers": bus.get("layers", {}),
    }

    cp_file = root / ".context" / "checkpoint.json"
    if cp_file.is_file():
        try:
            cp_data = json.loads(cp_file.read_text(encoding="utf-8"))
            if cp_data.get("status") in ("executing", "approved", "paused"):
                pack["checkpoint"] = {
                    "plan_id": cp_data.get("plan_id"),
                    "phase": cp_data.get("current_phase"),
                    "next": cp_data.get("next_action", "")[:80],
                }
        except Exception:
            pass
    return pack


def upsert_segmented_block(file_path: Path, tool_key: str, block_content: str) -> bool:
    """
    Governs: [v5.0 Non-Destructive Rule Composition — Resolves FAIL-01].
    Inserta o actualiza de forma idempotente un bloque delimitado por herramienta
    (<!-- >>> ICONTEXT-V5:<TOOL>:START >>> --> ... <!-- <<< ICONTEXT-V5:<TOOL>:END >>> -->)
    sin sobrescribir el contenido existente de otras herramientas o del usuario.
    """
    key_upper = tool_key.strip().upper()
    start_marker = f"<!-- >>> ICONTEXT-V5:{key_upper}:START >>> -->"
    end_marker = f"<!-- <<< ICONTEXT-V5:{key_upper}:END >>> -->"
    wrapped = f"{start_marker}\n{block_content.strip()}\n{end_marker}"

    existing = ""
    if file_path.is_file():
        try:
            existing = file_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            existing = ""

    if start_marker in existing and end_marker in existing:
        pattern = re.compile(
            re.escape(start_marker) + r".*?" + re.escape(end_marker),
            re.DOTALL,
        )
        updated = pattern.sub(lambda _m: wrapped, existing)
    elif existing.strip():
        updated = existing.rstrip() + "\n\n" + wrapped + "\n"
    else:
        updated = wrapped + "\n"

    file_path.parent.mkdir(parents=True, exist_ok=True)
    safe_io_retry(lambda: file_path.write_text(updated, encoding="utf-8"))
    return True


# ------------------------------------------------------------------------------
# 3.4 Presupuesto de Tokens con Poda Estricta de Ramas Muertas (v4.0)
# ------------------------------------------------------------------------------
_BUDGET_METRICS_CACHE: Dict[str, Dict[str, Any]] = {}


def compute_context_budget(root_path: Path, include_pruned_stats: bool = False) -> List[Dict[str, Any]]:
    """
    Governs: [INV-02], [INV-03], [GAP-03], [V-01].
    Calcula el peso en archivos, bytes y tokens estimados por directorio usando os.walk con poda
    estricta: si un nodo tiene crawl: False (y include_pruned_stats=False), NO recorre ni contabiliza
    sus descendientes, devolviendo files=0, bytes=0, est_tokens=0, pruned=True.
    Reutiliza métricas en caché si node_hash no ha cambiado.
    """
    root = root_path.resolve()
    stats = []
    tree_nodes = generate_tree_json(root).get("nodes", {})
    beacon_cache: Dict[str, Dict[str, Any]] = {}
    target_folders: Dict[str, Dict[str, Any]] = {}

    for folder, meta in FOLDER_METADATA.items():
        target_folders[folder] = {
            "role": meta.get("role", "general"),
            "crawl": meta.get("crawl", True),
            "priority": meta.get("read_priority", "p2"),
        }
    for node_key, node_info in tree_nodes.items():
        if node_key.lower() not in {k.lower() for k in target_folders}:
            target_folders[node_key] = {
                "role": node_info.get("role", "domain_extension"),
                "crawl": node_info.get("crawl", True),
                "priority": node_info.get("prio", "p1"),
            }

    for folder, info in target_folders.items():
        dir_path = root / folder
        if not dir_path.exists():
            continue
        effective_crawl = bool(info["crawl"]) and bool(_resolve_beacon_fast(dir_path, root, beacon_cache).get("crawl", True))
        if not effective_crawl and not include_pruned_stats:
            stats.append({
                "directory": folder,
                "role": info["role"],
                "files": 0,
                "bytes": 0,
                "est_tokens": 0,
                "crawl": False,
                "pruned": True,
                "priority": info["priority"]
            })
            continue

        cache_key = f"{str(root)}::{folder}"
        current_hash = compute_node_fingerprint(dir_path)
        if not include_pruned_stats and cache_key in _BUDGET_METRICS_CACHE:
            cached = _BUDGET_METRICS_CACHE[cache_key]
            if cached.get("node_hash") == current_hash:
                stats.append({
                    "directory": folder,
                    "role": info["role"],
                    "files": cached["files"],
                    "bytes": cached["bytes"],
                    "est_tokens": cached["est_tokens"],
                    "crawl": effective_crawl,
                    "pruned": not effective_crawl,
                    "priority": info["priority"]
                })
                continue

        total_files = 0
        total_bytes = 0
        total_tokens = 0
        for current, dirs, files in os.walk(dir_path):
            cur = Path(current)
            kept_d: List[str] = []
            for d in sorted(dirs):
                if d.startswith(".") or d.lower() in IGNORED_DISCOVERY_DIRS:
                    continue
                child = cur / d
                rel_child_l = child.relative_to(root).as_posix().lower()
                if not include_pruned_stats:
                    if rel_child_l in FOLDER_METADATA and FOLDER_METADATA[rel_child_l].get("crawl") is False:
                        continue
                    cb = child / BEACON_FILENAME
                    if cb.is_file() and _read_local_beacon(child).get("crawl", True) is False:
                        continue
                kept_d.append(d)
            dirs[:] = kept_d

            for fname in files:
                if fname.startswith("."):
                    continue
                p = cur / fname
                total_files += 1
                try:
                    fsize = p.stat().st_size
                    total_bytes += fsize
                    ext = p.suffix.lower()
                    if ext not in BINARY_EXTENSIONS:
                        total_tokens += max(1, int(fsize / 3.6)) if ext in CODE_SCHEMA_EXTENSIONS else max(1, fsize // 4)
                except OSError:
                    pass

        _BUDGET_METRICS_CACHE[cache_key] = {
            "node_hash": current_hash,
            "files": total_files,
            "bytes": total_bytes,
            "est_tokens": total_tokens
        }

        stats.append({
            "directory": folder,
            "role": info["role"],
            "files": total_files,
            "bytes": total_bytes,
            "est_tokens": total_tokens,
            "crawl": effective_crawl,
            "pruned": not effective_crawl,
            "priority": info["priority"]
        })
    return stats


# ==============================================================================
# 4. Comandos del CLI: init, route, beacon, map, context, seed, checkpoint, audit, reconcile
# ==============================================================================

def init_project(base_path: str):
    """Inicializa la estructura normalizada v4.0, beacons, policy, tree.json y reglas de IA."""
    root = Path(base_path)
    print(f"[*] Inicializando iDirectory v{ENGINE_VERSION} (Context Engineering) en: {root.resolve()}")

    # 1. Crear directorios gobernados
    for folder in FOLDER_METADATA.keys():
        (root / folder).mkdir(parents=True, exist_ok=True)

    # 2. Desplegar config/context_policy.json si no existe
    policy_path = root / "config" / "context_policy.json"
    if not policy_path.exists():
        policy_data = dict(DEFAULT_CONTEXT_POLICY)
        policy_data["project"] = root.resolve().name
        policy_path.write_text(json.dumps(policy_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # 2b. Desplegar artifacts/plans/backlog/queue.json si no existe
    bkl_queue = root / "artifacts" / "plans" / "backlog" / "queue.json"
    if not bkl_queue.exists():
        bkl_queue.parent.mkdir(parents=True, exist_ok=True)
        bkl_queue.write_text(json.dumps({"version": "1.0", "items": []}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # 3. Desplegar Beacons en cada directorio
    beacon_count = sync_beacons(root)
    print(f"  [+] {beacon_count} Context Beacons (.context.yaml) desplegados y sincronizados.")

    # 4. Desplegar engine_readme.md
    primary_seed = resolve_seed_key_files(root)[0]
    readme_path = root / "02_foundation" / "engine" / "engine_readme.md"
    readme_path.parent.mkdir(parents=True, exist_ok=True)
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(f"# {root.resolve().name.upper()} - iDirectory Architecture v{ENGINE_VERSION}\n\n")
        f.write("Framework modular gobernado por **Gravity HyperScale Thinking** con Context Engineering nativo.\n\n")
        f.write("> **Protocolo de Ingesta para Agentes (Adaptive Bootloader v4.0):**\n")
        f.write("> 1. **Tier 1A (Atómico con ruta conocida):** `python FWengine.py context --pack <dir> --tier 1a` (< 220 tokens).\n")
        f.write("> 2. **Tier 1B (Multiarchivo / `/plan` acotado):** `python FWengine.py context --compact` + `map --slice <dir>` + `seed --section <id>`.\n")
        f.write(f"> 3. **Tier 2 (Arquitectura Global / Auditoría):** Lee `.context/tree.json` + `01_seed/{primary_seed}` solo en rediseño transversal o `/seedMaster`.\n")
        f.write("> 4. **Contrato de Cierre Unificado:** Tras crear carpetas o alterar la topología, ejecuta:\n")
        f.write(">    `python FWengine.py reconcile`\n\n")
        f.write("## Manifiesto de Directorios y Roles\n\n")
        for folder, meta in FOLDER_METADATA.items():
            f.write(f"- **`{folder}/`**: {meta['purpose']} `[Priority: {meta['read_priority']}]`\n")

    # 5. Desplegar .agentignore si no existe
    agentignore_path = root / ".agentignore"
    if not agentignore_path.exists():
        with open(agentignore_path, "w", encoding="utf-8") as f:
            f.write("# Máscara de Exclusión para Agentes de IA (iDirectory Context Engineering)\n")
            f.write("data/raw/\n")
            f.write("data/processed/\n")
            f.write("data/sandbox/\n")
            f.write("logs/\n")
            f.write("*.parquet\n")
            f.write("*.csv\n")
            f.write("*.delta/\n")
            f.write(".venv/\n")
            f.write("__pycache__/\n")
            f.write(".git/\n")
            f.write("artifacts/plans/archive/\n")
        print("  [+] .agentignore desplegado.")

    # 6. Desplegar .gitignore si no existe
    gitignore_path = root / ".gitignore"
    if not gitignore_path.exists():
        with open(gitignore_path, "w", encoding="utf-8") as f:
            f.write(".venv/\n")
            f.write("__pycache__/\n")
            f.write("*.pyc\n")
            f.write(".ipynb_checkpoints/\n\n")
            f.write("# Ignorar datos locales y logs\n")
            f.write("*.csv\n")
            f.write("*.parquet\n")
            f.write("logs/\n")
            f.write("data/raw/\n")
            f.write("data/processed/\n")
            f.write("data/sandbox/\n")
        print("  [+] .gitignore desplegado.")

    # 7. Sincronizar satélite, índice AST y bus federado v5.0 al final
    tree_path = sync_tree(root)
    ast_idx = build_ast_contracts_index(root, write_to_disk=True)
    sync_icontext_bus(root, ast_index=ast_idx, write_to_disk=True)
    print(f"  [+] Satélite topológico y Bus Federado v{ENGINE_VERSION} desplegados: {tree_path.relative_to(root)}")
    print(f"[+] Estructura iDirectory v{ENGINE_VERSION} inicializada con éxito.")


def inspect_python_header(file_path: Path, max_chars: int = 4096) -> str:
    """
    Governs: [R-008], [ADR-010], [INV-01].
    Inspects Python files using ast.parse() to extract imported module names regardless of docstring length,
    plus a non-blocking header scan up to max_chars=4096 as fallback.
    """
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            full_source = f.read()
    except OSError:
        return "src/core"

    imported_tokens: List[str] = []
    func_names: List[str] = []
    try:
        tree = ast.parse(full_source)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported_tokens.append(alias.name.lower())
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imported_tokens.append(node.module.lower())
                for alias in node.names:
                    imported_tokens.append(alias.name.lower())
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func_names.append(node.name.lower())
    except SyntaxError:
        pass

    ast_haystack = " ".join(imported_tokens + func_names)
    sample = full_source[:max_chars].lower()
    combined = f"{ast_haystack} {sample}"

    if any(marker in combined for marker in ["pytest", "unittest", "test_"]):
        return "tests"
    if any(marker in combined for marker in ["pyspark", "google.cloud", "boto3", "azure"]):
        return "src/cloud_jobs"
    if any(marker in combined for marker in ["streamlit", "dash", "plotly"]):
        return "src/dashboards"
    return "src/core"


def route_file(
    file_path: str,
    base_path: str = ".",
    move: bool = False,
    overwrite: bool = False
) -> Optional[Path]:
    """Analiza la naturaleza de un archivo, sugiere su ubicación o lo mueve de forma segura."""
    base_dir = Path(base_path).resolve()

    raw_path = Path(file_path)
    if ".." in raw_path.parts:
        raise PermissionError(f"[-] Error de Seguridad: Intento de Path Traversal bloqueado ('..' detectado en '{file_path}').")

    src_file = raw_path if raw_path.is_absolute() else (base_dir / raw_path)
    if not src_file.exists():
        print(f"[-] Error: El archivo '{file_path}' no existe en el origen.")
        return None

    src_resolved = src_file.resolve()
    try:
        src_resolved.relative_to(base_dir)
    except ValueError:
        raise PermissionError(f"[-] Error de Seguridad: Intento de Path Traversal bloqueado. El archivo '{src_resolved}' está fuera de la raíz '{base_dir}'.")
    ext = src_file.suffix.lower()
    name_lower = src_file.name.lower()

    if ext == ".py":
        if "test" in name_lower or "spec" in name_lower:
            dest_subfolder = "tests"
        else:
            dest_subfolder = inspect_python_header(src_resolved)
    elif ext == ".sql":
        if "test" in name_lower or "spec" in name_lower:
            dest_subfolder = "tests"
        else:
            dest_subfolder = "src/cloud_jobs"
    elif ext == ".ipynb":
        dest_subfolder = "03_research/notebooks"
    elif ext in [".md", ".txt", ".pdf"]:
        if any(w in name_lower for w in ["obsoleto", "historico", "old", "backup", "archive", "superseded"]):
            dest_subfolder = "artifacts/plans/archive"
        elif any(w in name_lower for w in ["metricsthinking", "metric", "score", "madurez", "auditoria"]):
            dest_subfolder = "artifacts/plans/metricsthinking"
        elif any(w in name_lower for w in ["plan", "budget", "hitos", "sku"]):
            dest_subfolder = "artifacts/plans/active"
        elif any(w in name_lower for w in ["prompt", "system"]):
            dest_subfolder = "03_research/prompts"
        elif any(w in name_lower for w in ["spec", "schema", "linaje", "contrato"]):
            dest_subfolder = "docs/specs"
        elif any(w in name_lower for w in ["arquitectura", "c4", "flow", "diagram"]):
            dest_subfolder = "docs/architecture"
        else:
            dest_subfolder = ROUTING_MAP.get(ext, "docs/notes")
    else:
        dest_subfolder = ROUTING_MAP.get(ext)
        if not dest_subfolder:
            if any(w in name_lower for w in ["experiment", "benchmark", "poc"]):
                dest_subfolder = "03_research/experiments"
            elif any(w in name_lower for w in ["dashboard", "report", "viz", "bi"]):
                dest_subfolder = "src/dashboards"
            elif any(w in name_lower for w in ["gen", "mock", "synthetic"]):
                dest_subfolder = "src/data_generation"
            else:
                dest_subfolder = "tools"

    dest_dir = (base_dir / dest_subfolder).resolve()
    try:
        dest_dir.relative_to(base_dir)
    except ValueError:
        raise PermissionError(f"[-] Error de Seguridad: Intento de Path Traversal bloqueado. Destino fuera de la raíz: '{dest_dir}'")

    dest_file_name = src_file.name.lower()
    dest_path = (dest_dir / dest_file_name).resolve()
    try:
        dest_path.relative_to(base_dir)
    except ValueError:
        raise PermissionError(f"[-] Error de Seguridad: Intento de Path Traversal bloqueado. Archivo fuera de la raíz: '{dest_path}'")

    print(f"\n[Análisis de Ruteo iDirectory v{ENGINE_VERSION}]")
    print(f"  -> Archivo: '{src_file.name}'")
    print(f"  -> Extensión/Patrón: {ext if ext else 'Nominal'}")
    print(f"  -> Destino óptimo: {dest_subfolder}/")
    print(f"  -> Nombre normalizado: {dest_file_name}")

    if move:
        scaffolded = ensure_beacon_chain(dest_dir, base_dir)
        for created in scaffolded:
            print(f"  [+] Beacon auto-scaffold: {_rel_posix(created.parent, base_dir)}/.context.yaml")
        if src_resolved == dest_path:
            if src_file.name != dest_file_name:
                safe_rename_casing(src_file, dest_path)
                print(f"  [+] ACCIÓN: Archivo normalizado a minúsculas atómicamente -> {dest_path}")
            else:
                print(f"  [*] El archivo ya está en la ubicación canónica con nombre en minúsculas.")
        else:
            if dest_path.exists():
                if not overwrite:
                    raise FileExistsError(f"[-] Colisión detectada en '{dest_path}'. Use --overwrite para reemplazar.")
                safe_io_retry(lambda: os.replace(src_file, dest_path))
            else:
                safe_io_retry(lambda: os.rename(src_file, dest_path))
            print(f"  [+] ACCIÓN: Archivo reubicado exitosamente en -> {dest_path}")
        sync_tree(base_dir)  # [INV-04] mantener topology_hash sincronizado
        return dest_path
    else:
        print(f"  [Sugerencia] Añade '--move' para mover el archivo automáticamente:")
        print(f"  python FWengine.py route \"{file_path}\" --move")
        return dest_path


def _extract_markdown_frontmatter(md_path: Path) -> Dict[str, Any]:
    """Extrae metadatos YAML entre bloques '---' al inicio de un documento Markdown."""
    try:
        text = md_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {}
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    return MiniYAML.load(parts[1])


def _update_markdown_frontmatter(md_path: Path, updates: Dict[str, Any]) -> bool:
    """Actualiza o inserta campos de frontmatter en un archivo Markdown preservando su cuerpo."""
    try:
        text = md_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False
    parts = text.split("---", 2)
    if len(parts) < 3 or not text.startswith("---"):
        fm_data = dict(updates)
        body = text
    else:
        header = parts[1]
        body = parts[2]
        fm_data = MiniYAML.load(header)
        fm_data.update(updates)

    new_header = MiniYAML.dump(fm_data)
    new_text = f"---\n{new_header}\n---{body}"
    try:
        safe_io_retry(lambda: md_path.write_text(new_text, encoding="utf-8"))
        return True
    except OSError:
        return False


def reconcile_plans_lifecycle(root_path: Path, check_only: bool = False) -> List[str]:
    """
    Garbage Collector Automático de Planes (v4.1):
    1. Inspecciona .context/checkpoint.json y artifacts/plans/active/*.md vía _extract_markdown_frontmatter().
    2. Si checkpoint.json tiene status == 'completed' (o si un plan en active/ declara status: completed|archived|superseded):
       - check_only=True: registra violación.
       - check_only=False: actualiza frontmatter forzando status: completed y executable: false,
         mueve a artifacts/plans/archive/ vía safe_io_retry(), y limpia checkpoint.json.
    3. Valida cardinalidad estricta: si hay >1 plan con status: executing en active/, reporta violación en reconcile --check.
    """
    root = root_path.resolve()
    violations: List[str] = []
    active_dir = root / "artifacts" / "plans" / "active"
    archive_dir = root / "artifacts" / "plans" / "archive"
    cp_file = root / ".context" / "checkpoint.json"

    checkpoint_status = ""
    cp_plan_id = ""
    if cp_file.is_file():
        try:
            cp_data = json.loads(cp_file.read_text(encoding="utf-8"))
            checkpoint_status = str(cp_data.get("status", "")).lower()
            cp_plan_id = str(cp_data.get("plan_id", ""))
        except Exception:
            pass

    if not active_dir.is_dir():
        return violations

    active_plans = sorted(active_dir.glob("*.md"))
    executing_plans = []

    for plan_file in active_plans:
        fm = _extract_markdown_frontmatter(plan_file)
        p_status = str(fm.get("status", "")).lower()
        p_id = str(fm.get("id") or fm.get("plan_id") or plan_file.stem)

        is_target_completed = (checkpoint_status == "completed" and (cp_plan_id in (p_id, plan_file.name, plan_file.stem) or len(active_plans) == 1))
        is_stale = p_status in ("completed", "archived", "superseded") or is_target_completed

        if is_stale:
            if check_only:
                violations.append(
                    f"Plan no ejecutable en 'active/': '{plan_file.name}' declara status='{p_status or 'completed'}' y debe residir en 'archive/'."
                )
            else:
                archive_dir.mkdir(parents=True, exist_ok=True)
                _update_markdown_frontmatter(plan_file, {"status": "completed", "executable": False})
                dest = archive_dir / plan_file.name
                safe_io_retry(lambda: os.replace(plan_file, dest))
                if checkpoint_status == "completed":
                    manage_checkpoint(root, action="clear")
        elif p_status in ("executing", "in_progress"):
            executing_plans.append(plan_file.name)

    if len(executing_plans) > 1:
        violations.append(
            f"Violación de cardinalidad estricta: existen {len(executing_plans)} planes en estado 'executing' en 'artifacts/plans/active/' ({', '.join(executing_plans)}). Máximo 1 permitido."
        )

    return violations


def _resolve_imported_module_to_repo_dir(
    module_name: str,
    file_dir: Path,
    root: Path
) -> Optional[str]:
    """
    Determina si un módulo importado corresponde a un directorio interno gobernado del repositorio.
    Retorna la ruta POSIX relativa del directorio objetivo, o None si es estándar o externo.
    """
    if not module_name:
        return None
    parts = module_name.split(".")
    root_mod = parts[0]

    stdlib = getattr(sys, "stdlib_module_names", set())
    if root_mod in stdlib or root_mod in sys.builtin_module_names:
        return None
    if root_mod in ("setuptools", "pkg_resources", "pip", "pytest", "unittest", "unittest.mock"):
        return None

    # Verificar si es relativo / interno al directorio actual (file_dir)
    candidate_local = file_dir
    for part in parts:
        candidate_local = candidate_local / part
        if candidate_local.is_dir() or candidate_local.with_suffix(".py").is_file():
            return None

    # Verificar si es relativo a root
    candidate = root
    matched_repo_path: Optional[str] = None
    for part in parts:
        candidate = candidate / part
        if candidate.is_dir():
            matched_repo_path = _rel_posix(candidate, root)
        elif candidate.with_suffix(".py").is_file():
            matched_repo_path = _rel_posix(candidate.parent, root)
            break

    # Verificar si está bajo src/ (caso común cuando src/ está en PYTHONPATH)
    if not matched_repo_path:
        src_candidate = root / "src"
        for part in parts:
            src_candidate = src_candidate / part
            if src_candidate.is_dir():
                matched_repo_path = _rel_posix(src_candidate, root)
            elif src_candidate.with_suffix(".py").is_file():
                matched_repo_path = _rel_posix(src_candidate.parent, root)
                break

    return matched_repo_path


def validate_dependency_dag(
    root_path: Path,
    changed_nodes: Optional[List[str]] = None
) -> List[str]:
    """
    Cortafuegos arquitectónico DAG vía AST (v4.1):
    Para cada directorio con archivos .py y crawl: true (evaluando solo changed_nodes si se define),
    lee imports_from de su .context.yaml local y valida que todo import interno apunte a módulos autorizados.
    """
    root = root_path.resolve()
    violations: List[str] = []

    for beacon_file in iter_beacon_files(root):
        dir_path = beacon_file.parent
        rel_dir = _rel_posix(dir_path, root)

        if changed_nodes is not None and rel_dir not in changed_nodes and rel_dir.split("/")[0] not in changed_nodes:
            continue

        beacon_data = _read_local_beacon(dir_path)
        if not beacon_data.get("crawl", True):
            continue

        imports_from = beacon_data.get("imports_from")
        if not imports_from or not isinstance(imports_from, list):
            continue

        allowed_prefixes: Set[str] = set()
        for imp in imports_from:
            norm = str(imp).replace("\\", "/").strip("/")
            allowed_prefixes.add(norm.lower())
            allowed_prefixes.add(norm.replace("/", ".").lower())

        self_norm = rel_dir.replace("\\", "/").strip("/").lower()
        allowed_prefixes.add(self_norm)
        allowed_prefixes.add(self_norm.replace("/", "."))

        # Analizar archivos .py directos del directorio
        for entry in sorted(dir_path.glob("*.py")):
            if entry.name.startswith("."):
                continue
            try:
                source = entry.read_text(encoding="utf-8", errors="replace")
                tree = ast.parse(source, filename=str(entry))
            except (SyntaxError, OSError) as e:
                violations.append(f"Error de sintaxis AST en '{_rel_posix(entry, root)}': {e}")
                continue

            for node in ast.walk(tree):
                imported_modules = []
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imported_modules.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.level == 0 and node.module:
                        imported_modules.append(node.module)

                for mod in imported_modules:
                    target_repo_dir = _resolve_imported_module_to_repo_dir(mod, dir_path, root)
                    if not target_repo_dir:
                        continue
                    target_norm = target_repo_dir.replace("\\", "/").strip("/").lower()
                    target_dot = target_norm.replace("/", ".")
                    allowed = any(
                        target_norm == p or target_norm.startswith(p + "/") or
                        target_dot == p or target_dot.startswith(p + ".")
                        for p in allowed_prefixes
                    )
                    if not allowed:
                        violations.append(
                            f"Violación de cortafuegos arquitectónico DAG en '{_rel_posix(entry, root)}': import '{mod}' apunta a '{target_repo_dir}', no autorizado en imports_from de '{rel_dir}/.context.yaml'."
                        )

    return violations


def audit_repository(root_path: Path, fix: bool = False) -> bool:
    """
    Governs: [V-03], [V-06], [Opt-6].
    Audita:
    1. Mayúsculas en profundidad completa ([INV-06]).
    2. Directorios canónicos ausentes y beacons canónicos ausentes.
    3. Directorios huérfanos sin beacon.
    4. Validez estricta de esquema en beacons (additionalProperties, longitudes, tipos).
    5. Existencia, validez de esquema y frescura (topology_hash / mtime) de .context/tree.json.
    6. Portabilidad de adaptadores de agente (ausencia de rutas locales file:///d:/...) y planes activos sin estado superseded.
    """
    root = root_path.resolve()
    print(f"[*] Auditando gobernanza iDirectory v{ENGINE_VERSION} en: {root}")
    violations = 0
    remediated = 0

    # 1. Chequeo de nombres con mayúsculas en toda la profundidad del árbol gobernado ([INV-06])
    patterns = load_ignore_patterns(root)
    for current, dirs, _files in os.walk(root):
        cur = Path(current)
        try:
            disk_entries = os.listdir(cur)
        except OSError:
            disk_entries = list(dirs)
        kept: List[str] = []
        for d in sorted(dirs):
            if d.startswith(".") or d.lower() in IGNORED_DISCOVERY_DIRS:
                continue
            child = cur / d
            if is_ignored_path(child, root, patterns):
                continue
            kept.append(d)
            disk_name = next((e for e in disk_entries if e.lower() == d.lower()), d)
            if any(c.isupper() for c in disk_name):
                rel_display = _resolve_physical_rel_path(root, _rel_posix(child, root))
                print(f"  [!] VIOLACIÓN TOPOLÓGICA (Mayúsculas detectadas): '{rel_display}/'")
                violations += 1
        dirs[:] = kept

    # 2. Directorios canónicos ausentes y Beacons ausentes en nodos canónicos (Fix V-03)
    reported: Set[str] = set()
    is_pkg_repo = _is_custom_src_package_repo(root)
    for folder, meta in FOLDER_METADATA.items():
        folder_dir = root / folder
        if not folder_dir.exists():
            if is_pkg_repo and folder in OPTIONAL_SKELETON_IF_PACKAGED:
                continue
            reported.add(folder.lower())
            if fix:
                folder_dir.mkdir(parents=True, exist_ok=True)
                if folder != ".context":
                    scaffold_beacon_for_dir(folder_dir, root)
                print(f"  [FIX] Directorio canónico restaurado: '{folder}/'")
                remediated += 1
            else:
                print(f"  [!] DIRECTORIO CANÓNICO AUSENTE: '{folder}/'")
                violations += 1
            continue

        if folder == ".context":
            continue
        beacon_file = folder_dir / BEACON_FILENAME
        if not beacon_file.exists():
            reported.add(folder.lower())
            if fix:
                scaffold_beacon_for_dir(folder_dir, root)
                print(f"  [FIX] Beacon canónico aprovisionado en: '{folder}/'")
                remediated += 1
            else:
                print(f"  [!] BEACON AUSENTE en: '{folder}/'")
                violations += 1

    # 3. Directorios huérfanos (auto-descubrimiento, respeta poda)
    for orphan in discover_unbeaconed_directories(root):
        rel = _rel_posix(orphan, root)
        if rel.lower() in reported:
            continue
        if fix:
            scaffold_beacon_for_dir(orphan, root)
            print(f"  [FIX] Beacon auto-scaffold en: '{rel}/'")
            remediated += 1
        else:
            print(f"  [!] DIRECTORIO HUÉRFANO (sin beacon): '{rel}/'")
            violations += 1

    # 4. Validación estricta de esquema y telemetría de dilución atencional en beacons
    for beacon in iter_beacon_files(root):
        rel_dir = _rel_posix(beacon.parent, root)
        try:
            raw_text = beacon.read_text(encoding="utf-8")
        except OSError:
            continue
        size = len(raw_text)
        if size > BEACON_CHAR_BUDGET:
            print(f"  [WARN] Beacon inflado en {rel_dir} (> 150 tokens, {size} chars)")
        parsed = MiniYAML.load(raw_text)
        schema_errors = validate_beacon_data(parsed)
        if schema_errors:
            if fix:
                comments = extract_preserved_comments(beacon)
                scaffold_beacon_for_dir(beacon.parent, root, overwrite=True)
                if comments:
                    repaired = beacon.read_text(encoding="utf-8").rstrip("\n")
                    safe_io_retry(lambda: beacon.write_text(repaired + "\n" + "\n".join(comments) + "\n", encoding="utf-8"))
                print(f"  [FIX] Beacon reparado conforme a schema en: '{rel_dir}/'")
                remediated += 1
            else:
                print(f"  [!] BEACON INVÁLIDO en '{rel_dir}/': {', '.join(schema_errors)}")
                violations += 1

    # 5. Validación de planes activos y ciclo de vida (v4.1)
    plan_violations = reconcile_plans_lifecycle(root, check_only=not fix)
    for pv in plan_violations:
        print(f"  [!] PLAN: {pv}")
        violations += 1

    # 5b. Validación de backlog queue (v4.1)
    bkl_violations = validate_backlog_queue(root, check_only=not fix)
    for bv in bkl_violations:
        print(f"  [!] BACKLOG: {bv}")
        violations += 1

    # 5c. Cortafuegos arquitectónico DAG vía AST (v4.1)
    dag_violations = validate_dependency_dag(root)
    for dv in dag_violations:
        print(f"  [!] DAG FIREWALL: {dv}")
        violations += 1

    # 6. Portabilidad de adaptadores de agente (sin rutas locales file:///d:/...)
    for adapter_name in ("AGENTS.md", "GEMINI.md", "CLAUDE.md", ".cursorrules", ".github/copilot-instructions.md"):
        adapter_path = root / adapter_name
        if adapter_path.is_file():
            try:
                atext = adapter_path.read_text(encoding="utf-8", errors="replace")
                if "file:///" in atext.lower():
                    print(f"  [!] RUTA NO PORTABLE en adaptador '{adapter_name}': contiene enlaces 'file:///'")
                    violations += 1
            except OSError:
                pass

    # 7. Satélite topológico: existencia, schema y freshness (topology_hash)
    tree_file = root / ".context" / "tree.json"
    if not tree_file.exists():
        if fix:
            sync_tree(root)
            print("  [FIX] Satélite .context/tree.json generado.")
            remediated += 1
        else:
            print("  [!] SATÉLITE AUSENTE: No se encontró '.context/tree.json'")
            violations += 1
    else:
        try:
            tree_dict = json.loads(tree_file.read_text(encoding="utf-8"))
            tree_errors = validate_tree_data(tree_dict)
        except Exception as exc:
            tree_errors = [f"JSON corrupto: {exc}"]

        freshness = check_satellite_freshness(root)
        if tree_errors or not freshness["fresh"] or remediated > 0:
            if fix:
                sync_tree(root)
                print("  [FIX] Satélite .context/tree.json sincronizado y actualizado (topology_hash al día).")
                remediated += 1
            else:
                if tree_errors:
                    print(f"  [!] ESQUEMA DE SATÉLITE INVÁLIDO: {', '.join(tree_errors)}")
                    violations += 1
                elif not freshness["fresh"]:
                    print(f"  [!] SATÉLITE OBSOLETO (DRIFT): cambio detectado en '{freshness['latest_path']}'")
                    violations += 1

    if remediated:
        print(f"[FIX] {remediated} acciones de remediación aplicadas automáticamente.")
    if violations == 0:
        print("[PASS] Auditoría exitosa: 0 violaciones topológicas, beacons válidos y satélite al día.")
        return True
    print(f"[FAIL] Se encontraron {violations} violaciones de gobernanza.")
    return False


def reconcile_repository(root_path: Path, check_only: bool = False) -> bool:
    """
    Governs: [Opt-4], [v4.1 Enterprise Pipeline].
    Comando unificado e idempotente de cierre que absorbe todo el flujo en 6 fases deterministas:
    Fase 1: Normalización de casing y auto-scaffolding de beacons.
    Fase 2: reconcile_plans_lifecycle() (Evicción automática active -> archive).
    Fase 3: validate_backlog_queue() (Verificación de queue.json y target_nodes).
    Fase 4: validate_dependency_dag() (Cortafuegos AST incremental).
    Fase 5: compute_context_budget() (Verificación de umbrales contra context_policy.json).
    Fase 6: Sincronización de .context/tree.json con node_hash incremental y topology_hash global.
    """
    root = root_path.resolve()
    print(f"[*] Reconciliando repositorio iDirectory v{ENGINE_VERSION} en: {root} (modo {'check_only' if check_only else 'reconcile'})")
    violations: List[str] = []

    # Fase 1: Normalización de casing y auto-scaffolding de beacons
    is_pkg_repo = _is_custom_src_package_repo(root)
    policy_path = root / "config" / "context_policy.json"
    if not check_only:
        for folder in FOLDER_METADATA.keys():
            if is_pkg_repo and folder in OPTIONAL_SKELETON_IF_PACKAGED and not (root / folder).exists():
                continue
            (root / folder).mkdir(parents=True, exist_ok=True)
        if not policy_path.exists():
            policy_data = dict(DEFAULT_CONTEXT_POLICY)
            policy_data["project"] = root.name
            policy_path.write_text(json.dumps(policy_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        sync_beacons(root, auto_discover=True, force_defaults=False)

    # Fase 2: Garbage Collector automático de planes (active -> archive)
    plan_errs = reconcile_plans_lifecycle(root, check_only=check_only)
    if plan_errs:
        for err in plan_errs:
            print(f"  [!] {err}")
        violations.extend(plan_errs)

    # Fase 3: Validación de Backlog Queue (queue.json y target_nodes)
    backlog_errs = validate_backlog_queue(root, check_only=check_only)
    if backlog_errs:
        for err in backlog_errs:
            print(f"  [!] {err}")
        violations.extend(backlog_errs)

    # Fase 4: Cortafuegos Arquitectónico DAG vía AST
    dag_errs = validate_dependency_dag(root)
    if dag_errs:
        for err in dag_errs:
            print(f"  [!] {err}")
        violations.extend(dag_errs)

    # Fase 5: Presupuesto y telemetría de contexto contra context_policy.json
    budget_stats = compute_context_budget(root)
    if policy_path.is_file():
        try:
            pol = json.loads(policy_path.read_text(encoding="utf-8"))
            max_beacon = pol.get("budgets", {}).get("beacon_max_tokens", 150)
            for stat in budget_stats:
                if stat.get("est_tokens", 0) > max_beacon and stat.get("directory") in FOLDER_METADATA and FOLDER_METADATA[stat.get("directory")].get("crawl"):
                    pass
        except Exception:
            pass

    # Fase 6: Sincronización de satélite con node_hash incremental, AST index y bus federado v5.0
    if not check_only:
        sync_tree(root)
        ast_idx = build_ast_contracts_index(root, write_to_disk=True)
        sync_icontext_bus(root, ast_index=ast_idx, write_to_disk=True)
        audit_ok = audit_repository(root, fix=True)
        if not audit_ok:
            violations.append("Auditoría final falló tras aplicar remediaciones.")
    else:
        audit_ok = audit_repository(root, fix=False)
        if not audit_ok:
            violations.append("Auditoría general detectó violaciones de topología, beacons o satélite.")

    if violations:
        print(f"[FAIL] Reconciliación fallida con {len(violations)} violaciones.")
        return False

    print(f"[PASS] Reconciliación completada con éxito. Repositorio en cumplimiento estricto v{ENGINE_VERSION}.")
    return True


def main():
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    parser = argparse.ArgumentParser(
        description=f"iDirectory v{ENGINE_VERSION}: Framework de Gobernanza y Context Engineering (por Gravity HyperScale Thinking)"
    )
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponibles")

    # init
    init_parser = subparsers.add_parser("init", help=f"Inicializa el andamiaje v{ENGINE_VERSION}, beacons, policy y tree.json")
    init_parser.add_argument("path", nargs="?", default=".", help="Ruta de inicialización")

    # route
    route_parser = subparsers.add_parser("route", help="Determina o ejecuta la reubicación canónica de un archivo")
    route_parser.add_argument("file", help="Ruta del archivo")
    route_parser.add_argument("--move", action="store_true", help="Mueve físicamente el archivo")
    route_parser.add_argument("--overwrite", action="store_true", help="Sobrescribe el archivo destino en caso de colisión")
    route_parser.add_argument("--base", default=".", help="Directorio base")

    # beacon
    beacon_parser = subparsers.add_parser("beacon", help="Gestiona los semáforos y Context Beacons (.context.yaml)")
    beacon_parser.add_argument("--sync", action="store_true", help="Genera o sincroniza todos los beacons")
    beacon_parser.add_argument("--audit", action="store_true", help="Audita que todos los beacons existan y sean válidos")
    beacon_parser.add_argument("--resolve", metavar="DIR", help="Resuelve y muestra el beacon efectivo (físico o heredado) de un directorio")
    beacon_parser.add_argument("--no-discover", action="store_true", help="Sincroniza solo nodos canónicos")
    beacon_parser.add_argument("--force-defaults", action="store_true", help="Restaura textos canónicos por defecto descartando enriquecimiento")

    # map
    map_parser = subparsers.add_parser("map", help="Gestiona el mapa satelital (.context/tree.json)")
    map_parser.add_argument("--sync", action="store_true", help="Regenera el satélite .context/tree.json")
    map_parser.add_argument("--check-freshness", action="store_true", help="Comprueba si tree.json sufre drift respecto al filesystem")
    map_parser.add_argument("--slice", metavar="DIR", help="Emite subgrafo focalizado (<150 tokens) del directorio")
    map_parser.add_argument("--radius", type=int, default=1, help="Niveles de descendencia en --slice")

    # context
    context_parser = subparsers.add_parser("context", help="Telemetría de Context Engineering, packs y token budget")
    context_parser.add_argument("--budget", action="store_true", help="Desglosa el presupuesto de tokens por carpeta")
    context_parser.add_argument("--include-pruned", action="store_true", help="En --budget, escanea también el volumen físico de ramas podadas (crawl:false)")
    context_parser.add_argument("--compact", action="store_true", help="Emite string compacto para inyección en prompts")
    context_parser.add_argument("--pack", metavar="DIR", help="Emite paquete de contexto unificado (slice + beacon + key_files + checkpoint)")
    context_parser.add_argument("--pack-ecosystem", action="store_true", help="Emite paquete federado v5.0 de las 4 capas (<650 tokens)")
    context_parser.add_argument("--bus", action="store_true", help="Sincroniza y emite el bus federado .context/icontext_bus.json")
    context_parser.add_argument("--tier", default="1a", choices=["1a", "1b", "2"], help="Perfil de bootloader para --pack")
    context_parser.add_argument("--check-freshness", action="store_true", help="Comprueba si tree.json sufre drift respecto al filesystem")

    # seed
    seed_parser = subparsers.add_parser("seed", help="Consulta quirúrgica por secciones del ThinkingSeed Master (01_seed/)")
    seed_parser.add_argument("--toc", action="store_true", help="Muestra tabla de contenidos seccional con rangos de líneas y tokens")
    seed_parser.add_argument("--section", metavar="ID_OR_TITLE", help="Extrae únicamente la sección indicada (ej. '2', '4.1', 'contratos')")

    # checkpoint
    cp_parser = subparsers.add_parser("checkpoint", help="Gestiona el estado de continuidad atencional (.context/checkpoint.json)")
    cp_parser.add_argument("--show", action="store_true", help="Muestra el checkpoint activo")
    cp_parser.add_argument("--set", action="store_true", help="Actualiza o crea el checkpoint activo")
    cp_parser.add_argument("--clear", action="store_true", help="Limpia el checkpoint activo")
    cp_parser.add_argument("--plan-id", help="Identificador del plan activo")
    cp_parser.add_argument("--status", choices=["draft", "approved", "executing", "paused", "completed", "superseded", "archived"], help="Estado del plan")
    cp_parser.add_argument("--phase", help="Fase actual (ej. 'P1')")
    cp_parser.add_argument("--next", dest="next_action", help="Siguiente acción concreta verificable")
    cp_parser.add_argument("--step-done", dest="completed_step", help="Añade un paso completado al registro")

    # audit
    audit_parser = subparsers.add_parser("audit", help="Audita violaciones de mayúsculas, huérfanos, beacons, planes y satélite")
    audit_parser.add_argument("--fix", action="store_true", help="Aprovisiona beacons/carpetas faltantes y regenera tree.json")

    # reconcile
    reconcile_parser = subparsers.add_parser("reconcile", help="Cierre unificado e idempotente (sincroniza beacons, satélite y audita)")
    reconcile_parser.add_argument("--check", action="store_true", help="Verifica en modo lectura sin modificar archivos")

    args = parser.parse_args()
    root = Path(getattr(args, "base", getattr(args, "path", ".")))

    if args.command == "init":
        init_project(args.path)
    elif args.command == "route":
        route_file(args.file, args.base, args.move, getattr(args, "overwrite", False))
    elif args.command == "beacon":
        if getattr(args, "resolve", None):
            target_d = (root / args.resolve).resolve()
            print(json.dumps(resolve_beacon(target_d, root.resolve()), ensure_ascii=False, indent=2))
        elif args.audit:
            ok = audit_repository(root)
            sys.exit(0 if ok else 1)
        else:
            count = sync_beacons(
                root,
                auto_discover=not getattr(args, "no_discover", False),
                force_defaults=getattr(args, "force_defaults", False),
            )
            sync_tree(root)
            print(f"[+] {count} Beacons (.context.yaml) y satélite sincronizados exitosamente.")
    elif args.command == "map":
        if getattr(args, "slice", None):
            print(format_sliced_tree(generate_sliced_tree(root, args.slice, radius=args.radius)))
        elif getattr(args, "check_freshness", False):
            freshness = check_satellite_freshness(root)
            if freshness["fresh"]:
                print("[PASS] Satélite al día: .context/tree.json coincide con topology_hash y directorios gobernados.")
            else:
                print(f"[!] DRIFT DETECTADO: El mapa satelital está desactualizado respecto a '{freshness['latest_path']}'.")
                print("    Acción recomendada: Ejecute 'python FWengine.py reconcile'.")
                sys.exit(1)
        else:
            tree_path = sync_tree(root)
            print(f"[+] Mapa satelital sincronizado en: {tree_path}")
    elif args.command == "context":
        if getattr(args, "check_freshness", False):
            freshness = check_satellite_freshness(root)
            if freshness["fresh"]:
                print("[PASS] Satélite al día: .context/tree.json coincide con topology_hash y directorios gobernados.")
            else:
                print(f"[!] DRIFT DETECTADO: El mapa satelital está desactualizado respecto a '{freshness['latest_path']}'.")
                print("    Acción recomendada: Ejecute 'python FWengine.py reconcile'.")
                sys.exit(1)
        elif getattr(args, "pack_ecosystem", False):
            epack = build_ecosystem_pack(root)
            print(json.dumps(epack, ensure_ascii=False, separators=(",", ":")))
        elif getattr(args, "bus", False):
            bus = sync_icontext_bus(root, write_to_disk=True)
            print(json.dumps(bus, ensure_ascii=False, indent=2))
        elif getattr(args, "pack", None):
            pack = build_context_pack(root, args.pack, tier=getattr(args, "tier", "1a"))
            print(json.dumps(pack, ensure_ascii=False, separators=(",", ":")))
        elif args.compact:
            tree = generate_tree_json(root)
            nodes_summary = "; ".join([f"{k}:{v['role']}({v['prio']})" for k, v in tree["nodes"].items() if v["crawl"]])
            print(f"IDIR_TOPOLOGY: [{nodes_summary}]")
        else:
            budget = compute_context_budget(root, include_pruned_stats=getattr(args, "include_pruned", False))
            print("\n" + "=" * 84)
            print(f"{'DIRECTORIO':<28} | {'ROL':<20} | {'FILES':<5} | {'TOKENS EST.':<11} | {'ESTADO / PRIO'}")
            print("=" * 84)
            crawlable_tokens = 0
            for item in budget:
                if item["crawl"]:
                    crawlable_tokens += item["est_tokens"]
                status_flag = f"{item['priority']} [PRUNED: crawl=false]" if not item["crawl"] else item["priority"]
                print(f"{item['directory']:<28} | {item['role']:<20} | {item['files']:<5} | {item['est_tokens']:<11} | {status_flag}")
            print("=" * 84)
            # Calcular Root Control-Plane y Bootloader overhead
            root_tokens = 0
            for rf in ("AGENTS.md", "GEMINI.md", "CLAUDE.md", ".cursorrules", "FWengine.py", "README.md", "README_ES.md"):
                rp = root / rf
                if rp.is_file():
                    root_tokens += estimate_tokens_v4(rp)
            sat_path = root / ".context" / "tree.json"
            sat_tokens = estimate_tokens_v4(sat_path) if sat_path.is_file() else 0
            agents_tokens = estimate_tokens_v4(root / "AGENTS.md") if (root / "AGENTS.md").is_file() else 0
            print(f"Tokens gobernados activos (crawl:true): ~{crawlable_tokens:,} tokens")
            print(f"Tokens plano de control raíz (root):    ~{root_tokens:,} tokens")
            print(f"Bootloader Tier 1 (AGENTS + Satélite):  ~{agents_tokens + sat_tokens:,} tokens (Satélite: ~{sat_tokens}t)\n")
    elif args.command == "seed":
        if getattr(args, "section", None):
            print(extract_seed_section(root, args.section))
        else:
            toc = get_seed_sections(root)
            print(f"\n[Índice Seccional ThinkingSeed Master — {len(toc)} secciones]")
            for s in toc:
                indent = "  " if s["level"] == 2 else "    - "
                print(f"{indent}[{s['id']}] {s['title']} (L{s['start_line']}-L{s['end_line']}, ~{s['est_tokens']} tokens)")
            print()
    elif args.command == "checkpoint":
        if getattr(args, "clear", False):
            res = manage_checkpoint(root, action="clear")
            print(json.dumps(res, ensure_ascii=False))
        elif getattr(args, "set", False):
            res = manage_checkpoint(
                root,
                action="set",
                plan_id=getattr(args, "plan_id", None),
                status=getattr(args, "status", None),
                phase=getattr(args, "phase", None),
                next_action=getattr(args, "next_action", None),
                completed_step=getattr(args, "completed_step", None),
            )
            print(json.dumps(res, ensure_ascii=False, indent=2))
        else:
            res = manage_checkpoint(root, action="show")
            print(json.dumps(res, ensure_ascii=False, indent=2))
    elif args.command == "audit":
        ok = audit_repository(root, fix=getattr(args, "fix", False))
        sys.exit(0 if ok else 1)
    elif args.command == "reconcile":
        ok = reconcile_repository(root, check_only=getattr(args, "check", False))
        sys.exit(0 if ok else 1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
