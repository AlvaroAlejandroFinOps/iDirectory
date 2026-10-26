<SEED_ARCHITECTURAL_VECTOR version="3.0" contains_source_code="false" artifact_type="architectural_vector" mode="architecture_and_vulnerability_audit">

# THINKING SEED MASTER: iDirectory

> **[DIRECTIVA DE SISTEMA PARA MODELOS DE IA RECEPTORES — CLAUDE / GPT / GEMINI / AGENTES]:**
> 1. **Naturaleza del Artefacto:** Este documento es un **Vector Arquitectónico y Memoria Técnica (ThinkingSeed Master v3.0)** con `contains_source_code="false"`. **NO es el repositorio de código fuente completo** ni un volcado truncado. La ausencia de bloques de código de implementación es una **invariante deliberada de ingeniería** para maximizar la densidad semántica y preservar más del 99% de tu ventana de contexto.
> 2. **Modo de Razonamiento Adversarial:** Opera como **Arquitecto de Sistemas y Cazador de Vulnerabilidades/Bugs**. Utiliza las firmas simbólicas (Sección 4) y la superficie de tensión (Sección 7) para detectar condiciones de carrera, acoplamientos frágiles y casos borde antes de proponer cambios.
> 3. **Estado de Avance Real:** Los componentes etiquetados como `[FALTANTE]` o `[DEUDA]` reflejan el trabajo en progreso (WIP) real del proyecto, no defectos de este documento.

## Seed Changelog
- `2026-10-26 (v4.0)`: Reingeniería integral iDirectory v4.0 (Adaptive Context & Deterministic Control-Plane). Implementación de: (1) Fingerprint criptográfico determinista SHA-256 (`topology_hash`) en `./.context/tree.json` vía `compute_topology_hash()` inmune a distorsiones de `mtime`; (2) Poda estricta `crawl: false` en `compute_context_budget()` y estimador multimodal `estimate_tokens_v4()` que excluye binarios; (3) Bootloader Adaptativo de Dos Niveles y Tres Perfiles (Tier 1A, Tier 1B, Tier 2) gobernado por `./config/context_policy.json`; (4) Compilador de paquetes de contexto en un solo paso (`context --pack <dir> --tier 1a` < 220 tokens); (5) Navegación seccional del Seed Maestro (`seed --toc` y `seed --section <id>`); (6) Máquina de estados de continuidad atencional en `./.context/checkpoint.json` (`checkpoint --show/--set/--clear`); (7) Comando unificado e idempotente de cierre (`reconcile` y `reconcile --check`); (8) Esquemas formales Draft-07 ampliados (`checkpoint.schema.json`, `plan_metadata.schema.json`, `tree.schema.json` y `beacon.schema.json`). Expansión de la suite de pruebas a 68 tests automatizados (100% OK, 41.7s) incluyendo benchmark Tri-Baseline.
- `2026-10-24 (v3.5)`: Consolidación arquitectónica iDirectory v3.5 en commit `aeae4e4`. Verificación y sincronización de beacons estructurales en 31 nodos canónicos y de extensión (`02_foundation`, `03_research`, `artifacts`, `data`, `docs`, `infrastructure`, `src`). Integración estricta de validación formal en stdlib pura contra `./schemas/beacon.schema.json` y subgrafos condicionales en `./schemas/tree.schema.json`. Confirmación de 54 tests automatizados al 100% de tasa de éxito en 28.3s sin dependencias externas.
- `2026-10-24 (v3.3)`: Cierre integral de las 7 brechas forenses (`[GAP-01]` a `[GAP-07]`) detectadas en la auditoría post-v3.2: (1) Preservación automática de enriquecimiento agéntico (`purpose`, `instructions`, `key_files`, `imports_from`, `exported_to`) durante `sync_beacons()` con soporte para `--force-defaults`; (2) Simetría de des-escapado JSON en `MiniYAML._unquote()`; (3) Validación estructural de `.context.yaml` en stdlib pura (`validate_beacon_data()`) integrada en `audit_repository()` con auto-reparación en `--fix`; (4) Incorporación de `key_files` físicos locales y consumidores aguas abajo (`exported_to` -> `edge: "consumer"`) en `generate_sliced_tree()`; (5) Poda estricta `os.walk` en `check_satellite_freshness()` y `compute_context_budget()`; (6) Detección de mayúsculas en profundidad completa (`[INV-06]`). Suite ampliada a 54 tests (100% OK).
- `2026-10-24 (v3.2)`: Implementación integral del motor de auto-scaffolding reactivo de beacons (`[OBJ-01]`, `[OBJ-02]`, `[OBJ-03]`) en `FWengine.py`, erradicando la orfandad estructural de directorios mediante `discover_unbeaconed_directories()`, `scaffold_beacon_for_dir()`, `ensure_beacon_chain()` e integración atómica en `route_file()` y `audit --fix`. Fortalecimiento I/O contra bloqueos transitorios en Windows NTFS (`WinError 32/5`, `EACCES`, `EBUSY`) mediante `safe_io_retry()` con exponential backoff determinista y `safe_rename_casing()` con archivo temporal de dos pasos (`.tmp_{pid}_{name}`) y rollback atómico. Recorte topológico dinámico (`[OBJ-04]`) mediante `map --slice <dir>` generando subgrafos topológicos focalizados en `< 150 tokens` (>90% de compresión frente a `tree.json` completo). Formalización de esquemas: creación de `./schemas/beacon.schema.json` (Draft-07) para validación estricta de `.context.yaml` y extensión condicional de `./schemas/tree.schema.json` para subgrafos recortados. Protocolo agéntico `/idir enrich` para enriquecimiento semántico telegráfico con límite estricto de 600 caracteres (~150 tokens). Expansión de la suite de pruebas a 50 tests (37 en `test_fwengine.py` y 13 en `test_token_budget.py`) con tasa de éxito del 100%.
- `2026-10-21 (v3.1)`: Re-ingeniería completa de `FWengine.py` a v3.1 y sincronización con ThinkingSeed Master. Cierre integral de `BUG-01` a `BUG-04` y `DEBT-01` a `DEBT-04`. Desacoplamiento de `crawl: true` y `tier1_preload: false` en `01_seed/`, resolución dinámica de `key_files` vía `resolve_seed_key_files()`, auto-descubrimiento de carpetas de dominio (`domain_extension`), verificación física de casing en disco para NTFS/APFS vía `os.listdir()`, serialización compacta de `./.context/tree.json` (~824 tokens) superando el benchmark unitario de 1,000 tokens (95.9% de ahorro de contexto), formalización de `./schemas/tree.schema.json` (Draft-07), preservación de comentarios manuales `#` en `MiniYAML`, inspección de cabeceras AST (`max_chars=4096`), y protección anti-colisión en `route --move` mediante `--overwrite`. Expansión de la suite de pruebas a 31 tests unitarios en `test_fwengine.py` (35 totales en el repositorio) con tasa de éxito del 100%.
- `2026-10-21 (v3.0)`: Migración integral al estándar formal ThinkingSeed Master v3.0 con encapsulamiento XML determinista `<SEED_ARCHITECTURAL_VECTOR>`. Incorporación de firmas simbólicas AST de 1 línea para `./FWengine.py`, `./scripts/generate_benchmark_reports.py` y suites de test en `./tests/`. Integración de la matriz forense ampliada a 7 repositorios. Documentación adversarial de discrepancia en presupuesto de tokens de `./.context/tree.json` y schema `./schemas/tree.schema.json`.
- `2026-10-14`: Implementación del Two-Tier Bootloader con herencia jerárquica de beacons (`resolve_beacon`), filtro de encabezados de Python y telemetría de presupuesto de tokens.
- `2026-09-25`: Creación inicial de topología canónica normalizada en minúsculas y motor CLI de gobernanza con cero dependencias externas.

---

## 0. IDENTIDAD, METADATOS Y CONTRATO DEL RECEPTOR

