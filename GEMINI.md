# Reglas del Proyecto y Gobernanza Antigravity / Gemini

Este repositorio utiliza el sistema de gobernanza y ruteo inteligente **iDirectory v3.0** (Context Engineering), creado por **Gravity HyperScale Thinking**.

---

## 🚀 REGLA MAESTRA OBLIGATORIA (TWO-TIER BOOTLOADER)
Para optimizar el uso de tokens y evitar la degradación de contexto (*Context Drift* y dispersión en cabezales de atención), los agentes de Gemini/Antigravity **DEBEN** seguir el protocolo de dos niveles definido en [`AGENTS.md`](file:///d:/0001%20HyperScale%20Thinking/PROYECTOS%20CLOUD/iContext/iDirectory/AGENTS.md):

1. **Tier 1 (Operación Quirúrgica / Ejecución Atómica - Predeterminado):**
   - Secuencia: `AGENTS.md` -> `.context/tree.json` -> `.context.yaml` objetivo (o herencia ascendente) -> Ejecución.
   - **Prohibido precargar la semilla (`seed-idirectory-master.md`)** en este nivel para no quemar ~6,800 tokens de forma innecesaria.
2. **Tier 2 (Planificación Arquitectónica / Auditoría Mayor):**
   - Ingesta profunda del seed activada **únicamente** ante disparadores explícitos:
     - *Disparador 1 (Usuario):* `/seedMaster`, `/metrics`, `/ultraThinking`, `/plan` o rediseño integral.
     - *Disparador 2 (Beacon):* Directiva `seed_reference: required` en `.context.yaml`.
     - *Disparador 3 (Agente):* Duda no resuelta sobre contratos o dependencias no declaradas (lectura puntual).
3. **Contrato de Cierre:** Si creas o reestructuras directorios, ejecuta `beacon --sync` y `map --sync`.

---

## ⚡ Comando Rápido / Slash Work: `/idir`

Utiliza la habilidad `/idir` para interactuar con [`FWengine.py`](file:///d:/0001%20HyperScale%20Thinking/PROYECTOS%20CLOUD/iContext/iDirectory/FWengine.py):

1. **Auditoría:**
   ```powershell
   python "d:\0001 HyperScale Thinking\PROYECTOS CLOUD\iContext\iDirectory\FWengine.py" audit
   ```
2. **Ruteo de Archivo:**
   ```powershell
   python "d:\0001 HyperScale Thinking\PROYECTOS CLOUD\iContext\iDirectory\FWengine.py" route "<ruta_del_archivo>"
   ```
3. **Reubicación Física:**
   ```powershell
   python "d:\0001 HyperScale Thinking\PROYECTOS CLOUD\iContext\iDirectory\FWengine.py" route "<ruta_del_archivo>" --move
   ```
4. **Sincronización de Beacons:**
   ```powershell
   python "d:\0001 HyperScale Thinking\PROYECTOS CLOUD\iContext\iDirectory\FWengine.py" beacon --sync
   ```
5. **Presupuesto de Tokens:**
   ```powershell
   python "d:\0001 HyperScale Thinking\PROYECTOS CLOUD\iContext\iDirectory\FWengine.py" context --budget
   ```

