# MASTER HYBRID SEED: [Nombre del Proyecto]

> **Propósito:** Snapshot técnico, verificable y portable.
> **Instrucción al Agente:** Actúa como Arquitecto de Software Senior. Inspecciona el repo y llena este documento respetando las etiquetas de evidencia y la política de seguridad.

## 0. REGLAS DE GENERACIÓN (Epistemología y Seguridad)
*   **Etiquetas de Evidencia:** Toda afirmación debe llevar:
    *   `[CONFIRMADO]`: Observado directamente en código/config.
    *   `[INFERIDO]`: Deducción lógica (no declarado).
    *   `[FALTANTE]`: Esperado, pero no hallado.
*   **Política de Seguridad:** **PROHIBIDO** reproducir secretos, passwords, tokens o connection strings. Sustituye siempre por `<REDACTED>`. Si existen secretos versionados, regístralo como hallazgo sin reproducir el valor.

---

## 1. CORE MANIFESTO
   - 1.1 Objetivo Principal
   - 1.2 Problema que Resuelve
   - 1.3 Patrón Arquitectónico
   - 1.4 Stack Principal (Versiones y fuente: manifest/lockfile)

## 2. REPOSITORY TOPOLOGY
   - Tree completo (omitir ruido: `.git`, `node_modules`, `__pycache__`, etc.)
   - 2.x Diferenciaciones clave entre carpetas ambiguas.

## 3. EXECUTION FLOW
   - 3.1 Flujo E2E (Diagrama Mermaid o ASCII)
   - 3.2 Entry Points (Qué comandos/triggers inician qué procesos)
   - 3.3 Datos: Origen, transformación y persistencia.

## 4. CURRENT STATE & RULES
   - 4.1 Foco actual y estado de madurez.
   - 4.2 Reglas de código y convenciones (Style, linting, tipado).
   - 4.3 Convenciones de directorios.

## 5. ECOSYSTEM CONTEXT
   - Proyectos hermanos, dependencias externas, integraciones críticas.

## 6. CONFIGURATION REFERENCE
   - Tabla: Variable | Tipo | Default | Efecto | Sensible (Sí/No)

## 7. SEGURIDAD, RIESGOS Y FAILURE MODES
   - 7.1 Security Findings: Análisis de vulnerabilidades estáticas.
   - 7.2 Failure Modes: ¿Qué pasa si falla la fuente? ¿Qué pasa ante re-ejecución? ¿Existe idempotencia?
   - 7.3 Riesgos técnicos: Deuda técnica, bloqueos, dependencias críticas.

## 8. SECCIONES OPCIONALES (Si aplica)
   - Dependency Graph, Data Contracts, ADRs (Decisions Log), Testing Strategy.

---

## 9. CONTEXT HANDOFF (Instrucciones para el Modelo Receptor)
Este documento es la fuente primaria. Antes de proponer cambios, el modelo debe:

1.  **Entender:** Identificar el objetivo y componentes afectados.
2.  **Validar:** Si la información falta, **preguntar** en lugar de alucinar.
3.  **Justificar:** Citar rutas del repositorio al proponer cambios.
4.  **Respetar:** Mantener arquitectura, contratos y restricciones de seguridad.
5.  **Proponer:** Detallar archivos a modificar/crear y riesgos de rollback.
6.  **Supuestos:** Si debe asumir, marcar explícitamente: "Supongo que X debido a Y".
