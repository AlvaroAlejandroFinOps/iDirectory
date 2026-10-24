# Reglas del Proyecto y Gobernanza Antigravity / Gemini

Este repositorio utiliza el sistema de gobernanza y ruteo inteligente **iDirectory v3.1** (Context Engineering), creado por **Gravity HyperScale Thinking**.

---

## 🚀 REGLA MAESTRA OBLIGATORIA (TWO-TIER BOOTLOADER)
Para optimizar el uso de tokens y evitar la degradación de contexto (*Context Drift* y dispersión en cabezales de atención), los agentes de Gemini/Antigravity **DEBEN** seguir el protocolo de dos niveles definido en [`AGENTS.md`](./AGENTS.md):

1. **Tier 1 (Operación Quirúrgica / Ejecución Atómica - Predeterminado):**
   - Secuencia: `AGENTS.md` -> `.context/tree.json` -> `.context.yaml` objetivo (o herencia ascendente) -> Ejecución.
   - El satélite `.context/tree.json` consume `< 500 tokens` (`python FWengine.py context --compact` consume `~150 tokens`).
   - **Variante focalizada:** Si la tarea está confinada a un subdominio, usa `python FWengine.py map --slice <dir>` (< 150 tokens) en lugar de `tree.json` completo.
   - `01_seed/` posee `crawl: true` pero **`tier1_preload: false`**; queda **prohibido precargar la semilla** en este nivel para no quemar tokens de forma innecesaria.
2. **Tier 2 (Planificación Arquitectónica / Auditoría Mayor):**
   - Ingesta profunda del seed activada **únicamente** ante disparadores explícitos:
     - *Disparador 1 (Usuario):* `/seedMaster`, `/metrics`, `/ultraThinking`, `/plan` o rediseño integral.
     - *Disparador 2 (Beacon):* Directiva `seed_reference: required` en `.context.yaml`.
     - *Disparador 3 (Agente):* Duda no resuelta sobre contratos o dependencias no declaradas (lectura puntual).
3. **Contrato de Cierre:** Si creas o reestructuras directorios, ejecuta `audit --fix`, `beacon --sync` y `map --sync`.

---

## ⚡ Comando Rápido / Slash Work: `/idir`

Utiliza la habilidad `/idir` para interactuar con [`FWengine.py`](./FWengine.py):

1. **Auditoría:**
   ```powershell
   python FWengine.py audit
   ```
2. **Auto-Remediación:**
   ```powershell
   python FWengine.py audit --fix
   ```
3. **Subgrafo Focalizado:**
   ```powershell
   python FWengine.py map --slice <dir>
   ```
4. **Ruteo de Archivo:**
   ```powershell
   python FWengine.py route "<ruta_del_archivo>"
   ```
5. **Reubicación Física:**
   ```powershell
   python FWengine.py route "<ruta_del_archivo>" --move
   ```
6. **Reubicación con Sobrescritura Permitida:**
   ```powershell
   python FWengine.py route "<ruta_del_archivo>" --move --overwrite
   ```
7. **Sincronización de Beacons:**
   ```powershell
   python FWengine.py beacon --sync
   ```
8. **Presupuesto de Tokens:**
   ```powershell
   python FWengine.py context --budget
   ```