```yaml
seed_schema_version: "3.0"
project_name: "iDirectory"
repository_name: "iDirectory"
project_type: "context_engineering_governance_framework"
repository_mode: "monorepo"
generated_at: "2026-10-26T17:55:00-03:00"
generated_by: "Antigravity (Gemini 3.8 Flash High)"
repository_root: "./"
git_branch: "master"
git_commit: "900989e"
working_tree_state: "dirty"
analysis_mode: "static+git+validated"
coverage_level: "high"
known_analysis_limits:
  - "El motor FWengine.py opera bajo restricción estricta Zero-Dependency (100% Python Standard Library)"
  - "La suite de pruebas ejecuta operaciones I/O en carpetas temporales del SO (%TEMP% o /tmp)"
  - "La estimación de tokens en compute_context_budget() utiliza heurística determinista (~4 chars/token)"
```

### 0.1 Instrucciones para el modelo receptor
1. **ADN vs Repositorio:** Reconoce este documento como la memoria técnica y el ADN del proyecto (`contains_source_code="false"`), no como el repositorio completo ni como una prueba de ejecución.
2. **Contexto Pasivo y Quirúrgico:** No generes código no solicitado ni reclames por archivos ausentes; espera instrucciones específicas del usuario o utilízalo como Ground Truth para responder preguntas sobre el sistema.
3. **Estado de Avance:** Considera que los componentes marcados como `[FALTANTE]` o `[DEUDA]` representan el avance real del proyecto y oportunidades de asistencia, no errores del documento.
4. **Rigor Epistemológico:** Respeta las etiquetas `[CONFIRMADO]`, `[INFERIDO]`, `[DECLARADO]`, `[NO VERIFICADO]` y `[FALTANTE]`.
5. **Portabilidad de Rutas:** Cita siempre rutas relativas a la raíz del repositorio (`./ruta/archivo`) con `/`. Prohibido emitir rutas locales absolutas o enlaces con esquema `file` local.
6. **Contratos Simbólicos:** Conserva arquitectura, firmas simbólicas (Sección 4) e invariantes (`[INV-01]` a `[INV-08]`).
7. **Postura Adversarial Constructiva:** Revisa siempre la Sección 7 (Superficie de Tensión) antes de proponer cambios.
8. **Seguridad Zero-Trust:** No reveles ni solicites secretos. Usa placeholders (`<REDACTED>`).

---

## 1. RESUMEN EJECUTIVO Y ALCANCE

### 1.1 Propósito y Misión del Sistema `[DECLARADO]`
`iDirectory` es un framework de gobernanza topológica y optimización atencional (*Adaptive Context Engineering*) concebido para repositorios de software, datos, nube e inteligencia artificial. Su propósito es erradicar la degradación cognitiva de modelos de lenguaje grande (LLMs) y agentes autónomos (*Attention Sink*, *Context Drift* y dilución atencional en capas de atención multi-head), garantizando tiempos de respuesta ultrarrápidos y una reducción drástica en costos de inferencia por turno (>95% de ahorro en tokens de contexto inicial).

### 1.2 El Problema Fundamental Resuelto `[CONFIRMADO]`
1. **Atrofia Atencional por Ingesta Masiva:** Prácticas comunes de agentes autoinyectando volcados completos o archivos de semilla masivos (~14,000 tokens) o ejecutando escaneos recursivos no acotados (`find .`, `Get-ChildItem -Recurse`) agotan el presupuesto de tokens e incrementan el ruido en hasta un 85%.
2. **Ambigüedad y Caos de Ruteo:** La dispersión de scripts en la raíz del repositorio, la mezcla de pruebas con código productivo y la falta de segregación Medallion provocan colisiones y generación de código inconsistente.
3. **Deriva Topológica (Satellite Drift):** Modificaciones físicas en el sistema de archivos que dejan mapas satelitales desactualizados, provocando alucinaciones del agente sobre ubicaciones inexistentes.

### 1.3 Consumidores Principales y Perfiles de Uso `[CONFIRMADO]`
- **Agentes Autónomos (Google Antigravity/Gemini, Claude Code, OpenAI Codex, Cursor, Windsurf, GitHub Copilot, Aider):** Consumen el mapa satelital `./.context/tree.json` en ~163 tokens compactos (o paquetes focalizados vía `context --pack <dir> --tier 1a` en < 220 tokens) y micro-beacons `./.context.yaml` locales para navegación quirúrgica sin alucinaciones.
- **Ingenieros de Datos y Arquitectos de Software:** Disponen de una estructura estandarizada con segregación de capas Medallion (`./data/raw/`, `./data/processed/`, `./data/sandbox/`), pipelines de nube (`./src/cloud_jobs/`), esquemas y contratos (`./schemas/`) y documentación técnica desacoplada.
- **Canales de CI/CD (GitHub Actions):** Validación determinista de salud topológica, paridad de beacons, consistencia de `topology_hash` y suites de pruebas mediante `./FWengine.py audit` y `unittest` sin requerir aprovisionamiento previo de librerías de terceros.

---

## 2. ARQUITECTURA, TOPOLOGÍA Y FRONTERAS MODULARES

### 2.1 Bootloader Adaptativo de Dos Niveles y Tres Perfiles (v4.0) `[CONFIRMADO]`
La arquitectura v4.0 implementa una selección adaptativa de tres perfiles operacionales regulada por la política única `./config/context_policy.json`:

```
                               ┌────────────────────────┐
                               │     Entrada Agente     │
                               └───────────┬────────────┘
                                           │
         ┌─────────────────────────────────┼─────────────────────────────────┐
         ▼                                 ▼                                 ▼
   [Tier 1A: Atómico]             [Tier 1B: Acotado]              [Tier 2: Global]
   Ruta Conocida / Bug            Multiarchivo / /plan            /seedMaster, /metrics,
   < 220 tokens                   < 800 tokens                    Rediseño Arquitectónico
   ──────────────────             ────────────────────            ───────────────────────
   1. context --pack <dir>        1. context --compact            1. AGENTS.md
      (subgrafo + beacon          2. map --slice <dir>            2. .context/tree.json
       + checkpoint)              3. seed --section <id>             (topology_hash)
   2. Edición quirúrgica          4. Modificación acotada         3. 01_seed/master.md (SEED)
   3. Seed precarga: PROHIBIDA    5. Checkpoint continuado        4. Beacons relevantes
                                                                  5. Ejecución global
```

#### Matriz de Decisión de Disparadores (¿Cuándo consultar el Seed?) `[DECLARADO]`
| Nivel | Disparador | Condición Objetiva | Acción del Agente |
| :--- | :--- | :--- | :--- |
| **Disparador 1 (Explícito)** | **Usuario** | Invocación de `/seedMaster`, `/metrics`, `/ultraThinking` o solicitud explícita de rediseño arquitectónico integral. (`/plan` inicia en **Tier 1B** y solo escala a Tier 2 si cruza múltiples dominios). | **Tier 2:** Ingesta del seed maestro completo. |
| **Disparador 2 (Estructural)** | **Beacon** | El `.context.yaml` de la carpeta objetivo declara `seed_reference: required` (p. ej. en `01_seed/`). | Ingesta quirúrgica de la semilla. Si declara `seed_reference: optional`, **no se precarga**. |
| **Disparador 3 (Contingencia)** | **Agente** | Colisión de contratos con `./schemas/` o introducción de una dependencia transversal no registrada. | **Lectura Seccional:** `python FWengine.py seed --toc` seguido de `python FWengine.py seed --section <id>`. |

### 2.2 Topología Canónica Normalizada (All-Lowercase) `[CONFIRMADO]`
El sistema impone nombres de directorios raíz estrictamente en minúsculas para prevenir discrepancias entre sistemas de archivos Case-Sensitive (Linux) y Case-Insensitive / Case-Preserving (Windows NTFS, macOS APFS):

