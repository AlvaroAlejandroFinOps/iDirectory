# INFERRED OPERATIONAL ROADMAP: IDIRECTORY

> **Framework de Gobernanza:** MetricsThinking™ v1.0.0-ENTERPRISE (Taxonomía Adaptada a Skills Agénticas)  
> **Estado Consolidado:** `100.0% / 100.0%` — **Excelencia Operativa / Producción (90.0% - 100.0%)**  
> **Cuello de Botella Activo:** `Ninguno. Todos los módulos canónicos se encuentran al 100%.`  
> **Fecha de Emisión:** `2026-09-25 13:45:00`  

Este documento representa el **Roadmap Operacional y de Ejecución Técnica** derivado por ingeniería inversa a partir de la evidencia física (Ground Truth) del repositorio, adaptado estrictamente al dominio de **Skill y Framework de Gobernanza para Flujos Agénticos**. Todos los hitos y checklists han sido completados y verificados en disco.

---

## M01: Descubrimiento y Especificación de Skill Agéntica
**Avance:** `100.0%` | **Peso en Ciclo:** `5%` | **Estado:** 🟢 COMPLETADO

### Checklists de Implementación
- [x] **Especificación Formal de Skill (`SKILL.md`)** (`M01-C01`): Manifiesto de skill con frontmatter YAML (name: idir, description), objetivos claros y comandos operacionales. *(Evidencia: `.agents/skills/idir/SKILL.md`)*
- [x] **Guardrails y Límites Operativos Agénticos** (`M01-C02`): Declaración explícita de acciones prohibidas ('PROHIBIDO EL ESCANEO CIEGO RECURSIVO') y directivas de poda de ramas muertas (crawl: false). *(Evidencia: `AGENTS.md`)*
- [x] **Casos de Uso y Compatibilidad Agéntica** (`M01-C03`): Sección 1.3 define formalmente los sistemas consumidores: Google Antigravity/Gemini, Claude Code, Cursor, Windsurf, Aider. *(Evidencia: `01_seed/seed-idirectory-master.md`)*

### Entregables Tangibles Esperados
- ✅ Todos los artefactos y contratos físicos de **M01** han sido verificados satisfactoriamente en disco.

---

## M02: Arquitectura de Contexto, Contratos y Esquemas
**Avance:** `100.0%` | **Peso en Ciclo:** `10%` | **Estado:** 🟢 COMPLETADO

### Checklists de Implementación
- [x] **Modelos Canónicos y Contratos de Invocación** (`M02-C01`): Contrato canónico FOLDER_METADATA y ROUTING_MAP para normalización all-lowercase y subcomandos tipados. *(Evidencia: `FWengine.py`)*
- [x] **Reglas de Gobernanza Agéntica Unificadas (ADRs)** (`M02-C02`): Protocolo Bootloader de 4 pasos como contrato arquitectónico universal e inviolable. *(Evidencia: `AGENTS.md`)*
- [x] **Esquemas Formales de Contexto** (`M02-C03`): Esquema JSON Schema referenciado (tree.schema.json) y microcontratos .context.yaml validados. *(Evidencia: `.context/tree.json`)*
- [x] **Topología Satelital y Grafo de Contexto** (`M02-C04`): Grafo satelital ultraligero (~250 tokens) que encapsula roles, prioridades y directivas de poda de todo el sistema. *(Evidencia: `.context/tree.json`)*

### Entregables Tangibles Esperados
- ✅ Todos los artefactos y contratos físicos de **M02** han sido verificados satisfactoriamente en disco.

---

## M03: Gobernanza de Contexto, Seguridad y Token Budget
**Avance:** `100.0%` | **Peso en Ciclo:** `5%` | **Estado:** 🟢 COMPLETADO

### Checklists de Implementación
- [x] **Políticas de Privacidad y Poda de Datos Masivos** (`M03-C01`): Máscara de exclusión para indexadores de IA que aísla data/raw, data/processed, logs/ y binarios pesados. *(Evidencia: `.agentignore`)*
- [x] **Telemetría y Control Cuantitativo de Token Budget (cQS)** (`M03-C02`): Algoritmo compute_context_budget y densidad tipada (token_density) por carpeta para control presupuestario de tokens. *(Evidencia: `FWengine.py`)*
- [x] **Validación Estricta de Beacons y Coherencia Topológica** (`M03-C03`): Comando python FWengine.py beacon --audit que comprueba la presencia e integridad de los 24 beacons activos. *(Evidencia: `FWengine.py`)*

