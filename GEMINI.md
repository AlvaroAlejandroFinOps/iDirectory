# Reglas del Proyecto y Gobernanza Antigravity / Gemini

Este repositorio utiliza el sistema de gobernanza y ruteo inteligente **iDirectory v3.0** (Context Engineering), creado por **Gravity HyperScale Thinking**.

---

## 🚀 REGLA MAESTRA OBLIGATORIA
Para optimizar el uso de tokens y evitar la degradación de contexto, los agentes de Gemini/Antigravity **DEBEN** leer y seguir estrictamente la especificación maestra en [`AGENTS.md`](file:///d:/0001%20HyperScale%20Thinking/PROYECTOS%20CLOUD/iContext/iDirectory/AGENTS.md) y consultar el mapa satelital [`.context/tree.json`](file:///d:/0001%20HyperScale%20Thinking/PROYECTOS%20CLOUD/iContext/iDirectory/.context/tree.json) antes de explorar o modificar código.

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

