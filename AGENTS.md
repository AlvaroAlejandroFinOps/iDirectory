# AGENTS.md: Universal AI Coding Agent Governance & Context Engineering

Este repositorio está gobernado por la arquitectura **iDirectory v4.0** (creada por **Gravity HyperScale Thinking**), diseñada específicamente para maximizar la precisión contextual, garantizar continuidad atencional y prevenir la degradación de la ventana de contexto (*Context Engineering*) en modelos de lenguaje (LLMs) y agentes autónomos (Google Gemini/Antigravity, Anthropic Claude Code, OpenAI Codex, Cursor, Windsurf, GitHub Copilot, Aider).

> **Fuente Única de Política (`v4.0.0`):** [`./config/context_policy.json`](./config/context_policy.json)  
> **Orden de Precedencia Documental:** `1. Código ejecutable (FWengine.py) y Schemas (schemas/) -> 2. config/context_policy.json -> 3. Satélite (.context/tree.json) y Beacons (.context.yaml) -> 4. Checkpoint activo (.context/checkpoint.json) -> 5. Seed Maestro (01_seed/) -> 6. Planes activos vigentes (status: approved|executing)`.

---

## 🚀 BOOTLOADER ADAPTATIVO DE DOS NIVELES Y TRES PERFILES (v4.0)

Para maximizar la precisión contextual y evitar la dispersión atencional (*Attention Sink / Context Drift*), los agentes de IA **DEBEN** seleccionar el perfil mínimo suficiente según el alcance y riesgo de la tarea (no por el nombre lexical del comando):

### 🔹 Perfil Tier 1A: Operación Quirúrgica con Ruta Conocida (Predeterminado Atómico)
Aplica a: resolución de bugs, edición de código puntual, creación de tests o cambios en un subdominio identificado.
1. **Empaquetado en un solo paso (< 220 tokens):** Ejecuta `python FWengine.py context --pack <dir> --tier 1a` (o `python FWengine.py map --slice <dir>`). Obtendrás en una sola respuesta el subgrafo local, las directivas del beacon ya resueltas por herencia (`resolve_beacon`), los `key_files` verificados y el estado del checkpoint activo.
2. **Ejecución directa:** Abre únicamente los archivos relevantes del módulo y ejecuta pruebas focalizadas.
3. **Política de Seed:** **Prohibida la precarga** de [`./01_seed/seed-idirectory-master.md`](./01_seed/seed-idirectory-master.md) (`tier1_preload: false`).

### 🔹 Perfil Tier 1B: Cambio Multiarchivo o Planificación Acotada (Predeterminado para `/plan`)
Aplica a: refactorizaciones entre 2-3 módulos, adición de subcomandos o invocación de `/plan` sobre alcance acotado.
1. **Radar Compacto (~165 tokens):** Ejecuta `python FWengine.py context --compact` para orientación global rápida.
2. **Slices y Beacons Focalizados:** Ejecuta `python FWengine.py map --slice <dir>` sobre cada dominio afectado y consulta contratos en `./schemas/`.
3. **Consulta Seccional del Seed (< 1,200 tokens):** Si necesitas verificar contratos o invariantes transversales, consulta primero el índice con `python FWengine.py seed --toc` y extrae solo la sección requerida con `python FWengine.py seed --section <id>`.

### 🔸 Perfil Tier 2: Planificación Arquitectónica Global / Auditoría Forense Mayor
Aplica a: rediseño integral multi-dominio, cambios en invariantes fundamentales o comandos explícitos (`/seedMaster`, `/metrics`, `/ultraThinking`).
- **Secuencia de Ingesta:** `AGENTS.md` -> `./.context/tree.json` (verificando `topology_hash`) -> [`./01_seed/seed-idirectory-master.md`](./01_seed/seed-idirectory-master.md) -> Beacons de fronteras relevantes -> Ejecución.

---

### ⚖️ Matriz de Decisión de Disparadores (¿Cuándo consultar el Seed?)

| Nivel | Disparador | Condición Objetiva | Acción del Agente |
| :--- | :--- | :--- | :--- |
| **Disparador 1 (Explícito)** | **Usuario** | Invocación de `/seedMaster`, `/metrics`, `/ultraThinking` o solicitud explícita de rediseño arquitectónico integral. (`/plan` inicia en **Tier 1B** y solo escala a Tier 2 si cruza múltiples dominios). | **Tier 2:** Ingesta del seed maestro. |
| **Disparador 2 (Estructural)** | **Beacon** | El `.context.yaml` de la carpeta objetivo declara `seed_reference: required` (p. ej. en `01_seed/`). | Ingesta quirúrgica de la semilla. Si declara `seed_reference: optional`, **no se precarga**. |
| **Disparador 3 (Contingencia)** | **Agente** | Colisión de contratos con `./schemas/` o introducción de una dependencia transversal no registrada. | **Lectura Seccional:** `python FWengine.py seed --toc` seguido de `python FWengine.py seed --section <id>`. |

