<SEED_ARCHITECTURAL_VECTOR version="3.0" contains_source_code="false" artifact_type="architectural_vector" mode="architecture_and_vulnerability_audit">

# THINKING SEED MASTER: iDirectory

> **[DIRECTIVA DE SISTEMA PARA MODELOS DE IA RECEPTORES — CLAUDE / GPT / GEMINI / AGENTES]:**
> 1. **Naturaleza del Artefacto:** Este documento es un **Vector Arquitectónico y Memoria Técnica (ThinkingSeed Master v3.0)** con `contains_source_code="false"`. **NO es el repositorio de código fuente completo** ni un volcado truncado. La ausencia de bloques de código de implementación es una **invariante deliberada de ingeniería** para maximizar la densidad semántica y preservar más del 99% de tu ventana de contexto.
> 2. **Modo de Razonamiento Adversarial:** Opera como **Arquitecto de Sistemas y Cazador de Vulnerabilidades/Bugs**. Utiliza las firmas simbólicas (Sección 4) y la superficie de tensión (Sección 7) para detectar condiciones de carrera, acoplamientos frágiles y casos borde antes de proponer cambios.
> 3. **Estado de Avance Real:** Los componentes etiquetados como `[FALTANTE]` o `[DEUDA]` reflejan el trabajo en progreso (WIP) real del proyecto, no defectos de este documento.

## Seed Changelog
- `2026-10-24 (v3.5)`: Consolidación arquitectónica iDirectory v3.5 en commit `aeae4e4`. Verificación y sincronización de beacons estructurales en 31 nodos canónicos y de extensión (`02_foundation`, `03_research`, `artifacts`, `data`, `docs`, `infrastructure`, `src`). Integración estricta de validación formal en stdlib pura contra `./schemas/beacon.schema.json` y subgrafos condicionales en `./schemas/tree.schema.json`. Confirmación de 54 tests automatizados al 100% de tasa de éxito en 28.3s sin dependencias externas.
- `2026-10-24 (v3.3)`: Cierre integral de las 7 brechas forenses (`[GAP-01]` a `[GAP-07]`) detectadas en la auditoría post-v3.2: (1) Preservación automática de enriquecimiento agéntico (`purpose`, `instructions`, `key_files`, `imports_from`, `exported_to`) durante `sync_beacons()` con soporte para `--force-defaults`; (2) Simetría de des-escapado JSON en `MiniYAML._unquote()`; (3) Validación estructural de `.context.yaml` en stdlib pura (`validate_beacon_data()`) integrada en `audit_repository()` con auto-reparación en `--fix`; (4) Incorporación de `key_files` físicos locales y consumidores aguas abajo (`exported_to` -> `edge: "consumer"`) en `generate_sliced_tree()`; (5) Poda estricta `os.walk` en `check_satellite_freshness()` y `compute_context_budget()`; (6) Detección de mayúsculas en profundidad completa (`[INV-06]`). Suite ampliada a 54 tests (100% OK).
- `2026-10-24 (v3.2)`: Implementación integral del motor de auto-scaffolding reactivo de beacons (`[OBJ-01]`, `[OBJ-02]`, `[OBJ-03]`) en `FWengine.py`, erradicando la orfandad estructural de directorios mediante `discover_unbeaconed_directories()`, `scaffold_beacon_for_dir()`, `ensure_beacon_chain()` e integración atómica en `route_file()` y `audit --fix`. Fortalecimiento I/O contra bloqueos transitorios en Windows NTFS (`WinError 32/5`, `EACCES`, `EBUSY`) mediante `safe_io_retry()` con exponential backoff determinista y `safe_rename_casing()` con archivo temporal de dos pasos (`.tmp_{pid}_{name}`) y rollback atómico. Recorte topológico dinámico (`[OBJ-04]`) mediante `map --slice <dir>` generando subgrafos topológicos focalizados en `< 150 tokens` (>90% de compresión frente a `tree.json` completo). Formalización de esquemas: creación de `./schemas/beacon.schema.json` (Draft-07) para validación estricta de `.context.yaml` y extensión condicional de `./schemas/tree.schema.json` para subgrafos recortados. Protocolo agéntico `/idir enrich` para enriquecimiento semántico telegráfico con límite estricto de 600 caracteres (~150 tokens). Expansión de la suite de pruebas a 50 tests (37 en `test_fwengine.py` y 13 en `test_token_budget.py`) con tasa de éxito del 100%.
- `2026-10-21 (v3.1)`: Re-ingeniería completa de `FWengine.py` a v3.1 y sincronización con ThinkingSeed Master. Cierre integral de `BUG-01` a `BUG-04` y `DEBT-01` a `DEBT-04`. Desacoplamiento de `crawl: true` y `tier1_preload: false` en `01_seed/`, resolución dinámica de `key_files` vía `resolve_seed_key_files()`, auto-descubrimiento de carpetas de dominio (`domain_extension`), verificación física de casing en disco para NTFS/APFS vía `os.listdir()`, serialización compacta de `./.context/tree.json` (~824 tokens) superando el benchmark unitario de 1,000 tokens (95.9% de ahorro de contexto), formalización de `./schemas/tree.schema.json` (Draft-07), preservación de comentarios manuales `#` en `MiniYAML`, inspección de cabeceras AST (`max_chars=4096`), y protección anti-colisión en `route --move` mediante `--overwrite`. Expansión de la suite de pruebas a 31 tests unitarios en `test_fwengine.py` (35 totales en el repositorio) con tasa de éxito del 100%.
- `2026-10-21 (v3.0)`: Migración integral al estándar formal ThinkingSeed Master v3.0 con encapsulamiento XML determinista `<SEED_ARCHITECTURAL_VECTOR>`. Incorporación de firmas simbólicas AST de 1 línea para `./FWengine.py`, `./scripts/generate_benchmark_reports.py` y suites de test en `./tests/`. Integración de la matriz forense ampliada a 7 repositorios (con peritaje forense de `FlowAgentic` en `./artifacts/benchmarks/forensic_repo_07_flowagentic.md`). Documentación adversarial de discrepancia en presupuesto de tokens de `./.context/tree.json` y schema `./schemas/tree.schema.json`.
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
generated_at: "2026-10-24T22:55:00-03:00"
generated_by: "Antigravity (Gemini 3.8 Flash)"
repository_root: "./"
git_branch: "master"
git_commit: "aeae4e4"
working_tree_state: "clean"
analysis_mode: "static+git+validated"
coverage_level: "high"
known_analysis_limits:
  - "El motor FWengine.py opera bajo restricción estricta Zero-Dependency (100% Python Standard Library)"
  - "La suite test_token_budget.py genera directorios en el temporal del SO, requiriendo permisos de I/O en %TEMP% o /tmp"
  - "El estimador de tokens de compute_context_budget() utiliza la heurística empírica de 4 caracteres por token"
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
`iDirectory` es un framework de gobernanza topológica y optimización atencional (*Context Engineering*) concebido para repositorios de software, datos, nube e inteligencia artificial. Su propósito es erradicar la degradación cognitiva de modelos de lenguaje grande (LLMs) y agentes autónomos (*Attention Sink*, *Context Drift* y dilución atencional en capas de atención multi-head), garantizando tiempos de respuesta ultrarrápidos y una reducción drástica en costos de inferencia por turno (>95% de ahorro en tokens de contexto inicial).

