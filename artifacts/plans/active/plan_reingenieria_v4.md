---
plan_id: idirectory-v4-reengineering-plan
status: executing
executable: true
target_version: "4.0"
created_at: "2026-10-26"
updated_at: "2026-10-26"
supersedes: "implementation_plan_v2_superseded.md"
current_phase: "P2"
---

# Plan Activo v4.0: Reingeniería de Contexto Adaptativo y Plano de Control Verificable

Este plan ejecutable (`status: executing`, `target_version: 4.0`) gobierna la transición de **iDirectory** a su arquitectura **v4.0**, consolidando la validación de las sugerencias de GPT Sol 5.6 High y las 7 optimizaciones de Gemini 4 Argon (Medium).

## Invariantes No Negociables
- **`[INV-01]` Zero-Dependency:** 100% librería estándar de Python en `./FWengine.py`.
- **`[INV-02]` Prohibición de Escaneo Ciego:** Navegación guiada por `context --pack`, `context --compact`, `map --slice` o `.context/tree.json`.
- **`[INV-03]` Poda Absorbente (`crawl: false`):** Ningún subcomando ni agente explora ramas muertas (`data/raw`, `data/processed`, `data/sandbox`, `logs`, `artifacts/plans/archive`).
- **`[INV-04]` Sincronización por Fingerprint SHA-256:** Todo cambio estructural se cierra con `python FWengine.py reconcile`.
- **`[INV-06]` Topología All-Lowercase:** Prohibidas las mayúsculas en nombres de directorios gobernados.
- **`[INV-08]` Portabilidad de Rutas POSIX:** Prohibidas las rutas locales absolutas (`file:///`) y separadores `\` en contratos y adaptadores.

## Fases de Ejecución y Criterios de Aceptación
1. **P0 (Control de Contexto Verificable):** Poda estricta en `compute_context_budget()`, `topology_hash` SHA-256 en `.context/tree.json`, fallo de `audit` ante directorios canónicos ausentes o satélite desactualizado.
2. **P1 (Perfiles Tier 1A / 1B / 2 y Multi-Agente):** `context --pack <dir>`, `seed --toc` / `seed --section <id>`, política única en `./config/context_policy.json` y paridad de versión v4.0 en adaptadores.
3. **P2 (Continuidad Atencional):** Máquina de estados en `./.context/checkpoint.json` (`< 300 tokens`), frontmatter verificable en planes activos y cierre unificado `reconcile`.
4. **P3 (Validación Adversarial Tri-Baseline):** 68 pruebas automatizadas en `./tests/` con 100% de aprobación.
