# Plan de mejora de iDirectory: contexto, atención y economía de tokens

**Autor de la evaluación:** GPT Sol 5.6 High  
**Fecha:** 2026-10-26  
**Repositorio evaluado:** iDirectory  
**Naturaleza:** auditoría técnica y plan de recomendaciones; no constituye una orden de ejecución automática.  
**Base observada:** commit `61684b6` (`version 3.5`) con working tree limpio al iniciar la auditoría.

## 1. Dictamen ejecutivo

iDirectory contribuye de manera real y valiosa a la ingeniería de contexto. Su mayor aporte no es «ahorrar tokens» de forma aislada, sino imponer una secuencia de navegación, declarar fronteras de lectura y separar orientación topológica de memoria arquitectónica profunda. El mapa satelital, la herencia de `crawl:false`, los slices focalizados y la separación Tier 1/Tier 2 son decisiones correctas.

Sin embargo, la implementación actual sobreestima su madurez y mezcla tres conceptos que deben medirse por separado:

1. **Economía de contexto:** cuántos tokens se cargan.
2. **Calidad de contexto:** qué proporción de esos tokens es relevante y suficiente.
3. **Continuidad atencional:** cuánto cuesta reorientar al agente después de interrupciones, cambios de fase o ejecuciones largas.

El sistema optimiza bien el primer punto en navegación inicial, pero aún no mide de forma fiable los otros dos. La suite de 54 pruebas pasa, aunque sondas aisladas demostraron que varias garantías declaradas no están cubiertas. La conclusión no es eliminar satélites ni beacons: es conservarlos, reducir su duplicación y convertirlos en contratos verificables por comportamiento.

### Valoración resumida

| Componente | Utilidad real | Riesgo actual | Dictamen |
|---|---:|---:|---|
| `AGENTS.md` | Alta | Media | Buen contrato universal, demasiado extenso para toda tarea y con disparadores sobreamplios. |
| `.context/tree.json` | Alta | Media | Excelente orientación global, pero cuesta ~824 tokens y no representa subdirectorios dinámicos. |
| `context --compact` | Alta | Baja | Mejor radar inicial cuando el objetivo todavía es ambiguo: ~163 tokens. |
| `map --slice` | Muy alta | Media | Mejor mecanismo para tareas focalizadas; su límite de 150 tokens no está garantizado en todos los grafos. |
| `.context.yaml` | Media-alta | Media | Útil cuando contiene decisiones locales; el auto-scaffolding genérico aporta poco y multiplica artefactos. |
| Seed maestro | Alta en arquitectura | Alta en tareas menores | Memoria valiosa, pero actualmente ~13.561 tokens y con afirmaciones que ya divergen del código. |
| Adaptadores por agente | Media | Alta | Mejoran adopción, pero hoy duplican reglas, versiones y métricas contradictorias. |
| Planes y métricas | Baja/negativa en su estado actual | Muy alta | Hay documentos obsoletos marcados como activos o P0 que pueden dominar la atención. |

## 2. Evidencia observada

### 2.1 Coste contextual efectivo

Las cifras que importan para un agente no son sólo las del satélite:

- `AGENTS.md`: 7.367 bytes, aproximadamente 1.842 tokens con la heurística del proyecto.
- `.context/tree.json`: 3.296 bytes, aproximadamente 824 tokens.
- `context --compact`: aproximadamente 163 tokens.
- Beacon local: máximo declarado de aproximadamente 150 tokens.
- Seed maestro: aproximadamente 13.561 tokens según `context --budget`.

Por tanto, un arranque Tier 1 real consume aproximadamente:

- **Con satélite completo:** 1.842 + 824 + hasta 150 = **~2.816 tokens**, antes de leer código.
- **Con compacto:** 1.842 + 163 + hasta 150 = **~2.155 tokens**, antes de leer código.

Un Tier 2 consume alrededor de **~16.377 tokens** antes de abrir fuentes, y puede superar **~25.000 tokens** si además se activa `artifacts/plans/metricsthinking/` (~9.389 tokens). Esto es aceptable para una auditoría arquitectónica genuina, pero excesivo si `/plan` se activa para una modificación atómica.

### 2.2 Resultados de validación

- `python FWengine.py audit`: PASS, cero violaciones declaradas.
- `python FWengine.py map --check-freshness`: PASS en el repositorio actual.
- Suite completa: **54/54 pruebas OK** en 22,274 segundos.
- Satélite: ~824 tokens; compacto: ~163; slices observados: 60–121 tokens.
- Presupuesto informado por el motor: ~45.630 tokens en directorios gobernados.