### 1.2 El Problema Fundamental Resuelto `[CONFIRMADO]`
1. **Atrofia Atencional por Ingesta Masiva:** Prácticas comunes de agentes autoinyectando volcados completos o archivos de semilla masivos (~6,800 tokens) o ejecutando escaneos recursivos no acotados (`find .`, `Get-ChildItem -Recurse`) agotan el presupuesto de tokens e incrementan el ruido en hasta un 85%.
2. **Ambigüedad y Caos de Ruteo:** La dispersión de scripts en la raíz del repositorio, la mezcla de pruebas con código productivo y la falta de segregación Medallion provocan colisiones y generación de código inconsistente.
3. **Deriva Topológica (Satellite Drift):** Modificaciones físicas en el sistema de archivos que dejan mapas satelitales desactualizados, provocando alucinaciones del agente sobre ubicaciones inexistentes.

### 1.3 Consumidores Principales y Perfiles de Uso `[CONFIRMADO]`
- **Agentes Autónomos (Google Antigravity/Gemini, Claude Code, OpenAI Codex, Cursor, Windsurf, Aider):** Consumen el mapa satelital `./.context/tree.json` en ~149 tokens compactos (o subgrafos focalizados vía `map --slice` en < 150 tokens) y micro-beacons `./.context.yaml` locales para navegación quirúrgica sin alucinaciones.
- **Ingenieros de Datos y Arquitectos de Software:** Disponen de una estructura estandarizada con segregación de capas Medallion (`./data/raw/`, `./data/processed/`, `./data/sandbox/`), pipelines de nube (`./src/cloud_jobs/`), esquemas y contratos (`./schemas/`) y documentación técnica desacoplada.
- **Canales de CI/CD (GitHub Actions):** Validación determinista de salud topológica, paridad de beacons y suites de pruebas mediante `./FWengine.py audit` y `unittest` sin requerir aprovisionamiento previo de librerías de terceros.

---

## 2. ARQUITECTURA, TOPOLOGÍA Y FRONTERAS MODULARES

### 2.1 Protocolo Two-Tier Bootloader `[CONFIRMADO]`
La arquitectura v3.0/v3.5 implementa una bifurcación determinista en el arranque agéntico regulada por una matriz de decisión de 3 disparadores:

```
                          ┌────────────────────────┐
                          │     Entrada Agente     │
                          └───────────┬────────────┘
                                      │
                     ┌────────────────┴────────────────┐
                     ▼                                 ▼
         [Disparadores Activos?]                       │
          /seedMaster, /metrics,                       │
          seed_reference: required,                    │
          o Inconsistencia Contrato                    │
                     │                                 │
           SÍ        ▼                                 ▼ NO
      ┌─────────────────────────────┐    ┌─────────────────────────────┐
      │   TIER 2: Planificación     │    │     TIER 1: Operación       │
      │   Arquitectónica / Auditoría│    │     Quirúrgica (Default)    │
      ├─────────────────────────────┤    ├─────────────────────────────┤
      │ 1. AGENTS.md                │    │ 1. AGENTS.md                │
      │ 2. .context/tree.json       │    │ 2. .context/tree.json       │
      │ 3. 01_seed/master.md (SEED) │    │    (o map --slice <dir>)    │
      │ 4. Beacons relevantes       │    │ 3. resolve_beacon()         │
      │ 5. Ejecución global         │    │    (.context.yaml / parent) │
      │                             │    │ 4. Modificación atómica     │
      └─────────────────────────────┘    └─────────────────────────────┘
```

#### Matriz de Decisión de 3 Disparadores `[DECLARADO]`
- **Disparador 1 (Explícito - Usuario):** Invocación de comandos slash (`/seedMaster`, `/metrics`, `/ultraThinking`, `/plan`) o requerimientos de rediseño arquitectónico integral. Activa **Tier 2** con ingesta del seed completo.
- **Disparador 2 (Estructural - Beacon):** El beacon local `./.context.yaml` del directorio objetivo declara `seed_reference: required` (ej. en `./01_seed/` o `./artifacts/plans/metricsthinking/`). Activa ingesta quirúrgica de la semilla. Si declara `seed_reference: optional`, **permanece en Tier 1**.
- **Disparador 3 (Contingencia - Agente):** Detección de colisión de contratos con `./schemas/` o necesidad de introducir dependencias transversales no registradas. Permite lectura quirúrgica puntual sin volcado masivo.

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
| `./artifacts/plans/active/` | `active_plans` | `p1` | `true` | `optional` | Planes de capacidad (F-SKUs), presupuestos cloud e hitos operativos en curso. |
| `./artifacts/plans/metricsthinking/`| `metrics_evaluation`| `p0` | `true` | `required` | Evaluación forense de madurez y roadmap de remediación (`MetricsThinking.json`). |
| `./artifacts/plans/archive/` | `archived_plans` | `p3` | `false` | `optional` | Histórico de planes descartados y documentación obsoleta (rama muerta). |
| `./docs/architecture/` | `architecture_diagrams`| `p1` | `true` | `optional` | Diagramas de arquitectura multi-cloud, topologías C4 y flujos Medallion. |
| `./docs/specs/` | `technical_specs` | `p1` | `true` | `optional` | Especificaciones técnicas de negocio, linaje y requerimientos no funcionales. |
| `./docs/notes/` | `engineers_notes` | `p2` | `true` | `optional` | Bitácoras de ingeniería, ADRs rápidos y análisis de causa raíz (RCA). |
| `./config/` | `configuration` | `p1` | `true` | `optional` | Parámetros de entorno desacoplados por ambiente (`dev`, `staging`, `prod`). |
| `./data/raw/` | `bronze_storage` | `p3` | `false` | `optional` | Capa Bronze inmutable de aterrizaje local. Ignorado en Git y AI. |
| `./data/processed/` | `silver_gold_storage` | `p3` | `false` | `optional` | Capas Silver y Gold transformadas en formatos binarios (Parquet, Delta). |
| `./data/sandbox/` | `sandbox` | `p3` | `false` | `optional` | Entorno de experimentación aislado para científicos de datos. |
| `./schemas/` | `data_contracts` | `p1` | `true` | `optional` | Esquemas estrictos de datos (Avro, JSON Schema, DDL de SQL). |
| `./scripts/` | `ops_automation` | `p2` | `true` | `optional` | Scripts operativos del sistema operativo para mantenimiento y despliegue. |
| `./tests/` | `test_suites` | `p1` | `true` | `optional` | Suites de pruebas unitarias, integración, estrés y token budget. |
| `./tools/` | `tooling` | `p2` | `true` | `optional` | Herramientas internas, linters y scripts auxiliares. |
| `./logs/` | `logs` | `p3` | `false` | `optional` | Trazas locales de ejecución y volcados de error (rama muerta). |
| `./.context/` | `context_engineering` | `p0` | `true` | `optional` | Mapa topológico satelital (`tree.json`) y contratos de ingeniería de contexto. |
| `./infrastructure/` | `domain_extension` | `p1` | `true` | `optional` | Plantillas de IaC (Terraform, Bicep, Pulumi) descubiertas dinámicamente. |

