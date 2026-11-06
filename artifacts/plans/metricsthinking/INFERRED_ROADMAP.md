---
id: "inferred_roadmap"
title: "INFERRED OPERATIONAL ROADMAP: IDIRECTORY"
status: "active"
executable: true
version: "5.0"
---
# INFERRED OPERATIONAL ROADMAP: IDIRECTORY

> **Framework de Gobernanza:** MetricsThinking™ v5.0 Universal (SOFTWARE-ENGINEERING / Stage-Gate)  
> **Arquetipo de Dominio:** `software-engineering` | **Modo:** `source_code`  
> **Estado Consolidado:** `73.5% / 100.0%` — **Construcción Activa / Madurez Media (50.0% - 74.9%)**  
> **Cuello de Botella Activo:** `M03: Gobernanza y Cumplimiento (66.7% completado)`  
> **Fecha de Emisión:** `2026-10-31 20:02:27`  

Este documento representa el **Roadmap Operacional y de Ejecución Técnica** derivado por ingeniería inversa a partir de la evidencia física (Ground Truth) del repositorio. Sirve como guía de trabajo para el equipo de arquitectura y desarrollo.

---

## M01: Descubrimiento y Alcance
**Avance:** `100.0%` | **Peso en Ciclo:** `5%` | **Estado:** 🟢 COMPLETADO

### Checklists de Implementación
- [x] **Problem Statement Formalizado** (`M01-C01`): Problem statement formalizado en '01_seed/seed-idirectory-master.md'. *(Evidencia: `01_seed/seed-idirectory-master.md`)*
- [x] **Límites y Scope Declarados** (`M01-C02`): Límites de alcance y fronteras del sistema identificados en '01_seed/seed-idirectory-master.md'. *(Evidencia: `01_seed/seed-idirectory-master.md`)*
- [x] **Casos de Uso Formales** (`M01-C03`): Perfiles de uso y casos definidos en '01_seed/seed-idirectory-master.md'. *(Evidencia: `01_seed/seed-idirectory-master.md`)*

### Entregables Tangibles Esperados
- ✅ Todos los artefactos y contratos físicos de **M01** han sido verificados satisfactoriamente en disco.

---

## M02: Arquitectura y Diseño Técnico
**Avance:** `100.0%` | **Peso en Ciclo:** `10%` | **Estado:** 🟢 COMPLETADO

### Checklists de Implementación
- [x] **AST / Modelos Canónicos Desacoplados** (`M02-C01`): Modelos declarativos estructurados en esquemas (9 esquemas, e.g. 'schemas/backlog.schema.json'). *(Evidencia: `schemas/backlog.schema.json`)*
- [x] **ADRs Documentados** (`M02-C02`): Registro formal de decisiones arquitectónicas (ADRs) documentado en '01_seed/seed-idirectory-master.md'. *(Evidencia: `01_seed/seed-idirectory-master.md`)*
- [x] **Contratos JSON Schema Validados** (`M02-C03`): Contratos formales de datos / esquemas presentes (9 esquemas, e.g. 'schemas/backlog.schema.json'). *(Evidencia: `schemas/backlog.schema.json`)*
- [x] **Topología y Grafos Formales** (`M02-C04`): Modelado topológico o de grafos presente en 'schemas/tree.schema.json'. *(Evidencia: `schemas/tree.schema.json`)*

### Entregables Tangibles Esperados
- ✅ Todos los artefactos y contratos físicos de **M02** han sido verificados satisfactoriamente en disco.

---

## M03: Gobernanza y Cumplimiento
**Avance:** `66.7%` | **Peso en Ciclo:** `5%` | **Estado:** 🔵 EN CONSTRUCCIÓN

### Checklists de Implementación
- [x] **Detección y Marcado de PII** (`M03-C01`): Políticas de privacidad y clasificación PII documentadas en '01_seed/seed-idirectory-master.md'. *(Evidencia: `01_seed/seed-idirectory-master.md`)*
- [ ] **Reglas de Calidad Formales (cQS)** (`M03-C02`): Implementar reglas de calidad de datos o código cQS.
- [x] **Validación Estricta de Esquemas / Context** (`M03-C03`): Gobernanza contextual iDirectory activa con 30 archivos de contexto (.context.yaml). *(Evidencia: `01_seed/.context.yaml`)*

