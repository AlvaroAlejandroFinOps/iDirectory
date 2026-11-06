#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
iReadme Universal Documentation Generator (v5.0.0)
=================================================
Enterprise Paper-Grade v5.0 Dynamic Synthesizer & Federated Context Engineering Engine.

Ensambla de forma determinista y paramétrica README.md (Inglés) y README_ES.md (Español)
para cualquier repositorio cliente, consumiendo la telemetría del Bus Federado (.context/icontext_bus.json),
el satélite (.context/tree.json) y los beacons semánticos (.context.yaml).

Incorpora automáticamente:
- Insignias / escudos de estado (badges) de las metodologías iContext activas.
- Sección dedicada de 'Gobernanza Federada & Context Engineering iContext v5.0'.
- Resumen y propósito de cada una de las capas presentes (L0-L3).
- Paridad estructural estricta phi = 1.0, rigor matematico en LaTeX y cero rutas absolutas.
"""

import os
import sys
import json
import time
import uuid
import threading
import random
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

VERSION = "5.0.0"

LAYER_SPECS = {
    "l0_idirectory": {
        "title_en": "iDirectory (L0)",
        "title_es": "iDirectory (L0)",
        "name_en": "Topological Control Plane & Adaptive Context Engineering",
        "name_es": "Plano de Control Topológico & Context Engineering Adaptativo",
        "badge": "[![iDirectory L0](https://img.shields.io/badge/L0-iDirectory%20v5.0-2b2b2b?style=flat-square)](#)",
        "summary_en": "Enforces deterministic all-lowercase directory topology, boundary beacons (.context.yaml), cryptographic tree satellite (.context/tree.json), token budgeting, and subagent capsule isolation (<450 tokens).",
        "summary_es": "Gobierna la topología canónica all-lowercase, balizas semánticas (.context.yaml), satélite criptográfico (.context/tree.json), presupuestos de tokens y aislamiento mediante cápsulas para subagentes (<450 tokens)."
    },
    "l1_thinkingseed": {
        "title_en": "ThinkingSeed (L1)",
        "title_es": "ThinkingSeed (L1)",
        "name_en": "Symbolic Architectural DNA & Zero-Source-Code Vector",
        "name_es": "Vector de ADN Arquitectónico Simbólico & Memoria Zero-Code",
        "badge": "[![ThinkingSeed L1](https://img.shields.io/badge/L1-ThinkingSeed%20v5.0-34495e?style=flat-square)](#)",
        "summary_en": "Preserves architectural technical memory and AST symbolic contracts with zero implementation code leakage (Zero Source Code), strictly certified across 6 deterministic validation gates.",
        "summary_es": "Preserva la memoria técnica y contratos simbólicos AST sin fuga de código fuente (Zero Source Code), auditado bajo validación estricta de 6 Gates deterministas."
    },
    "l2_metricsthinking": {
        "title_en": "MetricsThinking (L2)",
        "title_es": "MetricsThinking (L2)",
        "name_en": "Forensic Technology Audit & Spectral FPIA Governance",
        "name_es": "Auditoría Forense Tecnológica & Gobernanza Espectral FPIA",
        "badge": "[![MetricsThinking L2](https://img.shields.io/badge/L2-MetricsThinking%20v5.0-4b5563?style=flat-square)](#)",
        "summary_en": "Computes ground-truth maturity scores across 10 canonical modules, AST semantic drift detection, FPIA spectral efficiency (S_spectral, PF_spectral), and Zero-Tolerance security scanning.",
        "summary_es": "Calcula madurez por Ground Truth en 10 módulos canónicos, deriva semántica AST, eficiencia espectral FPIA (S_spectral, PF_spectral) y escaneo de seguridad Zero-Trust."
    },
    "l3_ireadme": {
        "title_en": "iReadme (L3)",
        "title_es": "iReadme (L3)",
        "name_en": "Institutional Paper-Grade Dual Documentation Synthesizer",
        "name_es": "Sintetizador Institucional de Documentación Dual Paper-Grade",
        "badge": "[![iReadme L3](https://img.shields.io/badge/L3-iReadme%20v5.0-000000?style=flat-square)](#)",
        "summary_en": "Synchronizes dual English/Spanish documentation under the Enterprise Paper-Grade standard, guaranteeing structural parity phi = 1.0, formal KaTeX formulations, and zero local path leakages.",
        "summary_es": "Sincroniza documentación dual inglés/español bajo el estándar Enterprise Paper-Grade, garantizando paridad estructural phi = 1.0, formulación formal en KaTeX y cero fugas de ruta local."
    }
}


def detect_icontext_layers(repo_path: Path) -> Dict[str, Dict[str, Any]]:
    """
    Inspecciona exhaustivamente el repositorio para detectar cuáles de las 4 capas
    del ecosistema iContext (L0, L1, L2, L3) se encuentran incorporadas y activas.
    """
    repo = repo_path.resolve()
    bus_path = repo / ".context" / "icontext_bus.json"
    bus_data = {}
    if bus_path.is_file():
        try:
            bus_data = json.loads(bus_path.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            bus_data = {}

    layers_state: Dict[str, Dict[str, Any]] = {}
    bus_layers = bus_data.get("layers", {}) if isinstance(bus_data.get("layers"), dict) else {}

    # L0: iDirectory
    l0_bus = bus_layers.get("l0_idirectory", {})
    l0_present = bool(l0_bus.get("version")) or (repo / "FWengine.py").is_file() or (repo / ".context" / "tree.json").is_file()
    layers_state["l0_idirectory"] = {
        "present": l0_present,
        "version": str(l0_bus.get("version", "5.0.0")),
        "details": l0_bus,
        "spec": LAYER_SPECS["l0_idirectory"],
    }

    # L1: ThinkingSeed
    l1_bus = bus_layers.get("l1_thinkingseed", {})
    seed_dir = repo / "01_seed"
    has_seed = seed_dir.is_dir() and any(seed_dir.glob("seed-*.md"))
    l1_present = bool(l1_bus.get("present")) or has_seed
    layers_state["l1_thinkingseed"] = {
        "present": l1_present,
        "version": str(l1_bus.get("version", "5.0.0")),
        "details": l1_bus,
        "spec": LAYER_SPECS["l1_thinkingseed"],
    }

    # L2: MetricsThinking
    l2_bus = bus_layers.get("l2_metricsthinking", {})
    mt_dir = repo / "artifacts" / "plans" / "metricsthinking"
    has_mt = mt_dir.is_dir() or (repo / "MetricsThinking.json").is_file() or (repo / "src" / "metricsthinking").is_dir()
    l2_present = bool(l2_bus.get("present")) or has_mt
    layers_state["l2_metricsthinking"] = {
        "present": l2_present,
        "version": str(l2_bus.get("version", "5.0.0")),
        "details": l2_bus,
        "spec": LAYER_SPECS["l2_metricsthinking"],
    }

    # L3: iReadme
    l3_bus = bus_layers.get("l3_ireadme", {})
    has_dual_readme = (repo / "README.md").is_file() and (repo / "README_ES.md").is_file()
    has_skill = (repo / "skills" / "readme").is_dir() or (repo / "src" / "ireadme").is_dir()
    l3_present = bool(l3_bus.get("present")) or has_dual_readme or has_skill
    layers_state["l3_ireadme"] = {
        "present": l3_present,
        "version": str(l3_bus.get("version", "5.0.0")),
        "details": l3_bus,
        "spec": LAYER_SPECS["l3_ireadme"],
    }

    return layers_state


def render_badges_block(layers: Dict[str, Dict[str, Any]], custom_badges: Optional[List[str]] = None) -> str:
    """Genera el bloque monocromático de insignias para la cabecera del documento."""
    lines: List[str] = [
        "[![Standard](https://img.shields.io/badge/Standard-Enterprise%20Paper--Grade%20v5.0-2b2b2b?style=flat-square)](#)",
        "[![Ecosystem](https://img.shields.io/badge/Ecosystem-Multi--AI%20%28Google%20%7C%20Claude%20%7C%20OpenAI%20%7C%20Cursor%29-34495e?style=flat-square)](#)",
    ]

    # Insignia federada maestra si hay 2 o más capas presentes
    present_count = sum(1 for v in layers.values() if v.get("present"))
    if present_count >= 2:
        lines.append("[![iContext Federation](https://img.shields.io/badge/iContext-Federated%20v5.0-1a1a1a?style=flat-square)](#)")

    for k, v in layers.items():
        if v.get("present"):
            lines.append(v["spec"]["badge"])

    if custom_badges:
        lines.extend(custom_badges)

    return "\n".join(lines)


def render_federation_section(layers: Dict[str, Dict[str, Any]], lang: str = "en") -> str:
    """
    Genera la sección dedicada que documenta la gobernanza federada y el uso
    de las metodologías de Context Engineering v5.0 incorporadas en el proyecto.
    """
    present_layers = [k for k, v in layers.items() if v.get("present")]
    count = len(present_layers)

    if lang == "es":
        title = "### Gobernanza Federada & Context Engineering iContext v5.0"
        names = [LAYER_SPECS[k]["title_es"].split()[0] for k in present_layers]
        comp_summary = ", ".join(names[:-1]) + f" y {names[-1]}" if len(names) > 1 else (names[0] if names else "ninguna")
        intro = (
            f"Este proyecto implementa formalmente el protocolo **iContext Federation Protocol v5.0**, "
            f"incorporando **{count} de los 4 proyectos canónicos** ({comp_summary}) de gobernanza agéntica y optimización atencional "
            f"creados por Gravity HyperScale Thinking:"
        )
        table_header = "| Capa | Componente | Función Principal en este Repositorio | Estado |"
        table_sep = "| :--- | :--- | :--- | :--- |"
        closing = (
            "La interoperabilidad entre estas herramientas se orquesta de manera no-bloqueante a través del "
            "**Bus Cognitivo Federado** (`./.context/icontext_bus.json`), garantizando continuidad atencional, "
            "cero deriva satelital y protección estricta contra alucinaciones en agentes autónomos."
        )
    else:
        title = "### Federated Governance & Context Engineering (iContext v5.0)"
        names = [LAYER_SPECS[k]["title_en"].split()[0] for k in present_layers]
        comp_summary = ", ".join(names[:-1]) + f", and {names[-1]}" if len(names) > 1 else (names[0] if names else "none")
        intro = (
            f"This project formally implements the **iContext Federation Protocol v5.0**, "
            f"incorporating **{count} of the 4 canonical projects** ({comp_summary}) for autonomous agentic governance "
            f"and attentional optimization designed by Gravity HyperScale Thinking:"
        )
        table_header = "| Layer | Component | Primary Engineering Function in this Repository | Status |"
        table_sep = "| :--- | :--- | :--- | :--- |"
        closing = (
            "Interoperability across these tools is orchestrated in a non-blocking fashion via the "
            "**Federated Cognitive Bus** (`./.context/icontext_bus.json`), securing attentional continuity, "
            "zero satellite drift, and strict hallucination mitigation across autonomous AI agents."
        )

    rows: List[str] = []
    for key, spec in LAYER_SPECS.items():
        st = layers.get(key, {})
        is_p = st.get("present", False)
        status_tag = "ACTIVE (v5.0)" if is_p else "OPTIONAL"
        if lang == "es":
            c_name = f"**{spec['title_es']}** — {spec['name_es']}"
            c_desc = spec["summary_es"]
        else:
            c_name = f"**{spec['title_en']}** — {spec['name_en']}"
            c_desc = spec["summary_en"]

        if is_p:
            layer_id = key[:2].upper()
            rows.append(f"| `{layer_id}` | {c_name} | {c_desc} | `{status_tag}` |")

    table_content = "\n".join([table_header, table_sep] + rows)
    return f"{title}\n\n{intro}\n\n{table_content}\n\n{closing}\n"


def atomic_write_text(target: Path, content: str, encoding: str = "utf-8") -> None:
    """Escritura atómica segura con reemplazo y reintentos para entornos multi-agente."""
    target = target.resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    unique_suffix = f"{os.getpid()}_{threading.get_ident()}_{uuid.uuid4().hex[:8]}"
    temp_path = target.parent / f".tmp_{unique_suffix}_{target.name}"
    delay = 0.02
    try:
        temp_path.write_text(content, encoding=encoding)
        for attempt in range(10):
            try:
                os.replace(temp_path, target)
                return
            except OSError:
                if attempt == 9:
                    raise
                time.sleep(delay + random.uniform(0.01, 0.03))
                delay *= 1.4
    finally:
        if temp_path.exists():
            try:
                temp_path.unlink()
            except OSError:
                pass


def extract_project_metadata(repo_path: Path) -> Dict[str, Any]:
    """Extrae metadatos del proyecto desde pyproject.toml, package.json o tree.json."""
    repo = repo_path.resolve()
    name = repo.name
    desc_en = "High-performance enterprise systems platform and automated engineering core."
    desc_es = "Plataforma empresarial de sistemas de alto desempeño y núcleo automatizado de ingeniería."

    # Intentar pyproject.toml
    pyproject = repo / "pyproject.toml"
    if pyproject.is_file():
        try:
            txt = pyproject.read_text(encoding="utf-8")
            for line in txt.splitlines():
                if line.strip().startswith("name ="):
                    name = line.split("=")[1].strip().strip('"\'')
                elif line.strip().startswith("description ="):
                    desc_en = line.split("=")[1].strip().strip('"\'')
                    desc_es = desc_en
        except Exception:
            pass

    return {
        "name": name,
        "description_en": desc_en,
        "description_es": desc_es,
    }


def generate_universal_readmes(repo_path: Path, write_to_disk: bool = True, update_golden: bool = False) -> Tuple[str, str]:
    """Preserve authored text; update only an explicitly managed telemetry block."""
    import re
    from ireadme.runtime import atomic_write, read_json, publish_layer, validate_readmes
    repo = Path(repo_path).resolve()
    bus = read_json(repo / ".context/icontext_bus.json")
    layers = bus.get("layers", {})
    report = read_json(repo / "artifacts/plans/metricsthinking/MetricsThinking.json")
    measured = read_json(repo / ".context/benchmark_v6.json")
    def show(value):
        return "Not measured / No medido" if value is None else str(value)
    telemetry = "\n".join([
        "<!-- ICONTEXT-V6:TELEMETRY:START -->",
        "| Evidence / Evidencia | Recorded value / Valor registrado |",
        "| :--- | :--- |",
        f"| Metrics score | {show(report.get('consolidated_score'))} |",
        f"| Estimated spectral factor (auxiliary) | {show((report.get('fpai') or {}).get('power_factor_spectral'))} |",
        f"| Query latency p95 (ms) | {show(measured.get('query_p95_ms'))} |",
        "| Validity | Recorded evidence; verify freshness with icontext audit |",
        "<!-- ICONTEXT-V6:TELEMETRY:END -->",
    ])
    headings = {
      "README.md": ["Executive Abstract", "System Architecture & Topology", "Mathematical Formulation & Analytical Engines", "Empirical Performance & Benchmarks", "Repository Structure & Artifacts", "Execution & Verification Protocol", "Domain Glossary", "Academic & Engineering References"],
      "README_ES.md": ["Resumen Ejecutivo", "Arquitectura y Topología del Sistema", "Formulación Matemática y Motores Analíticos", "Rendimiento Empírico y Benchmarks", "Estructura del Repositorio y Artefactos", "Protocolo de Ejecución y Verificación", "Glosario de Dominio", "Referencias Académicas y de Ingeniería"]}
    result = []
    for filename, titles in headings.items():
        path = repo / filename
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            if re.search(r"<!-- ICONTEXT-V6:TELEMETRY:START -->.*?<!-- ICONTEXT-V6:TELEMETRY:END -->", text, re.S):
                text = re.sub(r"<!-- ICONTEXT-V6:TELEMETRY:START -->.*?<!-- ICONTEXT-V6:TELEMETRY:END -->", lambda m: telemetry, text, flags=re.S)
            else:
                match = re.search(r"(?m)^## 4\.[^\n]*\n", text)
                if not match:
                    raise ValueError(f"{filename}: agent must establish the eight-section layout before updating telemetry")
                text = text[:match.end()] + "\n" + telemetry + "\n" + text[match.end():]
        else:
            label = "Language" if filename == "README.md" else "Idioma"
            text = f"# {repo.name}\n\n**{label}:** [English](README.md) | [Español](README_ES.md)\n\n"
            text += "\n\n".join(f"## {i}. {title}\n\n" + (telemetry if i == 4 else "Pending project-specific authoring by the current agent.") for i, title in enumerate(titles, 1)) + "\n"
        result.append(text)
    if write_to_disk:
        for filename, text in zip(headings, result):
            atomic_write(repo / filename, text)
        errors = validate_readmes(repo)
        publish_layer(repo, "l3", {"present": True, "state": "invalid" if errors else "validated",
                                   "parity_score_phi": 0.0 if errors else 1.0, "validation_errors": errors})
        if update_golden:
            for filename, text in zip(("README_golden.md", "README_ES_golden.md"), result):
                atomic_write(repo / "tests/golden" / filename, text)
    return tuple(result)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="iReadme v6: preserve authored content and update measured telemetry")
    parser.add_argument("--target", default=".")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--update-golden", action="store_true", help="Explicitly accept reference snapshot changes")
    args = parser.parse_args()
    result = generate_universal_readmes(Path(args.target), not args.dry_run, args.update_golden)
    if args.dry_run:
        print(json.dumps({"readme_characters": [len(t) for t in result], "writes": False}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