### 2.3 Reglas de Poda e Invariantes de Crawling `[CONFIRMADO]`
- **Herencia Jerárquica de Poda:** Si un directorio o cualquiera de sus ancestros declara `crawl: false` (como `./data/raw/`, `./data/processed/`, `./data/sandbox/`, `./logs/`, `./artifacts/plans/archive/`), queda estrictamente prohibida la exploración o volcado recursivo por parte de agentes de IA.
- **Sincronización Obligatoria de Cierre:** Toda mutación estructural física impone la re-ejecución inmediata de:
  ```powershell
  python FWengine.py audit --fix
  python FWengine.py beacon --sync
  python FWengine.py map --sync
  ```

---

## 3. FLUJOS DE EJECUCIÓN, ENTRY POINTS Y CICLO DE VIDA

### 3.1 Puntos de Entrada (Entry Points) `[CONFIRMADO]`
1. **Motor CLI Central (`./FWengine.py`):** CLI unificada sin dependencias externas que provee los subcomandos `init`, `route`, `beacon`, `map`, `context` y `audit`.
2. **Skill Agéntica (`./.agents/skills/idir/SKILL.md`):** Manifiesto ejecutable vía `/idir` que orquesta acciones de gobernanza desde interfaces agénticas.
3. **Flujo de Integración Continua (`./.github/workflows/ci.yml`):** Validador automatizado multiplataforma (Ubuntu, Windows, macOS) ejecutando auditorías y suites unitarias.

### 3.2 Ciclos de Vida Operativos `[CONFIRMADO]`

#### Flujo 1: Ruteo Heurístico Híbrido (`FWengine.py route`)
```
Archivo Entrada -> Comprueba Path Traversal -> Inspecciona Extensión
       │
       ├─► .py / .sql -> ¿test/spec en nombre? -> tests/
       │                  └─► NO -> inspect_python_header() -> [tests | cloud_jobs | dashboards | core]
       ├─► .ipynb     -> 03_research/notebooks/
       ├─► .md/.txt   -> Analiza tokens de nombre -> [archive | metricsthinking | active | prompts | specs | architecture | notes]
       └─► Genérico   -> ROUTING_MAP -> Fallback por palabras clave -> tools/
       │
       └─► Flag --move? -> SÍ: Normalización case NTFS atómica vía archivo temporal -> Reubicación
                           NO: Emisión de sugerencia CLI
```

#### Flujo 2: Resolución Jerárquica Ascendente (`resolve_beacon()`)
```
Subdirectorio Objetivo (ej. src/core/services/auth/)
       │
       ▼
¿Existe .context.yaml físico?
       ├─► SÍ -> Carga directivas locales
       └─► NO -> Asciende recursivamente hacia parent hasta llegar a ROOT_DIR
                 Hereda role, purpose, relevance, read_priority e instructions
                 INVARIANTE: Si CUALQUIER ancestro tiene crawl: false -> crawl = false
```

#### Flujo 3: Detección de Deriva Satelital (`check_satellite_freshness()`)
```
FWengine.py map --check-freshness
       │
       ▼
Lee timestamp de ./.context/tree.json
Escanea mtime de carpetas clave (01_seed, 02_foundation, src, tests, etc.)
       │
       ├─► latest_mtime > (satellite_time + 1.0s) -> [FAIL] DRIFT DETECTADO -> Sugiere map --sync
       └─► latest_mtime <= (satellite_time + 1.0s) -> [PASS] Satélite al día
```

---

## 4. CONTRATOS SIMBÓLICOS, MODELO DE DATOS Y PERSISTENCIA

### 4.1 Firmas Simbólicas AST de 1 Línea `[CONFIRMADO]`

