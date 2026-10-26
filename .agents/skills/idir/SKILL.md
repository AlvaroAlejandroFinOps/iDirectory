---
name: idir
description: >-
  Ejecuta la gobernanza, Context Engineering y ruteo inteligente de archivos en la arquitectura iDirectory v4.0 invocando FWengine.py.
  Permite reconciliación unificada (reconcile), paquetes de contexto (context --pack), consulta seccional de seed (seed --toc/--section), checkpoints de sesión (checkpoint), subgrafos (map --slice), ruteo (route) y enriquecimiento (enrich).
---

# Skill: /idir (Gobernanza y Context Engineering de iDirectory v4.0)

Esta habilidad proporciona el flujo para consultar, auditar, reconciliar y clasificar elementos dentro de la estructura **iDirectory v4.0** gobernada por [`./FWengine.py`](./FWengine.py) y [`./config/context_policy.json`](./config/context_policy.json).

---

## 1. Modos de Uso

### A. Reconciliación y Cierre Unificado (`reconcile`)
Sincroniza beacons, actualiza el mapa satelital `.context/tree.json` (con `topology_hash` SHA-256) y ejecuta la auditoría de gobernanza en un solo paso idempotente.

```powershell
python FWengine.py reconcile
python FWengine.py reconcile --check
```

### B. Paquete de Contexto Unificado Tier 1A (`context --pack`)
Compila en una sola respuesta (< 220 tokens) el subgrafo recortado (`slice`), el beacon efectivo resuelto por herencia, los `key_files` con estimación de tokens y el estado del checkpoint activo.

```powershell
python FWengine.py context --pack src/core --tier 1a
```

### C. Subgrafo Focalizado (`map --slice`)
Emite en < 150 tokens el nodo objetivo, su padre, hijos inmediatos y dependencias (`imports_from` / `exported_to`).

```powershell
python FWengine.py map --slice src/core
python FWengine.py map --slice src --radius 2
```

### D. Consulta Seccional del Seed Maestro (`seed --toc` / `seed --section`)
Evita cargar los ~13,500 tokens de `01_seed/` en Tier 1B o ante dudas puntuales de contrato.

```powershell
python FWengine.py seed --toc
python FWengine.py seed --section 4
```

### E. Continuidad Atencional en Sesiones Largas (`checkpoint`)
Gestiona el estado de planes multi-fase en `.context/checkpoint.json` (< 300 tokens).

```powershell
python FWengine.py checkpoint --show
python FWengine.py checkpoint --set --plan-id "reingenieria-v4" --phase "P2" --next "Ejecutar suite unittest"
python FWengine.py checkpoint --clear
```

### F. Clasificar y Mover Archivos (`route` / `route --move`)
Analiza la extensión, cabeceras AST y patrones del nombre de un archivo para ubicarlo en su directorio canónico en minúsculas.

```powershell
python FWengine.py route "<ruta_al_archivo>"
python FWengine.py route "<ruta_al_archivo>" --move
python FWengine.py route "<ruta_al_archivo>" --move --overwrite
```

### G. Telemetría de Tokens (`context --budget` / `context --compact`)
Desglosa los tokens activos (`crawl: true`), el plano de control raíz y el overhead del Bootloader, o emite el radar compacto (`~165 tokens`).

```powershell
python FWengine.py context --budget
python FWengine.py context --compact
```

### H. Enriquecimiento Semántico (`/idir enrich <dir>`)
Protocolo agéntico:
1. Ejecuta `python FWengine.py context --pack <dir> --tier 1a`. Si el nodo tiene `crawl: false`, **aborta**.
2. Lee solo las interfaces públicas del módulo (firmas, `__all__`, exports). Prohibido leer `data/`, `.env` o secretos.
3. Edita `<dir>/.context.yaml`: `purpose` ≤ 200 chars, `instructions` ≤ 240 chars; `key_files` como `"archivo.py: fn(a) -> b"` (≤ 160 chars por ítem); `imports_from` / `exported_to` como listas planas con `/`.
4. Ejecuta `python FWengine.py reconcile` para validar el esquema y actualizar `topology_hash`.

---

## 2. Instrucciones de Ejecución para el Agente

1. Cuando el usuario invoque `/idir`, ejecuta la acción correspondiente invocando `FWengine.py`.
2. **Regla obligatoria de cierre:** tras crear o mover cualquier directorio o modificar beacons, ejecuta `python FWengine.py reconcile`.
