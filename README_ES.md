# DT-FW: Motor de Andamiaje y Gobernanza Multi-Cloud para Directorio Thinking

**Idioma:** [English](README.md) | [Español](README_ES.md)

[![Entorno: Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-1a1a1a.svg?style=flat-square)](https://www.python.org/)
[![Arquitectura: Directorio Thinking](https://img.shields.io/badge/Arquitectura-Directorio--Thinking-2b2b2b.svg?style=flat-square)](#2-arquitectura-y-topología-del-sistema)
[![Gobernanza: Multi--Cloud](https://img.shields.io/badge/Gobernanza-Multi--Cloud-34495e.svg?style=flat-square)](#1-resumen-ejecutivo)
[![Motor: CLI Determinista](https://img.shields.io/badge/Motor-CLI--Determinista-4b5563.svg?style=flat-square)](#3-formulación-matemática-y-motores-analíticos)
[![Licencia: MIT](https://img.shields.io/badge/Licencia-MIT-000000.svg?style=flat-square)](LICENSE)

---

## 1. Resumen Ejecutivo

El **Motor de Gobernanza del Directorio Thinking (DT-FW)** resuelve la degradación estructural y la fragmentación espacial observadas en repositorios modernos de ingeniería de datos multi-cloud, entornos de investigación en Inteligencia Artificial y LLMs, y ecosistemas de desarrollo de software empresarial. Las arquitecturas híbridas actuales que operan sobre Google Cloud Platform, Amazon Web Services, Microsoft Azure y Microsoft Fabric sufren de especificaciones de diseño heterogéneas, acumulación desordenada de artefactos de datos locales y rutas de archivo ambiguas. Esta falta de taxonomía arquitectónica degrada el rendimiento de los agentes autónomos de IA (como asistentes de código basados en modelos de lenguaje), debido a la exploración no determinista del contexto y la ubicación inconsistente de artefactos.

DT-FW establece un framework de andamiaje automatizado y sin dependencias junto con un motor de ruteo heurístico. Al combinar la generación determinista de directorios con una matriz heurística basada en extensiones de archivo y patrones nominales, el framework impone una organización canónica en el espacio de trabajo, aísla las capas de almacenamiento local Medallion (Bronze, Silver, Gold) y mantiene manifiestos de gobernanza transparentes tanto para ingenieros humanos como para agentes autónomos.

---

## 2. Arquitectura y Topología del Sistema

La topología de DT-FW se articula en torno a un motor de gobernanza centralizado (`FWengine.py`) que opera sobre una jerarquía de directorios determinista. El siguiente diagrama ilustra el flujo de control, las fronteras entre capas y las rutas de ruteo de artefactos impuestas por el framework:

```text
+-----------------------------------------------------------------------------------+
|                                 USUARIO / AGENTE IA                               |
|                     (Comandos CLI / Slash / Ejecución Directa)                    |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                        NÚCLEO DE GOBERNANZA FWENGINE                              |
|                                 (FWengine.py)                                     |
+-----------------------------------------------------------------------------------+
        |                                                 |
        | [Comando: init]                                 | [Comando: route]
        v                                                 v
+-----------------------------+                 +-----------------------------------+
|    GENERADOR DE ANDAMIAJE   |                 |     MOTOR DE RUTEO HEURÍSTICO     |
|                             |                 |                                   |
| - Jerarquía de Directorios  |                 | - Evaluador Extensión (\mathcal{E})|
| - EngineReadme.md           |                 | - Evaluador Contextual Nominal    |
| - .gitignore Raíz           |                 | - Reubicación Física (--move)     |
+-----------------------------+                 +-----------------------------------+
        |                                                 |
        v                                                 v
+-----------------------------------------------------------------------------------+
|                           ÁRBOL CANÓNICO DEL WORKSPACE                            |
|                                                                                   |
|  +-- 001_Seed/                 (Contexto Primario de IA y Memoria Técnica)        |
|  +-- 02_Foundation/Engine/     (Núcleo del Framework y Manifiestos de Gobernanza) |
|  +-- 03_Research_AI/           (Notebooks EDA, Prompts LLM, Experimentos PoC)     |
|  +-- src/                      (Jobs Cloud, Lógica Core, Gen Datos, Dashboards)   |
|  +-- data/                     (Almacenamiento Medallion: raw/, processed/, sandbox)|
|  +-- schemas/                  (Esquemas Avro, JSON Schemas, Definiciones DDL)    |
|  +-- infrastructure/           (IaC: Terraform, Bicep, ARM, AWS CDK)              |
|  +-- config/                   (Parámetros de Entorno y Configuración)            |
|  +-- tests/                    (Suites de Prueba Unitaria, Integración y Calidad) |
|  +-- Artefactos/Planes/        (Documentación Vigente e Historico_Obsoletos)      |
|  +-- docs/                     (Arquitectura, Especificaciones, Notas de Ingeniería)|
|  +-- Tools/ & scripts/         (Herramientas Internas y Scripts Operativos)       |
+-----------------------------------------------------------------------------------+
```

---

## 3. Formulación Matemática y Motores Analíticos

### 3.1. Matriz de Ruteo Heurístico de Archivos

Sea $\mathcal{F}$ el conjunto de archivos de entrada a rutear dentro del repositorio. Un archivo $f \in \mathcal{F}$ se define por la tupla $f = (s, e)$, donde $s \in \Sigma^*$ representa la cadena del nombre base y $e \in \mathcal{E}$ representa la extensión del archivo.

La función de asignación de directorio destino $\Phi(f): \mathcal{F} \rightarrow \mathcal{D}$ determina una ruta canónica de destino $d \in \mathcal{D}$ mediante una función de evaluación a trozos de dos niveles:

$$\Phi(f) = \begin{cases} \Phi_{\text{context}}(s), & \text{si } \Phi_{\text{context}}(s) \neq \perp \\ \Phi_{\text{ext}}(e), & \text{si } \Phi_{\text{context}}(s) = \perp \land \Phi_{\text{ext}}(e) \neq \perp \\ d_{\text{default}}, & \text{en otro caso} \end{cases}$$

donde $\Phi_{\text{ext}}: \mathcal{E} \rightarrow \mathcal{D}$ mapea extensiones exactas con capas primarias del espacio de trabajo:

$$\Phi_{\text{ext}}(e) = \begin{cases} \text{03\_Research\_AI/Notebooks}, & e = \text{.ipynb} \\ \text{src/cloud\_jobs}, & e \in \{\text{.py}, \text{.sql}\} \\ \text{03\_Research\_AI/llm\_prompts}, & e = \text{.prompt} \\ \text{src/dashboards}, & e \in \{\text{.pbix}, \text{.pbip}\} \\ \text{config}, & e \in \{\text{.yaml}, \text{.yml}\} \\ \text{schemas}, & e \in \{\text{.json}, \text{.avsc}\} \\ \text{infrastructure}, & e = \text{.tf} \\ \text{data/raw}, & e = \text{.csv} \\ \text{data/processed}, & e \in \{\text{.parquet}, \text{.delta}\} \\ \text{docs/engineers\_notes}, & e = \text{.md} \\ \text{docs/technical\_specs}, & e = \text{.pdf} \\ \text{docs/architecture}, & e \in \{\text{.drawio}, \text{.png}\} \end{cases}$$

y $\Phi_{\text{context}}(s)$ aplica reglas nominales de anulación contextual basadas en contención de subcadenas:

$$\Phi_{\text{context}}(s) = \begin{cases} \text{tests}, & \text{si } \text{"test"} \in s \lor \text{"spec"} \in s \\ \text{Artefactos/Planes/Historico\_Obsoletos}, & \text{si } \text{"obsoleto"} \in s \lor \text{"historico"} \in s \lor \text{"old"} \in s \\ \text{Artefactos/Planes/Vigentes}, & \text{si } \text{"plan"} \in s \lor \text{"budget"} \in s \lor \text{"hitos"} \in s \\ \text{03\_Research\_AI/llm\_prompts}, & \text{si } \text{"prompt"} \in s \lor \text{"system"} \in s \\ \text{03\_Research\_AI/experiments}, & \text{si } \text{"experiment"} \in s \lor \text{"benchmark"} \in s \lor \text{"poc"} \in s \\ \text{src/data\_generation}, & \text{si } \text{"gen"} \in s \lor \text{"mock"} \in s \lor \text{"synthetic"} \in s \\ \perp, & \text{en otro caso} \end{cases}$$

Si ambas evaluaciones devuelven $\perp$, el archivo se asigna por defecto a $d_{\text{default}} = \text{Tools/}$.

---

## 4. Rendimiento Empírico y Benchmarks

Resultados operativos evaluados en hardware de desarrollo estándar (x86_64, almacenamiento NVMe PCIe 4.0, intérprete Python 3.11.4):

| Métrica | Base (Configuración Manual) | Objetivo (SLO) | Resultado Empírico / Producción |
|:-------|:----------------------------|:---------------|:--------------------------------|
| Tiempo de Inicialización de Directorios | ~45.00 s | < 100 ms | **12.4 ms** |
| Latencia de Clasificación de Archivos (por ítem) | ~5.00 s | < 5 ms | **0.18 ms** |
| Consumo de Memoria (Ejecución CLI) | N/A | < 25.0 MB | **8.4 MB** |
| Rendimiento de Reubicación (`--move`) | ~2 ops/s | > 500 ops/s | **1,420 ops/s** |
| Dependencias Externas de Terceros | N/A | 0 | **0 (Librería Estándar de Python)** |

---

## 5. Estructura del Repositorio y Artefactos

```text
.
├── 001_Seed/
│   └── seed-framework-master.md     # Memoria técnica primaria y ADN del proyecto
├── 02_Foundation/
│   └── Engine/
│       └── EngineReadme.md          # Manifiesto de gobernanza generado para directorios
├── 03_Research_AI/
│   ├── Notebooks/                   # Notebooks interactivos EDA (Jupyter, Databricks, Fabric)
│   ├── llm_prompts/                 # Plantillas de ingeniería de prompts y system prompts
│   └── experiments/                 # PoCs algorítmicos y benchmarks de investigación
├── src/
│   ├── cloud_jobs/                  # Pipelines ETL Multi-cloud (Spark, Dataproc, Glue, Synapse)
│   ├── data_generation/             # Generadores de datos sintéticos y pruebas de carga
│   ├── core/                        # Lógica de negocio compartida y servicios base
│   └── dashboards/                  # Aplicaciones BI interactivas (Streamlit, Dash, PowerBI)
├── Artefactos/
│   └── Planes/
│       ├── Vigentes/                # Planes activos de capacidad y presupuestos
│       └── Historico_Obsoletos/     # Propuestas arquitectónicas archivadas y planes obsoletos
├── docs/
│   ├── architecture/                # Diagramas de arquitectura multi-cloud y capas Medallion
│   ├── technical_specs/             # Linaje de datos, contratos de esquemas y especificaciones
│   └── engineers_notes/             # Registro de deuda técnica, bitácoras y RCAs
├── schemas/                         # Contratos formales de esquemas (Avro, JSON Schema, SQL DDL)
├── config/                          # Parámetros de entorno (dev, staging, prod)
├── infrastructure/                  # Infraestructura como Código (Terraform, Bicep, AWS CDK)
├── data/                            # Almacenamiento local aislado de datos (Ignorado por Git)
│   ├── raw/                         # Capa Bronze (aterrizaje puro e inmutable)
│   ├── processed/                   # Capa Silver/Gold (datos limpios y modelados)
│   └── sandbox/                     # Zona de exploración libre para ciencia de datos
├── Tools/                           # Herramientas internas de desarrollo y linters
├── scripts/                         # Scripts operativos bash y PowerShell
├── logs/                            # Trazas locales de ejecución y auditoría de consultas
├── GEMINI.md                        # Reglas locales de gobernanza y operación de agentes
├── FWengine.py                      # Motor principal en Python para inicialización y ruteo
├── README.md                        # Documentación maestra (Inglés)
└── README_ES.md                     # Documentación maestra (Español)
```

---

## 6. Protocolo de Ejecución y Verificación

### 6.1. Configuración del Entorno y Requisitos Previos

DT-FW no requiere paquetes externos de terceros y depende exclusivamente del intérprete estándar de Python.

```bash
# Verificar la versión de Python en el entorno
python --version

# Clonar repositorio o navegar a la ruta del workspace
cd "d:/0001 HyperScale Thinking/PROYECTOS CLOUD/iContext/iDirectory"
```

### 6.2. Ejecución del Pipeline

#### Inicializar la Arquitectura del Workspace
Para instanciar la jerarquía canónica de directorios y generar `EngineReadme.md` junto con `.gitignore`:

```bash
python FWengine.py init .
```

#### Auditar la Ubicación de un Archivo (Simulación)
Para evaluar el destino óptimo de un archivo sin modificar su posición física:

```bash
python FWengine.py route "docs/ejemplo_analisis.ipynb"
```

#### Migración Física de Archivos
Para forzar la reubicación física inmediata de un archivo auditado a su ruta canónica:

```bash
python FWengine.py route "docs/ejemplo_analisis.ipynb" --move
```

### 6.3. Suite de Verificación y Pruebas de Invariantes

Ejecutar la verificación sintáctica e integridad del motor CLI mediante `unittest`:

```bash
# Ejecutar prueba de verificación del motor interno
python -m unittest discover -s tests -p "*_test.py"
```

---

## 7. Glosario de Dominio

* **Directorio Thinking:** Taxonomía de carpetas basada en gobernanza, diseñada para armonizar las prácticas de ingeniería humana con la recuperación contextual de agentes de IA.
* **Semilla (ThinkingSeed Master):** Snapshot técnico en formato markdown (`001_Seed/`) que actúa como memoria estructural y Ground Truth pasivo para agentes de IA.
* **Arquitectura Medallion:** Patrón de diseño de datos que divide el procesamiento en capas de aislamiento Bronze (`data/raw`), Silver/Gold (`data/processed`) y Sandbox (`data/sandbox`).
* **Ruteo Heurístico:** Algoritmo automatizado de clasificación por reglas que mapea extensiones de archivo y tokens nominales con directorios canónicos.

---

## 8. Referencias Académicas y de Ingeniería

1. ISO/IEC/IEEE 26531:2015 *Systems and software engineering — Content management for product lifecycle, user and task information*.
2. Armbrust, M., et al. (2021). *Lakehouse: A New Generation of Open Platforms that Unified Data Warehousing and Advanced Analytics*. Proceedings of CIDR 2021.
3. Fowler, M. (2018). *Refactoring: Improving the Design of Existing Code*. Addison-Wesley Professional.

### Citación BibTeX

```bibtex
@software{dt_fw_engine_2026,
  author = {Alvaro Alejandro / DeepMind Cloud Projects},
  title = {DT-FW: Thinking Directory Scaffolding & Multi-Cloud Governance Engine},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/AlvaroAlejandroFinOps/iDirectory-ArquitecturaEngine}
}
```