#### Módulo Central de Gobernanza: `./FWengine.py`
- `./FWengine.py::MiniYAML._unquote(raw: str) -> str` | Des-escapa cadenas entrecomilladas simétricamente vía `json.loads()` con fallback seguro a slice.
- `./FWengine.py::MiniYAML.dump(data: Dict[str, Any], prefix: str = "") -> str` | Serializador recursivo a YAML minimalista; maneja escalares, listas y diccionarios sin PyYAML.
- `./FWengine.py::MiniYAML.load(yaml_str: str) -> Dict[str, Any]` | Parser de YAML línea a línea para pares clave-valor y listas indentadas; soporta booleanos, enteros, floats y nulls.
- `./FWengine.py::_is_transient_io_error(exc: BaseException) -> bool` | Identifica códigos de error I/O transitorios de Windows NTFS (`WinError 5, 32, 33`) y POSIX (`EACCES`, `EBUSY`, `EAGAIN`).
- `./FWengine.py::safe_io_retry(operation: Callable[[], Any], max_attempts: int = 4, initial_delay_ms: float = 25.0) -> Any` | Envoltorio con exponential backoff determinista para neutralizar bloqueos transitorios de I/O en disco.
- `./FWengine.py::safe_rename_casing(src: pathlib.Path, dest: pathlib.Path) -> pathlib.Path` | Renombrado atómico en dos pasos mediante archivo temporal `.tmp_{pid}_{name}` con rollback ante excepciones.
- `./FWengine.py::resolve_seed_key_files(root_path: pathlib.Path) -> List[str]` | Escanea dinámicamente `01_seed/seed-*.md` en el repositorio o infiere `seed-{slug}-master.md` erradicando contaminación cruzada.
- `./FWengine.py::_resolve_physical_rel_path(root_path: pathlib.Path, canonical_rel: str) -> str` | Resuelve el casing exacto físico en disco (NTFS/APFS) mediante `os.listdir()`.
- `./FWengine.py::generate_beacon_content(folder: str, meta: Dict[str, Any], root_path: Optional[pathlib.Path] = None) -> str` | Construye el contenido serializado `.context.yaml` con `tier1_preload`, `key_files`, `imports_from` y `exported_to`.
- `./FWengine.py::resolve_beacon(dir_path: pathlib.Path, root_path: pathlib.Path) -> Dict[str, Any]` | Resuelve recursivamente directivas de beacon mediante ascenso jerárquico; garantiza propagación de `crawl: false`.
- `./FWengine.py::extract_preserved_comments(beacon_file: pathlib.Path) -> List[str]` | Extrae líneas de comentarios `#` existentes en un `.context.yaml` para preservarlas durante la resincronización.
- `./FWengine.py::validate_beacon_data(data: Dict[str, Any]) -> List[str]` | Valida en stdlib pura las claves obligatorias y enums de un `.context.yaml` frente a `schemas/beacon.schema.json`.
- `./FWengine.py::_rel_posix(path: pathlib.Path, root_path: pathlib.Path) -> str` | Normaliza un objeto `Path` a una cadena relativa POSIX usando separadores `/`.
- `./FWengine.py::load_ignore_patterns(root_path: pathlib.Path) -> List[str]` | Carga y normaliza máscaras de exclusión de `.agentignore` y `.gitignore`.
- `./FWengine.py::is_ignored_path(dir_path: pathlib.Path, root_path: pathlib.Path, patterns: Optional[List[str]] = None) -> bool` | Evalúa si una ruta coincide con exclusiones o ancestros con `crawl: false`.
- `./FWengine.py::discover_unbeaconed_directories(root_path: pathlib.Path) -> List[pathlib.Path]` | Descubre directorios no ignorados que carecen de `.context.yaml` físico.
- `./FWengine.py::infer_beacon_meta(dir_path: pathlib.Path, root_path: pathlib.Path) -> Dict[str, Any]` | Infiere rol, prioridad y metadatos de baliza combinando catálogo canónico y herencia ascendente.
- `./FWengine.py::scaffold_beacon_for_dir(dir_path: pathlib.Path, root_path: pathlib.Path, overwrite: bool = False) -> Optional[pathlib.Path]` | Auto-scaffoldea `.context.yaml` para un directorio huérfano si no existe previamente o si `overwrite=True`.
- `./FWengine.py::ensure_beacon_chain(target_dir: pathlib.Path, root_path: pathlib.Path) -> List[pathlib.Path]` | Asegura que toda la cadena de ancestros hasta `target_dir` posea `.context.yaml`.
- `./FWengine.py::iter_beacon_files(root_path: pathlib.Path) -> List[pathlib.Path]` | Itera sobre todos los `.context.yaml` válidos del repositorio sin entrar en ramas podadas.
- `./FWengine.py::sync_beacons(root_path: pathlib.Path, auto_discover: bool = True, force_defaults: bool = False) -> int` | Sincroniza micro-beacons preservando comentarios `#` y enriquecimiento agéntico salvo `force_defaults=True`; auto-descubre huérfanos.
- `./FWengine.py::generate_tree_json(root_path: pathlib.Path) -> Dict[str, Any]` | Construye el mapa satelital estructurado con auto-descubrimiento filtrado de `domain_extension` y lectura de beacons locales.
- `./FWengine.py::check_satellite_freshness(root_path: pathlib.Path) -> Dict[str, Any]` | Compara el timestamp del satélite frente a la marca de modificación más reciente con recorrido `os.walk` podado.
- `./FWengine.py::format_compact_tree_json(data: Dict[str, Any]) -> str` | Serializa el mapa satelital con un nodo por línea JSON compacta (< 1,000 tokens).
- `./FWengine.py::sync_tree(root_path: pathlib.Path) -> pathlib.Path` | Serializa el mapa satelital en `./.context/tree.json` en formato compacto; retorna ruta del archivo generado.
- `./FWengine.py::_read_local_beacon(dir_path: pathlib.Path) -> Dict[str, Any]` | Carga el `.context.yaml` directo de un directorio sin ascenso jerárquico.
- `./FWengine.py::generate_sliced_tree(root_path: pathlib.Path, target_path: str, radius: int = 1, max_children: int = 6) -> Dict[str, Any]` | Genera subgrafo topológico recortado (`focus`, `parent`, `child`, `dep`, `consumer`) en `< 150 tokens`.
- `./FWengine.py::format_sliced_tree(data: Dict[str, Any]) -> str` | Serializa el subgrafo recortado a JSON compacto de una sola línea.
- `./FWengine.py::compute_context_budget(root_path: pathlib.Path) -> List[Dict[str, Any]]` | Cuantifica volumen de archivos, peso en bytes y tokens estimados (~4 chars/token) con recorrido `os.walk` podado.
- `./FWengine.py::init_project(base_path: str) -> None` | Inicializa la topología canónica, despliega beacons, genera satélite, `engine_readme.md`, `.agentignore` y `.gitignore`.
- `./FWengine.py::inspect_python_header(file_path: pathlib.Path, max_chars: int = 4096) -> str` | Inspecciona imports mediante `ast.parse()` y fallback de hasta 4,096 caracteres para clasificar el destino arquitectónico.
- `./FWengine.py::route_file(file_path: str, base_path: str = '.', move: bool = False, overwrite: bool = False) -> Optional[pathlib.Path]` | Clasifica y reubica atómicamente archivos con protección anti-colisión, reintento I/O y auto-scaffolding de beacons.
- `./FWengine.py::audit_repository(root_path: pathlib.Path, fix: bool = False) -> bool` | Audita mayúsculas en profundidad completa, cobertura y validez de esquema de beacons; auto-remedia con `fix=True`.
- `./FWengine.py::main() -> None` | Dispatcher principal de CLI configurado con `argparse` para `init`, `route` (`--overwrite`), `beacon` (`--no-discover`, `--force-defaults`), `map` (`--slice`, `--radius`), `context` y `audit` (`--fix`).

#### Módulo de Reportes Forenses: `./scripts/generate_benchmark_reports.py`
- `./scripts/generate_benchmark_reports.py::<module>() -> None` | Ingesta `./artifacts/benchmarks/benchmark_matrix.json` y materializa reportes periciales markdown individuales en `./artifacts/benchmarks/`.

