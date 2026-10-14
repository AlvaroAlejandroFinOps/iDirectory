# ThinkingSeed Master: iDirectory

> [!NOTE]
> Snapshot de arquitectura y contexto técnico profundo para LLMs y Agentes Autónomos.
> Generado bajo el protocolo **seedMaster v3.0** (ThinkingSeed Master).

---

## 0. Identidad y Metadatos del Snapshot

- **Proyecto:** `iDirectory` (Gravity HyperScale Thinking) `[CONFIRMADO]`
- **Ruta Física Base:** `d:\0001 HyperScale Thinking\PROYECTOS CLOUD\iContext\iDirectory` `[CONFIRMADO]`
- **Versión de Arquitectura:** `v3.0` (Two-Tier Bootloader & Context Engineering Engine) `[CONFIRMADO]`
- **Fecha y Hora de Generación:** `2026-10-14 20:05:00 -03:00` `[CONFIRMADO]`
- **Agente Generador:** Antigravity IDE (Google DeepMind Advanced Agentic Coding) `[CONFIRMADO]`
- **Hash de Commit Git:** `106e760` `[CONFIRMADO]`
- **Estado del Working Tree:** `DIRTY` (Modificaciones de benchmark matrix y peritaje forense FlowAgentic en curso) `[CONFIRMADO]`
- **Arquetipo:** AI Agent Skills / Context Engineering / Repository Governance Engine `[CONFIRMADO]`
- **Lenguaje Base y Runtime:** Python 3.9+ (Zero-Dependency Invariant / Standard Library Pura) `[CONFIRMADO]`

### Convenciones Epistemológicas
- `[CONFIRMADO]`: Verificado directamente mediante lectura de código fuente, ejecución de pruebas o CLI.
- `[DECLARADO]`: Definido en especificaciones de arquitectura, contratos o documentación formal.
- `[INFERIDO]`: Deducido lógicamente de la topología física, patrones de uso o benchmarks.
- `[NO VERIFICADO]`: Presente en comentarios o roadmap pero sin suite de tests automatizada activa.
- `[FALTANTE]`: Brecha identificada durante la auditoría de contexto.

---

## 1. Resumen Ejecutivo y Propósito

### Propósito del Sistema `[DECLARADO]`
`iDirectory` es un framework de gobernanza topológica y optimización atencional (*Context Engineering*) diseñado para estructurar repositorios de código de forma que maximicen la eficiencia de tokens y eliminen la degradación de la ventana de contexto (*Attention Drift* y dispersión en cabezales de atención) en LLMs y agentes de codificación autónomos (Google Antigravity/Gemini, Anthropic Claude Code, OpenAI Codex, Cursor, Windsurf, Aider).

### El Problema Resuelto `[CONFIRMADO]`
1. **Atrofia Atencional por Ingesta Masiva:** La práctica habitual de los agentes de autoinyectar seeds completos de miles de tokens (~6,800 tokens) o escanear directorios recursivamente (`find .`, `Get-ChildItem -Recurse`) degrada la atención atencional y eleva el costo por turno en un 70–85%.
2. **Ambigüedad de Ruteo:** Proyectos sin convenciones canónicas acumulan scripts en la raíz o ubican modelos de datos y pruebas en directorios inconsistentes.
3. **Desincronización de Topología:** Cambios físicos en la estructura del proyecto que no alertan a los agentes, provocando que estos operen sobre mapas obsoletos (*Satellite Drift*).

