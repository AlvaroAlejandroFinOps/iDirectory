#!/usr/bin/env python3
"""
iDirectory: Framework de Gobernanza, Ruteo y Context Engineering (v3.0)
Creado por Gravity HyperScale Thinking.

Diseñado para sistemas Multi-Cloud (GCP, AWS, Azure, Fabric), IA, Datos y Analítica.
Implementa:
- Topología unificada en minúsculas (all-lowercase).
- Mapa topológico satelital (.context/tree.json) para descubrimiento en ~250 tokens.
- Semáforos de poda y relevancia de directorio (Context Beacons: .context.yaml).
- Secuencia canónica de ingesta agéntica (Protocolo Bootloader).
- Auto-scaffolding reactivo de beacons (audit --fix, route --move, beacon --sync).
- Subgrafos focalizados de contexto (map --slice <dir>, < 150 tokens).
- Cero dependencias externas (Python Standard Library pura).
"""

import os
import sys
import ast
import json
import time
import errno
import fnmatch
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional, Set, Callable

# ==============================================================================
# 1. MiniYAML: Serializador / Deserializador ligero sin dependencias (PyYAML-free)
# ==============================================================================
class MiniYAML:
    """Parser y emitter minimalista para el subconjunto de YAML usado en .context.yaml."""

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
    def load(yaml_str: str) -> Dict[str, Any]:
        """Parser básico línea por línea para diccionarios y listas simples."""
        result: Dict[str, Any] = {}
        current_list_key = None
        for raw_line in yaml_str.splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("- ") and current_list_key:
                val = line[2:].strip().strip('"\'')
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
                    elif v.startswith('"') and v.endswith('"'):
                        result[k] = v[1:-1]
                    elif v.startswith("'") and v.endswith("'"):
                        result[k] = v[1:-1]
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
# 2. Manifiesto Topológico Canónico v3.0 (All-Lowercase Topology)
# ==============================================================================
IGNORED_DISCOVERY_DIRS: Set[str] = {
    ".git", ".github", ".venv", "venv", "env", "__pycache__",
    ".pytest_cache", ".mypy_cache", ".ruff_cache", "node_modules",
    "target", "dist", "build", ".idea", ".vscode", ".agents", ".context"
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
        "instructions": "LECTURA CONDICIONAL (Tier 2 / Disparadores de Arquitectura). Prohibido precargar en Tier 1."
    },
    "02_foundation/engine": {
        "purpose": "Núcleo del framework de automatización, lógica de ruteo, indexación y governance engine.",
        "role": "core_engine",
        "relevance": "critical",
        "crawl": True,
        "read_priority": "p1",
        "seed_reference": "optional",
        "token_density": "low",
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
        "instructions": "Planes y decisiones vigentes. Consultar antes de modificar infraestructura o presupuestos."
    },
    "artifacts/plans/metricsthinking": {
        "purpose": "Evaluación forense de métricas de avance del proyecto, scores de madurez y roadmap de remediación SDD (MetricsThinking™).",
        "role": "metrics_evaluation",
        "relevance": "critical",
        "crawl": True,
        "read_priority": "p0",
        "seed_reference": "required",
        "token_density": "sparse",
        "key_files": ["MetricsThinking.md", "MetricsThinking.json"],
        "instructions": "LECTURA OBLIGATORIA / PRIORIDAD P0. Contiene la nota global de madurez del proyecto, cuellos de botella inmediatos y roadmap de remediación priorizado."
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
        "purpose": "Parámetros de entorno (dev, staging, prod) y variables de configuración desacopladas.",
        "role": "configuration",
        "relevance": "high",
        "crawl": True,
        "read_priority": "p1",
        "seed_reference": "optional",
        "token_density": "sparse",
        "instructions": "Variables y parámetros. NUNCA colocar claves secretas en texto plano."
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
        "purpose": "Directorio de telemetría, esquemas y mapas satelitales de Context Engineering de iDirectory.",
        "role": "context_engineering",
        "relevance": "critical",
        "crawl": True,
        "read_priority": "p0",
        "seed_reference": "optional",
        "token_density": "sparse",
        "key_files": ["tree.json"],
        "instructions": "Contiene el mapa satelital precargado del repositorio (tree.json)."
    }
}

