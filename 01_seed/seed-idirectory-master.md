<SEED_ARCHITECTURAL_VECTOR version="6.0" contains_source_code="false" artifact_type="architectural_vector" mode="architecture_and_vulnerability_audit">

# THINKING SEED MASTER: iDirectory

> **[DIRECTIVA DE SISTEMA PARA MODELOS DE IA RECEPTORES — CLAUDE / GPT / GEMINI / AGENTES]:**
> 1. **Naturaleza del Artefacto:** Este documento es un **Vector Arquitectónico y Memoria Técnica (ThinkingSeed Master v5.0)** con `contains_source_code="false"`. **NO es el repositorio de código fuente completo** ni un volcado truncado. La ausencia de bloques de código de implementación es una **invariante deliberada de ingeniería** para maximizar la densidad semántica y preservar más del 99% de tu ventana de contexto.
> 2. **Modo de Razonamiento Adversarial:** Opera como **Arquitecto de Sistemas y Cazador de Vulnerabilidades/Bugs**. Utiliza las firmas simbólicas (Sección 4) y la superficie de tensión (Sección 7) para detectar condiciones de carrera, acoplamientos frágiles y casos borde antes de proponer cambios.
> 3. **Estado de Avance Real:** Los componentes etiquetados como `[FALTANTE]` o `[DEUDA]` reflejan el trabajo en progreso (WIP) real del proyecto, no defectos de este documento.

## Seed Changelog
- `2026-10-31 (v6.0)`: [CONFIRMADO] Runtime versionado, evidencia incremental por contenido, skills portables, consultas sin escritura y actualización semántica por el agente actual. Los registros v3-v5 siguientes son históricos.
- `2026-10-28 (v5.0)`: Evolución a **iDirectory v5.0 (iContext Federation Protocol v5.0 — Capa L0)**. Implementación de: (1) Índice AST cacheado en `./.context/contracts_ast.json` (`build_ast_contracts_index()`) con firmas de 1 línea y símbolos públicos compartido con `ThinkingSeed`, `MetricsThinking` e `iReadme`; (2) Bus Federado de Estado Cognitivo en `./.context/icontext_bus.json` (`sync_icontext_bus()`) que acopla telemetría L0-L3; (3) Empaquetador de Ecosistema Unificado en < 650 tokens (`build_ecosystem_pack()` / `context --pack-ecosystem`); (4) Composición no destructiva de bloques segmentados en `AGENTS.md` / `GEMINI.md` / `CLAUDE.md` (`upsert_segmented_block()`); (5) Esquemas formales Draft-07 `./schemas/icontext_bus.schema.json` y `./schemas/contracts_ast.schema.json`; (6) Suite expandida a 77 pruebas automatizadas (69 en `test_fwengine.py` + 8 en `test_token_budget.py`) con 100% de éxito.
- `2026-10-28 (v4.1)`: Consolidación iDirectory v4.1 en commit `fa05e65`. Implementación de: (1) Reconciliación de planes y archivado automático (`reconcile_plans_lifecycle()`) para neutralizar "Zombie Plans"; (2) Formalización del directorio `artifacts/plans/backlog/` (`crawl: false`, `p2`) y esquema Draft-07 en `./schemas/backlog.schema.json` para registro atómico de intenciones (`queue.json`); (3) Verificación de DAG de dependencias inter-módulos (`validate_dependency_dag()`) y resolución inversa de imports cruzados (`_resolve_imported_module_to_repo_dir()`); (4) Cálculo de huella física por nodo (`compute_node_fingerprint()`) e integración reforzada en `reconcile`; (5) Expansión de la suite a 74 pruebas automatizadas (66 en `test_fwengine.py` y 8 en `test_token_budget.py`) con 100% de éxito.
- `2026-10-26 (v4.0)`: Reingeniería integral iDirectory v4.0 (Adaptive Context & Deterministic Control-Plane). Implementación de: (1) Fingerprint criptográfico determinista SHA-256 (`topology_hash`) en `./.context/tree.json` vía `compute_topology_hash()` inmune a distorsiones de `mtime`; (2) Poda estricta `crawl: false` en `compute_context_budget()` y estimador multimodal `estimate_tokens_v4()` que excluye binarios; (3) Bootloader Adaptativo de Dos Niveles y Tres Perfiles (Tier 1A, Tier 1B, Tier 2) gobernado por `./config/context_policy.json`; (4) Compilador de paquetes de contexto en un solo paso (`context --pack <dir> --tier 1a` < 220 tokens); (5) Navegación seccional del Seed Maestro (`seed --toc` y `seed --section <id>`); (6) Máquina de estados de continuidad atencional en `./.context/checkpoint.json` (`checkpoint --show/--set/--clear`); (7) Comando unificado e idempotente de cierre (`reconcile` y `reconcile --check`); (8) Esquemas formales Draft-07 ampliados (`checkpoint.schema.json`, `plan_metadata.schema.json`, `tree.schema.json` y `beacon.schema.json`).
- `2026-10-24 (v3.5)`: Consolidación arquitectónica iDirectory v3.5 en commit `aeae4e4`. Verificación y sincronización de beacons estructurales en 31 nodos canónicos y de extensión (`02_foundation`, `03_research`, `artifacts`, `data`, `docs`, `infrastructure`, `src`). Integración estricta de validación formal en stdlib pura contra `./schemas/beacon.schema.json` y subgrafos condicionales en `./schemas/tree.schema.json`.
- `2026-10-24 (v3.3)`: Cierre integral de las 7 brechas forenses (`[GAP-01]` a `[GAP-07]`) detectadas en la auditoría post-v3.2: (1) Preservación automática de enriquecimiento agéntico; (2) Simetría de des-escapado JSON en `MiniYAML._unquote()`; (3) Validación estructural de `.context.yaml` en stdlib pura; (4) Incorporación de `key_files` físicos locales y consumidores aguas abajo en `generate_sliced_tree()`; (5) Poda estricta `os.walk`; (6) Detección de mayúsculas en profundidad completa (`[INV-06]`).
- `2026-10-24 (v3.2)`: Implementación integral del motor de auto-scaffolding reactivo de beacons en `FWengine.py`. Fortalecimiento I/O contra bloqueos transitorios en Windows NTFS (`safe_io_retry` y `safe_rename_casing`). Recorte topológico dinámico mediante `map --slice <dir>` (< 150 tokens).
- `2026-10-21 (v3.1)`: Re-ingeniería completa de `FWengine.py` a v3.1 y sincronización con ThinkingSeed Master. Desacoplamiento de `crawl: true` y `tier1_preload: false` en `01_seed/`.
- `2026-10-21 (v3.0)`: Migración integral al estándar formal ThinkingSeed Master v3.0 con encapsulamiento XML determinista `<SEED_ARCHITECTURAL_VECTOR>`.
- `2026-10-14`: Implementación del Two-Tier Bootloader con herencia jerárquica de beacons.
- `2026-09-25`: Creación inicial de topología canónica normalizada en minúsculas y motor CLI de gobernanza con cero dependencias externas.