| Directorio | Rol Canónico | Prio | Crawl | Seed Ref | Propósito / Responsabilidad |
| :--- | :--- | :---: | :---: | :---: | :--- |
| `./01_seed/` | `dna` | `p0` | `true` | `required` | Memoria técnica profunda y snapshots arquitectónicos ThinkingSeed Master (`tier1_preload: false`). |
| `./02_foundation/engine/` | `core_engine` | `p1` | `true` | `optional` | Núcleo del framework de automatización, lógica de ruteo e indexación (`./02_foundation/engine/engine_readme.md`). |
| `./03_research/notebooks/` | `eda` | `p2` | `false` | `optional` | Notebooks exploratorios interactivos (Jupyter, Colab, Databricks). |
| `./03_research/prompts/` | `prompt_engineering` | `p1` | `true` | `optional` | Plantillas de inferencia, árboles de contexto y system prompts para LLMs. |
| `./03_research/experiments/` | `pocs_benchmarks` | `p2` | `false` | `optional` | Pruebas de concepto algorítmicas, prototipos e I+D descartable. |
| `./src/cloud_jobs/` | `production_pipelines` | `p1` | `true` | `optional` | Scripts productivos de ETL/ELT y orquestación (PySpark, Glue, Dataproc, Synapse). |
| `./src/data_generation/` | `synthetic_data` | `p2` | `true` | `optional` | Generación y simulación de datos sintéticos con rigor probabilístico. |
| `./src/core/` | `shared_backend` | `p1` | `true` | `optional` | Lógica de negocio compartida, utilitarios de backend y clientes de servicios. |
| `./src/dashboards/` | `bi_viz` | `p2` | `true` | `optional` | Tableros de BI y aplicaciones interactivas (Streamlit, Dash, PowerBI, Looker). |
| `./artifacts/plans/active/` | `active_plans` | `p1` | `true` | `optional` | Planes de capacidad, presupuestos cloud e hitos operativos en curso (`plan_reingenieria_v4.md`). |
| `./artifacts/plans/metricsthinking/`| `metrics_evaluation`| `p2` | `true` | `required` | Evaluación forense de madurez y roadmap de remediación (`MetricsThinking.json`). |
| `./artifacts/plans/archive/` | `archived_plans` | `p3` | `false` | `optional` | Histórico de planes descartados y documentación obsoleta (rama muerta). |
| `./docs/architecture/` | `architecture_diagrams`| `p1` | `true` | `optional` | Diagramas de arquitectura multi-cloud, topologías C4 y flujos Medallion. |
| `./docs/specs/` | `technical_specs` | `p1` | `true` | `optional` | Especificaciones técnicas de negocio, linaje y requerimientos no funcionales. |
| `./docs/notes/` | `engineers_notes` | `p2` | `true` | `optional` | Bitácoras de ingeniería, ADRs rápidos y análisis de causa raíz (RCA). |
| `./config/` | `configuration` | `p1` | `true` | `optional` | Parámetros de entorno y política unificada de contexto (`context_policy.json`). |
| `./data/raw/` | `bronze_storage` | `p3` | `false` | `optional` | Capa Bronze inmutable de aterrizaje local. Ignorado en Git y AI. |
| `./data/processed/` | `silver_gold_storage` | `p3` | `false` | `optional` | Capas Silver y Gold transformadas en formatos binarios (Parquet, Delta). |
| `./data/sandbox/` | `sandbox` | `p3` | `false` | `optional` | Entorno de experimentación aislado para científicos de datos. |
| `./schemas/` | `data_contracts` | `p1` | `true` | `optional` | Esquemas estrictos Draft-07 (`tree`, `beacon`, `checkpoint`, `plan_metadata`). |
| `./scripts/` | `ops_automation` | `p2` | `true` | `optional` | Scripts operativos del sistema operativo para mantenimiento y despliegue. |
| `./tests/` | `test_suites` | `p1` | `true` | `optional` | Suites de pruebas unitarias, adversariales, estrés y token budget Tri-Baseline. |
| `./tools/` | `tooling` | `p2` | `true` | `optional` | Herramientas internas, linters y scripts auxiliares. |
| `./logs/` | `logs` | `p3` | `false` | `optional` | Trazas locales de ejecución y volcados de error (rama muerta). |
| `./.context/` | `context_engineering` | `p0` | `true` | `optional` | Mapa topológico satelital (`tree.json`), fingerprint SHA-256 y continuidad (`checkpoint.json`). |
| `./infrastructure/` | `domain_extension` | `p1` | `true` | `optional` | Plantillas de IaC (Terraform, Bicep, Pulumi) descubiertas dinámicamente. |

### 2.3 Reglas de Poda e Invariantes de Crawling `[CONFIRMADO]`
- **Herencia Jerárquica de Poda (`[INV-03]`):** Si un directorio o cualquiera de sus ancestros declara `crawl: false` (como `./data/raw/`, `./data/processed/`, `./data/sandbox/`, `./logs/`, `./artifacts/plans/archive/`), queda estrictamente prohibida la exploración o volcado recursivo por parte de agentes de IA.
- **Contrato de Cierre Unificado e Idempotente (`[INV-04]`):** Toda mutación física topológica impone la ejecución de un único comando idempotente de cierre:
  ```powershell
  python FWengine.py reconcile
  ```

---

## 3. FLUJOS DE EJECUCIÓN, ENTRY POINTS Y CICLO DE VIDA

### 3.1 Puntos de Entrada (Entry Points) `[CONFIRMADO]`
1. **Motor CLI Central (`./FWengine.py`):** CLI unificada sin librerías externas que proporciona los subcomandos `reconcile`, `context` (`--pack`, `--compact`, `--budget`), `seed` (`--toc`, `--section`), `checkpoint` (`--show`, `--set`, `--clear`), `map` (`--slice`, `--sync`), `beacon` (`--sync`, `--audit`), `route` y `audit` (`--fix`).
2. **Skill Agéntica (`./.agents/skills/idir/SKILL.md`):** Manifiesto ejecutable vía `/idir` que orquesta acciones de gobernanza desde interfaces agénticas.
3. **Flujo de Integración Continua (`./.github/workflows/ci.yml`):** Validador automatizado multiplataforma (Ubuntu, Windows, macOS) ejecutando auditorías de esquemas y suites unitarias.

### 3.2 Ciclos de Vida Operativos `[CONFIRMADO]`

#### Flujo 1: Paquete de Contexto Unificado Tier 1A (`FWengine.py context --pack <dir> --tier 1a`)
```
Directorio Objetivo -> Resuelve Beacon Ascendente -> Extrae Key Files Físicos
       │
       ├─► Genera Subgrafo Local (Padre + Hijos + Deps)
       ├─► Adjunta Estado Activo de Checkpoint (.context/checkpoint.json)
       └─► Retorna Payload JSON Compacto (< 220 tokens)
```

#### Flujo 2: Navegación Seccional del Seed Maestro (`FWengine.py seed --toc / --section`)
```
Requerimiento de Consulta de ADN Arquitectónico
       │
       ├─► FWengine.py seed --toc -> Retorna Índice Seccional con Líneas y Tokens
       └─► FWengine.py seed --section <id> -> Extrae Seccionalmente (< 1,200 tokens)
           (Evita volcar los ~14,000 tokens del Seed Maestro al contexto)
```

#### Flujo 3: Reconciliación y Cierre Idempotente (`FWengine.py reconcile`)
```
FWengine.py reconcile
       │
       ├─► Audita y Normaliza Nombres de Directorios (Minus.)
       ├─► Descubre y Auto-Scaffoldea Beacons Faltantes
       ├─► Valida Estructuralmente Beacons contra schemas/beacon.schema.json
       ├─► Computa Fingerprint Criptográfico SHA-256 (topology_hash)
       └─► Regenera Satélite .context/tree.json Actualizado
```

---

## 4. CONTRATOS SIMBÓLICOS, MODELO DE DATOS Y PERSISTENCIA

### 4.1 Firmas Simbólicas AST de 1 Línea `[CONFIRMADO]`