El rótulo «Total estimado de tokens en repositorio» es inexacto: `compute_context_budget()` no contabiliza archivos raíz como `FWengine.py`, `AGENTS.md`, los READMEs y adaptadores de agente. Tampoco distingue correctamente contenido textual de binarios. Debe llamarse «contenido gobernado contabilizado» hasta corregirse.

### 2.3 Fallos confirmados mediante sondas temporales

1. **Poda rota en telemetría:** un archivo de 4.000 bytes creado dentro de `data/raw/` produjo 1.000 tokens en `context --budget`, aunque el nodo declaraba `crawl:false`.
2. **Frescura incompleta:** cambios posteriores en `artifacts/plans/active/` y en `src/core/.context.yaml` no marcaron el satélite como obsoleto.
3. **Auditoría con falso positivo:** tras eliminar `src/core/` completo en un fixture, `audit_repository()` devolvió PASS.
4. **Cobertura documental inconsistente:** las pruebas permiten hasta 1.000 tokens para el satélite aunque comentarios y guías prometen 250, 500 o 600 según el archivo.
5. **Baseline inflado:** el benchmark «naive recursive dump» excluye sólo `.git`; incluye `.venv`, `__pycache__` y árboles que `.agentignore` prohíbe leer. El ahorro de 95,9% es válido contra un agente no gobernado extremo, no contra una navegación moderna razonable.

## 3. Cómo navegan los distintos agentes

| Agente / familia | Entrada real observada | Fortalezas | Desvíos probables |
|---|---|---|---|
| OpenAI Codex | `AGENTS.md` + skill `.agents/skills/idir/SKILL.md` cuando aplica | Sigue jerarquía explícita y herramientas del repositorio; buen encaje con Tier 1/Tier 2. | Duplica reglas entre contrato y skill; `/plan` fuerza seed completo incluso para planes pequeños. |
| Claude Code | `CLAUDE.md` → `AGENTS.md` + `.claude/commands/idir.md` | Adaptador corto y comandos claros. | `CLAUDE.md` usa rutas `file:///d:/...` no portables, declara v3.0 y satélite ~250 tokens; el comando no expone slicing ni freshness. |
| Gemini / Antigravity | `GEMINI.md` + `AGENTS.md` + skill | Es el adaptador más completo y sí recomienda `map --slice`. | Declara v3.1, repite casi todo el contrato y añade otra capa de prioridad. |
| Cursor / Windsurf | `.cursorrules` | Muy bajo coste y reglas esenciales. | Omite `map --slice`, freshness, auto-remediación y parte de los disparadores; puede comportarse distinto a Gemini/Codex. |
| Aider | Sólo compatibilidad declarada en seed/AGENTS | Puede aprovechar la topología si el operador la inyecta. | No se observó adaptador específico ni prueba de cumplimiento automático. |
| GitHub Copilot | Sin contrato específico observado | Puede leer archivos bajo demanda. | No existe `.github/copilot-instructions.md`; la interoperabilidad no está demostrada. |

Los adaptadores ocultos `.agents/` y `.claude/` quedan fuera del satélite y del descubrimiento de beacons. Esto evita ruido, pero también impide auditar su vigencia desde el propio sistema. El satélite debería registrar sus nombres, versión y hash como **control-plane metadata**, sin abrirlos ni convertirlos en nodos de dominio.

## 4. Utilidad real de satélites y beacons

### 4.1 Satélite

El satélite sí aporta valor porque responde rápidamente «qué dominios existen, cuál es su prioridad y qué ramas no deben recorrerse». Es especialmente útil al inicio de una sesión o cuando el objetivo no identifica una ruta.

Sus límites actuales son:

- Se genera principalmente desde `FOLDER_METADATA`, no desde el estado físico completo.
- Incluye nodos canónicos aunque falten en disco.
- Sólo autodetecta extensiones de dominio de primer nivel; no muestra subdominios dinámicos como `artifacts/plans/openia/`.
- No incluye propósito ni instrucción del nodo; obliga a una segunda lectura.
- Su freshness excluye `artifacts/`, `infrastructure/`, archivos raíz, directorios ocultos y beacons.
- El documento promete distintos límites incompatibles: ~250, <500, <600 y <1.000 tokens.

Recomendación: mantener dos salidas con contratos distintos:

- **Radar compacto** para selección de dominio, con objetivo <=250 tokens.
- **Satélite verificable** para auditoría, sin un límite rígido artificial; debe priorizar completitud, hashes y presencia física.

### 4.2 Beacons

