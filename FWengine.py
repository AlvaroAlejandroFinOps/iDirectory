#!/usr/bin/env python3
import os
import sys
import argparse
from pathlib import Path

# 1. Manifiesto Centralizado de Gobernanza (Estructura expandida)
FOLDER_MANIFEST = {
    "001_Seed": "Seed (Semilla de proyecto.",
    "01_Status": "Carpeta para detallar los avances del proyecto y registrar el estado y reportes de desempeño.",
    "src/data_generation": "Módulos de generación y simulación de datos sintéticos. Rigor matemático en distribuciones y volumetría estadística para pruebas de carga.",
    "src/fabric_jobs": "Scripts productivos, definiciones de pipelines y orquestación nativa para Microsoft Fabric (PySpark/Spark SQL Jobs).",
    "docs/technical_specs": "Especificaciones técnicas detalladas, mapeos de linaje de datos, contratos de esquemas y requerimientos no funcionales.",
    "docs/engineers_notes": "Bitácoras de ingeniería, registro de deuda técnica, decisiones de diseño rápido y análisis de causa raíz (RCA).",
    "docs/architecture": "Diagramas de arquitectura multi-cloud, flujos de datos e información estratégica de las capas Medallion (Bronze, Silver, Gold).",
    "tests": "Suites de pruebas unitarias, de integración y de calidad de datos (Great Expectations / deequ) para garantizar consistencia lógica.",
    "Notebooks": "Notebooks de desarrollo interactivo y experimentación (Jupyter/Fabric) para análisis exploratorio (EDA) y prototipos de algoritmos.",
    "Artefactos/Planes": "Planes de capacidad (F-SKUs), presupuestos de cómputo cloud, hitos del proyecto y documentación de gobernanza.",
    "Tools": "Scripts utilitarios internos, herramientas de automatización local, linters, y configuraciones de debugging personalizado.",
    "config": "Parámetros de entorno (dev, staging, prod), llaves de configuración de esquemas y variables de conexión desacopladas del código.",
    "infrastructure": "Scripts de Infraestructura como Código (IaC) utilizando AWS CDK, Terraform o plantillas ARM para aprovisionamiento multi-cloud.",
    "data/raw": "Zona de aterrizaje local (Bronze) para almacenamiento de fuentes de datos puras e inmutables sin transformaciones.",
    "data/processed": "Datos refinados localmente (Silver/Gold) bajo esquemas validados, optimizados para consultas y entrenamiento de modelos.",
    "data/sandbox": "Entorno aislado para experimentación rápida de científicos de datos y arquitectos sin alterar zonas críticas.",
    "schemas": "Definiciones estrictas de esquemas (Avro, JSON Schema, DDL de SQL) para garantizar gobernanza y control de deriva de esquemas.",
    "scripts": "Scripts operativos del sistema (bash, make) para tareas de mantenimiento, sincronización de buckets y automatización local.",
    "logs": "Trazas locales de ejecución, auditorías de consultas y dumps de errores para análisis predictivo de fallas de pipelines.",
    "Engine": "El núcleo del framework de automatización del proyecto (este motor). Contiene la lógica de ruteo, indexación y scaffolding."
}

# 2. Matriz de Ruteo Inteligente
ROUTING_MAP = {
    # Documentación y Diseño
    ".md": "docs/engineers_notes",
    ".pdf": "docs/technical_specs",
    ".drawio": "docs/architecture",
    ".png": "docs/architecture",
    # Código y Cómputo
    ".ipynb": "Notebooks",
    ".py": "src/fabric_jobs",
    ".sql": "src/fabric_jobs",
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
    """Inicializa la estructura de carpetas y escribe un README.md explicativo en cada una."""
    root = Path(base_path)
    print(f"[*] Inicializando arquitectura de datos en: {root.resolve()}")
    
    # Crear estructura de carpetas
    for folder, desc in FOLDER_MANIFEST.items():
        folder_path = root / folder
        folder_path.mkdir(parents=True, exist_ok=True)
            
    # Crear el Master README en la carpeta Engine con el nombre EngineReadme.md
    engine_readme = root / "Engine" / "EngineReadme.md"
    with open(engine_readme, "w", encoding="utf-8") as f:
        f.write(f"# {root.name.upper()} - Data Architecture Infrastructure\n\n")
        f.write("Estructura corporativa optimizada para alta escala, trazabilidad interna y entornos Multi-cloud.\n\n")
        f.write("## Manifiesto de Gobernanza de Directorios\n\n")
        for folder, desc in FOLDER_MANIFEST.items():
            f.write(f"* **`{folder}/`**: {desc}\n")
        f.write("\n## Instrucciones de Git para cada nuevo proyecto\n\n")
        f.write("Repites el paso 2 (git init + .gitignore propio).\n\n")
        f.write("```text\n")
        f.write(".venv/\n")
        f.write("__pycache__/\n")
        f.write("*.pyc\n")
        f.write(".ipynb_checkpoints/\n\n")
        f.write("# Ignorar archivos de datos\n")
        f.write("*.csv\n")
        f.write("*.parquet\n")
        f.write("```\n")
        
    # Crear el archivo .gitignore automáticamente en la raíz del proyectoss
    gitignore_path = root / ".gitignore"
    with open(gitignore_path, "w", encoding="utf-8") as f:
        f.write(".venv/\n")
        f.write("__pycache__/\n")
        f.write("*.pyc\n")
        f.write(".ipynb_checkpoints/\n\n")
        f.write("# Ignorar archivos de datos\n")
        f.write("*.csv\n")
        f.write("*.parquet\n")
            
    print("[+] Estructura completa y manifiestos markdown (.md) desplegados exitosamente.")

def route_file(file_path, base_path, move=False):
    """Analiza la naturaleza de un archivo, sugiere su ubicación o lo automatiza físicamente."""
    src_file = Path(file_path)
    if not src_file.exists():
        print(f"[-] Error crítico: El archivo '{file_path}' no existe en el origen.")
        return
        
    ext = src_file.suffix.lower()
    dest_subfolder = ROUTING_MAP.get(ext)
    
    # Heurística avanzada por patrones si la extensión es genérica o ambiguas
    if not dest_subfolder:
        name_lower = src_file.name.lower()
        if "test" in name_lower or "spec" in name_lower:
            dest_subfolder = "tests"
        elif "plan" in name_lower or "budget" in name_lower or "hitos" in name_lower:
            dest_subfolder = "Artefactos/Planes"
        elif "gen" in name_lower or "mock" in name_lower:
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
        print(f"  [Comando] python3 Engine/engine.py route \"{file_path}\" --move")

def main():
    parser = argparse.ArgumentParser(description="Engine v1.0: Automatización, Gobernanza y Ruteo de Datos")
    subparsers = parser.add_subparsers(dest="command", help="Comandos operativos")
    
    # Comando 'init'
    init_parser = subparsers.add_parser("init", help="Inicializa el andamiaje del proyecto con su metadata .md")
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