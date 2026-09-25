![alt text](iDirectory.png)
# iDirectory: Motor de Andamiaje, Gobernanza Multi-Cloud y Context Engineering por Gravity HyperScale Thinking

**Idioma:** [English](README.md) | [Español](README_ES.md)

[![Entorno: Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-1a1a1a.svg?style=flat-square)](https://www.python.org/)
[![Arquitectura: iDirectory v3.0](https://img.shields.io/badge/Arquitectura-iDirectory%20v3.0-2b2b2b.svg?style=flat-square)](#2-arquitectura-y-topología-del-sistema)
[![Creado por: Gravity HyperScale Thinking](https://img.shields.io/badge/Creado%20por-Gravity%20HyperScale%20Thinking-34495e.svg?style=flat-square)](#1-resumen-ejecutivo)
[![Motor: CLI Determinista](https://img.shields.io/badge/Motor-CLI--Determinista-4b5563.svg?style=flat-square)](#3-formulación-matemática-y-motores-analíticos)
[![Verificación: 100% Superada](https://img.shields.io/badge/Verificaci%C3%B3n-100%25%20Superada-1a1a1a.svg?style=flat-square)](#6-protocolo-de-ejecución-y-verificación)
[![Licencia: MIT](https://img.shields.io/badge/Licencia-MIT-000000.svg?style=flat-square)](LICENSE)

---

## 1. Resumen Ejecutivo

**iDirectory**, creado y concebido por **Gravity HyperScale Thinking**, resuelve la degradación estructural, la fragmentación arquitectónica y la saturación de la ventana de contexto en plataformas modernas de ingeniería de datos multi-cloud, repositorios de investigación en Inteligencia Artificial y ecosistemas de agentes autónomos. Las arquitecturas empresariales contemporáneas que operan sobre Google Cloud Platform, Amazon Web Services, Microsoft Azure y Microsoft Fabric frecuentemente presentan estructuras de archivos heterogéneas, acumulación descontrolada de datos locales y dispersión ambigua de artefactos. En agentes autónomos de codificación (tales como Google Gemini/Antigravity, Anthropic Claude Code, OpenAI/Codex, Cursor y Windsurf), el escaneo ciego de directorios consume cientos de millones de tokens en ramas muertas y dependencias compiladas, desencadenando degradación de atención y alucinaciones catastróficas.

Para eliminar esta vulnerabilidad, **iDirectory v3.0** introduce un framework de andamiaje y Context Engineering determinista y sin dependencias externas gobernado por `FWengine.py`. Al integrar una matriz heurística basada en extensiones y patrones nominales con un radar topológico satelital (`.context/tree.json`) y balizas locales (`.context.yaml`), el sistema establece una organización canónica en el espacio de trabajo, aísla las capas de almacenamiento local Medallion (Bronze, Silver, Gold) y provee orientación espacial instantánea a los agentes autónomos. Las evaluaciones empíricas sobre repositorios de producción demuestran reducciones de tokens de contexto de entre **82.28% y 99.99%**, permitiendo decisiones de navegación sub-segundo sin exploración recursiva ciega del árbol de archivos.

---

## 2. Arquitectura y Topología del Sistema

La topología de **iDirectory** se articula en torno a un motor de gobernanza sin dependencias (`FWengine.py`) que opera sobre una jerarquía determinista completamente en minúsculas (*all-lowercase*). El siguiente diagrama ilustra el flujo de control, las fronteras entre capas y las rutas de ruteo de artefactos impuestas por el framework:

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

donde $\tau(v)$ representa el peso en tokens del nodo $v$.

Bajo el modelo de **Context Engineering de iDirectory**, cada directorio $v$ posee un estado de baliza $\beta(v) = (\text{prio}, \text{crawl})$, donde $\text{crawl} \in \{0, 1\}$. El radar satelital `.context/tree.json` construye una abstracción topológica $S(G)$ con cardinalidad acotada $|S(G)| \ll |V|$. El conjunto de exploración activa $V_{\text{active}}$ se define como:

$$V_{\text{active}} = \{ v \in V \mid \forall u \in \text{Ancestors}(v) \cup \{v\}, \text{crawl}(u) = 1 \}$$

El Ratio de Compresión de Tokens de Contexto $R_{\text{comp}}$ logrado por el protocolo satelital se expresa como:

$$R_{\text{comp}}(G) = 1 - \frac{\tau(S(G)) + \sum_{v \in V_{\text{target}}} \tau(\beta(v))}{T_{\text{blind}}(G)}$$

En repositorios empresariales con dependencias locales extensas, ramas muertas y datos crudos, $R_{\text{comp}}(G) \to 1.0$, asegurando ahorros de tokens de hasta el $99.99\%$.

---

## 4. Rendimiento Empírico y Benchmarks

### 4.1. Telemetría de Ejecución del Motor Núcleo

Métricas operativas evaluadas sobre hardware de desarrollo estándar (x86_64, almacenamiento NVMe PCIe 4.0, intérprete Python 3.11):

| Métrica | Línea Base (Manual / Script) | Objetivo (SLO) | Resultado Empírico en Producción |
| :--- | :--- | :--- | :--- |
| Tiempo de Inicialización de Directorio | ~45.00 s | < 100 ms | **12.4 ms** |
| Latencia de Clasificación de Archivos (por ítem) | ~5.00 s | < 5 ms | **0.18 ms** |
| Huella de Memoria (Ejecución CLI) | N/A | < 25.0 MB | **8.4 MB** |
| Rendimiento de Reubicación (`--move`) | ~2 ops/s | > 500 ops/s | **1,420 ops/s** |
| Dependencias Externas de Terceros | N/A | 0 | **0 (Solo Librería Estándar de Python)** |
| Tasa de Éxito en Suite de Invariantes | N/A | 100% | **20/20 Pruebas Superadas (100%)** |

### 4.2. Benchmark de Compresión de Tokens Multi-Repositorio

Evaluación empírica conducida sobre 6 repositorios locales heterogéneos utilizando arneses de Google Gemini 3.7 Flash y Gemini 3.8 Flash:

| Repositorio Evaluado | Total Archivos | Tokens Brutos del Codebase | Tokens Limpios del Codebase | Tokens Huella Satélite | Ratio de Compresión de Tokens | Tipo de Arquitectura |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Gravity - Hyperscale Thinking** | 44,804 | **481,022,531** | 10,899,017 | **24,474** | **99.99%** | Grafo Maestro / Semillas Híbridas |
| **SemanticFlow** | 12,090 | **95,297,872** | 6,618,150 | **29,039** | **99.97%** | Nativo v3.0 (Tree + 23 Beacons) |
| **ThinkingSeed** | 909 | **8,428,265** | 3,008,148 | **28,169** | **99.67%** | Nativo v3.0 (Tree + 23 Beacons) |
| **Gravity - Deep Space** | 37 | **517,820** | 475,775 | **3,630** | **99.30%** | ADN de Motor Monolítico |
| **MetricsThinking** | 95 | **273,693** | 156,408 | **39,871** | **85.43%** | Nativo v3.0 (Tree + 19 Beacons) |
| **ultraThinking** | 36 | **123,032** | 123,032 | **21,799** | **82.28%** | ADN Metodológico Puro |

*Los reportes forenses completos y los datasets JSON estructurados se encuentran documentados en `artifacts/benchmarks/`.*

---

## 5. Estructura del Repositorio y Artefactos

```text
iDirectory/
├── .github/
│   └── workflows/
│       └── ci.yml                   # Pipeline CI multi-OS (Ubuntu, Windows, macOS; Python 3.10-3.13)
├── .context/
│   ├── schema/
│   │   └── tree.schema.json         # Contrato JSON Schema para mapas satelitales topológicos
│   └── tree.json                    # Mapa topológico satelital consolidado (~250 tokens)
├── .agents/
│   └── skills/
│       └── idir/                    # Manifiesto de habilidad Antigravity para gobernanza (/idir)
│           └── SKILL.md
├── .claude/
│   └── commands/
│       └── idir.md                  # Adaptador de comandos de gobernanza para Claude Code
├── 01_seed/
│   ├── .context.yaml                # Baliza de directorio (Prioridad: P0, Relevancia: Crítica)
│   └── seed-idirectory-master.md    # Memoria técnica primaria y snapshot de ADN del proyecto
├── 02_foundation/
│   ├── .context.yaml                # Baliza de foundation
│   └── engine/
│       ├── .context.yaml
│       └── engine_readme.md         # Manifiesto de gobernanza generado para funciones de carpeta
├── 03_research/
│   ├── .context.yaml                # Baliza de research
│   ├── notebooks/                   # Notebooks interactivos EDA (Jupyter, Databricks, Fabric)
│   ├── prompts/                     # Plantillas de ingeniería de prompts y system prompts LLM
│   └── experiments/                 # PoCs de algoritmos y benchmarks de investigación
├── src/
│   ├── .context.yaml                # Baliza de código fuente
│   ├── cloud_jobs/                  # Pipelines ETL multi-cloud (Spark, Dataproc, Glue, Synapse)
│   ├── data_generation/             # Generadores de datos sintéticos y distribuciones de carga
│   ├── core/                        # Lógica de negocio compartida y servicios backend modulares
│   └── dashboards/                  # Aplicaciones BI interactivas (Streamlit, Dash, PowerBI)
├── data/                            # Almacenamiento local aislado (Ignorado por Git y agentes IA)
│   ├── .context.yaml                # Baliza de rama muerta (crawl: false, relevance: zero_for_llm)
│   ├── raw/                         # Capa Bronze (ingesta inmutable pura)
│   ├── processed/                   # Capa Silver/Gold (datos limpios y modelados)
│   └── sandbox/                     # Zona de exploración libre para ciencia de datos
├── schemas/                         # Contratos formales de esquemas (Avro, JSON Schema, SQL DDL)
├── infrastructure/                  # Infraestructura como Código (Terraform, Bicep, AWS CDK)
├── config/                          # Parámetros de entorno (dev, staging, prod)
├── tests/                           # Suites de verificación y pruebas de invariantes
│   ├── test_fwengine.py             # 16 pruebas unitarias de CLI, MiniYAML, ruteo y minúsculas
│   └── test_token_budget.py         # 4 pruebas de benchmarking para compresión de tokens
├── artifacts/
│   ├── benchmarks/                  # Suite de telemetría forense multi-repo (6 repos analizados)
│   │   ├── README.md                # Reporte máster de benchmark y análisis comparativo ejecutivo
│   │   ├── benchmark_matrix.json    # Matriz consolidada de telemetría en JSON
│   │   └── forensic_repo_*.md       # Auditorías forenses individuales detalladas
│   └── plans/
│       ├── active/                  # Planes de capacidad activos y roadmaps inferidos
│       ├── metricsthinking/         # Auditoría formal de madurez SDD MetricsThinking (Score 100%)
│       └── archive/                 # Propuestas archivadas y ramas muertas (crawl: false)
├── docs/                            # Repositorio vivo de documentación
│   ├── architecture/                # Diagramas de arquitectura multi-cloud y topología Medallion
│   ├── specs/                       # Linaje de datos, contratos de esquemas y especificaciones
│   └── notes/                       # Registro de deuda técnica, bitácoras y RCAs
├── tools/                           # Utilitarios internos de desarrollo, linters y helpers
├── scripts/                         # Scripts operativos de bash, PowerShell y generadores
├── logs/                            # Trazas locales de ejecución y volcados de auditoría (crawl: false)
├── AGENTS.md                        # Regla Maestra Universal y Protocolo Bootloader de 4 Pasos
├── GEMINI.md                        # Adaptador de gobernanza para Google Gemini y Antigravity
├── CLAUDE.md                        # Adaptador de gobernanza para Anthropic Claude Code
├── .cursorrules                     # Reglas de contexto para Cursor y Windsurf
├── .agentignore                     # Máscara de exclusión para indexadores de agentes IA
├── .gitignore                       # Reglas de exclusión estándar de Git
├── FWengine.py                      # Motor principal en Python para gobernanza, balizas y ruteo
├── LICENSE                          # Licencia de Código Abierto MIT
├── README.md                        # Documentación maestra (Inglés)
└── README_ES.md                     # Documentación maestra (Español)
```

---

## 6. Protocolo de Ejecución y Verificación

### 6.1. Configuración del Entorno y Prerrequisitos

**iDirectory** opera estrictamente dentro de la Librería Estándar de Python sin requerir instalación de paquetes externos.

```bash
# Verificar runtime del entorno Python (se recomienda 3.10+)
python --version

# Navegar a la raíz del repositorio
cd "ruta/a/iDirectory"
```

### 6.2. Ejecución del Pipeline y del Motor

#### Inicializar la Arquitectura del Workspace
Instancia la jerarquía canónica de directorios, despliega `.context/tree.json`, balizas de contexto, `.agentignore` y `.gitignore`:

```bash
python FWengine.py init .
```

#### Sincronizar y Auditar Balizas
Sincroniza todas las micro-balizas `.context.yaml` a lo largo del árbol y valida su consistencia de esquema:

```bash
python FWengine.py beacon --sync
```

#### Telemetría de Contexto y Presupuesto de Tokens
Evalúa la distribución del presupuesto de tokens y estima el consumo de contexto en los nodos activos:

```bash
python FWengine.py context --budget
```

#### Ruteo y Reubicación de Archivos
Evalúa la heurística de ubicación en modo de prueba (*dry-run*) o ejecuta la reubicación física inmediata:

```bash
# Evaluación preliminar (dry run)
python FWengine.py route "ruta/al/script_no_clasificado.py"

# Ejecución forzada de reubicación física canónica
python FWengine.py route "ruta/al/script_no_clasificado.py" --move
```

#### Auditoría Estructural de Gobernanza
Verifica invariantes de nomenclatura, detecta violaciones por mayúsculas y comprueba la integridad de balizas:

```bash
python FWengine.py audit
```

### 6.3. Suite de Verificación y Pruebas de Invariantes

Ejecuta la suite completa de pruebas unitarias y de compresión de tokens utilizando el framework estándar `unittest`:

```bash
python -m unittest discover tests
```

---

## 7. Glosario de Dominio

* **iDirectory:** Taxonomía de carpetas de alta gobernanza y motor de Context Engineering concebido por Gravity HyperScale Thinking para armonizar la ingeniería humana con la recuperación de contexto en agentes autónomos de IA.
* **Satélite Topológico (`tree.json`):** Mapa estructural ultraligero (~250 tokens) que encapsula nodos de directorio, prioridades arquitectónicas y directivas de poda para el arranque inmediato del agente.
* **Baliza de Contexto (`.context.yaml`):** Micromanifiesto local que define responsabilidades de directorio, dependencias entre módulos, niveles de prioridad (`p0` a `p3`) y directivas de rastreo (`crawl`).
* **Arquitectura Medallion:** Topología de procesamiento que segrega los activos de datos en zonas de aislamiento Bronze (`data/raw`), Silver/Gold (`data/processed`) y Sandbox (`data/sandbox`).
* **Ruteo Heurístico:** Clasificador determinista basado en reglas que proyecta nombres base y extensiones de archivo a sus directorios canónicos correspondientes.

---

## 8. Referencias Académicas y de Ingeniería

1. ISO/IEC/IEEE 26531:2015 *Systems and software engineering — Content management for product lifecycle, user and task information*.
2. Armbrust, M., et al. (2021). *Lakehouse: A New Generation of Open Platforms that Unified Data Warehousing and Advanced Analytics*. Proceedings of CIDR 2021.
3. Fowler, M. (2018). *Refactoring: Improving the Design of Existing Code*. Addison-Wesley Professional.
4. Vaswani, A., et al. (2017). *Attention Is All You Need*. Advances in Neural Information Processing Systems (NeurIPS 2017).

### Citación BibTeX

```bibtex
@software{idirectory_v3_2026,
  author = {Gravity HyperScale Thinking},
  title = {iDirectory: Multi-Cloud Governance & Context Engineering Scaffolding Engine},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/AlvaroAlejandroFinOps/iDirectory}
}
```