---

## 0. IDENTIDAD, METADATOS Y CONTRATO DEL RECEPTOR

```yaml
seed_schema_version: "6.0"
project_name: "iDirectory"
repository_name: "iDirectory"
project_type: "context_engineering_governance_framework"
repository_mode: "monorepo"
generated_at: "2026-10-31T19:22:24.618451+00:00"
generated_by: "Codex / iContext v6 migration"
repository_root: "./"
git_branch: "master"
git_commit: "fa05e65"
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

[CONFIRMADO] Gobierna la topología y entrega contexto acotado mediante inventario persistido, poda heredada, contratos AST por contenido y checkpoints por sesión. El motor mantiene cero dependencias externas y distribuye lanzadores compatibles desde un origen canónico.

[CONFIRMADO] Puede operar sin clones de los otros repositorios. La federación comparte artefactos versionados y ContextControl coordina el flujo cuando está disponible.

## 2. ARQUITECTURA, TOPOLOGÍA Y FRONTERAS MODULARES

### 2.0 Estado vigente v6

[CONFIRMADO] En v6, FWengine.py es un lanzador y tools/icontext_runtime es una distribución generada. Los orígenes mantenidos están en iDirectory/src/core y ContextControl/src/core; las copias generadas se verifican por manifest. skills/v6 contiene bundles con scripts y recursos completos. Las capas siguen siendo L0 iDirectory, L1 ThinkingSeed, L2 MetricsThinking y L3 iReadme.

### 2.1 Bootloader Adaptativo de Dos Niveles y Tres Perfiles (v4.1) `[CONFIRMADO]`
La arquitectura v4.1 implementa una selección adaptativa de tres perfiles operacionales regulada por la política única `./config/context_policy.json`:

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
| `./artifacts/plans/active/` | `active_plans` | `p1` | `true` | `optional` | Planes de capacidad e hitos vigentes (`plan_reingenieria_v4.md`). |
| `./artifacts/plans/metricsthinking/`| `metrics_evaluation`| `p2` | `true` | `optional` | Evaluación forense de madurez y roadmap de remediación (`MetricsThinking.json`). |
| `./artifacts/plans/backlog/` | `intent_backlog` | `p2` | `false` | `optional` | Registro estructurado de tareas pendientes e intenciones (`queue.json`). |
| `./artifacts/plans/archive/` | `archived_plans` | `p3` | `false` | `optional` | Histórico de planes descartados y documentación obsoleta (rama muerta). |
| `./docs/architecture/` | `architecture_diagrams`| `p1` | `true` | `optional` | Diagramas de arquitectura multi-cloud, topologías C4 y flujos Medallion. |
| `./docs/specs/` | `technical_specs` | `p1` | `true` | `optional` | Especificaciones técnicas de negocio, linaje y requerimientos no funcionales. |
| `./docs/notes/` | `engineers_notes` | `p2` | `true` | `optional` | Bitácoras de ingeniería, ADRs rápidos y análisis de causa raíz (RCA). |
| `./config/` | `configuration` | `p1` | `true` | `optional` | Parámetros de entorno y política unificada de contexto (`context_policy.json`). |
| `./data/raw/` | `bronze_storage` | `p3` | `false` | `optional` | Capa Bronze inmutable de aterrizaje local. Ignorado en Git y AI. |
| `./data/processed/` | `silver_gold_storage` | `p3` | `false` | `optional` | Capas Silver y Gold transformadas en formatos binarios (Parquet, Delta). |
| `./data/sandbox/` | `sandbox` | `p3` | `false` | `optional` | Entorno de experimentación aislado para científicos de datos. |
| `./schemas/` | `data_contracts` | `p1` | `true` | `optional` | Esquemas estrictos Draft-07 (`tree`, `beacon`, `checkpoint`, `plan_metadata`, `backlog`). |
| `./scripts/` | `ops_automation` | `p2` | `true` | `optional` | Scripts operativos del sistema operativo para mantenimiento y despliegue. |
| `./tests/` | `test_suites` | `p1` | `true` | `optional` | Suites de pruebas unitarias, adversariales, estrés y token budget Tri-Baseline. |
| `./tools/` | `tooling` | `p2` | `true` | `optional` | Herramientas internas, linters y scripts auxiliares. |
| `./logs/` | `logs` | `p3` | `false` | `optional` | Trazas locales de ejecución y volcados de error (rama muerta). |
| `./.context/` | `context_engineering` | `p0` | `true` | `optional` | Mapa topológico satelital (`tree.json`), fingerprint SHA-256 y continuidad (`checkpoint.json`). |
| `./infrastructure/` | `domain_extension` | `p1` | `true` | `optional` | Plantillas de IaC (Terraform, Bicep, Pulumi) descubiertas dinámicamente. |

### 2.3 Reglas de Poda e Invariantes de Crawling `[CONFIRMADO]`
- **Herencia Jerárquica de Poda (`[INV-03]`):** Si un directorio o cualquiera de sus ancestros declara `crawl: false` (como `./data/raw/`, `./data/processed/`, `./data/sandbox/`, `./logs/`, `./artifacts/plans/archive/`, `./artifacts/plans/backlog/`), queda estrictamente prohibida la exploración o volcado recursivo por parte de agentes de IA.
- **Contrato de Cierre Unificado e Idempotente (`[INV-04]`):** Toda mutación física topológica impone la ejecución de un único comando idempotente de cierre: `python FWengine.py reconcile`.

---

## 3. FLUJOS DE EJECUCIÓN, ENTRY POINTS Y CICLO DE VIDA

### 3.0 Estado vigente v6

[CONFIRMADO] El flujo v6 es detectar cambios, actualizar evidencia L0, preparar SeedMaster, evaluar Metrics y preparar README. sync devuelve 3 cuando el agente debe redactar, 1 ante fallo requerido y 0 al completar. prepare es de lectura; complete rechaza hashes de entrada que hayan cambiado. Sin subcomando se muestra ayuda; las reparaciones requieren doctor --fix.

### 3.1 Puntos de Entrada (Entry Points) `[CONFIRMADO]`
1. **Motor CLI Central (`./FWengine.py`):** CLI unificada sin librerías externas que proporciona los subcomandos `reconcile` (`--check`), `context` (`--pack`, `--pack-ecosystem`, `--bus`, `--tier`, `--compact`, `--budget`), `seed` (`--toc`, `--section`), `checkpoint` (`--show`, `--set`, `--clear`, `--plan-id`, `--status`, `--phase`, `--next`, `--step-done`), `map` (`--slice`, `--radius`, `--include-pruned`, `--sync`, `--check-freshness`), `beacon` (`--sync`, `--audit`, `--resolve`, `--no-discover`, `--force-defaults`), `route` (`--move`, `--base`, `--overwrite`) y `audit` (`--fix`).
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
       ├─► Reconcilia Ciclo de Vida de Planes (Archiva Superseded)
       ├─► Valida Cola de Backlog (queue.json) y DAG de Dependencias
       ├─► Descubre y Auto-Scaffoldea Beacons Faltantes
       ├─► Valida Estructuralmente Beacons contra schemas/beacon.schema.json
       ├─► Computa Fingerprint Criptográfico SHA-256 (topology_hash)
       └─► Regenera Satélite .context/tree.json Actualizado
```

