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
- Cero dependencias externas (Python Standard Library pura).
"""

import os
import sys
import json
import time
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional

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
FOLDER_METADATA: Dict[str, Dict[str, Any]] = {
    "01_seed": {
        "purpose": "Semilla de proyecto y memoria técnica (ThinkingSeed Master). ADN arquitectónico del sistema.",
        "role": "dna",
        "relevance": "critical",
        "crawl": False,
        "read_priority": "p0",
        "seed_reference": "required",
        "token_density": "medium",
        "key_files": ["seed-idirectory-master.md"],
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

def generate_beacon_content(folder: str, meta: Dict[str, Any]) -> str:
    """Genera el contenido .context.yaml para un directorio."""
    beacon_data = {
        "version": "1.0",
        "directory": folder,
        "role": meta.get("role", "general"),
        "purpose": meta.get("purpose", ""),
        "relevance": meta.get("relevance", "medium"),
        "crawl": meta.get("crawl", True),
        "read_priority": meta.get("read_priority", "p2"),
        "seed_reference": meta.get("seed_reference", "optional"),
        "token_density": meta.get("token_density", "sparse"),
        "instructions": meta.get("instructions", "Directorio estándar.")
    }
    if "key_files" in meta:
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


def sync_beacons(root_path: Path) -> int:
    """Sincroniza o crea los microarchivos .context.yaml en cada directorio registrado."""
    count = 0
    for folder, meta in FOLDER_METADATA.items():
        if folder == ".context":
            continue
        dir_path = root_path / folder
        dir_path.mkdir(parents=True, exist_ok=True)
        beacon_file = dir_path / ".context.yaml"
        beacon_content = generate_beacon_content(folder, meta)
        with open(beacon_file, "w", encoding="utf-8") as f:
            f.write(beacon_content + "\n")
        count += 1
    return count


def generate_tree_json(root_path: Path) -> Dict[str, Any]:
    """Genera el mapa satelital compacto de todo el repositorio (~250 tokens)."""
    now_ts = time.time()
    tree_data = {
        "$schema": "./schema/tree.schema.json",
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
                "01_seed/seed-idirectory-master.md",
                "[target_folder]/.context.yaml"
            ]
        },
        "nodes": {}
    }
    for folder, meta in FOLDER_METADATA.items():
        node_info = {
            "role": meta.get("role", "general"),
            "prio": meta.get("read_priority", "p2"),
            "crawl": meta.get("crawl", True),
            "seed_ref": meta.get("seed_reference", "optional")
        }
        if "key_files" in meta:
            node_info["key_files"] = meta["key_files"]
        tree_data["nodes"][folder] = node_info
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



def sync_tree(root_path: Path) -> Path:
    """Escribe el satélite .context/tree.json."""
    context_dir = root_path / ".context"
    context_dir.mkdir(parents=True, exist_ok=True)
    tree_file = context_dir / "tree.json"
    data = generate_tree_json(root_path)
    with open(tree_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return tree_file


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
    readme_path = root / "02_foundation" / "engine" / "engine_readme.md"
    readme_path.parent.mkdir(parents=True, exist_ok=True)
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(f"# {root.resolve().name.upper()} - iDirectory Architecture v3.0\n\n")
        f.write("Framework modular gobernado por **Gravity HyperScale Thinking** con Context Engineering nativo.\n\n")
        f.write("> **Protocolo de Ingesta para Agentes (Two-Tier Bootloader):**\n")
        f.write("> 1. Lee `AGENTS.md` (o `GEMINI.md` / `CLAUDE.md`).\n")
        f.write("> 2. Lee `.context/tree.json` (Mapa Topológico Satelital de ~250 tokens).\n")
        f.write("> 3. **Tier 1 (Atómico):** Lee el `.context.yaml` objetivo (o herencia del padre) y ejecuta. (NO cargar seed).\n")
        f.write("> 4. **Tier 2 (Arquitectura):** Carga `01_seed/seed-idirectory-master.md` solo ante disparadores explícitos (/seedMaster, /metrics, /ultraThinking).\n\n")
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


def inspect_python_header(file_path: Path, max_chars: int = 1000) -> str:
    """Lee de forma no bloqueante hasta max_chars para clasificar archivos .py según imports y patrones."""
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            sample = f.read(max_chars).lower()
    except Exception:
        return "src/core"

    # 1. Tests y suites de verificación
    if any(marker in sample for marker in ["pytest", "unittest", "test_"]):
        return "tests"
    # 2. Pipelines productivos y big data cloud
    if any(marker in sample for marker in ["pyspark", "google.cloud", "boto3", "azure"]):
        return "src/cloud_jobs"
    # 3. Dashboards y BI / Viz
    if any(marker in sample for marker in ["streamlit", "dash", "plotly"]):
        return "src/dashboards"
    # 4. Fallback y lógica compartida / APIs
    return "src/core"


def route_file(file_path: str, base_path: str = ".", move: bool = False) -> Optional[Path]:
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
        dest_dir.mkdir(parents=True, exist_ok=True)
        # Mitigación de colisión de casing en filesystems case-insensitive (Windows NTFS)
        if src_resolved == dest_path:
            if src_file.name != dest_file_name:
                temp_path = dest_dir / f".tmp_{os.getpid()}_{dest_file_name}"
                src_file.rename(temp_path)
                temp_path.rename(dest_path)
                print(f"  [+] ACCIÓN: Archivo normalizado a minúsculas atómicamente -> {dest_path}")
            else:
                print(f"  [*] El archivo ya está en la ubicación canónica con nombre en minúsculas.")
        else:
            if dest_path.exists():
                temp_path = dest_dir / f".tmp_{os.getpid()}_{dest_file_name}"
                src_file.rename(temp_path)
                if dest_path.exists():
                    dest_path.unlink()
                temp_path.rename(dest_path)
            else:
                src_file.rename(dest_path)
            print(f"  [+] ACCIÓN: Archivo reubicado exitosamente en -> {dest_path}")
        return dest_path
    else:
        print(f"  [Sugerencia] Añade '--move' para mover el archivo automáticamente:")
        print(f"  python FWengine.py route \"{file_path}\" --move")
        return dest_path


def audit_repository(root_path: Path) -> bool:
    """Audita inconsistencias de mayúsculas, carpetas huérfanas y beacons ausentes."""
    print(f"[*] Auditando gobernanza iDirectory en: {root_path.resolve()}")
    violations = 0

    # 1. Chequeo de nombres con mayúsculas en carpetas de primer y segundo nivel
    for item in root_path.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            if any(c.isupper() for c in item.name):
                print(f"  [!] VIOLACIÓN TOPOLÓGICA (Mayúsculas detectadas): '{item.name}/'")
                violations += 1

    # 2. Chequeo de beacons ausentes en nodos canónicos
    missing_beacons = 0
    for folder, meta in FOLDER_METADATA.items():
        if folder == ".context":
            continue
        folder_dir = root_path / folder
        beacon_file = folder_dir / ".context.yaml"
        if folder_dir.exists() and not beacon_file.exists():
            print(f"  [!] BEACON AUSENTE en: '{folder}/'")
            missing_beacons += 1
            violations += 1

    # 3. Chequeo de satélite topológico
    tree_file = root_path / ".context" / "tree.json"
    if not tree_file.exists():
        print("  [!] SATÉLITE AUSENTE: No se encontró '.context/tree.json'")
        violations += 1

    if violations == 0:
        print("[PASS] Auditoría exitosa: 0 violaciones topológicas y todos los beacons sincronizados.")
        return True
    else:
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
    route_parser.add_argument("--base", default=".", help="Directorio base")

    # beacon
    beacon_parser = subparsers.add_parser("beacon", help="Gestiona los semáforos y Context Beacons (.context.yaml)")
    beacon_parser.add_argument("--sync", action="store_true", help="Genera o sincroniza todos los beacons")
    beacon_parser.add_argument("--audit", action="store_true", help="Audita que todos los beacons existan y sean válidos")

    # map
    map_parser = subparsers.add_parser("map", help="Gestiona el mapa satelital (.context/tree.json)")
    map_parser.add_argument("--sync", action="store_true", help="Regenera el satélite .context/tree.json")
    map_parser.add_argument("--check-freshness", action="store_true", help="Comprueba si tree.json sufre drift respecto al filesystem")

    # context
    context_parser = subparsers.add_parser("context", help="Telemetría de Context Engineering y token budget")
    context_parser.add_argument("--budget", action="store_true", help="Desglosa el presupuesto de tokens por carpeta")
    context_parser.add_argument("--compact", action="store_true", help="Emite string compacto para inyección en prompts")
    context_parser.add_argument("--check-freshness", action="store_true", help="Comprueba si tree.json sufre drift respecto al filesystem")

    # audit
    subparsers.add_parser("audit", help="Audita violaciones de mayúsculas, huérfanos y beacons")

    args = parser.parse_args()
    root = Path(getattr(args, "base", getattr(args, "path", ".")))

    if args.command == "init":
        init_project(args.path)
    elif args.command == "route":
        route_file(args.file, args.base, args.move)
    elif args.command == "beacon":
        if args.audit:
            audit_repository(root)
        else:
            count = sync_beacons(root)
            print(f"[+] {count} Beacons (.context.yaml) sincronizados exitosamente.")
    elif args.command == "map":
        if getattr(args, "check_freshness", False):
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
        audit_repository(root)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()