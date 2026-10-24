---
name: idir
description: >-
  Ejecuta la gobernanza, Context Engineering y ruteo inteligente de archivos en la arquitectura iDirectory invocando FWengine.py.
  Permite inicializar la estructura (init), auditar/mover archivos (route), auto-scaffold de beacons (audit --fix), subgrafos (map --slice) y enriquecimiento (enrich).
---

# Skill: /idir (Gobernanza y Context Engineering de iDirectory v3.2)

Esta habilidad proporciona el flujo para consultar, auditar, inicializar y clasificar elementos dentro de la estructura **iDirectory v3.2** gobernada por [`FWengine.py`](./FWengine.py).

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

### F. Auditoría con Auto-Remediación (`audit --fix`)
Detecta directorios sin `.context.yaml` (respetando `.agentignore` y `crawl: false`), los aprovisiona sin sobrescribir beacons existentes y regenera `tree.json`.

```powershell
python FWengine.py audit --fix
```

### G. Subgrafo Focalizado (`map --slice`)
Emite en < 150 tokens el nodo objetivo, su padre, hijos inmediatos y dependencias (`imports_from`). Úsalo en Tier 1 en lugar del `tree.json` completo cuando la tarea está confinada a un subdominio.

```powershell
python FWengine.py map --slice src/core
python FWengine.py map --slice src --radius 2
```

### H. Enriquecimiento Semántico (`/idir enrich <dir>`)
Protocolo agéntico (no es un subcomando de FWengine.py):
1. Ejecuta `python FWengine.py map --slice <dir>`. Si el nodo tiene `crawl: false`, **aborta**.
2. Lee solo las interfaces públicas del módulo (firmas, `__all__`, exports). Prohibido leer `data/`, `.env` o secretos.
3. Edita `<dir>/.context.yaml`: `purpose` + `instructions` ≤ 80 palabras en total; `key_files` como `"archivo.py: fn(a) -> b"` (≤ 160 chars por ítem, ≤ 6 ítems); `imports_from` / `exported_to` como listas planas de rutas relativas con `/`.
4. No anides diccionarios (MiniYAML no los parsea). No borres líneas `#`.
5. Ejecuta `python FWengine.py audit`; corrige cualquier `[WARN] Beacon inflado` (> 600 chars).

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
4. **Regla obligatoria de creación de carpetas:** tras crear o mover cualquier directorio, ejecuta `python FWengine.py audit --fix` (equivale a `beacon --sync` + `map --sync` para huérfanos). Ninguna tarea se da por terminada con directorios sin beacon.