---

## 4. CONTRATOS SIMBÓLICOS, MODELO DE DATOS Y PERSISTENCIA

### 4.1 Contratos públicos vigentes v6

[CONFIRMADO] Firmas simbólicas extraídas de archivos activos, con hash de contenido y versión del analizador.

- `./skills/v6/idir/scripts/run.py::./skills/v6/idir/scripts/run.py::matches_version(path) -> Any`
- `./src/core/context_runtime.py::./src/core/context_runtime.py::read_json(path, default=None) -> Any`
- `./src/core/context_runtime.py::./src/core/context_runtime.py::digest(value) -> Any`
- `./src/core/context_runtime.py::./src/core/context_runtime.py::atomic_write(path, content) -> Any`
- `./src/core/context_runtime.py::./src/core/context_runtime.py::write_json(path, value) -> Any`
- `./src/core/context_runtime.py::./src/core/context_runtime.py::repository_lock(root, name='publish', timeout=10) -> Any`
- `./src/core/context_runtime.py::./src/core/context_runtime.py::publish_layer(root, layer, payload) -> Any`
- `./src/core/context_runtime.py::./src/core/context_runtime.py::ignore_patterns(root) -> Any`
- `./src/core/context_runtime.py::./src/core/context_runtime.py::ignored(relative, patterns) -> Any`
- `./src/core/context_runtime.py::./src/core/context_runtime.py::crawl_allowed(directory) -> Any`
- `./src/core/context_runtime.py::./src/core/context_runtime.py::iter_files(root, patterns=None) -> Any`
- `./src/core/context_runtime.py::./src/core/context_runtime.py::python_contracts(source, relative) -> Any`
- `./src/core/context_runtime.py::./src/core/context_runtime.py::inventory(root, persist=False, full=False) -> Any`
- `./src/core/context_runtime.py::./src/core/context_runtime.py::contracts_index(root, persist=False, full=False) -> Any`
- `./src/core/context_runtime.py::./src/core/context_runtime.py::input_hash(inv, layer) -> Any`
- `./src/core/context_runtime.py::./src/core/context_runtime.py::estimated_tokens(value) -> Any`
- `./src/core/context_runtime.py::./src/core/context_runtime.py::bounded(payload, limit, removable=('contracts_ast', 'edges', 'files', 'active_topology', 'layers')) -> Any`
- `./src/core/context_runtime.py::./src/core/context_runtime.py::query_orientation(root, target='.', tier='1a', expand=False) -> Any`
- `./src/core/context_runtime.py::./src/core/context_runtime.py::validate_seed(path, index=None) -> Any`
- `./src/core/context_runtime.py::./src/core/context_runtime.py::validate_readmes(root) -> Any`
- `./src/core/fwengine.py::./src/core/fwengine.py::MiniYAML(class)`
- `./src/core/fwengine.py::./src/core/fwengine.py::safe_io_retry(operation: Callable[[], Any], max_attempts: int=4, initial_delay_ms: float=25.0) -> Any`
- `./src/core/fwengine.py::./src/core/fwengine.py::safe_rename_casing(src: Path, dest: Path) -> Path`
- `./src/core/fwengine.py::./src/core/fwengine.py::estimate_tokens_v4(text_or_path: Any, fast_stat_only: bool=False) -> int`
- `./src/core/fwengine.py::./src/core/fwengine.py::resolve_seed_key_files(root_path: Path) -> List[str]`
- `./src/core/fwengine.py::./src/core/fwengine.py::generate_beacon_content(folder: str, meta: Dict[str, Any], root_path: Optional[Path]=None) -> str`
- `./src/core/fwengine.py::./src/core/fwengine.py::resolve_beacon(dir_path: Path, root_path: Path) -> Dict[str, Any]`
- `./src/core/fwengine.py::./src/core/fwengine.py::extract_preserved_comments(beacon_file: Path) -> List[str]`
- `./src/core/fwengine.py::./src/core/fwengine.py::validate_beacon_data(data: Dict[str, Any]) -> List[str]`
- `./src/core/fwengine.py::./src/core/fwengine.py::validate_tree_data(data: Dict[str, Any]) -> List[str]`
- `./src/core/fwengine.py::./src/core/fwengine.py::validate_backlog_data(data: Dict[str, Any]) -> List[str]`
- `./src/core/fwengine.py::./src/core/fwengine.py::validate_backlog_queue(root_path: Path, check_only: bool=False) -> List[str]`
- `./src/core/fwengine.py::./src/core/fwengine.py::load_ignore_patterns(root_path: Path) -> List[str]`
- `./src/core/fwengine.py::./src/core/fwengine.py::is_ignored_path(dir_path: Path, root_path: Path, patterns: Optional[List[str]]=None) -> bool`
- `./src/core/fwengine.py::./src/core/fwengine.py::discover_unbeaconed_directories(root_path: Path) -> List[Path]`
- `./src/core/fwengine.py::./src/core/fwengine.py::infer_beacon_meta(dir_path: Path, root_path: Path) -> Dict[str, Any]`
- `./src/core/fwengine.py::./src/core/fwengine.py::scaffold_beacon_for_dir(dir_path: Path, root_path: Path, overwrite: bool=False) -> Optional[Path]`
- `./src/core/fwengine.py::./src/core/fwengine.py::ensure_beacon_chain(target_dir: Path, root_path: Path) -> List[Path]`
- `./src/core/fwengine.py::./src/core/fwengine.py::iter_beacon_files(root_path: Path) -> List[Path]`
- `./src/core/fwengine.py::./src/core/fwengine.py::sync_beacons(root_path: Path, auto_discover: bool=True, force_defaults: bool=False) -> int`
- `./src/core/fwengine.py::./src/core/fwengine.py::compute_topology_hash(root_path: Path) -> str`
- `./src/core/fwengine.py::./src/core/fwengine.py::compute_node_fingerprint(dir_path: Path) -> str`
- `./src/core/fwengine.py::./src/core/fwengine.py::generate_tree_json(root_path: Path) -> Dict[str, Any]`
- `./src/core/fwengine.py::./src/core/fwengine.py::check_satellite_freshness(root_path: Path) -> Dict[str, Any]`
- `./src/core/fwengine.py::./src/core/fwengine.py::format_compact_tree_json(data: Dict[str, Any]) -> str`
- `./src/core/fwengine.py::./src/core/fwengine.py::sync_tree(root_path: Path) -> Path`
- `./src/core/fwengine.py::./src/core/fwengine.py::generate_sliced_tree(root_path: Path, target_path: str, radius: int=1, max_children: int=6) -> Dict[str, Any]`
- `./src/core/fwengine.py::./src/core/fwengine.py::format_sliced_tree(data: Dict[str, Any]) -> str`
- `./src/core/fwengine.py::./src/core/fwengine.py::build_context_pack(root_path: Path, target_path: str, tier: str='1a', expand: bool=False) -> Dict[str, Any]`
- `./src/core/fwengine.py::./src/core/fwengine.py::build_context_capsule(root_path: Path, target_path: str, task_description: str='') -> Dict[str, Any]`
- `./src/core/fwengine.py::./src/core/fwengine.py::get_seed_sections(root_path: Path) -> List[Dict[str, Any]]`
- `./src/core/fwengine.py::./src/core/fwengine.py::extract_seed_section(root_path: Path, query: str) -> str`
- `./src/core/fwengine.py::./src/core/fwengine.py::manage_checkpoint(root_path: Path, action='show', plan_id=None, status=None, phase=None, next_action=None, completed_step=None, session_id=None, objective=None, constraints=None, decisions=None, evidence_hash=None, expires_at=None) -> Any`
- `./src/core/fwengine.py::./src/core/fwengine.py::build_ast_contracts_index(root_path: Path, write_to_disk: bool=True) -> Dict[str, Any]`
- `./src/core/fwengine.py::./src/core/fwengine.py::sync_icontext_bus(root_path: Path, tree_data=None, ast_index=None, write_to_disk=True) -> Any`
- `./src/core/fwengine.py::./src/core/fwengine.py::build_ecosystem_pack(root_path: Path, expand: bool=False) -> Dict[str, Any]`
- `./src/core/fwengine.py::./src/core/fwengine.py::upsert_segmented_block(file_path: Path, tool_key: str, block_content: str) -> bool`
- `./src/core/fwengine.py::./src/core/fwengine.py::compute_context_budget(root_path: Path, include_pruned_stats: bool=False) -> List[Dict[str, Any]]`
- `./src/core/fwengine.py::./src/core/fwengine.py::init_project(base_path: str) -> Any`
- `./src/core/fwengine.py::./src/core/fwengine.py::inspect_python_header(file_path: Path, max_chars: int=4096) -> str`
- `./src/core/fwengine.py::./src/core/fwengine.py::route_file(file_path: str, base_path: str='.', move: bool=False, overwrite: bool=False) -> Optional[Path]`
- `./src/core/fwengine.py::./src/core/fwengine.py::reconcile_plans_lifecycle(root_path: Path, check_only: bool=False) -> List[str]`
- `./src/core/fwengine.py::./src/core/fwengine.py::validate_dependency_dag(root_path: Path, changed_nodes: Optional[List[str]]=None) -> List[str]`
- `./src/core/fwengine.py::./src/core/fwengine.py::audit_repository(root_path: Path, fix: bool=False) -> bool`
- `./src/core/fwengine.py::./src/core/fwengine.py::reconcile_repository(root_path: Path, check_only: bool=False) -> bool`
- `./src/core/fwengine.py::./src/core/fwengine.py::main() -> Any`
- `./tools/build_runtime.py::./tools/build_runtime.py::put(path, raw, check=False) -> Any`
- `./tools/build_runtime.py::./tools/build_runtime.py::build(check=False) -> Any`

