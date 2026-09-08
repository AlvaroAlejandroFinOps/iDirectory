#!/usr/bin/env python3
import os
import sys
import argparse
from pathlib import Path

# 1. Manifiesto Centralizado de Gobernanza (Directorio Thinking Multi-Cloud, IA y Datos)
FOLDER_MANIFEST = {
    "001_Seed": "Seed (Semilla de proyecto y contexto primario para agentes de IA y arquitectos).",
    "02_Foundation/Engine": "Núcleo del framework de automatización del proyecto. Contiene la lógica de ruteo, indexación y EngineReadme.md de gobernanza.",
    "03_Research_AI/Notebooks": "Notebooks de desarrollo interactivo y experimentación (Jupyter/Fabric/Databricks/Colab) para análisis exploratorio (EDA) y algoritmos.",
    "03_Research_AI/llm_prompts": "Estructuras de prompts para LLMs, system prompts, árboles de contexto y plantillas de inferencia generativa.",
    "03_Research_AI/experiments": "Espacio de pruebas de concepto (PoCs), prototipos de modelos, I+D y benchmarks algorítmicos.",
    "src/cloud_jobs": "Scripts productivos, definiciones de pipelines y orquestación multi-cloud (Fabric PySpark, AWS Glue/EMR, GCP Dataproc/Dataflow, Azure Synapse).",
    "src/data_generation": "Módulos de generación y simulación de datos sintéticos. Rigor matemático en distribuciones y volumetría estadística para pruebas de carga.",
    "src/core": "Lógica de negocio transversal, servicios modulares, utilitarios de backend y componentes de desarrollo de software.",
    "src/dashboards": "Aplicaciones de visualización, tableros de BI, cuadros de mando interactivos (Streamlit, Dash, PowerBI, Looker).",
    "Artefactos/Planes/Vigentes": "Planes de capacidad activos (F-SKUs), presupuestos de cómputo cloud vigentes, hitos del proyecto y documentación activa.",
    "Artefactos/Planes/Historico_Obsoletos": "Histórico de planes evaluados, arquitecturas descartadas y documentación obsoleta preservada como respaldo y trazabilidad.",
    "docs/technical_specs": "Especificaciones técnicas detalladas, mapeos de linaje de datos, contratos de esquemas y requerimientos no funcionales.",
    "docs/engineers_notes": "Bitácoras de ingeniería, registro de deuda técnica, decisiones de diseño rápido y análisis de causa raíz (RCA).",
    "docs/architecture": "Diagramas de arquitectura multi-cloud, flujos de datos e información estratégica de las capas Medallion (Bronze, Silver, Gold).",
    "tests": "Suites de pruebas unitarias, de integración y de calidad de datos (Great Expectations / deequ) para garantizar consistencia lógica.",
    "Tools": "Scripts utilitarios internos, herramientas de automatización local, linters, y configuraciones de debugging personalizado.",
    "config": "Parámetros de entorno (dev, staging, prod), llaves de configuración de esquemas y variables de conexión desacopladas del código.",
    "infrastructure": "Scripts de Infraestructura como Código (IaC) utilizando AWS CDK, Terraform o plantillas ARM/Bicep para aprovisionamiento multi-cloud.",
    "data/raw": "Zona de aterrizaje local (Bronze) para almacenamiento de fuentes de datos puras e inmutables sin transformaciones.",
    "data/processed": "Datos refinados localmente (Silver/Gold) bajo esquemas validados, optimizados para consultas y entrenamiento de modelos.",
    "data/sandbox": "Entorno aislado para experimentación rápida de científicos de datos y arquitectos sin alterar zonas críticas.",
    "schemas": "Definiciones estrictas de esquemas (Avro, JSON Schema, DDL de SQL) para garantizar gobernanza y control de deriva de esquemas.",
    "scripts": "Scripts operativos del sistema (bash, make, powershell) para tareas de mantenimiento, sincronización de buckets y automatización local.",
    "logs": "Trazas locales de ejecución, auditorías de consultas y dumps de errores para análisis predictivo de fallas de pipelines."
}