### Entregables Tangibles Esperados
- ✅ Todos los artefactos y contratos físicos de **M03** han sido verificados satisfactoriamente en disco.

---

## M04: Entorno de Ejecución y Zero-Dependency Tooling
**Avance:** `100.0%` | **Peso en Ciclo:** `5%` | **Estado:** 🟢 COMPLETADO

### Checklists de Implementación
- [x] **Entorno Reproducible / Zero-External Dependencies** (`M04-C01`): Arquitectura 'Zero-Dependency' pura sobre la librería estándar de Python (pathlib, json, argparse, sys, os, unittest). *(Evidencia: `FWengine.py`)*
- [x] **Compatibilidad de Runtime y Plataformas** (`M04-C02`): Sección 5.3 documenta soporte universal para Python 3.10+ en Windows, Linux y macOS. *(Evidencia: `01_seed/seed-idirectory-master.md`)*
- [x] **Fixtures y Escenarios de Validación Agéntica** (`M04-C03`): Entornos temporales aislados (tempfile.mkdtemp) para validación determinista de ciclo de vida. *(Evidencia: `tests/test_fwengine.py`)*

### Entregables Tangibles Esperados
- ✅ Todos los artefactos y contratos físicos de **M04** han sido verificados satisfactoriamente en disco.

---

## M05: Motor Nuclear de la Skill (Workflow Engine)
**Avance:** `100.0%` | **Peso en Ciclo:** `25%` | **Estado:** 🟢 COMPLETADO

### Checklists de Implementación
- [x] **Parsers y Manejo Declarativo de Contexto** (`M05-C01`): class MiniYAML: parser y emisor atómico autocontenido para procesar archivos .context.yaml sin requerir PyYAML. *(Evidencia: `FWengine.py`)*
- [x] **Motor de Ruteo e Inferencia Heurística** (`M05-C02`): Función route_file con clasificación semántica por extensión y heurística nominal. *(Evidencia: `FWengine.py`)*
- [x] **Orquestación y Sincronización de Contexto** (`M05-C03`): Funciones init_project, sync_beacons y sync_tree para orquestar la topología física y satelital. *(Evidencia: `FWengine.py`)*
- [x] **Generador de Telemetría y Presupuesto de Contexto** (`M05-C04`): Función compute_context_budget con cálculo de tokens por carpeta y modo --compact para inyección rápida en system prompts. *(Evidencia: `FWengine.py`)*

### Entregables Tangibles Esperados
- ✅ Todos los artefactos y contratos físicos de **M05** han sido verificados satisfactoriamente en disco.

---

## M06: Integración Multi-Proveedor e Interoperabilidad
**Avance:** `100.0%` | **Peso en Ciclo:** `15%` | **Estado:** 🟢 COMPLETADO

### Checklists de Implementación
- [x] **Shims y Adaptadores Multi-Plataforma Agéntica** (`M06-C01`): Multi-proveedor activo: Antigravity/Gemini (.agents/skills/idir/SKILL.md), Claude Code (.claude/commands/idir.md), Cursor/Windsurf (.cursorrules), Universal (AGENTS.md). *(Evidencia: `.agents/skills/idir/SKILL.md`)*
- [x] **Operaciones de Filesystem Seguras e Idempotentes** (`M06-C02`): Codificación forzada UTF-8 pura, creación segura de directorios padres y control de colisiones de mayúsculas en Windows. *(Evidencia: `FWengine.py`)*
- [x] **Exportación Multi-Formato para LLMs** (`M06-C03`): Soporte nativo de formatos de salida: JSON satelital, YAML compacto de beacons, Markdown y diagramas Mermaid. *(Evidencia: `.context/tree.json`)*

### Entregables Tangibles Esperados
- ✅ Todos los artefactos y contratos físicos de **M06** han sido verificados satisfactoriamente en disco.

---

## M07: Aseguramiento de Calidad y Robustez de Flujos
**Avance:** `100.0%` | **Peso en Ciclo:** `10%` | **Estado:** 🟢 COMPLETADO