CLI flags: `--audit`, `--base`, `--budget`, `--bus`, `--capsule`, `--check`, `--check-freshness`, `--clear`, `--compact`, `--constraint`, `--decision`, `--evidence-hash`, `--expand`, `--expires-at`, `--fix`, `--force-defaults`, `--include-pruned`, `--move`, `--next`, `--no-discover`, `--objective`, `--overwrite`, `--pack`, `--pack-ecosystem`, `--phase`, `--plan-id`, `--radius`, `--resolve`, `--section`, `--session-id`, `--set`, `--show`, `--slice`, `--status`, `--step-done`, `--sync`, `--target`, `--task`, `--tier`, `--toc`

### 4.2 Artefactos y propiedad de escritura

[CONFIRMADO] .context/orientation_cache.json conserva vistas compiladas; las consultas rápidas verifican poda y metadatos de archivos y declaran la generación registrada. El CLI usa UTF-8 en Windows.

[CONFIRMADO] .context/inventory.json mantiene evidencia; .context/contracts_ast.json conserva contratos; .context/layers contiene estados por productor y icontext_bus.json se agrega bajo bloqueo del repositorio. .context/sync_state.json registra entradas y salidas aceptadas. .context/update_request.json transfiere redacción pendiente. Los checkpoints de sesión tienen identidad, objetivo, restricciones, decisiones, evidencia y próxima acción.

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
- `./.agentignore`: Define la máscara de exclusión de lectura para agentes autónomos (`./data/raw/`, `./data/processed/`, `./data/sandbox/`, `./logs/`, `*.parquet`, `*.csv`, `*.delta/`, `.venv/`, `__pycache__/`, `.git/`, `./artifacts/plans/archive/`, `./artifacts/plans/backlog/`).
- `./.gitignore`: Ignora artefactos efímeros, entornos virtuales y datasets locales pesados.