### Consumidores Principales `[DECLARADO]`
- **Agentes Autónomos:** Lectura satelital del grafo topológico en ~250 tokens mediante [`.context/tree.json`](file:///.context/tree.json).
- **Ingenieros de Software / Data Engineers:** Estructura modular estándar con capas Medallion, orquestación, prompts y esquemas aislados.
- **Sistemas de CI/CD:** Linters y validadores de gobernanza deterministas ejecutables sin instalar dependencias vía `python FWengine.py audit`.

---

## 2. Arquitectura, Topología y Two-Tier Bootloader

### Protocolo Two-Tier Bootloader `[CONFIRMADO]`
La arquitectura v3.0 reemplaza el arranque monolítico lineal por un modelo bifurcado gobernado por una matriz de decisión estricta:

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
      │ 3. 01_seed/master.md (SEED) │    │ 3. resolve_beacon()         │
      │ 4. Beacons relevantes       │    │    (.context.yaml / parent) │
      │ 5. Ejecución global         │    │ 4. Modificación atómica     │
      └─────────────────────────────┘    └─────────────────────────────┘
```

#### Matriz de Decisión de 3 Disparadores `[DECLARADO]`
1. **Disparador 1 (Explícito - Usuario):** Comandos `/seedMaster`, `/metrics`, `/ultraThinking`, `/plan` o peticiones explícitas de reingeniería global. Habilita Tier 2.
2. **Disparador 2 (Estructural - Beacon):** El beacon local `.context.yaml` de la carpeta objetivo contiene `seed_reference: required`. (Si contiene `seed_reference: optional`, **permanece en Tier 1** sin precargar la semilla).
3. **Disparador 3 (Contingencia - Agente):** Detección de colisión de tipos/contratos con `schemas/` o necesidad de introducir una librería transversal no documentada. Permite lectura quirúrgica mediante `grep_search`.

### Topología Canónica Normalizada (All-Lowercase) `[CONFIRMADO]`
Todos los directorios raíz siguen la convención estricta en minúsculas para prevenir problemas de portabilidad y colisiones en sistemas de archivos Case-Preserving pero Case-Insensitive (Windows NTFS / macOS APFS):

| Directorio | Propósito y Contenido Canónico | Beacon | Directiva Crawl | Referencia a Semilla |
| :--- | :--- | :--- | :--- | :--- |
| `01_seed/` | ADN arquitectónico, snapshots `seed-*.md` y contratos base. | Sí | `crawl: true` | `seed_reference: required` |
| `02_foundation/` | Framework del motor `FWengine.py`, guías operativas. | Sí | `crawl: true` | `seed_reference: optional` |
| `03_research/` | Notebooks exploratorios, experimentos y prompts de IA. | Sí | `crawl: true` | `seed_reference: optional` |
| `src/` | Código de producción (`core/`, `cloud_jobs/`, `data_generation/`, `dashboards/`). | Sí | `crawl: true` | `seed_reference: optional` |
| `artifacts/` | Planes de implementación (`active/`, `archive/`), benchmarks y métricas. | Sí | `active: true`, `archive: false` | `metricsthinking: required` |
| `docs/` | Especificaciones de negocio, notas ADR y diagramas de arquitectura. | Sí | `crawl: true` | `seed_reference: optional` |
| `config/` | Archivos de configuración desacoplados por ambiente (`.yaml`, `.json`). | Sí | `crawl: true` | `seed_reference: optional` |
| `schemas/` | Contratos formales de datos (Avro, JSON Schema, DDL, Pydantic). | Sí | `crawl: true` | `seed_reference: optional` |
| `data/` | Capas Medallion locales (`raw/`, `processed/`, `sandbox/`). | Sí | `crawl: false` | `seed_reference: optional` |
| `tests/` | Suites de pruebas unitarias, integración y token budget. | Sí | `crawl: true` | `seed_reference: optional` |
| `tools/` | Utilidades de desarrollo, linters y scripts auxiliares. | Sí | `crawl: true` | `seed_reference: optional` |
| `scripts/` | Automatizaciones de despliegue y mantenimiento en terminal. | Sí | `crawl: true` | `seed_reference: optional` |
| `logs/` | Archivos de trazas operativas y auditorías locales. | Sí | `crawl: false` | `seed_reference: optional` |
| `.context/` | Satélite topológico `tree.json` y esquemas de Context Engineering. | Sí | `crawl: true` | `seed_reference: optional` |

---

## 3. Flujos de Ejecución y CLI: `FWengine.py`

El motor [`FWengine.py`](file:///d:/0001%20HyperScale%20Thinking/PROYECTOS%20CLOUD/iContext/iDirectory/FWengine.py) opera como una CLI unificada sin librerías externas.

### Comandos y Capacidades Principales `[CONFIRMADO]`

```powershell
# 1. Auditoría de gobernanza (reporte de salud, drift y estructura)
python FWengine.py audit

# 2. Inicialización / Actualización de topología estándar y beacons
python FWengine.py init

# 3. Ruteo heurístico híbrido (extensión + inspección de encabezado)
python FWengine.py route "ruta/archivo.py"

# 4. Reubicación física canónica del archivo ruteado
python FWengine.py route "ruta/archivo.py" --move

# 5. Sincronización de beacons (.context.yaml)
python FWengine.py beacon --sync

# 6. Sincronización del mapa satelital (.context/tree.json)
python FWengine.py map --sync

# 7. Telemetría de Context Engineering y Token Budget
python FWengine.py context --budget

# 8. Verificación de frescura satelital (detección de drift)
python FWengine.py audit --check-freshness
```

### Funciones Centrales del Motor `[CONFIRMADO]`
- `resolve_beacon(target_dir: Path, root_dir: Path) -> dict`: Implementa la **herencia jerárquica ascendente**. Si `target_dir` no posee un `.context.yaml` físico, asciende recursivamente por el árbol de directorios hasta encontrar el beacon del ancestro más próximo, combinando directivas de poda (`crawl: false`).
- `inspect_python_header(filepath: Path) -> Optional[str]`: Inspecciona de forma ultraligera las primeras 15 líneas de archivos Python para detectar palabras clave arquitectónicas (`pytest`, `unittest`, `streamlit`, `dash`, `pydantic`, `apache_beam`, `pyspark`) y evitar colisiones heurísticas basadas únicamente en la extensión.
- `check_satellite_freshness(root: Path) -> Tuple[bool, str]`: Valida que el archivo `.context/tree.json` no tenga una antigüedad mayor a la modificación física más reciente de la estructura del repositorio.
- `safe_relocate(src: Path, dst: Path)`: Previene ataques de *Path Traversal* validando que la ruta resuelta permanezca estrictamente contenida dentro del `ROOT_DIR`.
- `safe_rename_casing(folder: Path, canonical_name: str)`: En Windows NTFS, utiliza un directorio temporal intermedio (`__case_tmp__`) para garantizar cambios de mayúsculas/minúsculas atómicos sin pérdida de datos.

---

## 4. Modelos de Datos, Contratos y Esquemas

### Parser MiniYAML Incorporado `[CONFIRMADO]`
Dado el invariante de cero dependencias externas, `FWengine.py` incluye un parser/serializador determinista para microarchivos YAML compatible con subconjuntos clave-valor y listas indentadas:

#### Estructura de un Beacon Canónico (`.context.yaml`) `[DECLARADO]`
```yaml
module: src/core
role: Núcleo algorítmico y lógica de negocio pura
authority: Principal
crawl: true
seed_reference: optional
allowed_patterns:
  - "*.py"
forbidden_patterns:
  - "*.tmp"
  - "*.log"
dependencies: []
```

### Contrato del Satélite Topológico (`.context/tree.json`) `[CONFIRMADO]`
Genera una representación compacta en JSON optimizada para ser consumida en una sola llamada de lectura (~250 tokens):

```json
{
  "project": "iDirectory",
  "generated_at": "2026-10-14T20:00:00",
  "total_folders": 24,
  "structure": {
    "01_seed": {
      "role": "ADN arquitectónico del sistema y Ground Truth",
      "crawl": true,
      "seed_reference": "required"
    },
    "data/raw": {
      "role": "Datos crudos sin procesar",
      "crawl": false,
      "seed_reference": "optional"
    }
  }
}
```

---

## 5. Configuración y Entorno de Ejecución

- **Python Runtime:** 3.9 o superior `[CONFIRMADO]`.
- **Compatibilidad de SO:** Windows (PowerShell/CMD), Linux (Bash), macOS (Zsh) `[CONFIRMADO]`.
- **Políticas de Filesystem:**
  - Caracteres UTF-8 forzados en lectura/escritura (`encoding="utf-8"`).
  - Manejo de rutas nativas vía `pathlib.Path` agnóstica a barras `/` o `\`.
- **Zero-Dependency Invariant:** Prohibición absoluta de requerir `pip install` para la ejecución del motor `FWengine.py` `[CONFIRMADO]`.

---

## 6. Pruebas, Validación y Benchmarks

### Suite de Pruebas Unitarias `tests/test_fwengine.py` `[CONFIRMADO]`
La suite contiene 26 casos de prueba unitarios automatizados basados en `unittest` que cubren el 100% de los componentes críticos:

1. **Topología y Directorios:** Verificación de creación de las 24 carpetas canónicas en minúsculas.
2. **Parser MiniYAML:** Serialización y deserialización bidireccional de `.context.yaml`.
3. **Ruteo Heurístico Híbrido:** Validación de ruteo por extensión e inspección de encabezados (scripts de prueba a `tests/`, dashboards a `src/dashboards/`, schemas a `schemas/`).
4. **Herencia Jerárquica (`resolve_beacon`):** Prueba de resolución ascendente cuando subcarpetas anidadas carecen de beacon físico propio.
5. **Seguridad y Path Traversal:** Rechazo inmediato de rutas fuera del root (`../../evil.py`).
6. **Manejo de NTFS Casing:** Renombrado seguro sin colisión en Windows.
7. **Telemetría y Freshness:** Detección de drift en `tree.json` y cálculo del token budget.

*Resultado de ejecución local:* `Ran 26 tests in 0.082s - OK (100% Pass Rate)` `[CONFIRMADO]`.

### Matriz Forense de Benchmarks (`artifacts/benchmarks/`) `[CONFIRMADO]`
Se mantiene una matriz pericial documentada en [`artifacts/benchmarks/benchmark_matrix.json`](file:///d:/0001%20HyperScale%20Thinking/PROYECTOS%20CLOUD/iContext/iDirectory/artifacts/benchmarks/benchmark_matrix.json) que audita 7 repositorios bajo la metodología de Context Engineering:

- `repo_01` a `repo_06`: Repositorios base evaluados con reducciones promedio de 83.2% en consumo de tokens en arranque de agentes.
- `repo_07` (`FlowAgentic`): Repositorio recientemente evaluado con topología v2.0 preexistente, 12 beacons desincronizados y satélite ausente, documentado en [`forensic_repo_07_flowagentic.md`](file:///d:/0001%20HyperScale%20Thinking/PROYECTOS%20CLOUD/iContext/iDirectory/artifacts/benchmarks/forensic_repo_07_flowagentic.md).

---

## 7. Observabilidad, Telemetría y Modos de Fallo

### Telemetría de Token Budget `[CONFIRMADO]`
Ejecutable mediante `python FWengine.py context --budget`:
- **Consumo Satelital:** ~250 tokens (`tree.json`).
- **Consumo Beacon Unitario:** ~80–120 tokens (`.context.yaml`).
- **Ahorro Efectivo en Tier 1:** Evita la ingesta del archivo de semilla (~6,800 tokens), reduciendo la huella de inicio en más del 85%.

### Modos de Fallo y Mecanismos de Mitigación `[CONFIRMADO]`
| Modo de Fallo | Detección | Mitigación Implementada |
| :--- | :--- | :--- |
| **Path Traversal Attack** | Ruta normalizada no inicia con `ROOT_DIR`. | `ValueError("Intento de path traversal fuera del proyecto")` inmediato. |
| **Colisión de Casing NTFS** | `folder.rename()` falla silenciosamente en Windows. | Renombrado en dos pasos vía carpeta temporal UUID / `__case_tmp__`. |
| **Drift del Mapa Satelital** | `tree.json` mtime < carpetas mtime. | Advertencia en `FWengine.py audit` y flags de alerta en telemetría. |
| **Beacon Faltante** | Subcarpeta nueva sin inicializar. | `resolve_beacon()` hereda recursivamente del padre más cercano. |
| **Rama Muerta Masiva** | Agente intenta listar `data/raw/` o `logs/`. | Directiva `crawl: false` en árbol y beacons prohíbe el volcado. |

---

## 8. Seguridad, Privacidad y Gobernanza de Agentes

### Reglas para Agentes de IA (`AGENTS.md` / `GEMINI.md`) `[CONFIRMADO]`
1. **Invariante de Poda:** Prohibido ejecutar comandos de exploración ciega recursiva (`Get-ChildItem -Recurse`, `find .`, `ls -R`). Toda navegación debe estar guiada por `.context/tree.json`.
2. **Prohibición de Precarga en Tier 1:** El agente no debe leer este archivo (`01_seed/seed-idirectory-master.md`) a menos que ocurra uno de los 3 disparadores de la matriz de decisión.
3. **Contrato de Sincronización:** Cualquier adición o eliminación de directorios exige la ejecución de `python FWengine.py beacon --sync` y `python FWengine.py map --sync` antes del cierre de turno.
4. **Protección de Secretos:** Política estricta de ofuscación `<REDACTED>` para credenciales, API keys o tokens de acceso encontrados en archivos `.env` o configuraciones locales.

---

## 9. Estado Real, Deuda Técnica y Roadmap

### Nivel de Madurez Actual `[CONFIRMADO]`
- **Framework Core (v3.0):** 98% (Motor CLI, Two-Tier Bootloader, MiniYAML, Suite de Tests de 26 casos).
- **Cobertura de Beacons Locales:** 100% de los 24 directorios canónicos poseen beacon normalizado.
- **Suite de Benchmarks:** 7 repositorios analizados forensemente.

### Deuda Técnica Identificada `[DECLARADO]`
1. **Soporte de Comentarios en MiniYAML:** El parser serializa estructuras limpias pero descarta comentarios en línea `#` al reescribir `.context.yaml`.
2. **Linter Semántico de Tipos:** El validador heurístico de cabeceras Python cubre palabras clave frecuentes pero no realiza análisis AST profundo (reservado para mantener cero dependencias).

### Roadmap Próximo `[INFERIDO]`
- [x] Implementación de Two-Tier Bootloader y matrices de decisión en gobernanza Markdown.
- [x] Herencia jerárquica de beacons (`resolve_beacon`).
- [x] Inspección híbrida de encabezados de código fuente.
- [x] Peritaje forense e integración de `FlowAgentic` a la matriz de benchmarks.
- [ ] Auto-reparación asistida mediante `/idir --repair` para proyectos legacy externos.

---

## 10. Protocolo de Modificación y Traspaso de Contexto

Para modificar o extender la arquitectura de `iDirectory`:

1. **Verificar el Estado Base:** Ejecutar `python FWengine.py audit` para comprobar que no existan desincronizaciones previas.
2. **Ejecutar Pruebas Antes de Editar:** Asegurar que los 26 tests en `tests/test_fwengine.py` pasen limpiamente (`python -m unittest tests/test_fwengine.py`).
3. **Preservar Invariantes:**
   - Cero dependencias externas en `FWengine.py`.
   - Nombres de directorios raíz estrictamente en minúsculas (`all-lowercase`).
   - Mantener el contrato del satélite `.context/tree.json`.
4. **Sincronizar y Regenerar:**
   ```powershell
   python FWengine.py beacon --sync
   python FWengine.py map --sync
   ```
5. **Cierre de Turno:** Si se alteran contratos o arquitectura global, regenerar este ThinkingSeed Master mediante `/seedMaster`.