# Compatibilidad de mapeo simple
FOLDER_MANIFEST = {k: v["purpose"] for k, v in FOLDER_METADATA.items() if k != ".context"}

# Matriz de Ruteo Inteligente (v3.0)
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
# 3. Núcleo de Context Engineering (Beacons, Tree & Budgeting)
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
    beacon_data["token_density"] = meta.get("token_density", "sparse")
    beacon_data["instructions"] = meta.get("instructions", "Directorio estándar.")
    if folder == "01_seed":
        beacon_data["key_files"] = (
            resolve_seed_key_files(root_path)
            if root_path is not None
            else list(meta.get("key_files", []))
        )
    elif "key_files" in meta:
        beacon_data["key_files"] = meta["key_files"]
    if "dependencies" in meta:
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
            for k in ["role", "purpose", "relevance", "read_priority", "seed_reference", "token_density", "instructions"]:
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
    Extracts manual user comment lines (lines starting with '# USER_NOTE:' or trailing comment blocks)
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
# 3.1 Auto-descubrimiento y Auto-Scaffolding de Beacons (v3.2)
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
      - subdominio: hoja bajo un nodo existente; hereda role/seed_reference.
    Prioridad: p3 si crawl heredado es false; p1 para nombres de código; p2 para docs/utilitarios.
    """
    root = root_path.resolve()
    rel = _rel_posix(dir_path, root)
    rel_l = rel.lower()
    name = dir_path.name.lower()
    parent_rel = rel_l.rsplit("/", 1)[0] if "/" in rel_l else ""
    inherited = resolve_beacon(dir_path, root)
    crawl = bool(inherited.get("crawl", True))
    is_namespace = any(k.lower().startswith(rel_l + "/") for k in FOLDER_METADATA)

    if is_namespace:
        role = "namespace"
        purpose = f"Contenedor de subdominios canónicos de {rel}/."
        instructions = "Sin lógica propia. Leer el beacon del subdirectorio objetivo."
    elif "/" not in rel_l:
        role = "domain_extension"
        purpose = f"Dominio no canónico {name} (auto scaffold)."
        instructions = "Extensión de dominio. Enriquecer con /idir enrich."
    else:
        role = inherited.get("role", "general") if inherited.get("inherited") else "general"
        purpose = f"Subdominio {name} de {parent_rel}/ (auto scaffold)."
        source = inherited.get("inherited_from") or parent_rel
        instructions = f"Hereda directivas de {source}/. Enriquecer con /idir enrich."

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

    return {
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


def sync_beacons(root_path: Path, auto_discover: bool = True) -> int:
    """
    Sincroniza los .context.yaml canónicos (preservando comentarios '#') y, si auto_discover=True,
    auto-scaffoldea beacons en directorios huérfanos no ignorados (sin sobrescribir existentes).
    Retorna: nº de beacons canónicos sincronizados + nº de beacons nuevos auto-scaffoldeados.
    """
    count = 0
    for folder, meta in FOLDER_METADATA.items():
        if folder == ".context":
            continue
        dir_path = root_path / folder
        dir_path.mkdir(parents=True, exist_ok=True)
        beacon_file = dir_path / BEACON_FILENAME
        preserved_comments = extract_preserved_comments(beacon_file)
        beacon_content = generate_beacon_content(folder, meta, root_path=root_path)
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


def generate_tree_json(root_path: Path) -> Dict[str, Any]:
    """Genera el mapa satelital compacto de todo el repositorio (~250 tokens)."""
    now_ts = time.time()
    seed_files = resolve_seed_key_files(root_path)
    primary_seed = f"01_seed/{seed_files[0]}"
    tree_data: Dict[str, Any] = {
        "$schema": "../schemas/tree.schema.json",
        "version": "3.0",
        "project": root_path.resolve().name,
        "architecture": "Gravity HyperScale Thinking",
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "timestamp": now_ts,
        "bootloader": {
            "tier_1": [
                "AGENTS.md",
                ".context/tree.json",
                "[target_folder]/.context.yaml"
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

    for folder, meta in FOLDER_METADATA.items():
        physical_key = _resolve_physical_rel_path(root_path, folder)
        node_info: Dict[str, Any] = {
            "role": meta.get("role", "general"),
            "prio": meta.get("read_priority", "p2"),
            "crawl": meta.get("crawl", True),
            "seed_ref": meta.get("seed_reference", "optional")
        }
        if "tier1_preload" in meta:
            node_info["tier1_preload"] = meta["tier1_preload"]
        if folder == "01_seed":
            node_info["key_files"] = seed_files
        elif "key_files" in meta:
            node_info["key_files"] = meta["key_files"]
        tree_data["nodes"][physical_key] = node_info

    # Auto-discover non-canonical first-level domain directories
    if root_path.exists() and root_path.is_dir():
        try:
            disk_entries = sorted(os.listdir(root_path))
        except OSError:
            disk_entries = []
        for entry in disk_entries:
            if entry.startswith(".") or entry.lower() in IGNORED_DISCOVERY_DIRS:
                continue
            if entry.lower() in canonical_top_levels:
                continue
            full_entry = root_path / entry
            if full_entry.is_dir():
                tree_data["nodes"][entry] = {
                    "role": "domain_extension",
                    "prio": "p1",
                    "crawl": True,
                    "seed_ref": "optional"
                }

    return tree_data


def check_satellite_freshness(root_path: Path) -> Dict[str, Any]:
    """Verifica si .context/tree.json está al día respecto a los cambios en carpetas clave."""
    tree_file = root_path / ".context" / "tree.json"
    if not tree_file.exists():
        return {
            "fresh": False,
            "drift_detected": True,
            "satellite_time": 0.0,
            "latest_mtime": 0.0,
            "latest_path": None,
            "reason": "El archivo .context/tree.json no existe. Ejecute 'python FWengine.py map --sync'."
        }

    try:
        with open(tree_file, "r", encoding="utf-8") as f:
            tree_data = json.load(f)
        satellite_time = float(tree_data.get("timestamp", tree_file.stat().st_mtime))
    except Exception:
        satellite_time = tree_file.stat().st_mtime

    key_folders = [
        "01_seed", "02_foundation", "03_research", "src", "config",
        "schemas", "tests", "docs", "tools", "scripts"
    ]

    latest_mtime = 0.0
    latest_path = None

    for kf in key_folders:
        dir_path = root_path / kf
        if not dir_path.exists():
            continue
        d_mtime = dir_path.stat().st_mtime
        if d_mtime > latest_mtime:
            latest_mtime = d_mtime
            latest_path = dir_path
        for item in dir_path.rglob("*"):
            if item.is_file() and not item.name.startswith(".") and "__pycache__" not in item.parts:
                try:
                    m = item.stat().st_mtime
                    if m > latest_mtime:
                        latest_mtime = m
                        latest_path = item
                except OSError:
                    pass

    drift = latest_mtime > (satellite_time + 1.0)
    rel_path_str = str(latest_path.relative_to(root_path)).replace("\\", "/") if latest_path else "desconocido"
    return {
        "fresh": not drift,
        "drift_detected": drift,
        "satellite_time": satellite_time,
        "latest_mtime": latest_mtime,
        "latest_path": rel_path_str
    }



def format_compact_tree_json(data: Dict[str, Any]) -> str:
    """
    Governs: [R-005], [ADR-009], [INV-07].
    Serializes tree.json with one compact JSON line per node in 'nodes', keeping total size < 500 tokens.
    """
    lines: List[str] = ["{"]
    top_keys = [k for k in data.keys() if k != "nodes"]
    for k in top_keys:
        val_str = json.dumps(data[k], ensure_ascii=False, separators=(", ", ": "))
        lines.append(f'  "{k}": {val_str},')
    lines.append('  "nodes": {')
    node_items = list(data.get("nodes", {}).items())
    for idx, (node_key, node_val) in enumerate(node_items):
        comma = "," if idx < len(node_items) - 1 else ""
        compact_node = json.dumps(node_val, ensure_ascii=False, separators=(", ", ": "))
        lines.append(f'    {json.dumps(node_key, ensure_ascii=False)}: {compact_node}{comma}')
    lines.append("  }")
    lines.append("}")
    return "\n".join(lines) + "\n"


def sync_tree(root_path: Path) -> Path:
    """
    Governs: [R-005], [R-006], [INV-04], [INV-07].
    Writes .context/tree.json using format_compact_tree_json() to guarantee < 600 tokens.
    """
    context_dir = root_path / ".context"
    context_dir.mkdir(parents=True, exist_ok=True)
    tree_file = context_dir / "tree.json"
    data = generate_tree_json(root_path)
    with open(tree_file, "w", encoding="utf-8", newline="\n") as f:
        f.write(format_compact_tree_json(data))
    return tree_file


def _read_local_beacon(dir_path: Path) -> Dict[str, Any]:
    beacon = dir_path / BEACON_FILENAME
    if not beacon.exists():
        return {}
    try:
        return MiniYAML.load(beacon.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def generate_sliced_tree(
    root_path: Path,
    target_path: str,
    radius: int = 1,
    max_children: int = 6
) -> Dict[str, Any]:
    """
    Governs: [OBJ-04], [INV-02], [INV-03], [INV-08].
    Subgrafo focalizado: nodo foco + padre + descendientes hasta 'radius' niveles (máx. max_children)
    + dependencias declaradas en el beacon foco (clave 'imports_from').
    Garantiza len(format_sliced_tree(result)) <= SLICE_CHAR_BUDGET recortando hijos (campo 'truncated').
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
        if edge == "focus" and tn.get("key_files"):
            node["key_files"] = tn["key_files"]
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

    for dep in _read_local_beacon(focus_dir).get("imports_from", []) or []:
        dep_dir = (root / str(dep).strip("/")).resolve()
        try:
            dep_key = _rel_posix(dep_dir, root)
        except ValueError:
            continue
        if dep_dir.is_dir() and dep_key not in nodes:
            nodes[dep_key] = build_node(dep_dir, "dep")

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
    # Recorte determinista para garantizar presupuesto
    while len(format_sliced_tree(result)) > SLICE_CHAR_BUDGET and included > 0:
        included -= 1
        nodes.pop(_rel_posix(children[included], root), None)
        result["truncated"] = total_children - included
    if total_children > included and "truncated" not in result:
        result["truncated"] = total_children - included
    return result