---

## 6. PRUEBAS, CI/CD, DESPLIEGUE Y OPERACIÓN

### 6.1 Suite Unitaria (`./tests/test_fwengine.py`) `[CONFIRMADO]`
Contiene 66 casos de prueba automatizados con un ratio de éxito de 100% (`OK`) (74 casos de prueba totales en el repositorio incluyendo benchmarks):
- Verificación de serialización y deserialización simétrica de `MiniYAML` con tipos primitivos complejos y comillas escapadas.
- Inicialización determinista del andamiaje de directorios y satélite con cálculo de `topology_hash`.
- Ruteo heurístico por extensión y verificación de inspección de cabeceras de Python vía `ast.parse()`.
- Mecanismo seguro de renombrado case-insensitive en Windows NTFS (`.tmp_{pid}_{name}`) con exponential backoff (`safe_io_retry`).
- Herencia jerárquica y prevalencia de `crawl: false` en `resolve_beacon()`.
- Rechazo frontal de intentos de Path Traversal (`PermissionError`).
- Resolución dinámica del nombre de seeds en repositorios externos (`test_dynamic_seed_name_resolution`).
- Auto-descubrimiento de carpetas de dominio no canónicas (`test_domain_extension_autodiscovery`).
- Validación de existencia física de contratos formales de satélite, beacons, checkpoints, planes y backlog.
- Auto-scaffolding de balizas huérfanas, preservación de enriquecimiento semántico y validación activa de esquemas.
- Recorte topológico dinámico en subgrafos con aristas `dep` y `consumer` (`TestTreeSlicing`).
- Pruebas adversariales v4.0: Validación de `compute_topology_hash()`, inyección compacta Tier 1A (`context --pack`), navegación seccional del Seed (`seed --toc` y `seed --section`), máquina de estados de `checkpoint` y reconciliación unificada (`reconcile`).
- Pruebas de gobernanza v4.1: Validación de reconciliación de planes y archivado automático, integridad de `queue.json`, detección de ciclos en dependencias (`validate_dependency_dag`) y resolución estricta de imports.