#### Suites de Pruebas Automatizadas: `./tests/` (54 tests totales: 48 en `test_fwengine.py` + 6 en `test_token_budget.py`)
- `./tests/test_fwengine.py::TestMiniYAML` (5 tests: `test_dump_scalars_and_dict`, `test_dump_and_load_list`, `test_load_boolean_and_null`, `test_roundtrip_nested`, `test_escaped_quotes_roundtrip`).
- `./tests/test_fwengine.py::TestTopologicalManifest` (3 tests: `test_all_folders_are_lowercase`, `test_required_metadata_fields`, `test_pruning_policy_invariants`).
- `./tests/test_fwengine.py::TestRoutingMapAndHeuristics` (4 tests: `test_routing_map_destinations_are_canonical`, `test_notebooks_route_to_research`, `test_sql_routes_to_cloud_jobs`, `test_schemas_route_to_schemas`).
- `./tests/test_fwengine.py::TestLifecycleAndIdempotence` (7 tests: `test_init_project_creates_structure`, `test_sync_beacons_idempotency`, `test_sync_tree_generates_valid_schema`, `test_audit_repository_pass_and_fail`, `test_dynamic_seed_name_resolution`, `test_domain_extension_autodiscovery`, `test_tree_schema_file_exists`).
- `./tests/test_fwengine.py::TestTokenBudgetComputation` (1 test: `test_compute_budget_returns_records`).
- `./tests/test_fwengine.py::TestBeaconInheritance` (2 tests: `test_child_inherits_from_parent_beacon`, `test_strict_pruning_inheritance`).
- `./tests/test_fwengine.py::TestHybridRouting` (5 tests: `test_inspect_pytest_routes_to_tests`, `test_inspect_cloud_jobs_routes_to_cloud_jobs`, `test_inspect_dashboards_routes_to_dashboards`, `test_inspect_fallback_routes_to_core`, `test_header_inspection_with_long_docstring`).
- `./tests/test_fwengine.py::TestFileSystemHardening` (3 tests: `test_path_traversal_blocked`, `test_casing_collision_atomic_rename`, `test_route_move_collision_protection`).
- `./tests/test_fwengine.py::TestSatelliteFreshness` (2 tests: `test_fresh_satellite_returns_no_drift`, `test_drift_detected_on_new_file`).
- `./tests/test_fwengine.py::TestNTFSIOResilience` (4 tests: `test_safe_io_retry_recovers_transient_error`, `test_safe_io_retry_does_not_retry_logical_errors`, `test_safe_io_retry_exhausts_and_raises`, `test_no_tmp_residue_after_casing_rename`).
- `./tests/test_fwengine.py::TestAutoScaffoldAndRemediation` (9 tests: `test_init_leaves_no_orphans`, `test_auto_discovery_scaffolds_unbeaconed_folder`, `test_discovery_respects_crawl_false_and_hidden`, `test_scaffold_never_overwrites_existing_beacon`, `test_route_file_creates_beacon_on_new_target`, `test_audit_fix_flag_resolves_missing_beacons`, `test_sync_beacons_preserves_agent_enrichment`, `test_audit_detects_and_fixes_invalid_beacon_schema`, `test_audit_detects_deep_uppercase_directory`).
- `./tests/test_fwengine.py::TestTreeSlicing` (3 tests: `test_tree_slicing_structure_and_dependencies`, `test_slice_pruned_branch_has_no_children`, `test_slice_blocks_traversal`).
- `./tests/test_token_budget.py::TestTokenBudgetBenchmark` (4 tests: `test_satellite_tree_token_efficiency`, `test_compact_context_string_is_dense`, `test_beacon_token_density_threshold`, `test_tree_slicing_token_budget`).
- `./tests/test_token_budget.py::TestTopologicalScalingStress` (2 tests: `test_satellite_generation_latency`, `test_budget_computation_stability`).

### 4.2 Modelo de Datos y Esquemas Canónicos `[CONFIRMADO]`

#### Estructura del Beacon Canónico (`./.context.yaml`)
Campos serializados por `MiniYAML`:
- `version: "1.0"` `[CONFIRMADO]`
- `directory: str` (ej. `"src/core"`) `[CONFIRMADO]`
- `role: str` (identificador funcional del nodo) `[CONFIRMADO]`
- `purpose: str` (descripción semántica concisa) `[CONFIRMADO]`
- `relevance: str` (`"critical"` | `"high"` | `"medium"` | `"low"` | `"zero_for_llm"`) `[CONFIRMADO]`
- `crawl: bool` (`true` para exploración permitida, `false` para poda estricta) `[CONFIRMADO]`
- `read_priority: str` (`"p0"` | `"p1"` | `"p2"` | `"p3"`) `[CONFIRMADO]`
- `seed_reference: str` (`"required"` | `"optional"`) `[CONFIRMADO]`
- `token_density: str` (`"sparse"` | `"medium"` | `"dense"` | `"massive_text"`) `[CONFIRMADO]`
- `instructions: str` (directivas operativas para el agente) `[CONFIRMADO]`
- `key_files: List[str]` (archivos críticos declarados en el nodo, opcional) `[CONFIRMADO]`
- `dependencies: List[str]` (vínculos directos con otros módulos, opcional) `[CONFIRMADO]`
- `imports_from: List[str]` (orígenes de datos o dependencias ascendentes, opcional) `[CONFIRMADO]`
- `exported_to: List[str]` (consumidores de datos o módulos aguas abajo, opcional) `[CONFIRMADO]`

#### Estructura del Satélite Topológico (`./.context/tree.json`)
- `$schema: "../schemas/tree.schema.json"` `[CONFIRMADO]`
- `version: "3.0"` `[CONFIRMADO]`
- `project: str` (nombre del proyecto) `[CONFIRMADO]`
- `architecture: "Gravity HyperScale Thinking"` `[CONFIRMADO]`
- `updated_at: str` (ISO-8601 UTC timestamp) `[CONFIRMADO]`
- `timestamp: float` (epoch unix timestamp para validación de freshness) `[CONFIRMADO]`
- `bootloader: Dict[str, List[str]]` (secuencias de ingesta para `tier_1` y `tier_2`) `[CONFIRMADO]`
- `nodes: Dict[str, NodeInfo]` (mapa de carpetas con `role`, `prio`, `crawl`, `seed_ref`, `tier1_preload`, `key_files`) `[CONFIRMADO]`

#### Estructura del Esquema Formal de Satélite (`./schemas/tree.schema.json`) `[CONFIRMADO]`
- Especificación: JSON Schema Draft-07 (`http://json-schema.org/draft-07/schema#`).
- Validación Condicional (`oneOf` / `anyOf`): Valida tanto el árbol satelital completo (`version`, `project`, `architecture`, `updated_at`, `timestamp`, `bootloader`, `nodes`) como subgrafos recortados generados por `map --slice` (`sliced: true`, `focus_node: str`, `radius: int`, `nodes` con soporte para `"pruned": true`).