#### Módulo Central de Gobernanza: `./FWengine.py`
- `./FWengine.py::MiniYAML._unquote(raw: str) -> str` | Des-escapa comillas dobles y simples simétricamente mediante `json.loads` con fallback a slice `s[1:-1]`.
- `./FWengine.py::MiniYAML.dump(data: Dict[str, Any], prefix: str = "") -> str` | Serializador recursivo a YAML ligero; maneja escalares, listas y diccionarios indentados sin librerías externas.
- `./FWengine.py::MiniYAML.load(yaml_str: str) -> Dict[str, Any]` | Parser de YAML línea a línea para listas y pares clave-valor planos/anidados; soporta booleanos, enteros, floats y nulls.
- `./FWengine.py::_extract_markdown_frontmatter(md_path: pathlib.Path) -> Dict[str, Any]` | Extrae el bloque YAML frontmatter inicial de un archivo Markdown mediante `MiniYAML.load()`.
- `./FWengine.py::_has_dynamic_subdirectories(dir_path: pathlib.Path, root_path: pathlib.Path, patterns: List[str]) -> bool` | Detecta si un directorio gobernado aloja subcarpetas dinámicas que no son ignoradas ni podadas.
- `./FWengine.py::_is_transient_io_error(exc: BaseException) -> bool` | Identifica errores I/O transitorios de Windows NTFS (`WinError 5, 32, 33`) y POSIX (`EACCES`, `EBUSY`, `EAGAIN`).
- `./FWengine.py::_read_local_beacon(dir_path: pathlib.Path) -> Dict[str, Any]` | Lee directamente el archivo `.context.yaml` en el directorio sin realizar herencia ascendente.
- `./FWengine.py::_rel_posix(path: pathlib.Path, root_path: pathlib.Path) -> str` | Convierte una ruta de `Path` a cadena relativa normalizada estilo POSIX con separador `/`.
- `./FWengine.py::_resolve_beacon_fast(dir_path: pathlib.Path, root_path: pathlib.Path, beacon_cache: Optional[Dict[str, Dict[str, Any]]] = None) -> Dict[str, Any]` | Resuelve metadatos de baliza utilizando una caché en memoria para optimizar recorridos masivos.
- `./FWengine.py::_resolve_physical_rel_path(root_path: pathlib.Path, canonical_rel: str) -> str` | Resuelve el casing exacto físico en disco (insensible en NTFS/APFS) comparando componentes de ruta con `os.listdir()`.
- `./FWengine.py::audit_repository(root_path: pathlib.Path, fix: bool = False) -> bool` | Audita nombres de directorios (casing minúsculas), presencia y validez de esquema de beacons y frescura satelital; auto-remedia con `fix=True`.
- `./FWengine.py::build_context_pack(root_path: pathlib.Path, target_path: str, tier: str = "1a") -> Dict[str, Any]` | Empaqueta subgrafo local, directivas resueltas, `key_files` verificados y estado de checkpoint en un solo objeto (< 220 tokens).
- `./FWengine.py::check_satellite_freshness(root_path: pathlib.Path) -> Dict[str, Any]` | Comprueba si `.context/tree.json` está desfasado verificando `topology_hash` y marcas temporales de directorios clave.
- `./FWengine.py::compute_context_budget(root_path: pathlib.Path, include_pruned_stats: bool = False) -> List[Dict[str, Any]]` | Escanea directorios no podados estimando archivos, bytes y tokens (~4 caracteres/token) por nodo topológico.
- `./FWengine.py::compute_topology_hash(root_path: pathlib.Path) -> str` | Calcula un hash criptográfico SHA-256 determinista sobre el árbol topológico y metadatos de balizas.
- `./FWengine.py::discover_unbeaconed_directories(root_path: pathlib.Path) -> List[pathlib.Path]` | Realiza recorrido podado para descubrir directorios válidos que carecen de `.context.yaml` físico.
- `./FWengine.py::ensure_beacon_chain(target_dir: pathlib.Path, root_path: pathlib.Path) -> List[pathlib.Path]` | Garantiza que todos los directorios ancestros entre `root_path` y `target_dir` tengan un `.context.yaml` aprovisionado.
- `./FWengine.py::estimate_tokens_v4(text_or_path: Any, fast_stat_only: bool = False) -> int` | Estimador multimodal de tokens v4.0 que procesa rutas de texto, cadenas en memoria y excluye binarios.
- `./FWengine.py::extract_preserved_comments(beacon_file: pathlib.Path) -> List[str]` | Extrae líneas de comentarios manuales que inicien con `#` para preservarlas durante la resincronización de beacons.
- `./FWengine.py::extract_seed_section(root_path: pathlib.Path, query: str) -> str` | Extrae quirúrgicamente una sección específica del Seed Maestro por ID numérico o título sin cargar el documento entero.
- `./FWengine.py::format_compact_tree_json(data: Dict[str, Any]) -> str` | Serializa el mapa satelital en formato compacto JSON de un nodo por línea cumpliendo umbrales de compresión atencional (< 1,000 tokens).
- `./FWengine.py::format_sliced_tree(data: Dict[str, Any]) -> str` | Serializa el subgrafo recortado a JSON compacto en una sola línea.
- `./FWengine.py::generate_beacon_content(folder: str, meta: Dict[str, Any], root_path: Optional[pathlib.Path] = None) -> str` | Genera la cadena YAML formateada para un `.context.yaml` inyectando metadatos canónicos, `tier1_preload`, `key_files`, `imports_from` y `exported_to`.
- `./FWengine.py::generate_sliced_tree(root_path: pathlib.Path, target_path: str, radius: int = 1, max_children: int = 6) -> Dict[str, Any]` | Genera un subgrafo topológico recortado para `target_path` con dependencias, consumidores y aristas acotadas (< 150 tokens).
- `./FWengine.py::generate_tree_json(root_path: pathlib.Path) -> Dict[str, Any]` | Construye el diccionario estructurado del mapa satelital incorporando nodos canónicos, auto-descubrimiento, `topology_hash` y metadatos de bootloader.
- `./FWengine.py::get_seed_sections(root_path: pathlib.Path) -> List[Dict[str, Any]]` | Escanea el Seed Maestro y construye el índice estructurado de secciones con rangos de líneas y presupuesto de tokens estimado.
- `./FWengine.py::infer_beacon_meta(dir_path: pathlib.Path, root_path: pathlib.Path) -> Dict[str, Any]` | Infiere metadatos para un directorio no canónico basándose en el catálogo canónico o en el beacon del padre más cercano.
- `./FWengine.py::init_project(base_path: str) -> None` | Inicializa la topología canónica completa de iDirectory, desplegando carpetas, beacons, satélite, `.agentignore` y `.gitignore`.
- `./FWengine.py::inspect_python_header(file_path: pathlib.Path, max_chars: int = 4096) -> str` | Inspecciona AST de imports o texto inicial del archivo Python para clasificar su destino de ruteo (`tests`, `cloud_jobs`, `dashboards`, `core`).
- `./FWengine.py::is_ignored_path(dir_path: pathlib.Path, root_path: pathlib.Path, patterns: Optional[List[str]] = None) -> bool` | Determina si un directorio debe ser ignorado basándose en patrones de exclusión o carpetas ocultas (`.git`, `__pycache__`).
- `./FWengine.py::iter_beacon_files(root_path: pathlib.Path) -> List[pathlib.Path]` | Retorna lista de todos los archivos `.context.yaml` físicos en el árbol respetando directivas de poda y exclusión.
- `./FWengine.py::load_ignore_patterns(root_path: pathlib.Path) -> List[str]` | Carga y normaliza máscaras de exclusión de `.agentignore` y `.gitignore`.
- `./FWengine.py::main() -> None` | Dispatcher principal de CLI configurado con `argparse` para `reconcile`, `context`, `seed`, `checkpoint`, `map`, `beacon`, `route` y `audit`.
- `./FWengine.py::manage_checkpoint(root_path: pathlib.Path, action: str = "show", plan_id: Optional[str] = None, status: Optional[str] = None, phase: Optional[str] = None, next_action: Optional[str] = None, completed_step: Optional[str] = None) -> Dict[str, Any]` | Gestiona el archivo de continuidad atencional `.context/checkpoint.json` (< 300 tokens) para sesiones largas multi-fase.
- `./FWengine.py::reconcile_repository(root_path: pathlib.Path, check_only: bool = False) -> bool` | Punto de entrada unificado e idempotente de cierre: audita, aprovisiona balizas, valida esquemas y actualiza el satélite con `topology_hash`.
- `./FWengine.py::resolve_beacon(dir_path: pathlib.Path, root_path: pathlib.Path) -> Dict[str, Any]` | Resuelve recursivamente directivas de beacon mediante ascenso jerárquico; garantiza propagación de `crawl: false`.
- `./FWengine.py::resolve_seed_key_files(root_path: pathlib.Path) -> List[str]` | Localiza dinámicamente archivos `seed-*.md` existentes en `01_seed/` o genera `seed-{project_slug}-master.md` como fallback.
- `./FWengine.py::route_file(file_path: str, base_path: str = ".", move: bool = False, overwrite: bool = False) -> Optional[pathlib.Path]` | Clasifica y reubica atómicamente archivos con protección anti-colisión, reintento I/O y auto-scaffolding de beacons.
- `./FWengine.py::safe_io_retry(operation: Callable[[], Any], max_attempts: int = 4, initial_delay_ms: float = 25.0) -> Any` | Envoltorio con exponential backoff determinista para neutralizar bloqueos transitorios de I/O en disco.
- `./FWengine.py::safe_rename_casing(src: pathlib.Path, dest: pathlib.Path) -> pathlib.Path` | Renombrado atómico en dos pasos mediante archivo temporal `.tmp_{pid}_{name}` con rollback ante excepciones.
- `./FWengine.py::scaffold_beacon_for_dir(dir_path: pathlib.Path, root_path: pathlib.Path, overwrite: bool = False) -> Optional[pathlib.Path]` | Auto-scaffoldea `.context.yaml` para un directorio huérfano si no existe previamente o si `overwrite=True`.
- `./FWengine.py::sync_beacons(root_path: pathlib.Path, auto_discover: bool = True, force_defaults: bool = False) -> int` | Sincroniza micro-beacons preservando comentarios `#` y enriquecimiento agéntico salvo `force_defaults=True`; auto-descubre huérfanos.
- `./FWengine.py::sync_tree(root_path: pathlib.Path) -> pathlib.Path` | Serializa el mapa satelital en `./.context/tree.json` en formato compacto con `topology_hash`; retorna ruta del archivo generado.
- `./FWengine.py::validate_beacon_data(data: Dict[str, Any]) -> List[str]` | Valida en stdlib pura las claves obligatorias, tipos y enums de un `.context.yaml` frente a `schemas/beacon.schema.json`.
- `./FWengine.py::validate_tree_data(data: Dict[str, Any]) -> List[str]` | Valida en stdlib pura la estructura del mapa satelital (`tree.json`) o subgrafo recortado frente a `schemas/tree.schema.json`.