### 6.2 Benchmarks de Presupuesto de Tokens (`./tests/test_token_budget.py`) `[CONFIRMADO]`
Contiene 8 pruebas de telemetría y rendimiento que evalúan la compresión de contexto, densidad de balizas y presupuestos de subgrafos:
- Ahorro de contexto verificado: **95.3%** de reducción en tokens consumidos frente al escaneo recursivo ingenuo (`~20,336 tokens` vs `~955 tokens`).
- Benchmark Tri-Baseline verificado: Naive = 17,710 tokens, ModernIgnore = 379 tokens, Tier 1A Pack = **63 tokens**.
- Formato de inyección compacta (`IDIR_TOPOLOGY`): **~163 tokens** (cumpliendo holgadamente el umbral `< 250 tokens`).
- Subgrafos focalizados (`map --slice <dir>`): **~83 tokens** para subdirectorios (`src/core`), **~117 tokens** para ramas secundarias (`docs`), superando holgadamente el límite de `< 150 tokens`.
- Densidad de balizas: 100% de los archivos `.context.yaml` cumplen el límite de densidad estricta (`<= 600 caracteres` / `~150 tokens`).
- Latencia de generación satelital bajo estrés: **82.00 ms**; escaneo de budget: **172.42 ms**.

### 6.3 Pipeline de CI/CD (`./.github/workflows/ci.yml`) `[CONFIRMADO]`
Workflow automatizado activado en eventos `push` y `pull_request` sobre ramas `master` y `main`:
1. Matriz 3x4: 3 sistemas operativos (Ubuntu, Windows, macOS) x 4 versiones de Python (3.10 a 3.13).
2. Verificación de arquitectura Zero-Dependency.
3. Ejecución de reconciliación y auditoría de gobernanza: `python FWengine.py reconcile --check`.
4. Ejecución de suite unitaria: `python -m unittest discover -s tests -p "test_*.py" -v`.
5. Ejecución de benchmarks de token budget: `python -m unittest tests/test_token_budget.py -v`.

