# AGENTS.md: Universal AI Coding Agent Governance & Context Engineering

Este repositorio está gobernado por la arquitectura **iDirectory v3.0** (creada por **Gravity HyperScale Thinking**), diseñada específicamente para maximizar la eficiencia y prevenir la degradación de la ventana de contexto (*Context Engineering*) en modelos de lenguaje (LLMs) y agentes autónomos (Google Gemini/Antigravity, Anthropic Claude Code, OpenAI/Codex, Cursor, Windsurf, Aider).

---

## 🚀 PROTOCOLO BOOTLOADER DE DOS NIVELES (TWO-TIER BOOTLOADER)

Para maximizar la eficiencia de tokens y prevenir la dispersión atencional (*Attention Sink / Context Drift*), los agentes de IA **DEBEN** operar bajo una arquitectura de dos niveles:

### 🔹 Tier 1: Operación Quirúrgica / Ejecución Atómica (Predeterminado)
Aplica a: resolución de bugs, edición de código puntual, refactor modular, creación de tests y tareas acotadas.
1. **Paso 0 (Regla Activa):** Este documento (`AGENTS.md`) define los invariantes y contratos del proyecto.
2. **Paso 1 (Radar Topológico Satelital):** Lee [`.context/tree.json`](./.context/tree.json). En menos de 500 tokens (o ~150 tokens con `python FWengine.py context --compact`) obtendrás el mapa satelital completo, roles y directivas de poda sin consumir miles de tokens listando directorios recursivamente.
   - **Variante focalizada (recomendada si la tarea está confinada a un subdominio):** `python FWengine.py map --slice <dir>` (< 150 tokens) sustituye la lectura completa de `tree.json`.
3. **Paso 2 (Semaforización Local / Herencia Jerárquica):** Antes de operar en un directorio objetivo (p. ej., `src/core/`), lee su microarchivo local `.context.yaml`. Si no existe físicamente, resuelve sus directivas por **herencia recursiva** del directorio padre más cercano.
4. **Paso 3 (Ejecución):** Modifica o genera código directamente.

> [!IMPORTANT]
> **POLÍTICA DE TOKEN BUDGET EN TIER 1:**
> Queda **estrictamente prohibida la precarga automática** de [`01_seed/seed-idirectory-master.md`](./01_seed/seed-idirectory-master.md) al inicio de Tier 1 (`tier1_preload: false`). El agente solo podrá consultar secciones específicas de la semilla si se activa el *Disparador 2* o *Disparador 3* de la matriz de decisión.

---

### 🔸 Tier 2: Planificación Arquitectónica / Auditoría Global / Refactor Mayor
Aplica a: auditorías integrales de madurez, reconstrucción estructural de módulos o comandos arquitectónicos explícitos.
- **Secuencia de Ingesta:** `AGENTS.md` -> `.context/tree.json` -> `01_seed/seed-idirectory-master.md` -> Beacons relevantes -> Ejecución.

---

### ⚖️ Matriz de Decisión de 3 Disparadores (¿Quién decide abrir la semilla?)

| Nivel | Disparador | Condición Objetiva | Acción del Agente |
| :--- | :--- | :--- | :--- |
| **Disparador 1 (Explícito)** | **Usuario** | Invocación de comandos (`/seedMaster`, `/metrics`, `/ultraThinking`, `/plan`) o requerimientos explícitos de rediseño arquitectónico integral. | **Tier 2:** Ingesta obligatoria del seed completo. |
| **Disparador 2 (Estructural)** | **Beacon** | El `.context.yaml` de la carpeta objetivo declara `seed_reference: required` (p. ej. en `01_seed/` o `artifacts/plans/metricsthinking/`). | Ingesta quirúrgica de la semilla. Si declara `seed_reference: optional`, **no se precarga**. |
| **Disparador 3 (Contingencia)** | **Agente** | Se detecta colisión de contratos con `schemas/` o necesidad de introducir una dependencia transversal no registrada en el beacon local. | **Lectura Quirúrgica:** Búsqueda puntual (`grep_search` o sección específica) sin volcar todo el archivo. |

---