Los beacons son útiles cuando modifican una decisión: `crawl:false`, prioridad, contratos, archivos clave, dependencias, consumidores o una instrucción local no deducible. Su herencia ascendente es un buen diseño porque permite contexto local sin leer todo el repositorio.

El valor baja cuando cada carpeta recibe un beacon físico genérico con textos como «subdominio X» o «enriquecer con /idir enrich». En esos casos el agente gasta una lectura adicional para aprender algo que ya sabía por la ruta. La cobertura de 100% de archivos beacon no equivale a 100% de cobertura semántica.

Recomendación: distinguir dos clases:

- **Beacon materializado:** obligatorio en fronteras semánticas, ramas podadas, dominios con contratos o carpetas que cambian la estrategia de lectura.
- **Beacon virtual/heredado:** suficiente en contenedores y hojas sin reglas propias. La auditoría debe considerar válida esta herencia y no crear archivos por defecto.

La métrica correcta no debe ser «porcentaje de carpetas con beacon», sino «porcentaje de decisiones de navegación cubiertas por una directiva verificable».

## 5. Señales que desvían la atención

### 5.1 Señales críticas

1. **Planes obsoletos bajo `active/`:** `implementation_plan.md` propone `001_Seed/`, `03_Research_AI/`, `Artefactos/`, `Tools/` y otras rutas incompatibles con la topología vigente all-lowercase. Termina además preguntando si debe ejecutarse. Un agente prolongado puede reinterpretarlo como orden pendiente.
2. **Métrica P0 obsoleta:** `MetricsThinking.md` e `INFERRED_ROADMAP.md` declaran 100% de madurez con 16/20 pruebas y métricas de septiembre, mientras el repositorio actual tiene 54 pruebas y fallos no medidos. Su etiqueta «LECTURA OBLIGATORIA / PRIORIDAD P0» genera sesgo de confirmación.
3. **Versiones competidoras:** README v3.5, seed/changelog v3.5, skill v3.3, engine README/esquemas v3.2, `GEMINI.md` v3.1 y `AGENTS.md`/`CLAUDE.md`/CLI v3.0.
4. **Autoridades múltiples:** seed, README, planes, MetricsThinking y adaptadores se presentan como ground truth sin una precedencia formal ni caducidad.
5. **Activación lexical de `/plan`:** un término de interfaz se usa como indicador de complejidad. Planificar una edición de cinco líneas puede cargar más de 13.000 tokens de seed innecesariamente.

### 5.2 Señales importantes

- Repetición de las mismas reglas en cinco superficies, con pequeñas diferencias.
- Rutas absolutas locales `file:///d:/...` en documentación supuestamente portable.
- Lenguaje absoluto como «inviolable», «100%» o «resuelto» sin pruebas negativas equivalentes.
- `token_density` se declara pero no gobierna dinámicamente la cantidad de contexto que se lee.
- `read_priority` carece de una política de selección cuando existen varios p0/p1.
- El cierre exige tres comandos; `audit --fix` sólo regenera el satélite si remedió algo, por lo que no equivale siempre a `beacon --sync` + `map --sync`.
- El slice recorta hijos y consumidores, pero no dependencias ni `key_files`; un beacon muy conectado puede superar los 600 caracteres pese a la garantía declarada.
- La prueba de schema verifica que el archivo JSON exista, pero el validador de beacons no aplica todo el schema: no comprueba `additionalProperties`, longitudes ni todos los tipos.

### 5.3 Riesgo en tareas atómicas

Incluso una modificación puntual puede desviarse si:

- el nombre `/plan` activa Tier 2;
- se lee el satélite completo cuando la ruta ya es conocida;
- un beacon genérico añade ritual sin información;
- las reglas específicas del agente contradicen la versión universal;
- el agente interpreta la sincronización completa como requisito tras cambios sin impacto topológico.

La regla debe ser: **el contexto mínimo suficiente depende del riesgo y alcance, no del nombre del comando**.

### 5.4 Riesgo en planes y despliegues largos

En trabajos prolongados el problema principal deja de ser el coste inicial y pasa a ser la acumulación de estado histórico. Los planes actuales no declaran vigencia, commit objetivo, decisiones sustituidas ni siguiente checkpoint. Un agente puede reabrir un plan antiguo y reinyectar supuestos superados.

Todo plan ejecutable debería contener al menos:

- `status`: draft, approved, executing, paused, completed, superseded o archived.
- `created_at`, `updated_at`, `target_revision` y `valid_until` opcional.
- `scope` e invariantes no negociables.
- `supersedes` / `superseded_by`.
- `current_phase`, último resultado verificado y siguiente acción.
- criterios de aceptación y rollback.
- señal explícita `executable: true|false`.