---

## 7. SUPERFICIE DE TENSIÓN, CONTRADICCIONES Y MODOS DE FALLA

- [CONFIRMADO] La ruta rápida reutiliza tamaño y mtime_ns para evitar lecturas. La verificación --full recalcula contenidos, incluso ante timestamps restaurados; la consulta de estado registrada no certifica por sí sola la frescura física.
- [CONFIRMADO] Los contratos AST automáticos cubren Python a nivel de módulo. No equivalen a cobertura semántica de todos los lenguajes, cuerpos de funciones o comportamiento observado del producto.
- [CONFIRMADO] FPAI y el recuento heurístico de tokens son indicadores auxiliares. La distorsión y los resultados de atención no observados permanecen expresamente sin medir.
- [CONFIRMADO] complete comprueba estructura y contratos públicos; la exactitud narrativa requiere revisión del agente sobre la evidencia afectada. La ausencia de errores estructurales no demuestra ausencia de bugs.
- [CONFIRMADO] La agregación del bus usa bloqueo de proceso. El checkpoint compatible apunta a la última sesión seleccionada; la continuidad paralela debe usar identificadores de sesión explícitos.
- [CONFIRMADO] La paridad de bundles y sus comandos puede comprobarse sin invocar modelos. El éxito de tareas en sesiones reales de ambos proveedores requiere evidencia observada separada y no se presume de estas pruebas.

## 8. SEGURIDAD, PRIVACIDAD Y GUARDRAILS

### 8.1 Blindaje contra Path Traversal `[CONFIRMADO]`
- En `route_file()`, cualquier entrada que contenga secuencias relativas hacia arriba (`..` en `raw_path.parts`) es bloqueada antes de interactuar con el sistema de archivos lanzando `PermissionError("[-] Error de Seguridad: Intento de Path Traversal bloqueado ('..' detectado en '...').")`.
- Se valida estrictamente mediante `path.resolve().relative_to(base_dir)` que tanto el origen como el destino resuelto permanezcan contenidos dentro del límite físico del repositorio.