#### Estructura del Esquema Formal de Beacon (`./schemas/beacon.schema.json`) `[CONFIRMADO]`
- Especificación: JSON Schema Draft-07 (`http://json-schema.org/draft-07/schema#`).
- Propiedades Validadas: `version`, `directory`, `role`, `purpose`, `relevance` (`critical` | `high` | `medium` | `low` | `zero_for_llm`), `crawl` (boolean), `read_priority` (`p0` a `p3`), `seed_reference` (`required` | `optional`), `token_density` (`sparse` | `medium` | `dense` | `massive_text`), `tier1_preload` (boolean), `instructions` (string <= 200 chars), `key_files` (array de strings), `dependencies` (array de strings), `imports_from` (array de strings) y `exported_to` (array de strings).
- Validación de Cumplimiento: 100% de las balizas físicas del repositorio validadas con cero discrepancias.

---

## 5. CONFIGURACIÓN, ENTORNOS Y DEPENDENCIAS

### 5.1 Restricción Zero-Dependency `[INV-01]` `[CONFIRMADO]`
`FWengine.py` está diseñado para operar en entornos aislados, contenedores minimalistas, runners de CI/CD efímeros o máquinas de desarrolladores sin requerir `pip install` ni configurar entornos virtuales `.venv`.
- Dependencias utilizadas exclusivamente de la librería estándar: `os`, `sys`, `json`, `time`, `errno`, `fnmatch`, `argparse`, `datetime`, `pathlib`, `typing`, `unittest`, `ast`.

### 5.2 Compatibilidad Multi-Plataforma `[CONFIRMADO]`
- **Sistemas Operativos Soportados:** Linux (Ubuntu 20.04+), Windows 10/11 / Windows Server, macOS (Ventura+).
- **Runtimes Validados en CI:** Python 3.10, 3.11, 3.12, 3.13.
- **Políticas de Codificación y File System:**
  - Codificación UTF-8 forzada en todas las operaciones de I/O (`encoding="utf-8"`).
  - Manejo de rutas normalizadas mediante `pathlib.Path` para neutralizar diferencias entre separadores `/` y `\`.

### 5.3 Archivos de Configuración y Exclusión `[CONFIRMADO]`
- `./.agentignore`: Define la máscara de exclusión de lectura para agentes autónomos (`./data/raw/`, `./data/processed/`, `./data/sandbox/`, `./logs/`, `*.parquet`, `*.csv`, `*.delta/`, `.venv/`, `__pycache__/`, `.git/`, `./artifacts/plans/archive/`).
- `./.gitignore`: Ignora artefactos efímeros, entornos virtuales y datasets locales pesados.

---

## 6. PRUEBAS, CI/CD, DESPLIEGUE Y OPERACIÓN

### 6.1 Suite Unitaria (`./tests/test_fwengine.py`) `[CONFIRMADO]`
Contiene 48 casos de prueba automatizados con un ratio de éxito de 100% (`OK`) (54 casos de prueba totales en el repositorio incluyendo benchmarks):
- Verificación de serialización y deserialización simétrica de `MiniYAML` con tipos primitivos complejos y comillas escapadas (`test_escaped_quotes_roundtrip`).
- Inicialización determinista del andamiaje de directorios y satélite.
- Ruteo heurístico por extensión y verificación de inspección de cabeceras de Python vía `ast.parse()`.
- Mecanismo seguro de renombrado case-insensitive en Windows NTFS (`.tmp_{pid}_{name}`) con exponential backoff (`safe_io_retry`).
- Herencia jerárquica y prevalencia de `crawl: false` en `resolve_beacon()`.
- Rechazo frontal de intentos de Path Traversal (`PermissionError`).
- Resolución dinámica del nombre de seeds en repositorios externos (`test_dynamic_seed_name_resolution`).
- Auto-descubrimiento de carpetas de dominio no canónicas (`test_domain_extension_autodiscovery`).
- Validación de existencia física de contratos formales de satélite y beacon (`test_tree_schema_file_exists`).
- Inspección de cabeceras con docstrings extensos (>2,000 chars) vía AST (`test_header_inspection_with_long_docstring`).
- Protección anti-colisión en reubicación de archivos con `--overwrite` (`test_route_move_collision_protection`).
- Resiliencia NTFS I/O ante bloqueos temporales (`TestNTFSIOResilience`: 4 tests).
- Auto-scaffolding de balizas huérfanas, preservación de enriquecimiento semántico (`test_sync_beacons_preserves_agent_enrichment`), validación activa de esquemas (`test_audit_detects_and_fixes_invalid_beacon_schema`), detección profunda de casing (`test_audit_detects_deep_uppercase_directory`) y remediación en auditoría (`TestAutoScaffoldAndRemediation`: 9 tests).
- Recorte topológico dinámico en subgrafos con aristas `dep` y `consumer` (`TestTreeSlicing`: 3 tests).

### 6.2 Benchmarks de Presupuesto de Tokens (`./tests/test_token_budget.py`) `[CONFIRMADO]`
Contiene 6 pruebas de telemetría y rendimiento que evalúan la compresión de contexto, densidad de balizas y presupuestos de subgrafos:
- Ahorro de contexto verificado: **95.9%** de reducción en tokens consumidos frente al escaneo recursivo ingenuo (`~20,195 tokens` vs `~824 tokens`).
- Formato de inyección compacta (`IDIR_TOPOLOGY`): **~163 tokens** (cumpliendo holgadamente el umbral `< 250 tokens`).
- Subgrafos focalizados (`map --slice <dir>`): **~60 tokens** para subdirectorios (`src/core`), **~103 tokens** para ramas secundarias (`docs`), superando holgadamente el límite de `< 150 tokens` (>90% de compresión).
- Densidad de balizas: 100% de los archivos `.context.yaml` cumplen el límite de densidad estricta (`<= 600 caracteres` / `~150 tokens`).
- Latencia de generación satelital bajo estrés: **34.61 ms**; escaneo de budget: **49.76 ms**.

### 6.3 Pipeline de CI/CD (`./.github/workflows/ci.yml`) `[CONFIRMADO]`
Workflow automatizado activado en eventos `push` y `pull_request` sobre ramas `master` y `main`:
1. Matriz 3x4: 3 sistemas operativos (Ubuntu, Windows, macOS) x 4 versiones de Python (3.10 a 3.13).
2. Verificación de arquitectura Zero-Dependency.
3. Ejecución de auditoría de gobernanza: `python FWengine.py audit`.
4. Ejecución de suite unitaria: `python -m unittest discover -s tests -p "test_*.py" -v`.
5. Ejecución de benchmarks de token budget: `python -m unittest tests/test_token_budget.py -v`.

---

## 7. SUPERFICIE DE TENSIÓN, CONTRADICCIONES Y MODOS DE FALLA

Esta sección documenta de forma adversarial y objetiva los vectores de tensión reales, inconsistencias entre documentación y código, y riesgos operativos identificados en la auditoría física:

### 7.1 Parser YAML Minimalista sin Soporte para Estructuras Complejas `[CONFIRMADO]`
- **Vector de Riesgo:** `MiniYAML` es un serializador/parser artesanal de 60 líneas concebido para stdlib pura. No soporta multilínea con pipes (`|`, `>`), listas anidadas dentro de listas, diccionarios en línea (`{a: 1}`), o arrays compactos (`[x, y]`).
- **Modo de Falla:** Si un desarrollador o agente introduce sintaxis YAML avanzada manualmente en un `.context.yaml`, `MiniYAML.load()` omitirá o truncará las claves silenciosamente, pudiendo provocar corrupción en `sync_beacons()`.
- **Mitigación Activa:** `validate_beacon_data()` valida los tipos deserializados y `schemas/beacon.schema.json` previene discrepancias de estructura en CI.

### 7.2 Límite de Renombrado Atómico entre Dispositivos Físicos Distintos (EXDEV) `[CONFIRMADO]`
- **Vector de Riesgo:** `safe_rename_casing()` y `route_file()` utilizan `Path.rename()`. En sistemas POSIX y Windows, renombrar archivos entre sistemas de archivos o particiones de disco distintas (o entre montajes NFS) lanza `OSError: [Errno 18] Invalid cross-device link` (`EXDEV`).
- **Modo de Falla:** Fallo en reubicación si un repositorio reside parcialmente en enlaces simbólicos que cruzan particiones o si la carpeta temporal del sistema de archivos no comparte el dispositivo físico del repo.
- **Mitigación Activa:** `route_file()` confina las operaciones estrictamente dentro del árbol relativo de `root_path`.

### 7.3 Imprecisión Heurística en el Estimador de Tokens `[CONFIRMADO]`
- **Vector de Riesgo:** `compute_context_budget()` calcula el presupuesto asumiendo un divisor fijo de 4 caracteres por token (`chars // 4`).
- **Modo de Falla:** Para código en Python estándar o JSON esta aproximación oscila entre 3.6 y 4.2 chars/token. Sin embargo, para archivos Markdown enriquecidos con fórmulas LaTeX (`$$`), bloques Mermaid o texto multilingüe con caracteres no ASCII, el consumo real de tokens en BPE (Byte Pair Encoding) de Gemini o Claude puede ser entre un 15% y 30% superior al reportado.
- **Mitigación Activa:** Los umbrales de alerta operan con márgenes holgados de seguridad (límite satelital en 1,000 tokens vs 824 tokens reales; subgrafos en 150 vs 60 tokens).