### Checklists de Implementación
- [x] **Auditoría Automatizada de Gobernanza** (`M07-C01`): Subcomando audit que evalúa mayúsculas indebidas, beacons huérfanos e integridad del mapa satelital. *(Evidencia: `FWengine.py`)*
- [x] **Pruebas Unitarias y Regresión Determinista** (`M07-C02`): Suite formal con 16 pruebas unitarias (unittest) que validan MiniYAML, ruteo determinista, generación satelital e idempotencia al 100%. *(Evidencia: `tests/test_fwengine.py`)*
- [x] **Benchmarks de Reducción de Tokens / Estrés** (`M07-C03`): Suite de benchmarking automatizado que demuestra un 96.1% de ahorro en tokens frente al escaneo recursivo tradicional y generación sub-milisegundo (0.64ms). *(Evidencia: `tests/test_token_budget.py`)*

### Entregables Tangibles Esperados
- ✅ Todos los artefactos y contratos físicos de **M07** han sido verificados satisfactoriamente en disco con 20 pruebas automáticas en `tests/`.

---

## M08: Experiencia del Agente / Interfaz Humano-Agente
**Avance:** `100.0%` | **Peso en Ciclo:** `10%` | **Estado:** 🟢 COMPLETADO

### Checklists de Implementación
- [x] **Invocación por Slash Command / Skill Trigger** (`M08-C01`): Integración completa con Slash Command /idir y alias /dir para activación agéntica interactiva. *(Evidencia: `.agents/skills/idir/SKILL.md`)*
- [x] **Cockpit de Telemetría y Dashboards de Contexto** (`M08-C02`): Subcomando context --budget genera la tabla ejecutiva en consola de densidades, roles y presupuestos de tokens. *(Evidencia: `FWengine.py`)*
- [x] **CLI Interactiva de Diagnóstico y Operación** (`M08-C03`): CLI rica basada en argparse con 6 subcomandos (init, route, beacon, map, context, audit) y ayuda integrada. *(Evidencia: `FWengine.py`)*

### Entregables Tangibles Esperados
- ✅ Todos los artefactos y contratos físicos de **M08** han sido verificados satisfactoriamente en disco.

---

## M09: Distribución, Empaquetado y Automatización CI/CD
**Avance:** `100.0%` | **Peso en Ciclo:** `10%` | **Estado:** 🟢 COMPLETADO

### Checklists de Implementación
- [x] **Empaquetado Canónico de Skill / Portabilidad** (`M09-C01`): Organización canónica de la skill, lista para ser replicada o distribuida en cualquier proyecto gestionado por agentes. *(Evidencia: `.agents/skills/idir/`)*
- [x] **Pipeline CI/CD Automatizado y Pre-Commit Hooks** (`M09-C02`): Workflow de GitHub Actions con matriz multi-OS (Ubuntu, Windows, macOS) y multi-versión (Python 3.10-3.13) que ejecuta auditoría, unit tests y benchmarks en cada push/PR. *(Evidencia: `.github/workflows/ci.yml`)*

### Entregables Tangibles Esperados
- ✅ Todos los artefactos y contratos físicos de **M09** han sido verificados satisfactoriamente en disco.

---

## M10: Memoria Técnica, Documentación y Extensibilidad
**Avance:** `100.0%` | **Peso en Ciclo:** `5%` | **Estado:** 🟢 COMPLETADO

### Checklists de Implementación
- [x] **Memoria Técnica Exhaustiva (ThinkingSeed Master)** (`M10-C01`): ADN técnico exhaustivo (Ground Truth) de 262 líneas con contratos, invariantes y diagramas de flujo. *(Evidencia: `01_seed/seed-idirectory-master.md`)*
- [x] **Documentación Paper-Grade y CLI Help** (`M10-C02`): Documentación formal de alta ingeniería sin jerga informal (README.md, README_ES.md, engine_readme.md) más ayuda integrada --help. *(Evidencia: `README.md`)*
- [x] **Roadmap de Extensión y Adaptabilidad Futura** (`M10-C03`): Registro de deuda técnica y roadmap operacional de evolución formalmente documentado. *(Evidencia: `01_seed/seed-idirectory-master.md`)*

### Entregables Tangibles Esperados
- ✅ Todos los artefactos y contratos físicos de **M10** han sido verificados satisfactoriamente en disco.

---

> *Documento operacional generado automáticamente bajo la metodología **MetricsThinking™ Universal Project Auditor**.*
