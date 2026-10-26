# Reglas del Proyecto y Gobernanza Antigravity / Gemini (iDirectory v4.0)

Este repositorio utiliza el sistema de gobernanza y ruteo inteligente **iDirectory v4.0** (Adaptive Context Engineering), creado por **Gravity HyperScale Thinking**. Política canónica en [`./config/context_policy.json`](./config/context_policy.json).

---

## 🚀 REGLA MAESTRA OBLIGATORIA (BOOTLOADER ADAPTATIVO v4.0)
Para optimizar la precisión contextual y evitar la degradación de contexto (*Context Drift*), los agentes de Gemini/Antigravity **DEBEN** seguir los tres perfiles definidos en [`./AGENTS.md`](./AGENTS.md):

1. **Tier 1A (Ejecución Atómica con Ruta Conocida - Predeterminado):**
   - Ejecuta `python FWengine.py context --pack <dir> --tier 1a` (< 220 tokens) o `python FWengine.py map --slice <dir>` (< 150 tokens).
   - `01_seed/` posee **`tier1_preload: false`**; queda **prohibido precargar la semilla completa** en este nivel.
2. **Tier 1B (Multiarchivo o `/plan` Acotado):**
   - Usa `python FWengine.py context --compact` (~165 tokens) + `map --slice <dir>` en los módulos afectados.
   - Si requieres consultar el ADN arquitectónico, usa `python FWengine.py seed --toc` y `python FWengine.py seed --section <id>` en lugar de volcar el seed entero.
3. **Tier 2 (Planificación Arquitectónica Global / Auditoría Mayor):**
   - Ingesta profunda del seed activada **únicamente** ante rediseño transversal multi-dominio, `/seedMaster`, `/metrics`, `/ultraThinking`, o `seed_reference: required` en el beacon objetivo.
4. **Contrato de Cierre Unificado:** Si creas o reestructuras directorios o beacons, ejecuta un único comando idempotente:
   ```powershell
   python FWengine.py reconcile
   ```

---

## ⚡ Comando Rápido / Slash Work: `/idir`

Utiliza la habilidad `/idir` para interactuar con [`./FWengine.py`](./FWengine.py):

1. **Reconciliación y Cierre Unificado (Recomendado):**
   ```powershell
   python FWengine.py reconcile
   ```
2. **Paquete de Contexto Tier 1A (< 220 tokens):**
   ```powershell
   python FWengine.py context --pack <dir> --tier 1a
   ```
3. **Subgrafo Focalizado (< 150 tokens):**
   ```powershell
   python FWengine.py map --slice <dir>
   ```
4. **Consulta Seccional de Seed Maestro:**
   ```powershell
   python FWengine.py seed --toc
   python FWengine.py seed --section <id>
   ```
5. **Checkpoints de Continuidad Atencional:**
   ```powershell
   python FWengine.py checkpoint --show
   python FWengine.py checkpoint --set --plan-id "<id>" --phase "P1" --next "<accion>"
   ```
6. **Ruteo y Reubicación Física Canónica:**
   ```powershell
   python FWengine.py route "<ruta_del_archivo>" --move
   ```
7. **Presupuesto de Tokens y Radar Compacto:**
   ```powershell
   python FWengine.py context --budget
   python FWengine.py context --compact
   ```
8. **Auditoría y Auto-Remediación:**
   ```powershell
   python FWengine.py audit
   python FWengine.py audit --fix
   ```