### Entregables Tangibles Esperados
- 🎯 Cierre de brechas pendientes: Reglas de Calidad Formales (cQS).
- 📁 Materialización de especificaciones formales, código nuclear, contratos de validación o pruebas automatizadas asociadas.

---

## M04: Aprovisionamiento y Readiness
**Avance:** `100.0%` | **Peso en Ciclo:** `5%` | **Estado:** 🟢 COMPLETADO

### Checklists de Implementación
- [x] **Entorno Reproducible** (`M04-C01`): Manifiesto de empaquetado y entorno reproducible verificado en 'pyproject.toml'. *(Evidencia: `pyproject.toml`)*
- [x] **Dependencias Versionadas** (`M04-C02`): Especificación estricta de versiones de dependencias verificada en 'pyproject.toml'. *(Evidencia: `pyproject.toml`)*
- [x] **Fixture Enterprise Disponible** (`M04-C03`): Fixtures y datos de prueba disponibles (1 archivos, e.g. 'src/data_generation/.context.yaml'). *(Evidencia: `src/data_generation/.context.yaml`)*

### Entregables Tangibles Esperados
- ✅ Todos los artefactos y contratos físicos de **M04** han sido verificados satisfactoriamente en disco.

---

## M05: Construcción Núcleo (Core Engine)
**Avance:** `50.0%` | **Peso en Ciclo:** `25%` | **Estado:** 🔵 EN CONSTRUCCIÓN

### Checklists de Implementación
- [x] **Parsers Funcionales** (`M05-C01`): Módulos de procesamiento e implementación activos (15 archivos, e.g. '.agents/skills/idir/SKILL.md'). *(Evidencia: `.agents/skills/idir/SKILL.md`)*
- [x] **Inferencia Operativa de Roles** (`M05-C02`): Motor nuclear de procesamiento y lógica operativa verificado en 'src/core/context_runtime.py'. *(Evidencia: `src/core/context_runtime.py`)*
- [ ] **Resolución de Relaciones y Ciclos** (`M05-C03`): Asegurar algoritmos para resolver dependencias o relaciones.
- [ ] **Generador Canónico de Métricas / Lógica** (`M05-C04`): Implementar generador de código o síntesis de medidas.

### Entregables Tangibles Esperados
- 🎯 Cierre de brechas pendientes: Resolución de Relaciones y Ciclos, Generador Canónico de Métricas / Lógica.
- 📁 Materialización de especificaciones formales, código nuclear, contratos de validación o pruebas automatizadas asociadas.

---

## M06: Integración e Interoperabilidad
**Avance:** `80.0%` | **Peso en Ciclo:** `15%` | **Estado:** 🔵 EN CONSTRUCCIÓN

### Checklists de Implementación
- [ ] **Emisores de Dialecto Nativo** (`M06-C01`): Crear emisores hacia tecnologías destino en src/core/emitter o similar.
- [x] **Escritura Atómica y Safe-Encoding** (`M06-C02`): Manejo seguro de codificación UTF-8 / serialización protegida en 'src/core/context_runtime.py'. *(Evidencia: `src/core/context_runtime.py`)*
- [x] **Exportación Multi-Formato** (`M06-C03`): Soporte de representación multi-formato verificado en el repositorio (.json, .md, .png, .py, .toml).
- [x] **Resiliencia de Sistemas y Mitigación de SPOF** (`M06-C04`): Grafo de dependencias evaluado: 8 módulos analizados, acoplamiento estable.
- [x] **Patrones de Tolerancia a Fallos y Fallback** (`M06-C05`): Patrones de tolerancia a fallos verificados: {'timeout': 3, 'retry': 25, 'circuit_breaker': 0, 'fallback': 3} (cobertura=100.0%).

### Entregables Tangibles Esperados
- 🎯 Cierre de brechas pendientes: Emisores de Dialecto Nativo.
- 📁 Materialización de especificaciones formales, código nuclear, contratos de validación o pruebas automatizadas asociadas.

---

## M07: Aseguramiento de Calidad (QA & Stress)
**Avance:** `66.7%` | **Peso en Ciclo:** `10%` | **Estado:** 🔵 EN CONSTRUCCIÓN

