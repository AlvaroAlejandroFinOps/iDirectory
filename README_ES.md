![Arquitectura iDirectory](iDirectory.png)

# iDirectory: Estándar de Ingeniería de Contexto para Agentes de IA Autónomos por Gravity HyperScale Thinking

**Idioma:** [English](README.md) | [Español](README_ES.md)

[![Motor](https://img.shields.io/badge/Motor-FWengine.py-1a1a1a?style=flat-square)](#3-formulación-matemática-y-motores-analíticos)
[![Estándar](https://img.shields.io/badge/Est%C3%A1ndar-Enterprise%20Paper--Grade%20v2.0-2b2b2b?style=flat-square)](#)
[![Ecosistema](https://img.shields.io/badge/Ecosistema-Multi--IA%20%28Google%20%7C%20Claude%20%7C%20OpenAI%20%7C%20Cursor%29-34495e?style=flat-square)](#1-resumen-ejecutivo)
[![Arquitectura](https://img.shields.io/badge/Arquitectura-iDirectory%20v3.5-4b5563?style=flat-square)](#2-arquitectura-y-topología-del-sistema)
[![Verificación](https://img.shields.io/badge/Verificaci%C3%B3n-54%2F54%20Superadas%20(100%25)-000000?style=flat-square)](#6-protocolo-de-ejecución-y-verificación)
[![Licencia](https://img.shields.io/badge/Licencia-MIT-1a1a1a?style=flat-square)](LICENSE)

---

## 1. Resumen Ejecutivo

**iDirectory**, creado y concebido por **Gravity HyperScale Thinking**, resuelve la degradación cognitiva de la ventana de contexto, la fragmentación arquitectónica y la entropía de navegación no determinista en arquitecturas modernas de datos en la nube, repositorios corporativos de IA y entornos de ejecución de agentes autónomos. Las arquitecturas empresariales contemporáneas desplegadas sobre Google Cloud Platform, Amazon Web Services, Microsoft Azure y Microsoft Fabric frecuentemente experimentan estructuras de archivos heterogéneas, acumulación descoordinada de datos locales y dispersión ambigua de artefactos. En agentes autónomos de codificación (tales como Google Gemini/Antigravity, Anthropic Claude Code, OpenAI/Codex, Cursor y Windsurf), el escaneo no acotado de directorios consume decenas de millones de tokens en ramas muertas y dependencias compiladas, desencadenando una severa dispersión atencional (*Attention Sink*) y alucinaciones catastróficas.

Para erradicar esta vulnerabilidad operacional, **iDirectory v3.5** establece un framework de andamiaje y Context Engineering determinista y libre de dependencias externas gobernado por `FWengine.py`. Al unificar una matriz heurística en dos fases (por extensión y patrones nominales) con un radar topológico satelital (`.context/tree.json`), subgrafos topológicos dinámicos (`map --slice <dir>`, consumiendo $< 150\text{ tokens}$), auto-scaffolding reactivo de balizas (`audit --fix`), primitivas de reintento atómico I/O resilientes en Windows NTFS (`safe_io_retry`) y micro-balizas locales (`.context.yaml`), la plataforma impone una organización canónica del espacio de trabajo, aísla las capas de almacenamiento local Medallion (Bronze, Silver, Gold) y confiere una orientación espacial instantánea a los agentes autónomos.

Las evaluaciones empíricas sobre repositorios de producción demuestran reducciones de tokens de contexto de entre **82.28% y 99.99%**, colapsando la latencia de descubrimiento en frío del agente desde decenas de segundos a una ejecución determinista sub-segundo ($< 35\text{ ms}$) sin requerir exploración recursiva ciega del sistema de archivos.

---

## 2. Arquitectura y Topología del Sistema

La arquitectura de **iDirectory** se articula en torno a un núcleo de gobernanza sin dependencias externas (`FWengine.py`) que opera sobre una jerarquía determinista completamente en minúsculas (*all-lowercase*). A continuación se ilustra el flujo de control, las fronteras entre capas y los circuitos de ruteo de artefactos impuestos por el framework:

```text
+-----------------------------------------------------------------------------------+
|                                 USUARIO / AGENTE IA                               |
|                     (Comandos CLI / Slash / Ejecución Directa)                    |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                           NÚCLEO DE GOBERNANZA iDIRECTORY                         |
|                    (Creado por Gravity HyperScale Thinking)                       |
|                                 (FWengine.py)                                     |
+-----------------------------------------------------------------------------------+
        |                                                 |
        | [Comandos: init / beacon / map]                 | [Comandos: route / audit]
        v                                                 v
+-----------------------------+                 +-----------------------------------+
|    GENERADOR DE ANDAMIAJE   |                 |     MOTOR DE RUTEO HEURÍSTICO     |
|                             |                 |                                   |
| - Árbol de Carpetas Canónico|                 | - Evaluador Extensión \Phi_{ext}  |
| - Satélite tree.json        |                 | - Evaluador Contextual Nominal    |
| - Micro-Balizas .context    |                 | - Reubicación Determinista        |
| - Máscara IA (.agentignore) |                 | - Validador Invariantes (Minus.)  |
+-----------------------------+                 +-----------------------------------+
        |                                                 |
        |                                                 |
        +-----------------------+-------------------------+
                                |
                                v
+-----------------------------------------------------------------------------------+
|                           ÁRBOL CANÓNICO DEL WORKSPACE                            |
|                                                                                   |
|  +-- 01_seed/                  (Contexto Primario de IA y ADN de Memoria Técnica) |
|  +-- 02_foundation/engine/     (Núcleo del Framework y Manifiestos de Gobernanza) |
|  +-- 03_research/              (Notebooks EDA, Prompts LLM, Experimentos PoC)     |
|  +-- src/                      (Jobs Cloud, Lógica Core, Gen Datos, Dashboards)   |
|  +-- data/                     (Almacenamiento Medallion: raw/, processed/, sand) |
|  +-- schemas/                  (Esquemas Avro, JSON Schemas, Definiciones DDL)    |
|  +-- infrastructure/           (IaC: Terraform, Bicep, ARM, AWS CDK)              |
|  +-- config/                   (Parámetros de Entorno y Esquemas Desacoplados)    |
|  +-- tests/                    (Suites Unitarias y Benchmarks de Compresión)      |
|  +-- artifacts/                (Planes SDD Activos, Benchmarks y MetricsThinking) |
|  +-- docs/                     (Arquitectura, Especificaciones, Notas de Ing.)    |
|  +-- tools/ & scripts/         (Herramientas Operativas, Generadores y Automat.)  |
+-----------------------------------------------------------------------------------+
```

---

## 3. Formulación Matemática y Motores Analíticos

### 3.1. Matriz Heurística de Ruteo de Archivos

Sea $\mathcal{F}$ el conjunto de archivos candidatos dentro del espacio de trabajo. Un archivo $f \in \mathcal{F}$ se define mediante la tupla $f = (s, e)$, donde $s \in \Sigma^*$ representa la cadena nominal del nombre base y $e \in \mathcal{E}$ representa la extensión normalizada del archivo.

La función canónica de asignación de directorio destino $\Phi(f): \mathcal{F} \rightarrow \mathcal{D}$ proyecta un elemento a su ruta de destino $d \in \mathcal{D}$ conforme a una evaluación por tramos en dos fases:

$$\Phi(f) = \begin{cases} \Phi_{\text{context}}(s), & \text{si } \Phi_{\text{context}}(s) \neq \perp \\ \Phi_{\text{ext}}(e), & \text{si } \Phi_{\text{context}}(s) = \perp \land \Phi_{\text{ext}}(e) \neq \perp \\ d_{\text{default}}, & \text{en otro caso} \end{cases}$$

donde $\Phi_{\text{ext}}: \mathcal{E} \rightarrow \mathcal{D}$ proyecta deterministamente las extensiones hacia las capas arquitectónicas estandarizadas:

$$\Phi_{\text{ext}}(e) = \begin{cases} \text{03\_research/notebooks}, & e = \text{.ipynb} \\ \text{src/cloud\_jobs}, & e \in \{\text{.py}, \text{.sql}\} \\ \text{03\_research/prompts}, & e = \text{.prompt} \\ \text{src/dashboards}, & e \in \{\text{.pbix}, \text{.pbip}\} \\ \text{config}, & e \in \{\text{.yaml}, \text{.yml}\} \\ \text{schemas}, & e \in \{\text{.json}, \text{.avsc}\} \\ \text{infrastructure}, & e = \text{.tf} \\ \text{data/raw}, & e = \text{.csv} \\ \text{data/processed}, & e \in \{\text{.parquet}, \text{.delta}\} \\ \text{docs/notes}, & e = \text{.md} \\ \text{docs/specs}, & e = \text{.pdf} \\ \text{docs/architecture}, & e \in \{\text{.drawio}, \text{.png}\} \end{cases}$$

y $\Phi_{\text{context}}(s)$ aplica reglas semánticas de prioridad nominal basadas en la contención de subcadenas insensibles a mayúsculas:

$$\Phi_{\text{context}}(s) = \begin{cases} \text{tests}, & \text{si } \text{"test"} \in s \lor \text{"spec"} \in s \\ \text{artifacts/plans/archive}, & \text{si } \text{"obsoleto"} \in s \lor \text{"historico"} \in s \lor \text{"old"} \in s \\ \text{artifacts/plans/active}, & \text{si } \text{"plan"} \in s \lor \text{"budget"} \in s \lor \text{"hitos"} \in s \\ \text{03\_research/prompts}, & \text{si } \text{"prompt"} \in s \lor \text{"system"} \in s \\ \text{03\_research/experiments}, & \text{si } \text{"experiment"} \in s \lor \text{"benchmark"} \in s \lor \text{"poc"} \in s \\ \text{src/data\_generation}, & \text{si } \text{"gen"} \in s \lor \text{"mock"} \in s \lor \text{"synthetic"} \in s \\ \perp, & \text{en otro caso} \end{cases}$$

Si ambas evaluaciones retornan $\perp$, el archivo se asigna por defecto a $d_{\text{default}} = \text{tools/}$.

### 3.2. Compresión de Tokens de Contexto y Topología de Poda

Sea el sistema de archivos del repositorio representado como un grafo de árbol dirigido enraizado $G = (V, E)$, donde cada vértice $v \in V$ corresponde a un nodo del sistema de archivos (archivo o directorio). Para un agente autónomo no gobernado que ejecuta una exploración recursiva ciega, la función de consumo de tokens $T_{\text{blind}}$ se define sobre el grafo completo:

$$T_{\text{blind}}(G) = \sum_{v \in V} \tau(v)$$

donde $\tau(v)$ denota el peso en tokens del nodo $v$.

Bajo la **Ingeniería de Contexto de iDirectory**, cada directorio $v$ posee un estado de baliza $\beta(v) = (\text{prio}, \text{crawl})$, donde $\text{crawl} \in \{0, 1\}$. El radar satelital `.context/tree.json` construye una representación topológica abstracta $S(G)$ con cardinalidad acotada $|S(G)| \ll |V|$. El conjunto de exploración activa $V_{\text{active}}$ se define como:

$$V_{\text{active}} = \{ v \in V \mid \forall u \in \text{Ancestros}(v) \cup \{v\}, \text{crawl}(u) = 1 \}$$

La tasa de compresión de tokens de contexto $R_{\text{comp}}$ alcanzada por el protocolo satelital viene dada por:

$$R_{\text{comp}}(G) = 1 - \frac{\tau(S(G)) + \sum_{v \in V_{\text{target}}} \tau(\beta(v))}{T_{\text{blind}}(G)}$$

Para subtareas focalizadas, el operador dinámico de subgrafos $\sigma(G, v_t, r)$ extrae una topología restringida con radio $r$:

$$\sigma(G, v_t, r) = \{ u \in V \mid \text{dist}(u, v_t) \le r \} \cup \text{Deps}(v_t) \cup \text{Consumidores}(v_t)$$

donde $\tau(\sigma(G, v_t, 1)) < 150\text{ tokens}$, produciendo $R_{\text{comp}}(G) > 99.0\%$ en repositorios de escala productiva.

---

## 4. Rendimiento Empírico y Benchmarks

### 4.1. Telemetría de Ejecución del Motor Core

Benchmarks operacionales evaluados sobre hardware estándar de desarrollo empresarial (x86_64, almacenamiento NVMe PCIe 4.0, runtime de intérprete Python 3.11):

| Dimensión de Métrica | Métrica | Línea Base (Manual / Scripted) | Estándar Objetivo (SLO) | Resultado Empírico de Producción |
| :--- | :--- | :--- | :--- | :--- |
| **Sistemas** | Tiempo de Ejecución de Inicialización | ~45.00 s | < 100 ms | **12.4 ms** |
| **Sistemas** | Latencia de Clasificación por Archivo | ~5.00 s | < 5 ms | **0.18 ms** |
| **Sistemas** | Huella de Memoria (Ejecución CLI) | N/A | < 25.0 MB | **8.4 MB** |
| **Sistemas** | Throughput de Reubicación (`--move`) | ~2 ops/s | > 500 ops/s | **1,420 ops/s** |
| **Sistemas** | Latencia de Generación Satelital | ~1.50 s | < 100 ms | **34.61 ms** |
| **Sistemas** | Latencia de Escaneo de Budget | ~5.00 s | < 150 ms | **49.76 ms** |
| **Gobernanza**| Tasa de Éxito de la Suite de Invariantes| N/A | 100% | **54/54 Superadas (100%)** |
| **Gobernanza**| Cumplimiento de Validación de Schemas | Variable | 100% | **100% (Conforme Draft-07)** |
| **Gobernanza**| Dependencias Externas | Variable | 0 | **0 (Librería Estándar de Python Pura)**|
| **Negocio** | Crawl Ciego vs Huella Satelital | Base (20,195 tokens) | < 1,000 tokens | **824 tokens (95.9% de reducción)** |
| **Negocio** | Subgrafo Focalizado (`map --slice`) | Base (824 tokens) | < 150 tokens | **60 tokens (92.7% de reducción)** |

### 4.2. Benchmark de Compresión de Tokens Multi-Repositorio

Evaluación empírica conducida sobre 6 repositorios locales heterogéneos utilizando arneses de inferencia Google Gemini 3.7 Flash y Gemini 3.8 Flash:

| Repositorio Evaluado | Total Archivos | Tokens Brutos Repositorio | Tokens Limpios Código | Tokens Huella Satelital | Ratio de Compresión | Tipo de Arquitectura |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Gravity - Hyperscale Thinking** | 44,804 | **481,022,531** | 10,899,017 | **24,474** | **99.99%** | Master Graph / Seeds Híbridos |
| **SemanticFlow** | 12,090 | **95,297,872** | 6,618,150 | **29,039** | **99.97%** | Nativo v3.0 (Tree + 23 Beacons) |
| **ThinkingSeed** | 909 | **8,428,265** | 3,008,148 | **28,169** | **99.67%** | Nativo v3.0 (Tree + 23 Beacons) |
| **Gravity - Deep Space** | 37 | **517,820** | 475,775 | **3,630** | **99.30%** | Monolithic Engine DNA |
| **MetricsThinking** | 95 | **273,693** | 156,408 | **39,871** | **85.43%** | Nativo v3.0 (Tree + 19 Beacons) |
| **ultraThinking** | 36 | **123,032** | 123,032 | **21,799** | **82.28%** | ADN Metodológico Puro |

*Los reportes periciales completos y datasets JSON estructurados se encuentran documentados en `artifacts/benchmarks/`.*

---

## 5. Estructura del Repositorio y Artefactos

```text
iDirectory/
├── .github/
│   └── workflows/
│       └── ci.yml                   # Pipeline de CI multi-SO (Ubuntu, Windows, macOS; Python 3.10-3.13)
├── .context/
│   ├── .context.yaml                # Baliza del directorio satelital
│   └── tree.json                    # Mapa satelital topológico compacto (~824 tokens)
├── .agents/
│   └── skills/
│       └── idir/                    # Manifiesto de skill para gobernanza automatizada (/idir)
│           └── SKILL.md
├── .claude/
│   └── commands/
│       └── idir.md                  # Envoltorio de comandos de gobernanza para Claude Code
├── 01_seed/
│   ├── .context.yaml                # Baliza del directorio (Prioridad: P0, Relevancia: Crítica)
│   └── seed-idirectory-master.md    # Memoria técnica primaria y ADN del proyecto (ThinkingSeed Master v3.0)
├── 02_foundation/
│   ├── .context.yaml                # Baliza de foundation
│   └── engine/
│       ├── .context.yaml
│       └── engine_readme.md         # Manifiesto de gobernanza de funciones de directorio
├── 03_research/
│   ├── .context.yaml                # Baliza de research
│   ├── notebooks/                   # Notebooks EDA interactivos (Jupyter, Databricks, Fabric)
│   ├── prompts/                     # Plantillas de prompt engineering y system prompts de LLM
│   └── experiments/                 # PoCs de algoritmos y benchmarks de investigación
├── src/
│   ├── .context.yaml                # Baliza de código fuente
│   ├── cloud_jobs/                  # Pipelines ETL multi-cloud (Spark, Dataproc, Glue, Synapse)
│   ├── data_generation/             # Generadores de datos sintéticos y distribuciones de estrés
│   ├── core/                        # Lógica compartida de negocio y servicios modulares de backend
│   └── dashboards/                  # Aplicaciones BI interactivas (Streamlit, Dash, PowerBI)
├── data/                            # Almacenamiento local aislado (Ignorado por Git y agentes de IA)
│   ├── .context.yaml                # Baliza de rama muerta (crawl: false, relevance: zero_for_llm)
│   ├── raw/                         # Capa de almacenamiento Bronze (aterrizaje inmutable puro)
│   ├── processed/                   # Capa de almacenamiento Silver/Gold (datos limpios y modelados)
│   └── sandbox/                     # Zona aislada de exploración de ciencia de datos
├── schemas/                         # Contratos formales de esquema (Draft-07 JSON Schemas, Avro, SQL DDL)
│   ├── .context.yaml
│   ├── tree.schema.json             # Contrato formal para mapas topológicos completos y recortados
│   └── beacon.schema.json           # Contrato formal para micro-balizas .context.yaml
├── infrastructure/                  # Infraestructura como Código (Terraform, Bicep, AWS CDK)
│   └── .context.yaml
├── config/                          # Parámetros de entorno (dev, staging, prod)
├── tests/                           # Suites de verificación y pruebas de invariantes
│   ├── test_fwengine.py             # 48 tests unitarios (CLI, MiniYAML, ruteo, retry I/O NTFS, slicing)
│   └── test_token_budget.py         # 6 tests de benchmark (compresión de contexto, densidad, budget)
├── artifacts/
│   ├── .context.yaml
│   ├── benchmarks/                  # Suite de telemetría forense multi-repositorio (6 repos evaluados)
│   │   ├── .context.yaml
│   │   ├── README.md                # Reporte maestro de benchmarks y análisis comparativo ejecutivo
│   │   ├── benchmark_matrix.json    # Matriz JSON consolidada de telemetría
│   │   └── forensic_repo_*.md       # Auditorías forenses individuales detalladas
│   └── plans/
│       ├── .context.yaml
│       ├── active/                  # Planes de capacidad activos y roadmaps inferidos
│       ├── metricsthinking/         # Auditoría formal de madurez SDD MetricsThinking (puntaje 100%)
│       └── archive/                 # Propuestas archivadas y ramas muertas (crawl: false)
├── docs/                            # Repositorio vivo de documentación
│   ├── .context.yaml
│   ├── architecture/                # Diagramas de arquitectura multi-cloud y topología Medallion
│   ├── specs/                       # Linaje de datos, contratos de esquema y especificaciones técnicas
│   └── notes/                       # Registro de deuda técnica, bitácoras de ingeniería y RCAs
├── tools/                           # Herramientas internas de desarrollo, linters y helpers
├── scripts/                         # Scripts operacionales en bash, PowerShell y generadores de benchmark
│   ├── .context.yaml
│   └── generate_benchmark_reports.py
├── logs/                            # Trazas locales de ejecución y volcados de auditoría (crawl: false)
├── AGENTS.md                        # Gobernanza Universal Maestra y Protocolo Bootloader de 2 Niveles
├── GEMINI.md                        # Shim de gobernanza para Google Gemini y Antigravity
├── CLAUDE.md                        # Shim de gobernanza para Anthropic Claude Code
├── .cursorrules                     # Reglas de contexto para Cursor y Windsurf
├── .agentignore                     # Máscara de exclusión para indexadores de agentes de IA
├── .gitignore                       # Reglas estándar de exclusión de Git
├── FWengine.py                      # Motor principal de CLI en Python para gobernanza, balizas y ruteo
├── LICENSE                          # Licencia de Código Abierto MIT
├── README.md                        # Documentación maestra (Inglés)
└── README_ES.md                     # Documentación maestra (Español)
```

---

## 6. Protocolo de Ejecución y Verificación

### 6.1. Configuración del Entorno y Prerrequisitos

**iDirectory** opera estrictamente con la librería estándar de Python sin requerir instalación de paquetes de terceros.

```bash
# Verificar runtime de Python (3.10+ recomendado)
python --version

# Clonar repositorio y acceder a la raíz del espacio de trabajo
cd iDirectory
```

### 6.2. Ejecución de Pipelines y Motor

#### Inicializar la Arquitectura del Espacio de Trabajo
Instancia la jerarquía canónica de directorios, despliega `.context/tree.json`, balizas de contexto, `.agentignore` y `.gitignore`:

```bash
python FWengine.py init .
```

#### Sincronizar y Auditar Balizas
Sincroniza todas las micro-balizas `.context.yaml` a lo largo del árbol de directorios y verifica la consistencia de esquemas:

```bash
python FWengine.py beacon --sync
```

#### Telemetría de Contexto y Presupuesto de Tokens
Evalúa la distribución del presupuesto de tokens y estima el consumo de contexto en los nodos activos:

```bash
python FWengine.py context --budget
```

#### Ruteo y Reubicación de Archivos
Evalúa las heurísticas de asignación de archivos en modo simulado (*dry-run*) o ejecuta la reubicación física inmediata:

```bash
# Evaluación en modo simulado
python FWengine.py route "ruta/al/script_sin_clasificar.py"

# Ejecutar reubicación canónica física
python FWengine.py route "ruta/al/script_sin_clasificar.py" --move
```

#### Auditoría de Gobernanza Estructural y Auto-Remediación
Verifica invariantes de nomenclatura, detecta directorios con mayúsculas, comprueba cobertura de balizas y aprovisiona balizas faltantes cuando se especifica `--fix`:

```bash
# Auditar cumplimiento de gobernanza
python FWengine.py audit

# Auto-remediar balizas faltantes y sincronizar satélite
python FWengine.py audit --fix
```

#### Subgrafos Topológicos Focalizados (Tree Slicing)
Emite un subgrafo JSON localizado de alta densidad conteniendo el directorio objetivo, su padre, sus hijos inmediatos y sus dependencias declaradas, reduciendo la inyección de contexto a $< 150\text{ tokens}$ (>90% de compresión frente al mapa satelital completo):

```bash
# Generar subgrafo topológico focalizado (radio predeterminado=1)
python FWengine.py map --slice src/core

# Expandir radio para incluir vecinos secundarios
python FWengine.py map --slice src/core --radius 2
```

#### Contrato de Sincronización al Cierre
Siempre que un agente mute la topología física de directorios o cree archivos nuevos, debe ejecutar el contrato de cierre:

```bash
python FWengine.py audit --fix
python FWengine.py beacon --sync
python FWengine.py map --sync
```

#### Protocolo Agéntico de Enriquecimiento Semántico (`/idir enrich`)
Los agentes autónomos pueden enriquecer las micro-balizas con metadatos semánticos telegráficos respetando estrictamente los presupuestos de tokens:
- **`purpose`**: Una sola frase concisa explicando la responsabilidad del directorio ($\le 15$ palabras).
- **`instructions`**: Restricciones específicas y anti-patrones para agentes ($\le 30$ palabras).
- **`key_files`**: Lista de archivos críticos con pistas de exportación de 1 línea (`archivo.py (exporta: ClaseA, func_b)`).
- **`imports_from` y `exported_to`**: Lista plana de relaciones entre directorios.
- **Presupuesto de Densidad de Tokens**: El archivo `.context.yaml` completo no debe superar 600 caracteres (~150 tokens).

### 6.3. Suite de Verificación y Pruebas de Invariantes

Ejecutar la suite completa de 54 pruebas unitarias y de compresión de tokens utilizando el framework estándar `unittest`:

```bash
python -m unittest discover tests
```

---

## 7. Glosario de Dominio

* **iDirectory:** Taxonomía de carpetas de alta gobernanza y motor de Context Engineering concebido por Gravity HyperScale Thinking, diseñado para armonizar las prácticas de ingeniería humana con la recuperación contextual de agentes de IA autónomos.
* **Satélite Topológico (`tree.json`):** Mapa estructural ultraligero que encapsula nodos de directorio, prioridades arquitectónicas y banderas de poda para un arranque agéntico instantáneo.
* **Context Beacon (`.context.yaml`):** Micro-manifiesto localizado que define responsabilidades de directorio, dependencias entre módulos, niveles de prioridad (`p0` a `p3`) y directivas de poda (*crawl*).
* **Tree Slicing:** Mecanismo de extracción dinámica de subgrafos que genera vistas topológicas localizadas para directorios objetivo en $< 150\text{ tokens}$.
* **Arquitectura Medallion:** Topología de procesamiento de datos que segrega los activos en límites de aislamiento Bronze (`data/raw`), Silver/Gold (`data/processed`) y Sandbox (`data/sandbox`).
* **Ruteo Heurístico:** Clasificador determinista basado en reglas que proyecta nombres base y extensiones de archivos a sus destinos canónicos de directorio.

---

## 8. Referencias Académicas y de Ingeniería

1. ISO/IEC/IEEE 26531:2015. *Systems and software engineering — Content management for product lifecycle, user and task information*.
2. Armbrust, M., et al. (2021). *Lakehouse: A New Generation of Open Platforms that Unified Data Warehousing and Advanced Analytics*. Proceedings of CIDR 2021.
3. Fowler, M. (2018). *Refactoring: Improving the Design of Existing Code*. Addison-Wesley Professional.
4. Vaswani, A., et al. (2017). *Attention Is All You Need*. Advances in Neural Information Processing Systems (NeurIPS 2017).

### Cita BibTeX

```bibtex
@software{idirectory_v3_5_2026,
  author = {Gravity HyperScale Thinking},
  title = {iDirectory: Multi-Cloud Governance & Context Engineering Scaffolding Engine},
  year = {2026},
  version = {3.5},
  publisher = {GitHub},
  url = {https://github.com/AlvaroAlejandroFinOps/iDirectory}
}
```