def format_sliced_tree(data: Dict[str, Any]) -> str:
    """Governs: [OBJ-04]. Serialización de una línea, separadores mínimos (menor costo en tokens)."""
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def compute_context_budget(root_path: Path) -> List[Dict[str, Any]]:
    """Calcula el peso en archivos, bytes y tokens estimados por directorio."""
    stats = []
    for folder, meta in FOLDER_METADATA.items():
        dir_path = root_path / folder
        if not dir_path.exists():
            continue
        total_files = 0
        total_bytes = 0
        for p in dir_path.rglob("*"):
            if p.is_file() and not p.name.startswith("."):
                total_files += 1
                try:
                    total_bytes += p.stat().st_size
                except OSError:
                    pass
        # Heurística estándar: ~4 caracteres por token
        est_tokens = total_bytes // 4
        stats.append({
            "directory": folder,
            "role": meta.get("role", "general"),
            "files": total_files,
            "bytes": total_bytes,
            "est_tokens": est_tokens,
            "crawl": meta.get("crawl", True),
            "priority": meta.get("read_priority", "p2")
        })
    return stats


# ==============================================================================
# 4. Comandos del CLI: init, route, beacon, map, context, audit
# ==============================================================================

def init_project(base_path: str):
    """Inicializa la estructura normalizada v3.0, beacons, tree.json y reglas de IA."""
    root = Path(base_path)
    print(f"[*] Inicializando iDirectory v3.0 (Context Engineering) en: {root.resolve()}")

    # 1. Crear directorios gobernados
    for folder in FOLDER_METADATA.keys():
        (root / folder).mkdir(parents=True, exist_ok=True)

    # 2. Desplegar .context/tree.json
    tree_path = sync_tree(root)
    print(f"  [+] Satélite topológico desplegado: {tree_path.relative_to(root)}")

    # 3. Desplegar Beacons en cada directorio
    beacon_count = sync_beacons(root)
    print(f"  [+] {beacon_count} Context Beacons (.context.yaml) desplegados y sincronizados.")

    # 4. Desplegar engine_readme.md
    primary_seed = resolve_seed_key_files(root)[0]
    readme_path = root / "02_foundation" / "engine" / "engine_readme.md"
    readme_path.parent.mkdir(parents=True, exist_ok=True)
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(f"# {root.resolve().name.upper()} - iDirectory Architecture v3.0\n\n")
        f.write("Framework modular gobernado por **Gravity HyperScale Thinking** con Context Engineering nativo.\n\n")
        f.write("> **Protocolo de Ingesta para Agentes (Two-Tier Bootloader):**\n")
        f.write("> 1. Lee `AGENTS.md` (o `GEMINI.md` / `CLAUDE.md`).\n")
        f.write("> 2. Lee `.context/tree.json` (Mapa Topológico Satelital de ~250 tokens).\n")
        f.write("> 3. **Tier 1 (Atómico):** Lee el `.context.yaml` objetivo (o herencia del padre) y ejecuta. (NO cargar seed).\n")
        f.write(f"> 4. **Tier 2 (Arquitectura):** Carga `01_seed/{primary_seed}` solo ante disparadores explícitos (/seedMaster, /metrics, /ultraThinking).\n\n")
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

    print("[+] Estructura iDirectory v3.0 inicializada con éxito.")


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

    # 1. Tests y suites de verificación
    if any(marker in combined for marker in ["pytest", "unittest", "test_"]):
        return "tests"
    # 2. Pipelines productivos y big data cloud
    if any(marker in combined for marker in ["pyspark", "google.cloud", "boto3", "azure"]):
        return "src/cloud_jobs"
    # 3. Dashboards y BI / Viz
    if any(marker in combined for marker in ["streamlit", "dash", "plotly"]):
        return "src/dashboards"
    # 4. Fallback y lógica compartida / APIs
    return "src/core"