### 🛡️ Invariantes de Filesystem y Poda
1. **Herencia Jerárquica de Poda:** Si un directorio ancestro declara `crawl: false` (como `data/raw`, `data/processed`, `logs/`, `artifacts/plans/archive/`), **ningún subdirectorio hijo podrá ser explorado o volcado al contexto**. La poda es estricta e inviolable.
2. **Contrato de Sincronización al Cierre:** Si durante una tarea el agente crea nuevos directorios o muta la topología física, **DEBE** ejecutar:
   ```powershell
   python FWengine.py audit --fix
   python FWengine.py beacon --sync
   python FWengine.py map --sync
   ```
   antes de dar la tarea por concluida.

> [!CAUTION]
> **PROHIBIDO EL ESCANEO CIEGO RECURSIVO:**
> Queda estrictamente prohibido ejecutar comandos de búsqueda masiva o listados recursivos sin filtro (`Get-ChildItem -Recurse`, `find .`, `ls -R`). Cualquier exploración debe estar guiada por `.context/tree.json`.
> Queda estrictamente prohibido ejecutar comandos de búsqueda masiva o listados recursivos sin filtro (`Get-ChildItem -Recurse`, `find .`, `ls -R`). Cualquier exploración debe estar guiada por `.context/tree.json`.
>
> Las carpetas con `crawl: false` en sus beacons (como `data/raw`, `data/processed`, `logs/`, `artifacts/plans/archive/`) son **ramas muertas o almacenes masivos**. No intentes volcar ni analizar su contenido.
>
> *Nota sobre `01_seed/`:* Posee `crawl: true`, `seed_reference: required` y `tier1_preload: false` para habilitar auditorías arquitectónicas en Tier 2 y `/seedMaster` sin violar `[INV-03]`.

---

## 🛠️ Herramienta CLI de Gobernanza: `FWengine.py` / `/idir`

Los agentes pueden interactuar con la gobernanza del proyecto mediante terminal o el comando rápido `/idir`:

### Acciones Soportadas:
1. **Auditoría de Gobernanza:**
   ```powershell
   python FWengine.py audit
   ```
2. **Ruteo y Clasificación Heurística de Archivos:**
   ```powershell
   python FWengine.py route "<ruta_del_archivo>"
   ```
3. **Reubicación Física Canónica:**
   ```powershell
   python FWengine.py route "<ruta_del_archivo>" --move
   ```
4. **Sincronización de Beacons (.context.yaml):**
   ```powershell
   python FWengine.py beacon --sync
   ```
5. **Telemetría de Contexto y Token Budget:**
   ```powershell
   python FWengine.py context --budget
   ```
6. **Subgrafo Focalizado (< 150 tokens):**
   ```powershell
   python FWengine.py map --slice <directorio>
   ```
7. **Auto-Remediación y Sincronización:**
   ```powershell
   python FWengine.py audit --fix
   ```

---

## 📌 Topología Canónica Normalizada (All-Lowercase)

- **`01_seed/`**: ADN arquitectónico del sistema (Ground Truth).
- **`02_foundation/engine/`**: Núcleo del framework y `engine_readme.md`.
- **`03_research/`**: Notebooks (`notebooks/`), prompts (`prompts/`) y experimentos (`experiments/`).
- **`src/`**: Pipelines de datos (`cloud_jobs/`), sintéticos (`data_generation/`), dashboards (`dashboards/`) y core (`core/`).
- **`artifacts/plans/`**: Planes vigentes (`active/`), evaluaciones de madurez (`metricsthinking/`) e históricos descartados (`archive/`).
- **`docs/`**: Especificaciones (`specs/`), notas y ADRs (`notes/`), arquitectura (`architecture/`).
- **`config/`**: Parámetros desacoplados y configuración de entorno.
- **`schemas/`**: Esquemas estrictos de datos (Avro, JSON Schema, DDL).
- **`data/`**: Capas Medallion locales ignoradas en Git y AI (`raw/`, `processed/`, `sandbox/`).
- **`tests/`**: Suites de pruebas unitarias e integración.
- **`tools/`**: Utilitarios internos y linters.
- **`scripts/`**: Automatización operativa de terminal.
- **`logs/`**: Trazas y auditorías locales.
- **`.context/`**: Mapa satelital (`tree.json`) y esquemas de Context Engineering.
