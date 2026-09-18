---
name: idir
description: >-
  Ejecuta la gobernanza y ruteo inteligente de archivos en la arquitectura del Directorio Thinking invocando FWengine.py.
  Permite inicializar la estructura del proyecto (init) o auditar/mover elementos a sus directorios óptimos (route).
---

# Skill: /idir (Gobernanza y Ruteo de Arquitectura Thinking)

Esta habilidad proporciona el flujo para consultar, inicializar y clasificar elementos dentro de la estructura **Directorio Thinking** gobernada por [`FWengine.py`](file:///d:/0001%20HyperScale%20Thinking/PROYECTOS%20CLOUD/iContext/iDirectory/FWengine.py).

---

## 1. Modos de Uso

### A. Inicializar Estructura (`init`)
Inicializa la estructura modular de directorios e interactúa creando el manifiesto `02_Foundation/Engine/EngineReadme.md` y `.gitignore`.

```powershell
python "d:\0001 HyperScale Thinking\PROYECTOS CLOUD\iContext\FrameWork\FWengine.py" init [ruta]
```

### B. Auditar / Clasificar Archivo (`route` sugerencia)
Analiza la extensión y patrones del nombre de un archivo para indicar en qué subdirectorio de gobernanza debe residir.

```powershell
python "d:\0001 HyperScale Thinking\PROYECTOS CLOUD\iContext\FrameWork\FWengine.py" route "<ruta_al_archivo>"
```

### C. Mover Archivo Físicamente (`route --move`)
Reubica de forma automatizada un archivo a su subdirectorio óptimo.

```powershell
python "d:\0001 HyperScale Thinking\PROYECTOS CLOUD\iContext\FrameWork\FWengine.py" route "<ruta_al_archivo>" --move
```

---

## 2. Matriz de Gobernanza Rápida

| Tipo / Extensión | Subdirectorio de Destino | Descripción |
| :--- | :--- | :--- |
| `.ipynb` | `03_Research_AI/Notebooks/` | Notebooks interactivos y EDA |
| `.py`, `.sql` (pipeline/job) | `src/cloud_jobs/` | PySpark, SQL y scripts de ETL |
| `.py`, `.sql` (tests/specs) | `tests/` | Pruebas unitarias y de calidad |
| `.prompt` | `03_Research_AI/llm_prompts/` | System prompts y plantillas LLM |
| `.pbix`, `.pbip` | `src/dashboards/` | Tableros BI y visualización |
| `.yaml`, `.yml` | `config/` | Configuración y variables |
| `.json`, `.avsc` | `schemas/` | Contratos de datos y esquemas |
| `.tf` | `infrastructure/` | IaC (Terraform) |
| `.csv` | `data/raw/` | Zona Bronze local |
| `.parquet`, `.delta` | `data/processed/` | Zona Silver/Gold local |
| `.md`, `.txt`, `.pdf` | `docs/` or `Artefactos/` | Documentación según palabras clave |

---

## 3. Instrucciones de Ejecución para el Agente

1. Cuando el usuario invoque el comando `/idir` o solicite clasificar/mover archivos, ejecuta la acción invocando `FWengine.py` mediante el tool `run_command`.
2. Si el usuario pasa un argumento de archivo, ejecuta `route "<archivo>"`. Si incluye la intención de mover o reubicar, añade `--move`.
3. Reporta siempre al usuario la sugerencia o el resultado del movimiento del archivo.