### 7.4 Sensibilidad de Casing y Bloqueos I/O en Windows NTFS `[RESUELTO EN v3.2]`
- **Estado:** En v3.2 se implementó `safe_io_retry()` con exponential backoff determinista (capturando `WinError 5, 32, 33`, `EACCES`, `EBUSY`, `EAGAIN`) y `safe_rename_casing()` con archivo temporal intermedio `.tmp_{pid}_{name}` y rollback atómico, eliminando excepciones por bloqueos transitorios de antivirus o indexadores de Windows Search.

### 7.5 Orfandad Estructural de Beacons en Nuevos Directorios `[RESUELTO EN v3.2]`
- **Estado:** Se implementó auto-scaffolding reactivo en `route_file()` mediante `ensure_beacon_chain()`, auto-descubrimiento de directorios huérfanos en `sync_beacons(auto_discover=True)` y auto-remediación inmediata mediante el flag `python FWengine.py audit --fix`.

### 7.6 Inflación de Contexto por Ingesta Global de Satélite `[RESUELTO EN v3.2]`
- **Estado:** Se incorporó el recorte topológico dinámico (*Tree Slicing*) mediante `generate_sliced_tree()` y el comando `python FWengine.py map --slice <dir>`, emitiendo subgrafos compactos con el nodo foco, su padre, sus hijos inmediatos y sus dependencias en `< 150 tokens` (>90% de compresión frente a `tree.json` completo).

---

## 8. SEGURIDAD, PRIVACIDAD Y GUARDRAILS

### 8.1 Blindaje contra Path Traversal `[CONFIRMADO]`
- En `route_file()`, cualquier entrada que contenga secuencias relativas hacia arriba (`..` en `raw_path.parts`) es bloqueada antes de interactuar con el sistema de archivos lanzando `PermissionError("[-] Error de Seguridad: Intento de Path Traversal bloqueado ('..' detectado en '...').")`.
- Se valida estrictamente mediante `path.resolve().relative_to(base_dir)` que tanto el origen como el destino resuelto permanezcan contenidos dentro del límite físico del repositorio.

### 8.2 Guardrails para Agentes de Inteligencia Artificial `[CONFIRMADO]`
1. **Prohibición de Escaneo Ciego Recursivo (`[INV-02]`):** Queda prohibida la ejecución de comandos de exploración profunda no restringidos (`Get-ChildItem -Recurse`, `find .`, `ls -R`). Toda navegación debe iniciar consultando `./.context/tree.json`.
2. **Invariante de Ramas Muertas (`[INV-03]`):** Los directorios con directiva `crawl: false` (`./data/raw/`, `./data/processed/`, `./data/sandbox/`, `./logs/`, `./artifacts/plans/archive/`) son considerados almacenes de datos o ramas muertas; los agentes tienen prohibido volcar su contenido al contexto.
3. **Contrato de Sincronización al Cierre (`[INV-04]`):** Cualquier cambio estructural en la topología física exige sincronizar beacons y satélite antes de dar la tarea por finalizada (`python FWengine.py audit --fix`).
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

### 9.2 Deuda Técnica Identificada y Priorizada `[DECLARADO]`