## 6. Arquitectura objetivo recomendada

### 6.1 Mantener dos niveles, con perfiles dentro de Tier 1

No es necesario abandonar el Two-Tier Bootloader. Conviene refinarlo:

#### Tier 1A — Atómico con ruta conocida

1. Contrato universal resumido ya inyectado por el harness.
2. `map --slice <ruta>` o lectura directa del beacon si no se necesita topología.
3. Interfaces/archivos afectados y pruebas focalizadas.
4. Seed prohibido salvo conflicto de contrato confirmado.

#### Tier 1B — Multiarchivo o plan acotado

1. `context --compact` para orientación global.
2. Slices y beacons de los dominios afectados.
3. Contratos de schemas y planes vigentes con metadatos válidos.
4. Seed por secciones, no completo, si aparece una decisión transversal.

#### Tier 2 — Arquitectura, auditoría global o migración

1. Satélite verificable.
2. Seed completo sólo si su revisión coincide con el estado del repositorio.
3. Beacons de fronteras relevantes.
4. Evidencia física, pruebas negativas y registro de discrepancias.

`/plan` debe seleccionar Tier 1B por defecto. Sólo debe elevarse a Tier 2 si el alcance cruza dominios, cambia invariantes, introduce dependencias transversales o el usuario pide auditoría/rediseño global.

### 6.2 Fuente única y adaptadores generados

Crear una política canónica estructurada —por ejemplo `config/context_policy.json`— que contenga:

- versión efectiva;
- perfiles de carga;
- invariantes;
- disparadores;
- límites como rangos y no como cifras contradictorias;
- lista de adaptadores soportados;
- precedencia documental.

Generar o validar desde esa fuente `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.cursorrules` y comandos. Los adaptadores deben contener sólo diferencias del harness, no duplicar toda la arquitectura.

### 6.3 Contexto adaptativo, no restrictivo

Cambiar «máximo fijo» por **presupuesto con escalamiento**:

- Inicio pequeño y focalizado.
- Expansión automática si falta una dependencia, falla una prueba o aparece una contradicción.
- Registro de por qué se amplió el contexto.
- Sin límite de tokens cuando la evidencia necesaria lo justifique; el límite debe disparar revisión, no truncamiento ciego.

Para los slices, preservar primero foco, contratos, dependencias y consumidores; truncar descripciones o hijos de baja prioridad. Si aun así se supera el presupuesto, emitir `budget_exceeded:true` y una lista de continuaciones, no ocultar nodos silenciosamente.

## 7. Plan priorizado de implementación

### Fase P0 — Restaurar confiabilidad del control de contexto

1. **Corregir poda en `compute_context_budget()`:** si el nodo efectivo es `crawl:false`, no recorrer ni contabilizar descendientes; devolver sólo metadatos y `pruned:true`.
2. **Hacer freshness exhaustivo y dirigido:** incluir `artifacts/`, `infrastructure/`, archivos de control raíz, adaptadores y `.context.yaml`; usar un fingerprint determinista de rutas/metadatos relevantes en lugar de sólo `mtime`.
3. **Fortalecer `audit_repository()`:** fallar por directorios canónicos ausentes, satélite stale, esquema de tree inválido y divergencia entre fuente canónica, beacons y adaptadores.
4. **Retirar señales obsoletas:** mover `implementation_plan.md` a archivo histórico; marcar `INFERRED_ROADMAP.md` y MetricsThinking de septiembre como `superseded`; quitarles P0 hasta regenerarlos.
5. **Unificar versión y métricas:** una única versión efectiva, un único umbral contractual y generación automática de cifras observadas.

**Criterio de salida P0:** las tres sondas negativas documentadas deben fallar antes de la corrección y pasar después; `audit` no puede emitir PASS ante un directorio canónico ausente o un satélite stale.

### Fase P1 — Mejorar precisión y navegación multiagente

1. Implementar perfiles Tier 1A, Tier 1B y Tier 2; eliminar `/plan` como activador incondicional del seed completo.
2. Convertir el radar compacto en entrada Tier 1 por defecto cuando la ruta sea desconocida; usar slice directo cuando ya se conoce.
3. Añadir al slice el `purpose`, una instrucción local compacta, archivos clave y un indicador explícito de truncamiento.
4. Incorporar subdominios materializados al índice verificable o declarar `has_dynamic_children` para obligar a un slice.
5. Registrar adaptadores de agente con versión/hash y añadir validaciones específicas para Codex, Claude, Gemini, Cursor/Windsurf, Aider y Copilot.
6. Sustituir beacons genéricos por herencia virtual; conservar físicos donde cambie una decisión de navegación.