def route_file(
    file_path: str,
    base_path: str = ".",
    move: bool = False,
    overwrite: bool = False
) -> Optional[Path]:
    """Analiza la naturaleza de un archivo, sugiere su ubicación o lo mueve de forma segura."""
    base_dir = Path(base_path).resolve()

    # Blindaje contra Path Traversal en la ruta del archivo
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

    # Heurística contextual avanzada
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
        if any(w in name_lower for w in ["obsoleto", "historico", "old", "backup", "archive"]):
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

    # Blindaje contra Path Traversal
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

    print(f"\n[Análisis de Ruteo iDirectory v3.0]")
    print(f"  -> Archivo: '{src_file.name}'")
    print(f"  -> Extensión/Patrón: {ext if ext else 'Nominal'}")
    print(f"  -> Destino óptimo: {dest_subfolder}/")
    print(f"  -> Nombre normalizado: {dest_file_name}")

    if move:
        scaffolded = ensure_beacon_chain(dest_dir, base_dir)
        for created in scaffolded:
            print(f"  [+] Beacon auto-scaffold: {_rel_posix(created.parent, base_dir)}/.context.yaml")
        # Mitigación de colisión de casing en filesystems case-insensitive (Windows NTFS)
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
                # os.replace sobrescribe atómicamente en NTFS y POSIX
                safe_io_retry(lambda: os.replace(src_file, dest_path))
            else:
                # os.rename (no replace) para no pisar un archivo creado en carrera
                safe_io_retry(lambda: os.rename(src_file, dest_path))
            print(f"  [+] ACCIÓN: Archivo reubicado exitosamente en -> {dest_path}")
        if scaffolded:
            sync_tree(base_dir)  # [INV-04] topología mutada
        return dest_path
    else:
        print(f"  [Sugerencia] Añade '--move' para mover el archivo automáticamente:")
        print(f"  python FWengine.py route \"{file_path}\" --move")
        return dest_path


