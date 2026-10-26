# Plan de Implementación v2: "Directorio Thinking" Multi-Cloud, IA y Datos

Basado en tus requerimientos exactos y retroalimentación, hemos reformulado por completo la propuesta para alinearse con tu visión de un **Directorio Thinking** modular, ordenado, creativo y orientado a proyectos de alta exigencia (Multi-cloud: GCP, AWS, Azure, Fabric, IA/LLMs, Ingeniería de Datos, Dashboards y Planes históricos).

---

## 1. Principios Clave de la Nueva Estructura

1. **`001_Seed/` prioritario en la cúspide:** Sigue intacto en la raíz para garantizar que el contexto inicial y la semilla del agente/arquitecto sea lo primero que se cargue y visualice.
2. **`01_Status/` eliminado:** Se descarta completamente por falta de uso.
3. **`02_Foundation/Engine/` centralizado:** Alberga el núcleo del framework, la explicación de la arquitectura y las plantillas.
4. **Extracción de `seed_template`:** Se elimina el bloque de texto hardcodeado en `FWengine.py` y se aloja en un archivo físico template independiente (`seed_template.md`).
5. **Incorporación de `03_Research_AI/`:** Espacio creativo de I+D con `Notebooks/`, `llm_prompts/` y `experiments/`.
6. **Multi-cloud unificado:** Sustitución de `src/fabric_jobs` por `src/cloud_jobs/` (o `src/cloud_workloads/`) que abarca Fabric, Databricks, GCP (BigQuery/Dataproc), AWS (Glue/EMR) y Azure.
7. **Estructuración de Planes en Artefactos:** División formal de `Artefactos/Planes/` en `Vigentes/` y `Historico_Obsoletos/` para conservar decisiones y planes evaluados.
8. **Ingeniería de Datos, BI y Visualizaciones:** Inclusión formal de `dashboards/` y refinamiento de capas de datos y software.

---

## 2. Topología Detallada del Directorio Thinking

```text
[Raíz del Proyecto]
│
├── 001_Seed/                               # Semilla de proyecto (Snapshot técnico ThinkingSeed_MasterHybrid.md)
│
├── 02_Foundation/
│   └── Engine/                             # Núcleo del framework, automatización, ruteo y manifiesto
│       ├── EngineReadme.md                 # Documentación y manifiesto del directorio
│       └── seed_template.md                # Plantilla maestra desacoplada de la semilla
│
├── 03_Research_AI/                         # Espacio creativo de I+D e Inteligencia Artificial
│   ├── Notebooks/                          # Notebooks exploratorios (Jupyter, Fabric, Databricks, Colab)
│   ├── llm_prompts/                        # System prompts, plantillas de inferencia y context trees
│   └── experiments/                        # PoCs, benchmarks de modelos y pruebas de concepto
│
├── src/                                    # Código fuente productivo y modular
│   ├── cloud_jobs/                         # Pipelines y Jobs Multi-cloud (Fabric PySpark, AWS Glue, GCP Dataproc/Dataflow, Azure)
│   ├── data_generation/                    # Simuladores y generación de datos sintéticos
│   ├── core/                               # Lógica de negocio, servicios backend y utilitarios comunes
│   └── dashboards/                         # Visualizaciones, apps de BI (Streamlit, Dash, PowerBI/PBIP, Looker)
│
├── data/                                   # Medallion Architecture / Datos Locales (ignorado en Git)
│   ├── raw/                                # Bronze: Fuentes crudas e inmutables
│   ├── processed/                          # Silver/Gold: Datos transformados, Delta, Parquet
│   └── sandbox/                            # Zona libre para experimentación y EDA
│
├── schemas/                                # Contratos de datos, DDL SQL, Avro, JSON Schemas
├── infrastructure/                         # IaC Multi-Cloud (Terraform, CloudFormation, Bicep, ARM)
├── config/                                 # Variables desacopladas de entorno (.yaml, .env templates)
│
├── tests/                                  # Testing unitario, integración y calidad de datos (Great Expectations)
│
├── Artefactos/                             # Entregables, presupuestos y planes estratégicos
│   └── Planes/
│       ├── Vigentes/                       # Planes actuales, capacidad (F-SKUs), arquitecturas activas
│       └── Historico_Obsoletos/            # Planes previos evaluados, descartados o históricos (respaldo)
│
├── docs/                                   # Documentación técnica viva
│   ├── architecture/                       # Diagramas de arquitectura C4, flujos multi-cloud
│   ├── technical_specs/                    # Especificaciones funcionales y no funcionales
│   └── engineers_notes/                    # Bitácoras de ingeniería, ADRs, post-mortems y RCA
│
├── Tools/                                  # Scripts auxiliares, linters y automatizaciones de entorno
├── scripts/                                # Automatización bash/powershell del sistema operativo
└── logs/                                   # Trazas locales de ejecución y auditoría
```

---

## 3. Plan de Cambios en Código (`FWengine.py`)

### A. Extracción del Template
1. Crear el archivo `Engine/seed_template.md` (o dentro de `02_Foundation/Engine/seed_template.md`) con el contenido actual de la semilla.
2. Eliminar la variable `SEED_TEMPLATE = """..."""` de `FWengine.py`.
3. Ajustar `save_seed_file()` para leer directamente el archivo `seed_template.md`. Si no existe, crearlo como plantilla inicial.

### B. Actualización de `FOLDER_MANIFEST`
Reemplazar el diccionario con la nueva topología:
- Eliminar `01_Status`.
- Reemplazar `Engine` por `02_Foundation/Engine`.
- Agregar `03_Research_AI/Notebooks`, `03_Research_AI/llm_prompts`, `03_Research_AI/experiments`.
- Reemplazar `src/fabric_jobs` por `src/cloud_jobs`.
- Agregar `src/core` y `src/dashboards`.
- Reemplazar `Artefactos/Planes` por `Artefactos/Planes/Vigentes` y `Artefactos/Planes/Historico_Obsoletos`.

### C. Ajuste de la Matriz de Ruteo (`ROUTING_MAP`)
- `.ipynb` -> `03_Research_AI/Notebooks`
- `.py`, `.sql` -> `src/cloud_jobs`
- Archivos de planes / presupuestos (`plan`, `budget`, `obsoleto`, `historico`) -> discriminación a `Artefactos/Planes/Vigentes` o `Historico_Obsoletos`.
- `.pbix`, `.pbip`, `.streamlit` -> `src/dashboards`

### D. Actualización de `EngineReadme.md`
- Actualizar el generador del `EngineReadme.md` para que documente la nueva estructura dividida lógicamente en su manifiesto.

---

## 4. Plan de Verificación

1. **Ejecución en seco (`init`):** Ejecutar `python FWengine.py init test_env` en un directorio temporal de prueba para comprobar la creación exacta de las carpetas y archivos.
2. **Validación del desacople de `seed_template.md`:** Verificar que `ThinkingSeed_MasterHybrid.md` se genere idéntico en `001_Seed/` leyendo desde `seed_template.md`.
3. **Prueba de Ruteo (`route`):** Probar el comando `route` con scripts `.py`, notebooks `.ipynb`, prompts `.txt/.md`, y planes para validar que se envíen a los nuevos destinos.
4. **Limpieza:** Eliminar `test_env` tras la validación exitosa.

---

¿Estás de acuerdo con este nuevo plan para proceder con la implementación en `FWengine.py` y `EngineReadme.md`?