### Checklists de Implementación
- [x] **Cobertura y Tasa de Éxito de Pruebas** (`M07-C01`): Suite de pruebas presente (2 archivos de prueba en tests/, e.g. 'tests/test_fwengine.py'). *(Evidencia: `tests/test_fwengine.py`)*
- [ ] **Golden Regression Tests Validados** (`M07-C02`): Añadir tests de regresión con archivos golden / snapshots esperados.
- [x] **Suites de Estrés / Benchmark Masivo** (`M07-C03`): Suites de estrés o benchmarks masivos verificados en 'scripts/generate_benchmark_reports.py'. *(Evidencia: `scripts/generate_benchmark_reports.py`)*

### Entregables Tangibles Esperados
- 🎯 Cierre de brechas pendientes: Golden Regression Tests Validados.
- 📁 Materialización de especificaciones formales, código nuclear, contratos de validación o pruebas automatizadas asociadas.

---

## M08: Validación y Aceptación Organizacional
**Avance:** `40.0%` | **Peso en Ciclo:** `10%` | **Estado:** 🔵 EN CONSTRUCCIÓN

### Checklists de Implementación
- [ ] **Proyecciones por Rol (Persona Lenses)** (`M08-C01`): Implementar proyecciones adaptadas a diferentes perfiles (lenses/personas).
- [ ] **Leadership Cockpit / Tableros Ejecutivos** (`M08-C02`): Proveer dashboard o cockpit de resumen ejecutivo.
- [ ] **CLI de Diagnóstico y Exploración** (`M08-C03`): Exponer comandos CLI de diagnóstico o auditoría.
- [x] **Seguridad Zero-Tolerance contra Secretos y Credenciales** (`M08-C04`): Zero-Tolerance verificado: Ninguna credencial ni clave activa expuesta en el repositorio. *(Evidencia: `.agentignore`)*
- [x] **Control de Entropía de Shannon e Inyecciones de Prompt** (`M08-C05`): Superficie de seguridad verificada: Max H=4.06 <= 4.5, inyecciones=0, ataque=10.0.

### Entregables Tangibles Esperados
- 🎯 Cierre de brechas pendientes: Proyecciones por Rol (Persona Lenses), Leadership Cockpit / Tableros Ejecutivos, CLI de Diagnóstico y Exploración.
- 📁 Materialización de especificaciones formales, código nuclear, contratos de validación o pruebas automatizadas asociadas.

---

## M09: Despliegue y Automatización (CI/CD)
**Avance:** `100.0%` | **Peso en Ciclo:** `10%` | **Estado:** 🟢 COMPLETADO

### Checklists de Implementación
- [x] **Pipeline CI/CD Automatizado** (`M09-C01`): Pipeline de integración continua automatizado verificado en '.github/workflows/ci.yml'. *(Evidencia: `.github/workflows/ci.yml`)*
- [x] **Empaquetado y Distribución Estandarizada** (`M09-C02`): Configuración de empaquetado estándar/entry points verificada en 'pyproject.toml'. *(Evidencia: `pyproject.toml`)*

### Entregables Tangibles Esperados
- ✅ Todos los artefactos y contratos físicos de **M09** han sido verificados satisfactoriamente en disco.

---

## M10: Cierre, Extensibilidad y Documentación
**Avance:** `100.0%` | **Peso en Ciclo:** `5%` | **Estado:** 🟢 COMPLETADO

### Checklists de Implementación
- [x] **Documentación Técnica Exhaustiva (Seed)** (`M10-C01`): Memoria técnica formal (ThinkingSeed) identificada en '01_seed/seed-idirectory-master.md'. *(Evidencia: `01_seed/seed-idirectory-master.md`)*
- [x] **CLI Help Documentado** (`M10-C02`): Instrucciones operativas y ayuda de comandos documentadas en 'README_ES.md'. *(Evidencia: `README_ES.md`)*
- [x] **Adaptadores Multicanal / Roadmap** (`M10-C03`): Roadmap formal de extensibilidad y capacidades futuras documentado en '01_seed/seed-idirectory-master.md'. *(Evidencia: `01_seed/seed-idirectory-master.md`)*
- [x] **Eficiencia Contextual Espectral FPAI** (`M10-C04`): Indicador FPAI estimado (distorsión no medida): PF_spectral=1.000 >= 0.70 (S_spectral=136077, S_linear=136077). *(Evidencia: `.agentignore`)*

### Entregables Tangibles Esperados
- ✅ Todos los artefactos y contratos físicos de **M10** han sido verificados satisfactoriamente en disco.

---

> *Documento operacional generado automáticamente por **MetricsThinking™ Universal Project Auditor**.*