def audit_repository(root_path: Path, fix: bool = False) -> bool:
    """
    Audita mayúsculas, beacons canónicos ausentes, directorios huérfanos sin beacon, satélite ausente
    y beacons inflados (> BEACON_CHAR_BUDGET, solo advertencia).
    Con fix=True aprovisiona beacons faltantes y regenera tree.json (no cuentan como violación).
    """
    print(f"[*] Auditando gobernanza iDirectory en: {root_path.resolve()}")
    violations = 0
    remediated = 0

    # 1. Chequeo de nombres con mayúsculas en carpetas de primer y segundo nivel
    for item in root_path.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            try:
                disk_name = next(e for e in os.listdir(root_path) if e.lower() == item.name.lower())
            except (StopIteration, OSError):
                disk_name = item.name
            if any(c.isupper() for c in disk_name):
                print(f"  [!] VIOLACIÓN TOPOLÓGICA (Mayúsculas detectadas): '{disk_name}/'")
                violations += 1
            # Segundo nivel
            try:
                sub_entries = os.listdir(item)
            except OSError:
                sub_entries = []
            for sub in sub_entries:
                sub_path = item / sub
                if sub_path.is_dir() and not sub.startswith("."):
                    if any(c.isupper() for c in sub):
                        print(f"  [!] VIOLACIÓN TOPOLÓGICA (Mayúsculas detectadas en subdirectorio): '{disk_name}/{sub}/'")
                        violations += 1

    # 2. Beacons ausentes en nodos canónicos
    reported: Set[str] = set()
    for folder, meta in FOLDER_METADATA.items():
        if folder == ".context":
            continue
        folder_dir = root_path / folder
        beacon_file = folder_dir / BEACON_FILENAME
        if folder_dir.exists() and not beacon_file.exists():
            reported.add(folder.lower())
            if fix:
                scaffold_beacon_for_dir(folder_dir, root_path)
                print(f"  [FIX] Beacon canónico aprovisionado en: '{folder}/'")
                remediated += 1
            else:
                print(f"  [!] BEACON AUSENTE en: '{folder}/'")
                violations += 1

    # 3. Directorios huérfanos (auto-descubrimiento, respeta poda)
    for orphan in discover_unbeaconed_directories(root_path):
        rel = _rel_posix(orphan, root_path)
        if rel.lower() in reported:
            continue
        if fix:
            scaffold_beacon_for_dir(orphan, root_path)
            print(f"  [FIX] Beacon auto-scaffold en: '{rel}/'")
            remediated += 1
        else:
            print(f"  [!] DIRECTORIO HUÉRFANO (sin beacon): '{rel}/'")
            violations += 1

    # 4. Satélite topológico
    tree_file = root_path / ".context" / "tree.json"
    if fix and (remediated > 0 or not tree_file.exists()):
        sync_tree(root_path)
        print("  [FIX] Satélite .context/tree.json regenerado.")
    elif not tree_file.exists():
        print("  [!] SATÉLITE AUSENTE: No se encontró '.context/tree.json'")
        violations += 1

    # 5. Telemetría de dilución atencional (advertencia, no violación)
    for beacon in iter_beacon_files(root_path):
        try:
            size = len(beacon.read_text(encoding="utf-8"))
        except OSError:
            continue
        if size > BEACON_CHAR_BUDGET:
            rel_dir = _rel_posix(beacon.parent, root_path)
            print(f"  [WARN] Beacon inflado en {rel_dir} (> 150 tokens, {size} chars)")

    if remediated:
        print(f"[FIX] {remediated} beacons aprovisionados automáticamente.")
    if violations == 0:
        print("[PASS] Auditoría exitosa: 0 violaciones topológicas y todos los beacons sincronizados.")
        return True
    print(f"[FAIL] Se encontraron {violations} violaciones de gobernanza.")
    return False


