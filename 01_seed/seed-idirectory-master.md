<!-- ============================================================================== -->
<!-- THINKINGSEED: ADN DEL PROYECTO (CONTEXTO PASIVO PARA MODELOS DE LENGUAJE)     -->
<!-- ============================================================================== -->
> [!NOTE]
> ### 🧬 DEFINICIÓN Y ROL DE ESTE DOCUMENTO
> 1. **¿Qué es este archivo?:** Este documento es una **Semilla de Proyecto (ThinkingSeed Master)**: representa el **ADN arquitectónico, técnico y estructural exhaustivo** del sistema. **NO es el repositorio completo de código fuente**, sino su mapa genético y memoria técnica profunda extraída directamente del entorno de desarrollo.
> 2. **Estado de Avance (Work in Progress):** Este documento refleja el **estado actual del desarrollo**. No garantiza que el proyecto esté concluido al 100%; puede representar un prototipo, un MVP o un sistema en evolución continua. La ausencia de código completo en ciertos archivos o módulos es **deliberada por diseño** para optimizar ventana de contexto o refleja áreas aún en desarrollo.
> 3. **Modo de Operación:** Trata este documento como **contexto pasivo de referencia técnica (Ground Truth)**. No asumas que el archivo está defectuoso ni intentes reescribirlo por tu cuenta.
<!-- ============================================================================== -->

# THINKING SEED MASTER: iDirectory

## 0. IDENTIDAD Y METADATOS
```yaml
seed_schema_version: "2.0"
project_name: "iDirectory"
repository_name: "iDirectory"
project_type: "infra"
repository_mode: "single-project"
generated_at: "2026-09-20T00:33:00-03:00"
generated_by: "Antigravity Agent (Gemini 3.6 Flash)"
repository_root: "d:/0001 HyperScale Thinking/PROYECTOS CLOUD/iContext/iDirectory"
git_branch: "master"
git_commit: "eadff5604e48cadc2ab46914e2bc8ed7935ab9b4"
working_tree_state: "dirty"
analysis_mode: "static"
coverage_level: "high"
known_analysis_limits:
  - "Inspección estática basada en código fuente, manifiestos del framework, árbol de directorios, beacons .context.yaml, mapa topológico .context/tree.json, auditoría MetricsThinking™ y reglas multi-proveedor."
```

### 0.1 Instrucciones para el modelo receptor
1. **ADN vs Repositorio:** Reconoce este documento como la memoria técnica y el ADN del proyecto, no como el repositorio completo ni como una prueba de ejecución.
2. **Contexto Pasivo:** No generes código no solicitado ni reclames por archivos ausentes; espera instrucciones específicas del usuario o utilízalo como contexto pasivo para responder preguntas sobre el funcionamiento del sistema.
3. **Estado de Avance:** Considera que las secciones incompletas o componentes marcados como `[FALTANTE]` representan el avance real del proyecto y oportunidades de asistencia, no errores del documento.
4. **Evidencia:** Respeta las etiquetas de evidencia y no transformes inferencias en hechos.
5. **Rutas:** Antes de proponer cambios, identifica módulos y archivos afectados citando sus rutas exactas relativas al repositorio.
6. **Contratos:** Conserva arquitectura, convenciones, contratos y restricciones declaradas.
7. **Preguntas Dirigidas:** No inventes componentes ausentes. Formula preguntas solo cuando la incertidumbre impida una respuesta segura.
8. **Seguridad:** No reveles ni solicites secretos. Usa placeholders (`<REDACTED>`).
9. **Impacto:** Evalúa impactos laterales en pruebas, configuración, datos, seguridad, observabilidad y despliegue.
10. **Asistencia:** Distingue entre solución inmediata, deuda técnica y recomendación futura.

---