#### Módulo de Reportes Forenses: `./scripts/generate_benchmark_reports.py`
- `./scripts/generate_benchmark_reports.py::<module>() -> None` | Ingesta `./artifacts/benchmarks/benchmark_matrix.json` y materializa reportes periciales markdown individuales en `./artifacts/benchmarks/`.

#### Suites de Pruebas Automatizadas: `./tests/` (68 tests totales: 60 en `test_fwengine.py` + 8 en `test_token_budget.py`)
- `./tests/test_fwengine.py::TestMiniYAML` (5 tests)
- `./tests/test_fwengine.py::TestTopologicalManifest` (3 tests)
- `./tests/test_fwengine.py::TestRoutingMapAndHeuristics` (4 tests)
- `./tests/test_fwengine.py::TestLifecycleAndIdempotence` (7 tests)
- `./tests/test_fwengine.py::TestTokenBudgetComputation` (1 test)
- `./tests/test_fwengine.py::TestBeaconInheritance` (2 tests)
- `./tests/test_fwengine.py::TestHybridRouting` (5 tests)
- `./tests/test_fwengine.py::TestFileSystemHardening` (3 tests)
- `./tests/test_fwengine.py::TestSatelliteFreshness` (2 tests)
- `./tests/test_fwengine.py::TestNTFSIOResilience` (4 tests)
- `./tests/test_fwengine.py::TestAutoScaffoldAndRemediation` (9 tests)
- `./tests/test_fwengine.py::TestTreeSlicing` (3 tests)
- `./tests/test_fwengine.py::TestV4AdversarialAndContinuity` (12 tests)
- `./tests/test_token_budget.py::TestTokenBudgetBenchmark` (5 tests)
- `./tests/test_token_budget.py::TestTopologicalScalingStress` (3 tests)

### 4.2 Modelo de Datos y Esquemas Canónicos `[CONFIRMADO]`

#### Política Canónica de Contexto (`./config/context_policy.json`)
Fuente única de verdad de la política de Context Engineering (versión 4.0.0). Define los perfiles operacionales `tier_1a` (< 220 tokens), `tier_1b` (< 800 tokens) y `tier_2` (< 16,000 tokens), los presupuestos máximos de satélite, baliza y checkpoint, el contrato de cierre (`reconcile`), el orden estricto de precedencia documental (6 niveles) y la lista de adaptadores agénticos soportados.

#### Estructura del Satélite Topológico (`./.context/tree.json`)
- `$schema: "../schemas/tree.schema.json"` `[CONFIRMADO]`
- `version: "3.0"` `[CONFIRMADO]`
- `project: "iDirectory"` `[CONFIRMADO]`
- `architecture: "Gravity HyperScale Thinking"` `[CONFIRMADO]`
- `updated_at: str` (ISO-8601 UTC timestamp) `[CONFIRMADO]`
- `timestamp: float` (epoch unix timestamp) `[CONFIRMADO]`
- `topology_hash: str` (hash SHA-256 de 64 caracteres hex que valida la inmutabilidad física del árbol) `[CONFIRMADO]`
- `bootloader: Dict[str, List[str]]` (secuencias de ingesta para `tier_1` y `tier_2`) `[CONFIRMADO]`
- `nodes: Dict[str, NodeInfo]` (mapa de carpetas con `role`, `prio`, `crawl`, `seed_ref`, `tier1_preload`, `key_files`) `[CONFIRMADO]`

#### Estructura del Checkpoint de Continuidad (`./.context/checkpoint.json`)
Validado por `./schemas/checkpoint.schema.json` (Draft-07). Registra el plan activo (`plan_id`), estado (`draft`, `approved`, `executing`, `paused`, `completed`, `superseded`, `archived`), fase actual (`current_phase`), pasos completados (`completed_steps`), siguiente acción atómica (`next_action`), evidencias verificadas (`verified_evidence`), invariantes activas y marca de actualización (`updated_at`). Presupuesto: < 300 tokens.

#### Estructura de Metadatos de Planes (`./schemas/plan_metadata.schema.json`)
Validado por Draft-07. Inspecciona el frontmatter YAML de documentos en `artifacts/plans/` verificando `status`, `executable`, `supersedes` y `superseded_by` para prevenir la reactivación inadvertida de planes obsoletos.

#### Estructura de Micro-Balizas (`./schemas/beacon.schema.json`)
Validado por Draft-07 con `additionalProperties: false`. Restringe el tamaño máximo a 600 caracteres (~150 tokens) y valida tipos y enums de `version`, `directory`, `role`, `purpose`, `relevance`, `crawl`, `read_priority`, `seed_reference`, `token_density`, `instructions`, `key_files`, `imports_from` y `exported_to`.

---

## 5. CONFIGURACIÓN, ENTORNOS Y DEPENDENCIAS

### 5.1 Restricción Zero-Dependency `[INV-01]` `[CONFIRMADO]`
`FWengine.py` está diseñado para operar en entornos aislados, contenedores minimalistas, runners de CI/CD efímeros o máquinas de desarrolladores sin requerir `pip install` ni configurar entornos virtuales `.venv`.
- Dependencias utilizadas exclusivamente de la librería estándar: `os`, `sys`, `json`, `time`, `errno`, `fnmatch`, `argparse`, `datetime`, `pathlib`, `typing`, `unittest`, `ast`, `hashlib`.