**Criterio de salida P1:** todos los agentes reciben la misma decisión de Tier, poda y cierre para un mismo escenario; ninguna ruta absoluta local aparece en artefactos portables.

### Fase P2 — Continuidad en ejecuciones largas

1. Definir schema de plan con estado, vigencia, revisión objetivo, precedencia y relaciones de supersesión.
2. Añadir un checkpoint compacto para ejecuciones largas: objetivo, fase, evidencia validada, decisiones, riesgos y siguiente acción.
3. Crear un comando único `reconcile` que ejecute de forma idempotente auditoría, sincronización de beacons, satélite y freshness.
4. Separar «memoria arquitectónica» de «historial»: el seed debe describir el presente; changelogs extensos y métricas pasadas deben residir fuera de la ruta de carga.
5. Permitir consulta seccional del seed mediante índice y anchors, reservando la carga completa para auditoría global.

**Criterio de salida P2:** después de una interrupción, un agente puede reanudar una ejecución usando un checkpoint menor a 500 tokens sin reabrir todo el historial.

### Fase P3 — Evaluación empírica y gobierno continuo

Construir un benchmark de navegación con escenarios equivalentes para cada harness:

1. Bug atómico en un módulo conocido.
2. Cambio multiarchivo con schema compartido.
3. Plan de despliegue de larga duración con interrupción y reanudación.
4. Carpeta `crawl:false` con gran volumen.
5. Plan obsoleto deliberadamente marcado como `superseded`.
6. Dependencia no declarada que obliga a ampliar contexto.

Medir por escenario:

- tokens hasta el primer archivo relevante;
- tokens totales de orientación;
- precisión contextual = tokens relevantes / tokens cargados;
- recall de dependencias necesarias;
- número de lecturas redundantes;
- tiempo y herramientas hasta una decisión correcta;
- tasa de obediencia a poda;
- incidencias de instrucciones stale;
- calidad funcional final;
- coste de reorientación tras interrupción.

**Criterio de salida P3:** publicar medianas y percentiles por agente; no declarar ahorro o madurez global a partir de un único baseline sintético.

## 8. Cambios de pruebas recomendados

Añadir como mínimo:

1. `compute_context_budget` no abre ni contabiliza descendientes de nodos `crawl:false`.
2. Freshness detecta cambios en beacons, planes, infraestructura, archivos raíz y adaptadores.
3. Audit falla si falta un directorio canónico y si tree está stale o no cumple schema.
4. El satélite no declara nodos inexistentes sin marcarlos explícitamente como `expected`.
5. Slices con muchas dependencias siguen dentro del presupuesto o emiten `budget_exceeded` sin pérdida silenciosa.
6. Validación completa de `additionalProperties`, longitudes y tipos del schema de beacon.
7. Benchmark contra tres baselines: escaneo ciego, navegación moderna con ignores y navegación iDirectory.
8. Pruebas de convergencia entre adaptadores: mismo escenario, misma política efectiva.
9. Planes `superseded` no se seleccionan como vigentes.
10. El comando de cierre/reconcile es idempotente y detecta toda mutación topológica.

## 9. Decisiones recomendadas

1. **Conservar satélite y slicing.** Son el núcleo con mayor retorno.
2. **Conservar beacons, pero materializarlos sólo donde aportan una decisión.** La herencia ya permite reducir archivos.
3. **No optimizar únicamente por tokens.** Priorizar precisión, recall y continuidad.
4. **Degradar MetricsThinking de P0 hasta regenerarlo.** Su estado actual desvía más de lo que ayuda.
5. **Archivar el plan v2 antiguo.** Su topología contradice el sistema vigente.
6. **Eliminar `/plan` como activador global.** Clasificar por alcance y riesgo.
7. **Convertir documentación derivada en outputs generados o validados.** Evitar múltiples ground truths.
8. **Sustituir afirmaciones de 100% por garantías verificables y pruebas adversariales.**

## 10. Resultado esperado

Tras estas mejoras, iDirectory debería poder demostrar no sólo que reduce el contexto inicial, sino que entrega el **mínimo contexto suficiente**, amplía evidencia cuando corresponde, mantiene coherencia entre agentes y evita que planes, métricas o versiones antiguas capturen la atención durante trabajos largos.

La meta equilibrada no es «menos tokens siempre». Es:

> **Menos tokens irrelevantes, más evidencia útil y una ruta explícita para ampliar contexto sin perder continuidad.**