# 2. Matriz de Ruteo Inteligente
ROUTING_MAP = {
    # Documentación y Diseño
    ".md": "docs/engineers_notes",
    ".pdf": "docs/technical_specs",
    ".drawio": "docs/architecture",
    ".png": "docs/architecture",
    # Código y Cómputo / IA
    ".ipynb": "03_Research_AI/Notebooks",
    ".py": "src/cloud_jobs",
    ".sql": "src/cloud_jobs",
    # Prompts / Inferencia IA
    ".prompt": "03_Research_AI/llm_prompts",
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

def init_project(base_path):
    """Inicializa la estructura de carpetas y escribe el EngineReadme.md explicativo."""
    root = Path(base_path)
    print(f"[*] Inicializando Directorio Thinking en: {root.resolve()}")
    
    # 1. Crear estructura de carpetas definida en el manifiesto
    for folder in FOLDER_MANIFEST.keys():
        folder_path = root / folder
        folder_path.mkdir(parents=True, exist_ok=True)
            
    # 2. Crear el Master README en 02_Foundation/Engine/EngineReadme.md
    engine_readme = root / "02_Foundation" / "Engine" / "EngineReadme.md"
    engine_readme.parent.mkdir(parents=True, exist_ok=True)
    
    project_title = root.resolve().name.upper() if root.resolve().name else "PROJECT"
    with open(engine_readme, "w", encoding="utf-8") as f:
        f.write(f"# {project_title} - Directorio Thinking Architecture\n\n")
        f.write("Estructura modular híbrida optimizada para Multi-Cloud (GCP, AWS, Azure, Fabric), IA/LLMs, Ingeniería de Datos e I+D.\n\n")
        f.write("> **Guía de Gobernanza para Agentes de IA y Desarrolladores:**\n")
        f.write("> Este documento define el propósito canónico de cada directorio. Los agentes deben consultar este manifiesto para ubicar o generar artefactos en su ruta correspondiente.\n\n")
        f.write("## Manifiesto de Gobernanza de Directorios\n\n")
        for folder, desc in FOLDER_MANIFEST.items():
            f.write(f"* **`{folder}/`**: {desc}\n")
        f.write("\n## Reglas de Ignorado Git (.gitignore)\n\n")
        f.write("```text\n")
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
        f.write("```\n")
        
    # 3. Crear el archivo .gitignore en la raíz del proyecto si no existe
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
            
    print("[+] Estructura Thinking Directory y EngineReadme.md desplegados exitosamente.")

def route_file(file_path, base_path, move=False):
    """Analiza la naturaleza de un archivo, sugiere su ubicación óptima o lo reubica físicamente."""
    src_file = Path(file_path)
    if not src_file.exists():
        print(f"[-] Error crítico: El archivo '{file_path}' no existe en el origen.")
        return
        
    ext = src_file.suffix.lower()
    dest_subfolder = ROUTING_MAP.get(ext)
    name_lower = src_file.name.lower()

    # Heurística contextual avanzada
    if ext == ".ipynb":
        dest_subfolder = "03_Research_AI/Notebooks"
    elif ext in [".py", ".sql"] and ("test" in name_lower or "spec" in name_lower):
        dest_subfolder = "tests"
    elif ext in [".md", ".txt", ".pdf"]:
        if "obsoleto" in name_lower or "historico" in name_lower or "old" in name_lower or "backup" in name_lower:
            dest_subfolder = "Artefactos/Planes/Historico_Obsoletos"
        elif "plan" in name_lower or "budget" in name_lower or "hitos" in name_lower:
            dest_subfolder = "Artefactos/Planes/Vigentes"
        elif "prompt" in name_lower or "system" in name_lower:
            dest_subfolder = "03_Research_AI/llm_prompts"
    elif not dest_subfolder:
        if "experiment" in name_lower or "benchmark" in name_lower or "poc" in name_lower:
            dest_subfolder = "03_Research_AI/experiments"
        elif "dashboard" in name_lower or "report" in name_lower or "viz" in name_lower:
            dest_subfolder = "src/dashboards"
        elif "gen" in name_lower or "mock" in name_lower or "synthetic" in name_lower:
            dest_subfolder = "src/data_generation"
        else:
            dest_subfolder = "Tools" # Repositorio por defecto seguro
            
    dest_dir = Path(base_path) / dest_subfolder
    dest_path = dest_dir / src_file.name
    
    print(f"\n[Análisis de Engine] Archivo detectado: '{src_file.name}'")
    print(f"  -> Clasificación por Extensión/Patrón: {ext if ext else 'Evaluación nominal'}")
    print(f"  -> Destino óptimo determinado: {dest_subfolder}/")
    
    if move:
        dest_dir.mkdir(parents=True, exist_ok=True)
        src_file.rename(dest_path)
        print(f"  [+] ACCIÓN: Archivo movido automáticamente a -> {dest_path}")
    else:
        print(f"  [Sugerencia] Para ejecutar la migración automatizada, añade el flag '--move'")
        print(f"  [Comando] python FWengine.py route \"{file_path}\" --move")

def main():
    parser = argparse.ArgumentParser(description="FWengine: Gobernanza, Automatización y Ruteo para Directorios Thinking")
    subparsers = parser.add_subparsers(dest="command", help="Comandos operativos")
    
    # Comando 'init'
    init_parser = subparsers.add_parser("init", help="Inicializa el andamiaje del proyecto con su manifiesto de gobernanza")
    init_parser.add_argument("path", nargs="?", default=".", help="Ruta de inicialización")
    
    # Comando 'route'
    route_parser = subparsers.add_parser("route", help="Determina y procesa la ubicación idónea de un elemento")
    route_parser.add_argument("file", help="Ruta del archivo a auditar/mover")
    route_parser.add_argument("--move", action="store_true", help="Fuerza la reubicación física instantánea del archivo")
    route_parser.add_argument("--base", default=".", help="Ruta base de la arquitectura")
    
    args = parser.parse_args()
    
    if args.command == "init":
        init_project(args.path)
    elif args.command == "route":
        route_file(args.file, args.base, args.move)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()