### 5.2 Compatibilidad Multi-Plataforma `[CONFIRMADO]`
- **Sistemas Operativos Soportados:** Linux (Ubuntu 20.04+), Windows 10/11 / Windows Server, macOS (Ventura+).
- **Runtimes Validados en CI:** Python 3.10, 3.11, 3.12, 3.13.
- **Políticas de Codificación y File System:**
  - Codificación UTF-8 forzada en todas las operaciones de I/O (`encoding="utf-8"`).
  - Manejo de rutas normalizadas mediante `pathlib.Path` para neutralizar diferencias entre separadores `/` y `\`.

### 5.3 Archivos de Configuración y Exclusión `[CONFIRMADO]`
- `./config/context_policy.json`: Fuente única canónica de política de Context Engineering v4.0.0.
- `./.agentignore`: Define la máscara de exclusión de lectura para agentes autónomos (`./data/raw/`, `./data/processed/`, `./data/sandbox/`, `./logs/`, `*.parquet`, `*.csv`, `*.delta/`, `.venv/`, `__pycache__/`, `.git/`, `./artifacts/plans/archive/`).
- `./.gitignore`: Ignora artefactos efímeros, entornos virtuales y datasets locales pesados.

---

## 6. PRUEBAS, CI/CD, DESPLIEGUE Y OPERACIÓN

### 6.1 Suite Unitaria (`./tests/test_fwengine.py`) `[CONFIRMADO]`
Contiene 60 casos de prueba automatizados con un ratio de éxito de 100% (`OK`) (68 casos de prueba totales en el repositorio incluyendo benchmarks):
- Verificación de serialización y deserialización simétrica de `MiniYAML` con tipos primitivos complejos y comillas escapadas.
- Inicialización determinista del andamiaje de directorios y satélite con cálculo de `topology_hash`.
- Ruteo heurístico por extensión y verificación de inspección de cabeceras de Python vía `ast.parse()`.
- Mecanismo seguro de renombrado case-insensitive en Windows NTFS (`.tmp_{pid}_{name}`) con exponential backoff (`safe_io_retry`).
- Herencia jerárquica y prevalencia de `crawl: false` en `resolve_beacon()`.
- Rechazo frontal de intentos de Path Traversal (`PermissionError`).
- Resolución dinámica del nombre de seeds en repositorios externos (`test_dynamic_seed_name_resolution`).
- Auto-descubrimiento de carpetas de dominio no canónicas (`test_domain_extension_autodiscovery`).
- Validación de existencia física de contratos formales de satélite, beacons, checkpoints y planes.
- Auto-scaffolding de balizas huérfanas, preservación de enriquecimiento semántico y validación activa de esquemas.
- Recorte topológico dinámico en subgrafos con aristas `dep` y `consumer` (`TestTreeSlicing`).
- Pruebas adversariales v4.0: Validación de `compute_topology_hash()`, inyección compacta Tier 1A (`context --pack`), navegación seccional del Seed (`seed --toc` y `seed --section`), máquina de estados de `checkpoint` y reconciliación unificada (`reconcile`).

### 6.2 Benchmarks de Presupuesto de Tokens (`./tests/test_token_budget.py`) `[CONFIRMADO]`
Contiene 8 pruebas de telemetría y rendimiento que evalúan la compresión de contexto, densidad de balizas y presupuestos de subgrafos:
- Ahorro de contexto verificado: **95.5%** de reducción en tokens consumidos frente al escaneo recursivo ingenuo (`~20,297 tokens` vs `~908 tokens`).
- Benchmark Tri-Baseline verificado: Naive = 17,679 tokens, ModernIgnore = 383 tokens, Tier 1A Pack = **63 tokens**.
- Formato de inyección compacta (`IDIR_TOPOLOGY`): **~163 tokens** (cumpliendo holgadamente el umbral `< 250 tokens`).
- Subgrafos focalizados (`map --slice <dir>`): **~83 tokens** para subdirectorios (`src/core`), **~117 tokens** para ramas secundarias (`docs`), superando holgadamente el límite de `< 150 tokens`.
- Densidad de balizas: 100% de los archivos `.context.yaml` cumplen el límite de densidad estricta (`<= 600 caracteres` / `~150 tokens`).
- Latencia de generación satelital bajo estrés: **79.68 ms**; escaneo de budget: **174.00 ms**.

### 6.3 Pipeline de CI/CD (`./.github/workflows/ci.yml`) `[CONFIRMADO]`
Workflow automatizado activado en eventos `push` y `pull_request` sobre ramas `master` y `main`:
1. Matriz 3x4: 3 sistemas operativos (Ubuntu, Windows, macOS) x 4 versiones de Python (3.10 a 3.13).
2. Verificación de arquitectura Zero-Dependency.
3. Ejecución de reconciliación y auditoría de gobernanza: `python FWengine.py reconcile --check`.
4. Ejecución de suite unitaria: `python -m unittest discover -s tests -p "test_*.py" -v`.
5. Ejecución de benchmarks de token budget: `python -m unittest tests/test_token_budget.py -v`.

---

## 7. SUPERFICIE DE TENSIÓN, CONTRADICCIONES Y MODOS DE FALLA

Esta sección documenta de forma adversarial y objetiva los vectores de tensión reales, inconsistencias entre documentación y código, y riesgos operativos identificados en la auditoría física:

### 7.1 Parser YAML Minimalista sin Soporte para Estructuras Complejas `[CONFIRMADO]`
- **Vector de Riesgo:** `MiniYAML` es un serializador/parser artesanal de 60 líneas concebido para stdlib pura. No soporta multilínea con pipes (`|`, `>`), listas anidadas dentro de listas, diccionarios en línea (`{a: 1}`), o arrays compactos (`[x, y]`).
- **Modo de Falla:** Si un desarrollador o agente introduce sintaxis YAML avanzada manualmente en un `.context.yaml`, `MiniYAML.load()` omitirá o truncará las claves silenciosamente, pudiendo provocar corrupción en `sync_beacons()`.
- **Mitigación Activa:** `validate_beacon_data()` valida los tipos deserializados y `schemas/beacon.schema.json` con `additionalProperties: false` previene discrepancias de estructura en CI.

### 7.2 Límite de Renombrado Atómico entre Dispositivos Físicos Distintos (EXDEV) `[CONFIRMADO]`
- **Vector de Riesgo:** `safe_rename_casing()` y `route_file()` utilizan `Path.rename()`. En sistemas POSIX y Windows, renombrar archivos entre sistemas de archivos o particiones de disco distintas (o entre montajes NFS) lanza `OSError: [Errno 18] Invalid cross-device link` (`EXDEV`).
- **Modo de Falla:** Fallo en reubicación si un repositorio reside parcialmente en enlaces simbólicos que cruzan particiones o si la carpeta temporal del sistema de archivos no comparte el dispositivo físico del repo.
- **Mitigación Activa:** `route_file()` confina las operaciones estrictamente dentro del árbol relativo de `root_path`.

### 7.3 Imprecisión Heurística en el Estimador de Tokens `[CONFIRMADO]`
- **Vector de Riesgo:** `compute_context_budget()` y `estimate_tokens_v4()` calculan presupuestos asumiendo un divisor empírico de aproximadamente 4 caracteres por token (`chars // 4`).
- **Modo de Falla:** Para código en Python estándar o JSON esta aproximación oscila entre 3.6 y 4.2 chars/token. Sin embargo, para archivos Markdown enriquecidos con fórmulas LaTeX (`$$`), bloques Mermaid o texto multilingüe con caracteres no ASCII, el consumo real de tokens en BPE (Byte Pair Encoding) de Gemini o Claude puede ser entre un 15% y 30% superior al reportado.
- **Mitigación Activa:** Los umbrales de alerta operan con márgenes holgados de seguridad (límite satelital en 1,000 tokens vs 908 tokens reales; subgrafos en 150 vs 83 tokens; paquetes Tier 1A en 220 vs 63 tokens).

