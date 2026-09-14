# Reglas del Proyecto y Gobernanza Antigravity / Gemini

Este repositorio utiliza el sistema de gobernanza y ruteo inteligente **Directorio Thinking Architecture**.

---

## 🚀 Comando Rápido / Slash Work: `/dir`

Utiliza la habilidad `/dir` para ejecutar la lógica de gobernanza y ruteo definida en [`FWengine.py`](file:///d:/0001%20HyperScale%20Thinking/PROYECTOS%20CLOUD/DeepMind/FrameWork/FWengine.py).

### Acciones Soportadas:
1. **Inicialización de Estructura**:
   ```powershell
   python "d:\0001 HyperScale Thinking\PROYECTOS CLOUD\DeepMind\FrameWork\FWengine.py" init
   ```
2. **Auditoría / Recomendación de ubicación de archivo**:
   ```powershell
   python "d:\0001 HyperScale Thinking\PROYECTOS CLOUD\DeepMind\FrameWork\FWengine.py" route "<ruta_del_archivo>"
   ```
3. **Reubicación Física Automática**:
   ```powershell
   python "d:\0001 HyperScale Thinking\PROYECTOS CLOUD\DeepMind\FrameWork\FWengine.py" route "<ruta_del_archivo>" --move
   ```

---

## 📌 Guía de Gobernanza de Directorios

- **`001_Seed/`**: Semilla de proyecto y contexto primario para agentes de IA.
- **`02_Foundation/Engine/`**: Núcleo del framework de automatización y `EngineReadme.md`.
- **`03_Research_AI/`**: Notebooks (`.ipynb`), prompts (`.prompt`) y experimentos de I+D.
- **`src/`**: Pipelines de datos (`cloud_jobs/`), generadores sintéticos (`data_generation/`), dashboards (`dashboards/`) y core.
- **`Artefactos/Planes/`**: Planes de capacidad vigentes e histórico de descartados.
- **`docs/`**: Especificaciones técnicas (`technical_specs`), notas de ingenieros (`engineers_notes`) y diagramas (`architecture`).
- **`schemas/`**: Esquemas de datos (`.json`, `.avsc`).
- **`config/`**: Parámetros de entorno (`.yaml`, `.yml`).
- **`infrastructure/`**: Scripts de IaC (`.tf`).
- **`data/`**: Datos locales aislados (`raw/`, `processed/`, `sandbox/`).

---

## 🤖 Regla para Agentes de IA
Al crear o guardar nuevos archivos, consulta siempre el manifiesto de `FWengine.py` o ejecuta `/dir route` para garantizar que los artefactos se ubiquen en su directorio canónico correspondiente.
