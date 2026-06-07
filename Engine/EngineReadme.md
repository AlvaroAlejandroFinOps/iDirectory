#  - Data Architecture Infrastructure

Estructura corporativa optimizada para alta escala, trazabilidad interna y entornos Multi-cloud.

## Manifiesto de Gobernanza de Directorios

* **`src/data_generation/`**: Módulos de generación y simulación de datos sintéticos. Rigor matemático en distribuciones y volumetría estadística para pruebas de carga.
* **`src/fabric_jobs/`**: Scripts productivos, definiciones de pipelines y orquestación nativa para Microsoft Fabric (PySpark/Spark SQL Jobs).
* **`docs/technical_specs/`**: Especificaciones técnicas detalladas, mapeos de linaje de datos, contratos de esquemas y requerimientos no funcionales.
* **`docs/engineers_notes/`**: Bitácoras de ingeniería, registro de deuda técnica, decisiones de diseño rápido y análisis de causa raíz (RCA).
* **`docs/architecture/`**: Diagramas de arquitectura multi-cloud, flujos de datos e información estratégica de las capas Medallion (Bronze, Silver, Gold).
* **`tests/`**: Suites de pruebas unitarias, de integración y de calidad de datos (Great Expectations / deequ) para garantizar consistencia lógica.
* **`Notebooks/`**: Notebooks de desarrollo interactivo y experimentación (Jupyter/Fabric) para análisis exploratorio (EDA) y prototipos de algoritmos.
* **`Artefactos/Planes/`**: Planes de capacidad (F-SKUs), presupuestos de cómputo cloud, hitos del proyecto y documentación de gobernanza.
* **`Tools/`**: Scripts utilitarios internos, herramientas de automatización local, linters, y configuraciones de debugging personalizado.
* **`config/`**: Parámetros de entorno (dev, staging, prod), llaves de configuración de esquemas y variables de conexión desacopladas del código.
* **`infrastructure/`**: Scripts de Infraestructura como Código (IaC) utilizando AWS CDK, Terraform o plantillas ARM para aprovisionamiento multi-cloud.
* **`data/raw/`**: Zona de aterrizaje local (Bronze) para almacenamiento de fuentes de datos puras e inmutables sin transformaciones.
* **`data/processed/`**: Datos refinados localmente (Silver/Gold) bajo esquemas validados, optimizados para consultas y entrenamiento de modelos.
* **`data/sandbox/`**: Entorno aislado para experimentación rápida de científicos de datos y arquitectos sin alterar zonas críticas.
* **`schemas/`**: Definiciones estrictas de esquemas (Avro, JSON Schema, DDL de SQL) para garantizar gobernanza y control de deriva de esquemas.
* **`scripts/`**: Scripts operativos del sistema (bash, make) para tareas de mantenimiento, sincronización de buckets y automatización local.
* **`logs/`**: Trazas locales de ejecución, auditorías de consultas y dumps de errores para análisis predictivo de fallas de pipelines.
* **`Engine/`**: El núcleo del framework de automatización del proyecto (este motor). Contiene la lógica de ruteo, indexación y scaffolding.

## Instrucciones de Git para cada nuevo proyecto

Repites el paso 2 (git init + .gitignore propio).

```text
.venv/
__pycache__/
*.pyc
.ipynb_checkpoints/

# Ignorar archivos de datos
*.csv
*.parquet
```