### 8.2 Guardrails para Agentes de Inteligencia Artificial `[CONFIRMADO]`
1. **Prohibición de Escaneo Ciego Recursivo (`[INV-02]`):** Queda prohibida la ejecución de comandos de exploración profunda no restringidos (`Get-ChildItem -Recurse`, `find .`, `ls -R`). Toda navegación debe iniciar consultando `context --pack`, `context --compact` o `.context/tree.json`.
2. **Invariante de Ramas Muertas (`[INV-03]`):** Los directorios con directiva `crawl: false` (`./data/raw/`, `./data/processed/`, `./data/sandbox/`, `./logs/`, `./artifacts/plans/archive/`, `./artifacts/plans/backlog/`) son considerados almacenes de datos o ramas muertas; los agentes tienen prohibido volcar su contenido al contexto.
3. **Contrato de Cierre Unificado e Idempotente (`[INV-04]`):** Cualquier cambio estructural en la topología física exige ejecutar `python FWengine.py reconcile` antes de dar la tarea por finalizada.
4. **Política Zero-Trust de Credenciales (`[INV-05]`):** Ofuscación estricta `<REDACTED>` para tokens, credenciales o API keys detectados en configuraciones o entornos locales.

---

## 9. ESTADO REAL, DEUDA TÉCNICA Y DECISIONES (ADRs)

### 9.0 Estado vigente v6

[CONFIRMADO] La migración v6 conserva los comandos compatibles y registra las pruebas y mediciones de esta entrega en .context/v6_validation.json y .context/benchmark_v6.json. Las reglas y workflows anteriores se conservan como referencias históricas podadas. La versión de cada proyecto puede fijarse en .context/toolchain.json.

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
- `[ADR-010]` **Gestión de Backlog de Intenciones y Validación de DAG:** Se segregó `artifacts/plans/backlog/` (`crawl: false`) con `schemas/backlog.schema.json` y se añadió verificación estricta de aciclicidad en el DAG de dependencias inter-módulos.

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
| `DEBT-10` | `./artifacts/plans/active/` | **Media** | Riesgo de reactivación de planes obsoletos ("Zombie Plans") consumiendo tokens de contexto. | `[RESUELTO EN v4.1]` Implementado `reconcile_plans_lifecycle()` que archiva a `archive/` en `reconcile`. |

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
- **Intent Backlog (`queue.json`):** Cola estructurada y validada por esquema que almacena intenciones diferidas sin saturar el contexto de planes activos.

### 10.3 Índice de Evidencias Físicas
- Motor de gobernanza y CLI: `./FWengine.py` `[CONFIRMADO]`
- Satélite topológico principal: `./.context/tree.json` `[CONFIRMADO]`
- Bus Cognitivo Federado v5.0: `./.context/icontext_bus.json` `[CONFIRMADO]`
- Índice Cacheado de Contratos AST v5.0: `./.context/contracts_ast.json` `[CONFIRMADO]`
- Checkpoint de continuidad atencional: `./.context/checkpoint.json` `[CONFIRMADO]`
- Política canónica de contexto: `./config/context_policy.json` `[CONFIRMADO]`
- Cola de backlog de intenciones: `./artifacts/plans/backlog/queue.json` `[CONFIRMADO]`
- Esquema formal del satélite: `./schemas/tree.schema.json` `[CONFIRMADO]`
- Esquema formal de micro-balizas: `./schemas/beacon.schema.json` `[CONFIRMADO]`
- Esquema formal de checkpoint: `./schemas/checkpoint.schema.json` `[CONFIRMADO]`
- Esquema formal de planes: `./schemas/plan_metadata.schema.json` `[CONFIRMADO]`
- Esquema formal de backlog: `./schemas/backlog.schema.json` `[CONFIRMADO]`
- Esquema formal del bus federado v5.0: `./schemas/icontext_bus.schema.json` `[CONFIRMADO]`
- Esquema formal del índice de contratos AST v5.0: `./schemas/contracts_ast.schema.json` `[CONFIRMADO]`
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
> "Esto es una semilla de proyecto (**ThinkingSeed Master v5.0**): el vector arquitectónico y ADN del proyecto (`contains_source_code="false"`), no su repositorio completo. Refleja el avance real, los contratos simbólicos y la superficie de tensión del sistema hasta la fecha. Como modelo receptor, tu función es usar esta semilla como memoria técnica para:
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
1. Un saludo confirmando que asimilaste el ADN arquitectónico v5.0 de **iDirectory** (`<SEED_ARCHITECTURAL_VECTOR>`) y su stack principal (Python Standard Library, Adaptive Context Engineering, iContext Federation Protocol v5.0, Three-Profile Bootloader, Intent Backlog).
2. Un breve resumen de 2-3 líneas sobre el objetivo, su estado actual y sus principales vectores de tensión (resiliencia NTFS I/O mediante safe_io_retry, paquetes atómicos Tier 1A y Ecosistema v5.0 mediante context --pack / --pack-ecosystem, bus federado icontext_bus.json y reconciliación unificada mediante reconcile).
3. Una frase poniéndote a disposición para resolver dudas sobre su funcionamiento o colaborar en los siguientes pasos de desarrollo.

</SEED_ARCHITECTURAL_VECTOR>