def main():
    parser = argparse.ArgumentParser(
        description="iDirectory: Framework de Gobernanza y Context Engineering (por Gravity HyperScale Thinking)"
    )
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponibles")

    # init
    init_parser = subparsers.add_parser("init", help="Inicializa el andamiaje v3.0, beacons y tree.json")
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
    beacon_parser.add_argument("--no-discover", action="store_true", help="Sincroniza solo nodos canónicos")

    # map
    map_parser = subparsers.add_parser("map", help="Gestiona el mapa satelital (.context/tree.json)")
    map_parser.add_argument("--sync", action="store_true", help="Regenera el satélite .context/tree.json")
    map_parser.add_argument("--check-freshness", action="store_true", help="Comprueba si tree.json sufre drift respecto al filesystem")
    map_parser.add_argument("--slice", metavar="DIR", help="Emite subgrafo focalizado (<150 tokens) del directorio")
    map_parser.add_argument("--radius", type=int, default=1, help="Niveles de descendencia en --slice")

    # context
    context_parser = subparsers.add_parser("context", help="Telemetría de Context Engineering y token budget")
    context_parser.add_argument("--budget", action="store_true", help="Desglosa el presupuesto de tokens por carpeta")
    context_parser.add_argument("--compact", action="store_true", help="Emite string compacto para inyección en prompts")
    context_parser.add_argument("--check-freshness", action="store_true", help="Comprueba si tree.json sufre drift respecto al filesystem")

    # audit
    audit_parser = subparsers.add_parser("audit", help="Audita violaciones de mayúsculas, huérfanos y beacons")
    audit_parser.add_argument("--fix", action="store_true", help="Aprovisiona beacons faltantes y regenera tree.json")

    args = parser.parse_args()
    root = Path(getattr(args, "base", getattr(args, "path", ".")))

    if args.command == "init":
        init_project(args.path)
    elif args.command == "route":
        route_file(args.file, args.base, args.move, getattr(args, "overwrite", False))
    elif args.command == "beacon":
        if args.audit:
            audit_repository(root)
        else:
            count = sync_beacons(root, auto_discover=not getattr(args, "no_discover", False))
            print(f"[+] {count} Beacons (.context.yaml) sincronizados exitosamente.")
    elif args.command == "map":
        if getattr(args, "slice", None):
            print(format_sliced_tree(generate_sliced_tree(root, args.slice, radius=args.radius)))
        elif getattr(args, "check_freshness", False):
            freshness = check_satellite_freshness(root)
            if freshness["fresh"]:
                print("[PASS] Satélite al día: .context/tree.json está sincronizado con los directorios clave.")
            else:
                print(f"[!] DRIFT DETECTADO: El mapa satelital está desactualizado respecto a '{freshness['latest_path']}'.")
                print("    Acción recomendada: Ejecute 'python FWengine.py map --sync' y 'python FWengine.py beacon --sync'.")
        else:
            tree_path = sync_tree(root)
            print(f"[+] Mapa satelital sincronizado en: {tree_path}")
    elif args.command == "context":
        if getattr(args, "check_freshness", False):
            freshness = check_satellite_freshness(root)
            if freshness["fresh"]:
                print("[PASS] Satélite al día: .context/tree.json está sincronizado con los directorios clave.")
            else:
                print(f"[!] DRIFT DETECTADO: El mapa satelital está desactualizado respecto a '{freshness['latest_path']}'.")
                print("    Acción recomendada: Ejecute 'python FWengine.py map --sync' y 'python FWengine.py beacon --sync'.")
        elif args.compact:
            tree = generate_tree_json(root)
            nodes_summary = "; ".join([f"{k}:{v['role']}({v['prio']})" for k, v in tree["nodes"].items() if v["crawl"]])
            print(f"IDIR_TOPOLOGY: [{nodes_summary}]")
        else:
            budget = compute_context_budget(root)
            print("\n" + "=" * 80)
            print(f"{'DIRECTORIO':<28} | {'ROL':<20} | {'FILES':<5} | {'TOKENS EST.':<10} | {'PRIO'}")
            print("=" * 80)
            total_tokens = 0
            for item in budget:
                total_tokens += item["est_tokens"]
                crawl_flag = " [NO-CRAWL]" if not item["crawl"] else ""
                print(f"{item['directory']:<28} | {item['role']:<20} | {item['files']:<5} | {item['est_tokens']:<10} | {item['priority']}{crawl_flag}")
            print("=" * 80)
            print(f"Total estimado de tokens en repositorio: ~{total_tokens:,} tokens\n")
    elif args.command == "audit":
        ok = audit_repository(root, fix=getattr(args, "fix", False))
        sys.exit(0 if ok else 1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()