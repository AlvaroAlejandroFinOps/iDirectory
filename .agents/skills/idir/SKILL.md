---
name: idir
description: >-
  Ejecuta la gobernanza, Context Engineering y ruteo inteligente de archivos en la arquitectura iDirectory invocando FWengine.py.
  Permite inicializar la estructura (init), auditar/mover archivos (route), sincronizar beacons y consultar telemetría de tokens (context).
---

# Skill: /idir (Gobernanza y Context Engineering de iDirectory v3.0)

Esta habilidad proporciona el flujo para consultar, auditar, inicializar y clasificar elementos dentro de la estructura **iDirectory v3.0** gobernada por [`FWengine.py`](file:///d:/0001%20HyperScale%20Thinking/PROYECTOS%20CLOUD/iContext/iDirectory/FWengine.py).

---

## 1. Modos de Uso

### A. Inicializar / Sincronizar Estructura (`init`)
Inicializa la estructura modular de directorios, satélite `.context/tree.json`, beacons `.context.yaml` y `.agentignore`.

```powershell
python "d:\0001 HyperScale Thinking\PROYECTOS CLOUD\iContext\iDirectory\FWengine.py" init [ruta]
```

### B. Auditar / Clasificar Archivo (`route` sugerencia)
Analiza la extensión y patrones del nombre de un archivo para indicar en qué subdirectorio canónico debe residir.

```powershell
python "d:\0001 HyperScale Thinking\PROYECTOS CLOUD\iContext\iDirectory\FWengine.py" route "<ruta_al_archivo>"
```

### C. Mover Archivo Físicamente (`route --move`)
Reubica de forma automatizada un archivo a su subdirectorio óptimo.

```powershell
python "d:\0001 HyperScale Thinking\PROYECTOS CLOUD\iContext\iDirectory\FWengine.py" route "<ruta_al_archivo>" --move
```

### D. Sincronizar Context Beacons (`beacon --sync`)
Genera o actualiza los microarchivos `.context.yaml` en cada carpeta raíz.

```powershell
python "d:\0001 HyperScale Thinking\PROYECTOS CLOUD\iContext\iDirectory\FWengine.py" beacon --sync
```

### E. Telemetría de Tokens (`context --budget`)
Calcula el tamaño y tokens estimados por directorio para prevenir sobrecarga de contexto.

```powershell
python "d:\0001 HyperScale Thinking\PROYECTOS CLOUD\iContext\iDirectory\FWengine.py" context --budget
```

---

## 2. Matriz de Gobernanza Rápida (All-Lowercase)

| Tipo / Extensión | Subdirectorio de Destino | Descripción / Rol |
| :--- | :--- | :--- |
| `.ipynb` | `03_research/notebooks/` | Notebooks interactivos y EDA |
| `.py`, `.sql` (pipeline/job) | `src/cloud_jobs/` | PySpark, SQL y scripts de ETL |
| `.py`, `.sql` (tests/specs) | `tests/` | Pruebas unitarias y de calidad |
| `.prompt` | `03_research/prompts/` | System prompts y plantillas LLM |
| `.pbix`, `.pbip` | `src/dashboards/` | Tableros BI y visualización |
| `.yaml`, `.yml` | `config/` | Configuración y variables |
| `.json`, `.avsc` | `schemas/` | Contratos de datos y esquemas |
| `.tf` | `infrastructure/` | IaC (Terraform) |
| `.csv` | `data/raw/` | Zona Bronze local (crawl: false) |
| `.parquet`, `.delta` | `data/processed/` | Zona Silver/Gold local (crawl: false) |
| `.md`, `.txt`, `.pdf` (planes) | `artifacts/plans/` | `active/` vigentes, `metricsthinking/` evaluaciones, `archive/` descartados |
| `.md`, `.txt`, `.pdf` (doc) | `docs/` | `specs/`, `notes/`, `architecture/` |

---

## 3. Instrucciones de Ejecución para el Agente

1. Cuando el usuario invoque el comando `/idir` o solicite clasificar/mover archivos, ejecuta la acción invocando `FWengine.py` mediante el tool `run_command`.
2. Si el usuario pasa un argumento de archivo, ejecuta `route "<archivo>"`. Si incluye la intención de mover o reubicar, añade `--move`.
3. Reporta siempre al usuario la sugerencia o el resultado del movimiento del archivo.