| ID | Componente | Severidad | Descripción de Deuda Técnica | Remediation Plan / Estado |
| :---: | :--- | :---: | :--- | :--- |
| `DEBT-01` | `./tests/test_token_budget.py` | **Alta** | Test unitario fallaba por discrepancia de tamaño de `tree.json` (1,019 tokens > 1,000 límite). | `[RESUELTO EN v3.1]` Formato JSON compacto por línea (< 1,000 tokens; 95.9% de ahorro verificado). |
| `DEBT-02` | `./schemas/tree.schema.json` | **Media** | Schema referenciado en `tree.json` no existía físicamente en el repositorio. | `[RESUELTO EN v3.1]` Materializado Draft-07 en `./schemas/tree.schema.json` y referenciado formalmente. |
| `DEBT-03` | `./FWengine.py` (MiniYAML) | **Baja** | Pérdida de comentarios `#` al serializar `.context.yaml`. | `[RESUELTO EN v3.1]` Implementada extracción y retención de comentarios manuales en `sync_beacons()`. |
| `DEBT-04` | `./FWengine.py` (route) | **Media** | Riesgo de sobrescritura destructiva sin backup al mover archivos con colisión de nombre. | `[RESUELTO EN v3.1]` Implementada protección `FileExistsError` y habilitación explícita vía flag `--overwrite`. |
| `DEBT-05` | `./FWengine.py` (beacon) | **Alta** | Orfandad estructural de balizas en carpetas creadas por agentes o SO sin beacon. | `[RESUELTO EN v3.2]` Auto-scaffolding reactivo en `route_file()`, `ensure_beacon_chain()` y `audit --fix`. |
| `DEBT-06` | `./FWengine.py` (casing/io) | **Media** | Bloqueos transitorios I/O en Windows NTFS (`WinError 32/5`) por antivirus o indexadores. | `[RESUELTO EN v3.2]` Implementado `safe_io_retry()` con exponential backoff y `safe_rename_casing()`. |
| `DEBT-07` | `./.context/tree.json` | **Media** | Inflación de contexto al leer mapa satelital global en tareas acotadas a subdominios. | `[RESUELTO EN v3.2]` Recorte topológico dinámico `map --slice <dir>` consumiendo `< 150 tokens`. |
| `DEBT-08` | `./schemas/beacon.schema.json` | **Media** | Ausencia de contrato formal de esquema JSON para balizas locales `.context.yaml`. | `[RESUELTO EN v3.2]` Creado `schemas/beacon.schema.json` (Draft-07); 100% de beacons validados. |

---

## 10. REGLAS DE MODIFICACIÓN, GLOSARIO E ÍNDICE DE EVIDENCIAS

### 10.1 Invariantes del Sistema (System Invariants)
- `[INV-01]` **Zero External Dependencies:** `FWengine.py` debe compilar y ejecutarse exclusivamente con la librería estándar de Python 3.9+.
- `[INV-02]` **No Blind Recursive Scan:** Prohibida la búsqueda recursiva no acotada sin consultar `.context/tree.json`.
- `[INV-03]` **Crawl False Inviolability:** Carpetas con `crawl: false` jamás deben ser volcadas a la ventana de contexto de un agente.
- `[INV-04]` **Post-Mutation Synchronization:** Modificaciones de carpetas requieren `python FWengine.py audit --fix`, `beacon --sync` y `map --sync`.
- `[INV-05]` **Zero Secret Leakage:** Prohibida la inclusión de credenciales en claro; aplicar `<REDACTED>`.
- `[INV-06]` **All-Lowercase Directories:** Todos los directorios gobernados deben nombrarse estrictamente en minúsculas.
- `[INV-07]` **Deterministic Two-Tier Bootloader:** Prohibido autoinyectar el seed en Tier 1 a menos que se active uno de los 3 disparadores.
- `[INV-08]` **Relative Unix-Style Paths:** Todas las referencias documentales y de código deben usar rutas relativas con barra `/` (`./ruta/archivo`). Prohibido el uso de rutas absolutas locales o esquemas URI de archivo local.

### 10.2 Glosario Técnico
- **Two-Tier Bootloader:** Protocolo de arranque agéntico de dos fases (Tier 1 atómico y Tier 2 arquitectónico) para control estricto del presupuesto de tokens.
- **Context Engineering:** Metodología sistemática de diseño de repositorios de software para optimizar la atención de modelos de lenguaje y reducir tokens residuales.
- **Context Beacon (`.context.yaml`):** Microarchivo descriptor de semáforos, roles y directivas de poda ubicado en cada directorio gobernado.
- **Mapa Satelital (`tree.json`):** Representación topológica estructurada y ultraligera que describe todo el sistema en un solo archivo.
- **Satellite Drift:** Desincronización temporal entre la topología física del sistema de archivos y el mapa satelital.
- **Medallion Layers:** Arquitectura de datos de tres capas segregadas: Bronze (`data/raw`), Silver/Gold (`data/processed`) y Experimentación (`data/sandbox`).
- **Tree Slicing:** Recorte topológico dinámico que genera un subgrafo restringido al nodo en foco, su padre, sus hijos y sus dependencias en < 150 tokens.

### 10.3 Índice de Evidencias Físicas
- Motor de gobernanza y CLI: `./FWengine.py` `[CONFIRMADO]`
- Satélite topológico principal: `./.context/tree.json` `[CONFIRMADO]`
- Esquema formal del satélite: `./schemas/tree.schema.json` `[CONFIRMADO]`
- Esquema formal de micro-balizas: `./schemas/beacon.schema.json` `[CONFIRMADO]`
- Manifiesto de skill agéntica: `./.agents/skills/idir/SKILL.md` `[CONFIRMADO]`
- Reglas de gobernanza para agentes: `./AGENTS.md` y `./GEMINI.md` `[CONFIRMADO]`
- Guía operativa del motor: `./02_foundation/engine/engine_readme.md` `[CONFIRMADO]`
- Suite de pruebas unitarias: `./tests/test_fwengine.py` `[CONFIRMADO]`
- Suite de pruebas de presupuesto de tokens: `./tests/test_token_budget.py` `[CONFIRMADO]`
- Flujo de integración continua: `./.github/workflows/ci.yml` `[CONFIRMADO]`
- Matriz de evaluación forense: `./artifacts/plans/metricsthinking/MetricsThinking.json` `[CONFIRMADO]`
- Matriz consolidada de benchmarks: `./artifacts/benchmarks/benchmark_matrix.json` `[CONFIRMADO]`
- Peritaje forense FlowAgentic: `./artifacts/benchmarks/forensic_repo_07_flowagentic.md` `[CONFIRMADO]`

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
1. Un saludo confirmando que asimilaste el ADN arquitectónico v3.0 de **iDirectory** (`<SEED_ARCHITECTURAL_VECTOR>`) y su stack principal (Python Standard Library, Two-Tier Bootloader, Context Engineering).
2. Un breve resumen de 2-3 líneas sobre el objetivo, su estado actual y sus principales vectores de tensión (resiliencia NTFS I/O mediante safe_io_retry, auto-scaffolding reactivo de beacons y tree slicing con map --slice).
3. Una frase poniéndote a disposición para resolver dudas sobre su funcionamiento o colaborar en los siguientes pasos de desarrollo.

</SEED_ARCHITECTURAL_VECTOR>