### 7.4 Sensibilidad de Casing y Bloqueos I/O en Windows NTFS `[RESUELTO EN v3.2]`
- **Estado:** En v3.2 se implementó `safe_io_retry()` con exponential backoff determinista (capturando `WinError 5, 32, 33`, `EACCES`, `EBUSY`, `EAGAIN`) y `safe_rename_casing()` con archivo temporal intermedio `.tmp_{pid}_{name}` y rollback atómico, eliminando excepciones por bloqueos transitorios de antivirus o indexadores de Windows Search.

### 7.5 Orfandad Estructural de Beacons en Nuevos Directorios `[RESUELTO EN v3.2]`
- **Estado:** Se implementó auto-scaffolding reactivo en `route_file()` mediante `ensure_beacon_chain()`, auto-descubrimiento de directorios huérfanos en `sync_beacons(auto_discover=True)` y auto-remediación inmediata mediante el comando unificado `python FWengine.py reconcile`.

### 7.6 Inflación de Contexto por Ingesta Global de Satélite `[RESUELTO EN v3.2/v4.0]`
- **Estado:** Se incorporó el recorte topológico dinámico (*Tree Slicing*) mediante `map --slice <dir>` (< 150 tokens) y el compilador de paquetes atómicos `context --pack <dir> --tier 1a` (< 220 tokens), erradicando la necesidad de cargar los 908 tokens del satélite completo para tareas locales identificadas.

---

## 8. SEGURIDAD, PRIVACIDAD Y GUARDRAILS

### 8.1 Blindaje contra Path Traversal `[CONFIRMADO]`
- En `route_file()`, cualquier entrada que contenga secuencias relativas hacia arriba (`..` en `raw_path.parts`) es bloqueada antes de interactuar con el sistema de archivos lanzando `PermissionError("[-] Error de Seguridad: Intento de Path Traversal bloqueado ('..' detectado en '...').")`.
- Se valida estrictamente mediante `path.resolve().relative_to(base_dir)` que tanto el origen como el destino resuelto permanezcan contenidos dentro del límite físico del repositorio.

### 8.2 Guardrails para Agentes de Inteligencia Artificial `[CONFIRMADO]`
1. **Prohibición de Escaneo Ciego Recursivo (`[INV-02]`):** Queda prohibida la ejecución de comandos de exploración profunda no restringidos (`Get-ChildItem -Recurse`, `find .`, `ls -R`). Toda navegación debe iniciar consultando `context --pack`, `context --compact`, o `.context/tree.json`.
2. **Invariante de Ramas Muertas (`[INV-03]`):** Los directorios con directiva `crawl: false` (`./data/raw/`, `./data/processed/`, `./data/sandbox/`, `./logs/`, `./artifacts/plans/archive/`) son considerados almacenes de datos o ramas muertas; los agentes tienen prohibido volcar su contenido al contexto.
3. **Contrato de Cierre Unificado e Idempotente (`[INV-04]`):** Cualquier cambio estructural en la topología física exige ejecutar `python FWengine.py reconcile` antes de dar la tarea por finalizada.
4. **Política Zero-Trust de Credenciales (`[INV-05]`):** Ofuscación estricta `<REDACTED>` para tokens, credenciales o API keys detectados en configuraciones o entornos locales.

---

## 9. ESTADO REAL, DEUDA TÉCNICA Y DECISIONES (ADRs)

### 9.1 Registro de Decisiones de Arquitectura (ADRs)

- `[ADR-001]` **Adopción de Topología All-Lowercase:** Se decidió forzar minúsculas en todos los directorios raíz para evitar inconsistencias de importación y colisiones de nombres entre Windows NTFS, macOS APFS y Linux ext4.
- `[ADR-002]` **Invariante Zero-Dependencies en Motor Core:** Se prohibió el uso de librerías de terceros (como `pyyaml`, `click` o `rich`) en `FWengine.py`, garantizando portabilidad instantánea en cualquier runner o contenedor con Python base.
- `[ADR-003]` **Arquitectura Two-Tier Bootloader:** Se desacopló la ingesta agéntica en dos niveles para erradicar el consumo innecesario de tokens de la semilla en tareas atómicas cotidianas (Tier 1).
- `[ADR-004]` **Herencia Jerárquica Ascendente (`resolve_beacon`):** Se implementó resolución recursiva hacia el directorio padre para garantizar cobertura de contexto del 100% incluso en árboles anidados sin beacons físicos locales.
- `[ADR-005]` **Inspección Híbrida de Código Fuente:** Se combinó el ruteo por extensión con una lectura preliminar ligera del encabezado (`inspect_python_header`) para desambiguar scripts de prueba, jobs cloud y tableros.
- `[ADR-006]` **Auto-Scaffolding Reactivo y Tree Slicing en CLI:** Se formalizó la auto-remediación topológica (`audit --fix`) y el recorte de subgrafos (`map --slice`) para mantener el mapa satelital sub-150 tokens.
- `[ADR-007]` **Bootloader Adaptativo de Tres Perfiles y Context Policy Desacoplada:** Se formalizó `./config/context_policy.json` estableciendo perfiles Tier 1A (Atómico, < 220t), Tier 1B (Acotado, < 800t) y Tier 2 (Global), eliminando el consumo innecesario del Seed Maestro en tareas acotadas.
- `[ADR-008]` **Continuidad Atencional y Checkpoints de Sesión:** Se introdujo `./.context/checkpoint.json` (< 300 tokens) gobernado por `manage_checkpoint()` para preservar el estado operacional en ejecuciones agénticas multi-fase.
- `[ADR-009]` **Fingerprint Criptográfico Topológico (`topology_hash`) y Reconciliación Unificada:** Se implementó SHA-256 determinista sobre el árbol topológico en `tree.json` y el comando de cierre `FWengine.py reconcile`.

### 9.2 Deuda Técnica Identificada y Priorizada `[DECLARADO]`

| ID | Componente | Severidad | Descripción de Deuda Técnica | Remediation Plan / Estado |
| :---: | :--- | :---: | :--- | :--- |
| `DEBT-01` | `./tests/test_token_budget.py` | **Alta** | Test unitario fallaba por discrepancia de tamaño de `tree.json` (1,019 tokens > 1,000 límite). | `[RESUELTO EN v3.1]` Formato JSON compacto por línea (< 1,000 tokens; 95.9% de ahorro verificado). |
| `DEBT-02` | `./schemas/tree.schema.json` | **Media** | Schema referenciado en `tree.json` no existía físicamente en el repositorio. | `[RESUELTO EN v3.1]` Materializado Draft-07 en `./schemas/tree.schema.json` y referenciado formalmente. |
| `DEBT-03` | `./FWengine.py` (MiniYAML) | **Baja** | Pérdida de comentarios `#` al serializar `.context.yaml`. | `[RESUELTO EN v3.1]` Implementada extracción y retención de comentarios manuales en `sync_beacons()`. |
| `DEBT-04` | `./FWengine.py` (route) | **Media** | Riesgo de sobrescritura destructiva sin backup al mover archivos con colisión de nombre. | `[RESUELTO EN v3.1]` Implementada protección `FileExistsError` y habilitación explícita vía flag `--overwrite`. |
| `DEBT-05` | `./FWengine.py` (beacon) | **Alta** | Orfandad estructural de balizas en carpetas creadas por agentes o SO sin beacon. | `[RESUELTO EN v3.2]` Auto-scaffolding reactivo en `route_file()`, `ensure_beacon_chain()` y `audit --fix`. |
| `DEBT-06` | `./FWengine.py` (casing/io) | **Media** | Bloqueos transitorios I/O en Windows NTFS (`WinError 32/5`) por antivirus o indexadores. | `[RESUELTO EN v3.2]` Implementado `safe_io_retry()` con exponential backoff y `safe_rename_casing()`. |
| `DEBT-07` | `./.context/tree.json` | **Media** | Inflación de contexto al leer mapa satelital global en tareas acotadas a subdominios. | `[RESUELTO EN v3.2/v4.0]` Recorte topológico dinámico `map --slice` (< 150t) y paquete Tier 1A `context --pack` (< 220t). |
| `DEBT-08` | `./schemas/beacon.schema.json` | **Media** | Ausencia de contrato formal de esquema JSON para balizas locales `.context.yaml`. | `[RESUELTO EN v3.2]` Creado `schemas/beacon.schema.json` (Draft-07); 100% de beacons validados. |
| `DEBT-09` | `./.context/checkpoint.json` | **Media** | Ausencia de mecanismo de persistencia para reanudar sesiones agénticas largas tras interrupción. | `[RESUELTO EN v4.0]` Implementada máquina de estados de checkpoint en stdlib con esquema formal Draft-07. |

