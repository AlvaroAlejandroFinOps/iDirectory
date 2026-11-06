> **Contrato operativo v6:** resolver scripts y recursos desde la skill instalada. Usar `prepare seed` / `complete seed` para el master y `prepare hybrid` / `complete hybrid` para el snapshot ágil, con el hash devuelto por el runtime. No exigir FWengine.py ni scripts de validación en el proyecto destino; la skill los resuelve desde su instalación. Conservar secciones ajenas al diferencial y distinguir estimaciones de mediciones.

<SEED_ARCHITECTURAL_VECTOR version="6.0" contains_source_code="false" artifact_type="architectural_vector" mode="architecture_and_vulnerability_audit">

# MASTER HYBRID SEED: [Nombre del Proyecto] (v6.0)

> **[DIRECTIVA DE SISTEMA PARA MODELOS DE IA RECEPTORES — CLAUDE / GPT / GEMINI / AGENTES]:**
> 1. **¿Qué es este archivo?:** Este documento es un **Vector Arquitectónico Híbrido (ThinkingSeed v6.0)** con `contains_source_code="false"`. Representa el **ADN arquitectónico, contratos simbólicos y memoria técnica** del sistema (Capa L1 del protocolo **iContext Federation v6.0**). **NO es el repositorio completo de código fuente**, sino su mapa genético de alta densidad extraído del entorno de desarrollo.
> 2. **Estado de Avance (Work in Progress):** Refleja el estado real del desarrollo. La ausencia de bloques de código fuente es una **invariante deliberada de diseño (Zero Source Code)** para optimizar la ventana de contexto. Los componentes etiquetados como `[FALTANTE]` reflejan áreas en desarrollo (WIP).
> 3. **Modo de Operación:** Trata este documento como **Ground Truth arquitectónico** y analiza críticamente sus contratos y vectores de tensión antes de proponer cambios.

---

## 0. IDENTIDAD, METADATOS Y REGLAS DE GENERACIÓN (v6.0)

```yaml
seed_schema_version: "6.0"
project_name: "<nombre>"
repository_root: "./"
git_branch: "<rama o unknown>"
git_commit: "<hash corto o unknown>"
generated_at: "<ISO-8601>"
```

### 0.1 Instrucciones para el modelo receptor y reglas de evidencia
1. **ADN vs Repositorio:** Reconoce este documento como memoria técnica (`contains_source_code="false"`), no como un repositorio truncado.
2. **Etiquetas Epistemológicas:** Respeta `[CONFIRMADO]` (observado en código/config), `[INFERIDO]` (deducción lógica), `[DECLARADO]` (en docs) y `[FALTANTE]` (esperado pero ausente).
3. **Cero Rutas Absolutas:** Exclusivamente rutas relativas (`./`). Cero unidades `C:`, `D:` o esquemas `file://`.
4. **Firmas AST de 1 Línea:** Todo símbolo debe expresarse como firma concisa sin bloques de implementación (`path/module.py::func(arg: Type) -> Ret | Inv`).

---

## 1. PROPÓSITO DEL SISTEMA, STACK Y CAPACIDADES
- Documenta en formato conciso el stack tecnológico verificado y la arquitectura de componentes.

---

## 2. TOPOLOGÍA FÍSICA Y MAPA DE DIRECTORIOS
- Describe los directorios canónicos normalizados en `all-lowercase`.

---

## 3. ARQUITECTURA DE DATOS, MODELOS Y ESQUEMAS
- Tablas, entidades y contratos de datos principales.

---

## 4. CONTRATOS SIMBÓLICOS AST (ZERO SOURCE CODE)
- Firmas públicas de funciones, clases y comandos CLI de 1 línea.

---

## 5. DEPENDENCIAS Y MANIFIESTOS DE CONSTRUCCIÓN
- Versiones fijadas de paquetes y herramientas operativas.

---

## 6. INVARIANTES DE ARQUITECTURA Y LÍMITES DE SEGURIDAD
- Reglas no negociables (`[INV-XX]`) y decisiones arquitectónicas (`[ADR-XXX]`).

---

## 7. SUPERFICIE DE TENSIÓN ADVERSARIAL Y FRONTERAS DE CONFIANZA
- Hallazgos críticos, dependencias externas no declaradas y áreas de fricción técnica.

---

## 8. DEUDA TÉCNICA Y ESTADO DE AVANCE REAL
- Componentes en desarrollo (`[FALTANTE]`) y deuda priorizada (`[DEBT-XX]`).

---

## 9. PROTOCOLO DE EJECUCIÓN, TEST SUITE Y CI/CD
- Comandos exactos de verificación determinista.

---

## 10. GLOSARIO DE TÉRMINOS Y CONVENCIONES DEL SISTEMA
- Definiciones técnicas operativas y referencias clave.

---

## 📌 CONTEXT HANDOFF & PROTOCOLO DE ASISTENCIA

> **Orientación para el modelo de IA receptor:**
> "Este documento es una semilla técnica (**ThinkingSeed Hybrid v6.0**): el ADN del proyecto (`contains_source_code="false"`) y no su repositorio completo. Refleja la arquitectura, contratos simbólicos y el avance real hasta la fecha. Como modelo receptor, utiliza esta semilla como memoria de trabajo para:
> 1. **Responder preguntas** sobre la arquitectura, funcionamiento, dependencias y flujos del sistema.
> 2. **Auditar riesgos y sugerir mejoras** basadas en la superficie de tensión (Sección 7) y áreas pendientes (`[FALTANTE]`).
> 3. **Generar código o soluciones compatibles** respetando las rutas relativas (`./`), contratos simbólicos y patrones definidos aquí, cuando el usuario te lo solicite."

### Directrices de interacción para la IA receptora:
1. **Entender:** Identificar el objetivo y los componentes afectados antes de proponer código.
2. **Validar:** Si falta información crítica, preguntar puntualmente en vez de alucinar.
3. **Citar Rutas Relativas:** Usar siempre las rutas relativas (`./...`) declaradas en la topología al sugerir modificaciones.
4. **Respetar:** Mantener el stack, firmas simbólicas y restricciones de seguridad (`<REDACTED>`).
5. **Acuse de Recibo Inicial:** Si el usuario adjuntó esta semilla sin una pregunta concreta, responde en máximo 3 líneas resumiendo el nombre del proyecto, stack y objetivo, confirmando que has asimilado el ADN v6.0 del proyecto y quedando a la espera de sus consultas o tareas.

</SEED_ARCHITECTURAL_VECTOR>