## 1. RESUMEN EJECUTIVO
- **1.1 Proyecto en una frase:** Framework de gobernanza, ruteo heurístico y Context Engineering (**iDirectory v3.0**), creado y concebido por **Gravity HyperScale Thinking** para optimizar el rendimiento, reducir hasta en un 92% el desperdicio de tokens y evitar la degradación de contexto en agentes autónomos de IA y equipos de ingeniería de datos multi-cloud. `[CONFIRMADO]`
- **1.2 Problema que resuelve:** Erradica la exploración ciega (*blind tree crawling*), la dispersión desordenada de artefactos y la saturación de la ventana de contexto en modelos de lenguaje cuando analizan repositorios complejos de software y datos. `[CONFIRMADO]`
- **1.3 Usuarios o sistemas consumidores:** Agentes de codificación autónomos (Google Antigravity/Gemini, Anthropic Claude Code, OpenAI/Codex, Cursor, Windsurf, Aider), Arquitectos de Datos, Ingenieros Cloud y Científicos de Datos. `[CONFIRMADO]`
- **1.4 Alcance y límites del sistema:** Incluye el motor CLI (`FWengine.py` v3.0), satélite topológico precargado (`.context/tree.json`), semáforos de poda de ramas muertas (`.context.yaml`), máscara de exclusión de IA (`.agentignore`), evaluación de madurez (`artifacts/plans/metricsthinking/`), reglas unificadas multi-proveedor (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.cursorrules`, `.agents/skills/idir/SKILL.md`) y documentación de nivel Paper-Grade (`README.md`, `README_ES.md`). No incluye ejecución de cargas de datos remotas ni aprovisionamiento cloud en runtime. `[CONFIRMADO]`

---

## 2. ARQUITECTURA Y TOPOLOGÍA
- **2.1 Estilo arquitectónico:** Motor de Scaffolding, Gobernanza y Context Engineering modular, desacoplado y autocontenido en Python Standard Library pura (`pathlib`, `json`, `argparse`, `sys`, `os`), complementado con integración agéntica multi-proveedor, auditoría MetricsThinking™ y documentación formal Paper-Grade. `[CONFIRMADO]`
- **2.2 Árbol estructural del repositorio (All-Lowercase):**
```text
iDirectory/
├── .context/                                   # Telemetría y mapas satelitales de Context Engineering
│   └── tree.json                               # Mapa topológico consolidado (~250 tokens)
├── .agents/                                    # Customizaciones de agentes Antigravity/Gemini
│   └── skills/
│       └── idir/                               # Skill canónica /idir v3.0
│           └── SKILL.md
├── .claude/                                    # Adaptadores de comandos para Claude Code
│   └── commands/
│       └── idir.md
├── 01_seed/                                    # Semilla de proyecto y memoria técnica (ThinkingSeed Master)
│   ├── .context.yaml                           # Beacon local (Priority: P0, Relevance: Critical, Crawl: False)
│   └── seed-idirectory-master.md
├── 02_foundation/
│   ├── .context.yaml                           # Beacon local
│   └── engine/                                 # Núcleo del framework y governance engine
│       ├── .context.yaml
│       └── engine_readme.md                    # Documentación maestra generada de directorios
├── 03_research/                                # Investigación e Inteligencia Artificial
│   ├── .context.yaml                           # Beacon local
│   ├── notebooks/                              # Notebooks de exploración (EDA, algoritmos interactivos)
│   ├── prompts/                                # System prompts, árboles de contexto y plantillas LLM
│   └── experiments/                            # PoCs, prototipos de modelos y benchmarks
├── src/                                        # Código fuente productivo
│   ├── .context.yaml                           # Beacon local
│   ├── cloud_jobs/                             # Scripts de producción y pipelines Multi-Cloud (Fabric, AWS, GCP, Azure)
│   ├── data_generation/                        # Generación y simulación de datos sintéticos
│   ├── core/                                   # Lógica de negocio modular y backend
│   └── dashboards/                             # Tableros BI y visualización (Streamlit, PowerBI, Dash)
├── data/                                       # Arquitectura Medallion local (Ignorado en Git y AI)
│   ├── .context.yaml                           # Beacon local (crawl: false, relevance: zero_for_llm)
│   ├── raw/                                    # Bronze: Fuentes puras e inmutables
│   ├── processed/                              # Silver/Gold: Datos transformados y optimizados
│   └── sandbox/                                # Zona de experimentación rápida
├── schemas/                                    # Definiciones formales de esquemas (Avro, JSON Schema, DDL)
│   └── .context.yaml                           # Beacon local
├── infrastructure/                             # IaC Multi-Cloud (Terraform, Bicep, ARM, CDK)
│   └── .context.yaml                           # Beacon local
├── config/                                     # Parámetros de entorno y variables desacopladas
│   └── .context.yaml                           # Beacon local
├── tests/                                      # Pruebas unitarias, integración y calidad de datos
│   └── .context.yaml                           # Beacon local
├── artifacts/                                  # Entregables y planes estratégicos
│   ├── .context.yaml                           # Beacon local
│   └── plans/
│       ├── active/                             # Planes de capacidad activos (F-SKUs, presupuestos)
│       ├── metricsthinking/                    # Evaluación forense de madurez del proyecto (Priority: P0)
│       │   ├── .context.yaml                   # Beacon local (Priority: P0, Relevance: Critical)
│       │   ├── MetricsThinking.md              # Reporte Markdown con score, bottleneck y roadmap
│       │   └── MetricsThinking.json            # Dataset estructurado de auditoría SDD
│       └── archive/                            # Histórico de arquitecturas descartadas (crawl: false)
├── docs/                                       # Documentación técnica viva
│   ├── .context.yaml                           # Beacon local
│   ├── architecture/                           # Diagramas de arquitectura y flujos Medallion
│   │   ├── folder_manifest.json                # Manifiesto JSON de la topología
│   │   └── folder_manifest.yaml                # Manifiesto YAML de la topología
│   ├── specs/                                  # Especificaciones funcionales y contratos
│   └── notes/                                  # Bitácoras de ingeniería, ADRs y RCA
├── tools/                                      # Utilitarios locales, linters y scripts de debugging
│   └── .context.yaml                           # Beacon local
├── scripts/                                    # Scripts operativos (bash, powershell, make)
│   └── .context.yaml                           # Beacon local
├── logs/                                       # Trazas locales de ejecución y auditoría (crawl: false)
│   └── .context.yaml                           # Beacon local
├── AGENTS.md                                   # Regla Maestra Universal (Single Source of Truth)
├── GEMINI.md                                   # Shim de gobernanza para Google Gemini / Antigravity
├── CLAUDE.md                                   # Shim de gobernanza para Anthropic Claude Code
├── .cursorrules                                # Reglas contextuales para Cursor / Windsurf
├── .agentignore                                # Máscara de exclusión para indexadores de IA
├── .gitignore                                  # Reglas de exclusión para Git
├── LICENSE                                     # Licencia MIT del proyecto
├── FWengine.py                                 # Motor principal v3.0 (CLI de inicialización, beacons y ruteo)
├── README.md                                   # Documentación de alta ingeniería formal (Inglés)
└── README_ES.md                                # Documentación de alta ingeniería formal (Español)
```
- **2.3 Responsabilidad por directorio y archivo clave:**
  - `FWengine.py`: Orquestador CLI principal que alberga la lógica de ruteo, MiniYAML, generación de beacons y satélite topológico. `[CONFIRMADO]`
  - `AGENTS.md`: Contrato maestro universal de Context Engineering con el Protocolo Bootloader de 4 pasos. `[CONFIRMADO]`
  - `.context/tree.json`: Satélite topológico precargado que previene el blind crawling (~250 tokens). `[CONFIRMADO]`
  - `artifacts/plans/metricsthinking/`: Directorio crítico P0 que almacena las métricas cuantitativas y roadmap de madurez SDD (`MetricsThinking.md` y `MetricsThinking.json`). `[CONFIRMADO]`
  - `.agents/skills/idir/SKILL.md`: Declaración formal de la habilidad del agente para invocar `FWengine.py`. `[CONFIRMADO]`
  - `02_foundation/engine/engine_readme.md`: Documento derivado que describe la gobernanza para desarrolladores y agentes en el espacio de trabajo. `[CONFIRMADO]`
- **2.4 Límites modulares y acoplamiento:** Desacoplamiento total; `FWengine.py` no depende de librerías de terceros (Zero-Dependency CLI). `[CONFIRMADO]`

---

## 3. FLUJOS DE EJECUCIÓN Y ENTRY POINTS
- **3.1 Puntos de entrada principales:**
  - `python FWengine.py init [path]`: Inicializa el andamiaje canónico, genera el satélite `.context/tree.json`, beacons `.context.yaml`, `.agentignore` y `.gitignore`. `[CONFIRMADO]`
  - `python FWengine.py route <file> [--move] [--base <path>]`: Audita y clasifica un archivo según su extensión y heurística nominal, recomendando o reubicando físicamente el elemento. `[CONFIRMADO]`
  - `python FWengine.py beacon [--sync|--audit]`: Genera, sincroniza y audita todos los microarchivos `.context.yaml`. `[CONFIRMADO]`
  - `python FWengine.py map [--sync]`: Regenera el mapa satelital `.context/tree.json`. `[CONFIRMADO]`
  - `python FWengine.py context [--budget|--compact]`: Muestra telemetría de densidad y presupuesto de tokens por directorio o emite cadena de inyección rápida para prompts. `[CONFIRMADO]`
  - `python FWengine.py audit`: Audita inconsistencias de mayúsculas, carpetas huérfanas y beacons ausentes. `[CONFIRMADO]`
  - Invocación vía Slash Command `/idir` o `/dir`: Agentes Antigravity ejecutan la lógica CLI de forma contextual y transparente. `[CONFIRMADO]`
  - Invocación vía Slash Command `/metrics`: Ejecuta el motor evaluador de madurez y genera el reporte en `artifacts/plans/metricsthinking/`. `[CONFIRMADO]`
- **3.2 Diagrama de flujo principal E2E:**
```mermaid
graph TD
    A[Agente de IA / Ingeniero] -->|Paso 0| B[Lectura de AGENTS.md / GEMINI.md / CLAUDE.md]
    B -->|Paso 1| C[Lectura Satelital .context/tree.json ~250 tokens]
    C -->|Paso 2| D[Lectura de ADN 01_seed/seed-idirectory-master.md]
    D -->|Paso 3| E[Lectura de Beacon Local .context.yaml de Carpeta Destino]
    E -->|Paso 4| F{Directiva crawl: true?}
    F -->|Sí| G[Operación Quirúrgica en Archivo]
    F -->|No| H[Poda de Rama Muerta / Acceso Prohibido]
    G --> I[Ejecución de FWengine.py route / audit / beacon]
```
- **3.3 Ciclo de vida de la ejecución y estados:**
  1. Lectura de argumentos vía `argparse`.
  2. Verificación de integridad y existencia de archivos.
  3. Ejecución determinista / heurística con salida estructurada en `stdout` y código de retorno `0`. `[CONFIRMADO]`

---

## 4. MODELO DE DATOS, CONTRATOS Y PERSISTENCIA
- **4.1 Esquemas y entidades principales:**
  - `FOLDER_METADATA` (`dict[str, dict]`): Metadatos completos por directorio incluyendo propósito, rol, relevancia, directiva `crawl`, prioridad de lectura y densidad de tokens (incluyendo `artifacts/plans/metricsthinking`). `[CONFIRMADO]`
  - `ROUTING_MAP` (`dict[str, str]`): Mapeo determinista de extensiones (`.py`, `.ipynb`, `.md`, `.sql`, `.tf`, `.yaml`, `.csv`, `.parquet`, etc.) a sus carpetas canónicas en minúsculas. `[CONFIRMADO]`
  - Schema de Beacons (`.context.yaml`): Estructura YAML serializada con `MiniYAML` que define rol, propósito, prioridad, dependencias y reglas de poda. `[CONFIRMADO]`
  - Schema Satelital (`.context/tree.json`): Diccionario estructurado con nodos y prioridades para carga ultraligera en agentes. `[CONFIRMADO]`
  - Schema MetricsThinking™ (`MetricsThinking.json`): Contrato de evaluación de madurez SDD con scores ponderados, bandas de madurez y roadmap de remediación. `[CONFIRMADO]`
- **4.2 Almacenamiento, motores y migraciones:** Persistencia directa en sistema de archivos local utilizando operaciones seguras de `pathlib.Path` (`mkdir(parents=True, exist_ok=True)`, `rename`). `[CONFIRMADO]`
- **4.3 Interfaces externas:** CLI estandarizado sin dependencias externas. `[CONFIRMADO]`

---

## 5. CONFIGURACIÓN Y AMBIENTE
- **5.1 Tabla de variables de entorno:**
| Variable | Tipo | Default | Efecto | Sensible |
| :--- | :--- | :--- | :--- | :--- |
| N/A | N/A | N/A | Sin variables de entorno obligatorias; CLI autocontenido en Python Standard Library. | No `[CONFIRMADO]` |
- **5.2 Perfiles de ejecución:** Entorno universal (dev, staging, prod) soportado mediante parametrización en subdirectorio `config/`. `[CONFIRMADO]`
- **5.3 Prerrequisitos de sistema:** Python 3.10+ instalado en el entorno ejecutor (Windows, Linux, macOS). `[CONFIRMADO]`

---

## 6. PRUEBAS, CI/CD Y OPERACIÓN
- **6.1 Estrategia de pruebas:** Auditoría automatizada vía `python FWengine.py audit` que valida que no existan carpetas con mayúsculas, que todos los beacons estén presentes y que el satélite topológico esté sincronizado. `[CONFIRMADO]`
- **6.2 Automatización y pipelines CI/CD:** Compatible con GitHub Actions, pre-commit hooks y linters estándar. `[INFERIDO]`
- **6.3 Operación:** Ejecutable como script interactivo o integrado en automatizaciones agénticas de Antigravity, Claude Code, Cursor y Windsurf. `[CONFIRMADO]`

---

## 7. OBSERVABILIDAD Y MODOS DE FALLA
- **7.1 Logs y métricas:** Impresión estructurada en `stdout` durante la ejecución CLI, telemetría de presupuesto de tokens vía `python FWengine.py context --budget` y preservación de logs en `logs/`. `[CONFIRMADO]`
- **7.2 Modos de falla conocidos y estrategias de recuperación:**
  - *Archivo inexistente en `route`:* El motor captura la excepción, emite mensaje descriptivo en consola y retorna de forma controlada sin fallar el proceso. `[CONFIRMADO]`
  - *Colisión de mayúsculas en Windows al renombrar:* Mitigado mediante paso intermedio temporal en migraciones de filesystem. `[CONFIRMADO]`
- **7.3 Idempotencia:** Los comandos `init`, `beacon --sync` y `map --sync` son 100% idempotentes. `[CONFIRMADO]`

---

## 8. SEGURIDAD Y PRIVACIDAD
- **8.1 Hallazgos de seguridad estática:** Zero external dependencies (Cero superficie de ataque por paquetes vulnerables de terceros). `[CONFIRMADO]`
- **8.2 Manejo de secretos:** Sin almacenamiento de credenciales ni tokens. El archivo `.gitignore` y `.agentignore` excluyen deliberadamente carpetas de datos locales (`data/raw`, `data/processed`, `data/sandbox`) y logs (`logs/`). `[CONFIRMADO]`
- **8.3 Privacidad de datos:** Las directivas `crawl: false` en los beacons de `data/` evitan que los agentes vuelquen datos crudos a los modelos de lenguaje. `[CONFIRMADO]`

---

## 9. ESTADO REAL, DEUDA TÉCNICA Y LIMITACIONES
- **9.1 Nivel de madurez y avance real:** Versión v3.0 consolidada; motor CLI funcional, topología normalizada all-lowercase, beacons desplegados, satélite topológico activo y soporte multi-proveedor verificado con auditoría `PASS`. Score MetricsThinking™: `32.50%` (Cuello de botella actual: M02 Arquitectura a 75%, M05 Core Engine a 0%). `[CONFIRMADO]`
- **9.2 Deuda técnica identificada:**
  - Desarrollar la suite de pruebas automatizadas en `tests/` y parsers del núcleo en `src/core/`. `[FALTANTE]`
  - Sincronizar el diagrama ASCII de la Sección 5 en `README.md` y `README_ES.md` con los nombres normalizados en minúsculas. `[CONFIRMADO]`
- **9.3 Inconsistencias entre código y documentación:** Ninguna detectada en el motor y la topología física; pendiente reflejar la nueva topología minúscula en el árbol visual de los READMEs públicos. `[CONFIRMADO]`

---

## 10. REGLAS PARA MODIFICAR EL PROYECTO
- **10.1 Convenciones de estilo:** Python PEP8 estricto, tipado y sintaxis canónica de `pathlib.Path` para neutralidad de plataforma operativa. Todos los nombres de carpetas en minúsculas strictly (`all-lowercase`). `[CONFIRMADO]`
- **10.2 Reglas arquitectónicas inviolables:**
  - `01_seed/` es prioritario e inamovible como repositorio del ADN técnico. `[CONFIRMADO]`
  - No agregar dependencias de terceros a `FWengine.py`; debe mantenerse exclusivamente con la librería estándar de Python. `[CONFIRMADO]`
  - Todo agente debe seguir strictly el Protocolo Bootloader de 4 pasos declarado en `AGENTS.md`. `[CONFIRMADO]`
- **10.3 Checklist de verificación previa a commit:**
  1. Ejecutar `python FWengine.py audit` y comprobar que devuelva código de salida 0 sin violaciones.
  2. Verificar que ningún dato sensible o binario pesado haya sido añadido fuera de `.gitignore` y `.agentignore`.
  3. Ejecutar `/seedMaster` para actualizar la memoria técnica si hubo cambios estructurales.

---

## 📌 CONTEXT HANDOFF & PROTOCOLO DE ASISTENCIA

> **Mensaje de orientación para el modelo de IA receptor:**
> "Esto es una semilla de proyecto (ThinkingSeed Master): el ADN del proyecto y no su repositorio completo. Refleja el avance real y la arquitectura del sistema hasta la fecha. Como modelo receptor, tu función es usar esta semilla como memoria técnica para:
> 1. **Responder preguntas** sobre la arquitectura, funcionamiento, dependencias y flujos del sistema.
> 2. **Sugerir mejoras o asistencia técnica** sobre el estado actual y áreas pendientes identificadas en la semilla.
> 3. **Generar código o soluciones compatibles** respetando las rutas, convenciones y patrones definidos aquí, cuando el usuario te lo solicite."

### Pautas de resolución:
Antes de resolver una solicitud:
1. Identifica el objetivo del usuario.
2. Localiza los componentes afectados usando las rutas del Seed.
3. Revisa restricciones, reglas y contratos declarados.
4. Explicita supuestos cuando sea necesario: "Supongo que X debido a Y".
5. Propone cambios por archivo con rutas claras.
6. Añade pruebas, riesgos y criterios de aceptación.

### 🤝 Acuse de Recibo Inicial
Si el usuario adjuntó esta semilla **sin una instrucción específica**, no intentes generar código ni completar archivos vacíos. Responde únicamente con:
1. Un saludo confirmando que asimilaste el ADN de **iDirectory v3.0** y su stack principal.
2. Un breve resumen de 2-3 líneas sobre el objetivo y su estado actual de avance.
3. Una frase poniéndote a disposición para resolver dudas sobre su funcionamiento o colaborar en los siguientes pasos de desarrollo.
