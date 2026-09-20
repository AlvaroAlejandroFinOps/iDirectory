# AGENTS.md: Universal AI Coding Agent Governance & Context Engineering

Este repositorio está gobernado por la arquitectura **iDirectory v3.0** (creada por **Gravity HyperScale Thinking**), diseñada específicamente para maximizar la eficiencia y prevenir la degradación de la ventana de contexto (*Context Engineering*) en modelos de lenguaje (LLMs) y agentes autónomos (Google Gemini/Antigravity, Anthropic Claude Code, OpenAI/Codex, Cursor, Windsurf, Aider).

---

## 🚀 PROTOCOLO BOOTLOADER DE 4 PASOS (OBLIGATORIO)

Cualquier agente de IA que inicie operaciones en este repositorio **DEBE** respetar estrictamente el siguiente orden de ingesta secuencial antes de explorar o mutar código:

1. **Paso 0 (Regla Activa):** Este documento (`AGENTS.md`) define los invariantes y contratos inviolables del proyecto.
2. **Paso 1 (Radar Topológico Satelital):** Lee [`.context/tree.json`](file:///.context/tree.json). En tan solo ~250 tokens obtendrás el mapa satelital completo, roles y directivas de poda (`crawl: false`) sin consumir miles de tokens listando directorios recursivamente.
3. **Paso 2 (ADN del Proyecto / Ground Truth):** Lee [`01_seed/seed-idirectory-master.md`](file:///01_seed/seed-idirectory-master.md). Representa la memoria técnica, arquitectura y restricciones base.
4. **Paso 3 (Semaforización Local / Context Beacons):** Antes de operar en un directorio objetivo (p. ej., `src/cloud_jobs/`), lee su microarchivo local `.context.yaml` para conocer dependencias, relevancia y acciones prohibidas.

> [!CAUTION]
> **PROHIBIDO EL ESCANEO CIEGO RECURSIVO:**
> Queda estrictamente prohibido ejecutar comandos de búsqueda masiva o listados recursivos sin filtro (`Get-ChildItem -Recurse`, `find .`, `ls -R`). Cualquier exploración debe estar guiada por `.context/tree.json`.
>
> Las carpetas con `crawl: false` en sus beacons (como `data/raw`, `data/processed`, `logs/`, `artifacts/plans/archive/`) son **ramas muertas o almacenes masivos**. No intentes volcar ni analizar su contenido.

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