---

### 🛡️ Invariantes de Filesystem, Poda y Continuidad
1. **Herencia Jerárquica de Poda (`[INV-03]`):** Si un directorio ancestro declara `crawl: false` (como `data/raw`, `data/processed`, `data/sandbox`, `logs/`, `artifacts/plans/archive/`), **ningún subdirectorio hijo podrá ser explorado o volcado al contexto**.
2. **Continuidad Atencional en Sesiones Largas:** En planes multi-fase, registra y consulta el progreso en `./.context/checkpoint.json` (< 300 tokens) mediante `python FWengine.py checkpoint --show` o `--set`.
3. **Contrato de Cierre Unificado e Idempotente (`[INV-04]`):** Si durante una tarea creas directorios, mueves archivos o mutas la topología física, ejecuta un único comando antes de cerrar:
   ```powershell
   python FWengine.py reconcile
   ```

> [!CAUTION]
> **PROHIBIDO EL ESCANEO CIEGO RECURSIVO (`[INV-02]`):**
> Queda estrictamente prohibido ejecutar comandos de búsqueda masiva o listados recursivos sin filtro (`Get-ChildItem -Recurse`, `find .`, `ls -R`). Toda exploración debe guiarse por `context --pack`, `context --compact`, `map --slice` o `.context/tree.json`.

---

## 🛠️ Herramienta CLI de Gobernanza: `FWengine.py` v4.0 / `/idir`

1. **Cierre y Reconciliación Unificada (Idempotente):**
   ```powershell
   python FWengine.py reconcile
   python FWengine.py reconcile --check
   ```
2. **Paquete de Contexto Unificado Tier 1A (< 220 tokens):**
   ```powershell
   python FWengine.py context --pack <directorio> --tier 1a
   ```
3. **Subgrafo Focalizado (< 150 tokens):**
   ```powershell
   python FWengine.py map --slice <directorio>
   ```
4. **Consulta Seccional del Seed Maestro:**
   ```powershell
   python FWengine.py seed --toc
   python FWengine.py seed --section <id_o_titulo>
   ```
5. **Checkpoints de Continuidad Atencional (< 300 tokens):**
   ```powershell
   python FWengine.py checkpoint --show
   python FWengine.py checkpoint --set --plan-id "<id>" --phase "P1" --next "<accion>"
   ```
6. **Ruteo y Reubicación Física Canónica:**
   ```powershell
   python FWengine.py route "<ruta_del_archivo>" --move
   ```
7. **Telemetría de Contexto y Token Budget:**
   ```powershell
   python FWengine.py context --budget
   python FWengine.py context --compact
   ```
8. **Auditoría Estricta de Gobernanza:**
   ```powershell
   python FWengine.py audit
   python FWengine.py audit --fix
   ```

---

## 📌 Topología Canónica Normalizada (All-Lowercase)

- **`01_seed/`**: ADN arquitectónico del sistema (Ground Truth; consulta vía `seed --toc` / `--section`).
- **`02_foundation/engine/`**: Núcleo del framework y `engine_readme.md`.
- **`03_research/`**: Notebooks (`notebooks/`), prompts (`prompts/`) y experimentos (`experiments/`).
- **`src/`**: Pipelines de datos (`cloud_jobs/`), sintéticos (`data_generation/`), dashboards (`dashboards/`) y core (`core/`).
- **`artifacts/plans/`**: Planes vigentes (`active/`), evaluaciones de madurez (`metricsthinking/`) e históricos descartados (`archive/`).
- **`docs/`**: Especificaciones (`specs/`), notas y ADRs (`notes/`), arquitectura (`architecture/`).
- **`config/`**: Parámetros desacoplados y política canónica (`context_policy.json`).
- **`schemas/`**: Esquemas estrictos JSON Schema (`tree.schema.json`, `beacon.schema.json`, `checkpoint.schema.json`, `plan_metadata.schema.json`).
- **`data/`**: Capas Medallion locales podadas en Git y AI (`raw/`, `processed/`, `sandbox/`).
- **`tests/`**: Suites de pruebas unitarias, adversariales y benchmarks Tri-Baseline.
- **`tools/`**: Utilitarios internos y linters.
- **`scripts/`**: Automatización operativa de terminal.
- **`logs/`**: Trazas y auditorías locales (`crawl: false`).
- **`.context/`**: Mapa satelital verificable (`tree.json` con `topology_hash`) y continuidad (`checkpoint.json`).