---

## 10. REGLAS DE MODIFICACIÓN, GLOSARIO E ÍNDICE DE EVIDENCIAS

### 10.1 Invariantes del Sistema (System Invariants)
- `[INV-01]` **Zero External Dependencies:** `FWengine.py` debe compilar y ejecutarse exclusivamente con la librería estándar de Python 3.9+.
- `[INV-02]` **No Blind Recursive Scan:** Prohibida la búsqueda recursiva no acotada sin consultar `context --pack`, `context --compact` o `.context/tree.json`.
- `[INV-03]` **Crawl False Inviolability:** Carpetas con `crawl: false` jamás deben ser volcadas a la ventana de contexto de un agente.
- `[INV-04]` **Post-Mutation Synchronization:** Modificaciones de carpetas requieren la ejecución de `python FWengine.py reconcile`.
- `[INV-05]` **Zero Secret Leakage:** Prohibida la inclusión de credenciales en claro; aplicar `<REDACTED>`.
- `[INV-06]` **All-Lowercase Directories:** Todos los directorios gobernados deben nombrarse estrictamente en minúsculas.
- `[INV-07]` **Deterministic Adaptive Bootloader:** Prohibido autoinyectar el seed en Tier 1A a menos que se active uno de los 3 disparadores.
- `[INV-08]` **Relative Unix-Style Paths:** Todas las referencias documentales y de código deben usar rutas relativas con barra `/` (`./ruta/archivo`). Prohibido el uso de rutas absolutas locales o esquemas URI de archivo local.

### 10.2 Glosario Técnico
- **Bootloader Adaptativo:** Protocolo de arranque agéntico de dos niveles y tres perfiles (Tier 1A atómico, Tier 1B acotado y Tier 2 arquitectónico) para control estricto del presupuesto de tokens.
- **Context Engineering:** Metodología sistemática de diseño de repositorios de software para optimizar la atención de modelos de lenguaje y reducir tokens residuales.
- **Context Beacon (`.context.yaml`):** Microarchivo descriptor de semáforos, roles y directivas de poda ubicado en cada directorio gobernado.
- **Mapa Satelital (`tree.json`):** Representación topológica estructurada y ultraligera que describe todo el sistema en un solo archivo con fingerprint SHA-256 (`topology_hash`).
- **Satellite Drift:** Desincronización temporal entre la topología física del sistema de archivos y el mapa satelital.
- **Medallion Layers:** Arquitectura de datos de tres capas segregadas: Bronze (`data/raw`), Silver/Gold (`data/processed`) y Experimentación (`data/sandbox`).
- **Tree Slicing:** Recorte topológico dinámico que genera un subgrafo restringido al nodo en foco, su padre, sus hijos y sus dependencias en < 150 tokens.
- **Attentional Continuity Checkpoint (`checkpoint.json`):** Estructura formal que registra el plan activo, fase, pasos completados y siguiente acción para reanudar sesiones agénticas complejas en < 300 tokens.

### 10.3 Índice de Evidencias Físicas
- Motor de gobernanza y CLI: `./FWengine.py` `[CONFIRMADO]`
- Satélite topológico principal: `./.context/tree.json` `[CONFIRMADO]`
- Checkpoint de continuidad atencional: `./.context/checkpoint.json` `[CONFIRMADO]`
- Política canónica de contexto: `./config/context_policy.json` `[CONFIRMADO]`
- Esquema formal del satélite: `./schemas/tree.schema.json` `[CONFIRMADO]`
- Esquema formal de micro-balizas: `./schemas/beacon.schema.json` `[CONFIRMADO]`
- Esquema formal de checkpoint: `./schemas/checkpoint.schema.json` `[CONFIRMADO]`
- Esquema formal de planes: `./schemas/plan_metadata.schema.json` `[CONFIRMADO]`
- Manifiesto de skill agéntica: `./.agents/skills/idir/SKILL.md` `[CONFIRMADO]`
- Reglas de gobernanza para agentes: `./AGENTS.md` y `./GEMINI.md` `[CONFIRMADO]`
- Guía operativa del motor: `./02_foundation/engine/engine_readme.md` `[CONFIRMADO]`
- Suite de pruebas unitarias: `./tests/test_fwengine.py` `[CONFIRMADO]`
- Suite de pruebas de presupuesto de tokens: `./tests/test_token_budget.py` `[CONFIRMADO]`
- Flujo de integración continua: `./.github/workflows/ci.yml` `[CONFIRMADO]`
- Matriz de evaluación forense: `./artifacts/plans/metricsthinking/MetricsThinking.json` `[CONFIRMADO]`
- Matriz consolidada de benchmarks: `./artifacts/benchmarks/benchmark_matrix.json` `[CONFIRMADO]`
- Plan de reingeniería v4.0: `./artifacts/plans/active/plan_reingenieria_v4.md` `[CONFIRMADO]`

---

## 📌 CONTEXT HANDOFF & PROTOCOLO DE ASISTENCIA

> **Mensaje de orientación para el modelo de IA receptor:**
> "Esto es una semilla de proyecto (**ThinkingSeed Master v3.0**): el vector arquitectónico y ADN del proyecto (`contains_source_code="false"`), no su repositorio completo. Refleja el avance real, los contratos simbólicos y la superficie de tensión del sistema hasta la fecha. Como modelo receptor, tu función es usar esta semilla como memoria técnica para:
> 1. **Responder preguntas** sobre la arquitectura, contratos simbólicos, dependencias y flujos del sistema.
> 2. **Auditar riesgos y sugerir mejoras** evaluando activamente la Superficie de Tensión (Sección 7) y las áreas marcadas como `[DEUDA]` o `[FALTANTE]`.
> 3. **Generar código o soluciones compatibles** respetando las rutas relativas (`./`), firmas simbólicas e invariantes definidas aquí, cuando el usuario te lo solicite."

### Pautas de resolución:
Antes de resolver una solicitud:
1. Identifica el objetivo del usuario.
2. Localiza los componentes afectados usando las rutas relativas (`./`) del Seed.
3. Revisa restricciones (`[INV-01]` a `[INV-08]`), contratos simbólicos (Sección 4) y vectores de tensión (Sección 7).
4. Explicita supuestos cuando sea necesario: "Supongo que X debido a Y".
5. Propone cambios por archivo con rutas relativas claras y separadores Unix (`/`).
6. Añade pruebas, riesgos y criterios de aceptación.

### 🤝 Acuse de Recibo Inicial
Si el usuario adjuntó esta semilla **sin una instrucción específica**, no intentes generar código ni completar archivos vacíos. Responde únicamente con:
1. Un saludo confirmando que asimilaste el ADN arquitectónico v4.0 de **iDirectory** (`<SEED_ARCHITECTURAL_VECTOR>`) y su stack principal (Python Standard Library, Adaptive Context Engineering, Three-Profile Bootloader).
2. Un breve resumen de 2-3 líneas sobre el objetivo, su estado actual y sus principales vectores de tensión (resiliencia NTFS I/O mediante safe_io_retry, paquetes atómicos Tier 1A mediante context --pack, y reconciliación unificada mediante reconcile).
3. Una frase poniéndote a disposición para resolver dudas sobre su funcionamiento o colaborar en los siguientes pasos de desarrollo.

</SEED_ARCHITECTURAL_VECTOR>
