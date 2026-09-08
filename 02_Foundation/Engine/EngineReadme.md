# FRAMEWORK - Directorio Thinking Architecture

Estructura modular híbrida optimizada para Multi-Cloud (GCP, AWS, Azure, Fabric), IA/LLMs, Ingeniería de Datos e I+D.

> **Guía de Gobernanza para Agentes de IA y Desarrolladores:**
> Este documento define el propósito canónico de cada directorio. Los agentes deben consultar este manifiesto para ubicar o generar artefactos en su ruta correspondiente.

## Manifiesto de Gobernanza de Directorios

* **`001_Seed/`**: Seed (Semilla de proyecto y contexto primario para agentes de IA y arquitectos).
* **`02_Foundation/Engine/`**: Núcleo del framework de automatización del proyecto. Contiene la lógica de ruteo, indexación y EngineReadme.md de gobernanza.
* **`03_Research_AI/Notebooks/`**: Notebooks de desarrollo interactivo y experimentación (Jupyter/Fabric/Databricks/Colab) para análisis exploratorio (EDA) y algoritmos.
* **`03_Research_AI/llm_prompts/`**: Estructuras de prompts para LLMs, system prompts, árboles de contexto y plantillas de inferencia generativa.
* **`03_Research_AI/experiments/`**: Espacio de pruebas de concepto (PoCs), prototipos de modelos, I+D y benchmarks algorítmicos.
* **`src/cloud_jobs/`**: Scripts productivos, definiciones de pipelines y orquestación multi-cloud (Fabric PySpark, AWS Glue/EMR, GCP Dataproc/Dataflow, Azure Synapse).
* **`src/data_generation/`**: Módulos de generación y simulación de datos sintéticos. Rigor matemático en distribuciones y volumetría estadística para pruebas de carga.
* **`src/core/`**: Lógica de negocio transversal, servicios modulares, utilitarios de backend y componentes de desarrollo de software.
* **`src/dashboards/`**: Aplicaciones de visualización, tableros de BI, cuadros de mando interactivos (Streamlit, Dash, PowerBI, Looker).
* **`Artefactos/Planes/Vigentes/`**: Planes de capacidad activos (F-SKUs), presupuestos de cómputo cloud vigentes, hitos del proyecto y documentación activa.
* **`Artefactos/Planes/Historico_Obsoletos/`**: Histórico de planes evaluados, arquitecturas descartadas y documentación obsoleta preservada como respaldo y trazabilidad.
* **`docs/technical_specs/`**: Especificaciones técnicas detalladas, mapeos de linaje de datos, contratos de esquemas y requerimientos no funcionales.
* **`docs/engineers_notes/`**: Bitácoras de ingeniería, registro de deuda técnica, decisiones de diseño rápido y análisis de causa raíz (RCA).
* **`docs/architecture/`**: Diagramas de arquitectura multi-cloud, flujos de datos e información estratégica de las capas Medallion (Bronze, Silver, Gold).
* **`tests/`**: Suites de pruebas unitarias, de integración y de calidad de datos (Great Expectations / deequ) para garantizar consistencia lógica.
* **`Tools/`**: Scripts utilitarios internos, herramientas de automatización local, linters, y configuraciones de debugging personalizado.
* **`config/`**: Parámetros de entorno (dev, staging, prod), llaves de configuración de esquemas y variables de conexión desacopladas del código.
* **`infrastructure/`**: Scripts de Infraestructura como Código (IaC) utilizando AWS CDK, Terraform o plantillas ARM/Bicep para aprovisionamiento multi-cloud.
* **`data/raw/`**: Zona de aterrizaje local (Bronze) para almacenamiento de fuentes de datos puras e inmutables sin transformaciones.
* **`data/processed/`**: Datos refinados localmente (Silver/Gold) bajo esquemas validados, optimizados para consultas y entrenamiento de modelos.
* **`data/sandbox/`**: Entorno aislado para experimentación rápida de científicos de datos y arquitectos sin alterar zonas críticas.
* **`schemas/`**: Definiciones estrictas de esquemas (Avro, JSON Schema, DDL de SQL) para garantizar gobernanza y control de deriva de esquemas.
* **`scripts/`**: Scripts operativos del sistema (bash, make, powershell) para tareas de mantenimiento, sincronización de buckets y automatización local.
* **`logs/`**: Trazas locales de ejecución, auditorías de consultas y dumps de errores para análisis predictivo de fallas de pipelines.

## Reglas de Ignorado Git (.gitignore)

```text
.venv/
__pycache__/
*.pyc
.ipynb_checkpoints/

# Ignorar datos locales y logs
*.csv
*.parquet
logs/
data/raw/
data/processed/
data/sandbox/
```
