---
name: idir
description: >-
  Ejecuta la gobernanza, Context Engineering y ruteo inteligente de archivos en la arquitectura iDirectory invocando FWengine.py.
  Permite inicializar la estructura (init), auditar/mover archivos (route), sincronizar beacons y consultar telemetría de tokens (context).
---

# Skill: /idir (Gobernanza y Context Engineering de iDirectory v3.1)

Esta habilidad proporciona el flujo para consultar, auditar, inicializar y clasificar elementos dentro de la estructura **iDirectory v3.1** gobernada por [`FWengine.py`](./FWengine.py).

---

## 1. Modos de Uso

### A. Inicializar / Sincronizar Estructura (`init`)
Inicializa la estructura modular de directorios, satélite `.context/tree.json`, beacons `.context.yaml` y `.agentignore`.

```powershell
python FWengine.py init [ruta]
```

### B. Auditar / Clasificar Archivo (`route` sugerencia)
Analiza la extensión y patrones del nombre de un archivo para indicar en qué subdirectorio canónico debe residir.

```powershell
python FWengine.py route "<ruta_al_archivo>"
```

### C. Mover Archivo Físicamente (`route --move`)
Reubica de forma automatizada un archivo a su subdirectorio óptimo. Por defecto, protege contra colisiones destructivas si el destino ya existe (`FileExistsError`).

```powershell
python FWengine.py route "<ruta_al_archivo>" --move
```

Para permitir el reemplazo explícito en colisiones:
```powershell
python FWengine.py route "<ruta_al_archivo>" --move --overwrite
```

### D. Sincronizar Context Beacons (`beacon --sync`)
Genera o actualiza los microarchivos `.context.yaml` en cada carpeta raíz preservando comentarios manuales del usuario.

```powershell
python FWengine.py beacon --sync
```

### E. Telemetría de Tokens (`context --budget` / `context --compact`)
Calcula el tamaño y tokens estimados por directorio para prevenir sobrecarga de contexto, o emite el resumen ultracompacto para prompts (`~150 tokens`).

```powershell
python FWengine.py context --budget
python FWengine.py context --compact
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
| *Carpetas de dominio no canónicas* | Raíz descubierta (p. ej. `crates/`) | Auto-descubiertas como `role: domain_extension` en `tree.json` |

---

## 3. Instrucciones de Ejecución para el Agente

1. Cuando el usuario invoque el comando `/idir` o solicite clasificar/mover archivos, ejecuta la acción invocando `FWengine.py` mediante el tool `run_command`.
2. Si el usuario pasa un argumento de archivo, ejecuta `route "<archivo>"`. Si incluye la intención de mover o reubicar, añade `--move` (y `--overwrite` si solicitó sobrescribir).
3. Reporta siempre al usuario la sugerencia o el resultado del movimiento del archivo.

