# 🚀 Engine v1.0: Automatización, Gobernanza y Ruteo de Datos

**Engine v1.0** es la herramienta núcleo de infraestructura de datos diseñada para establecer, auditar y gobernar la estructura del Lakehouse. Automatiza el andamiaje (scaffolding) de directorios alineados con mejores prácticas multi-cloud (Bronze, Silver, Gold) y gestiona el flujo de entrada a través de un ruteador inteligente de archivos basado en metadatos y tipos de archivo.

---

## 📐 TRIPLE PERSPECTIVA ARQUITECTÓNICA

### 1. 🧮 PERSPECTIVA MATEMÁTICA (Rigor, Algoritmia e Integridad)
* **Algoritmo de Ruteo Decisional:** El motor implementa una función de asignación determinista $f(ext) \to subfolder$ mediante la matriz `ROUTING_MAP` con complejidad temporal constante $O(1)$.
* **Heurística de Clasificación Basada en Patrones:** Para archivos con extensiones genéricas o no mapeadas, se evalúa mediante un clasificador de reglas lexicográficas que analiza tokens y subcadenas del nombre del archivo en minúsculas (ej. busca `"test"`, `"spec"`, `"plan"`, `"gen"`, `"mock"`), logrando una categorización robusta sin coste de procesamiento complejo ($O(N)$ donde $N$ es la longitud del nombre del archivo).
* **Integridad Estructural:** El sistema valida la integridad referencial de los directorios de destino antes de ejecutar cualquier migración física, garantizando la consistencia y previniendo la pérdida de datos o la creación de rutas huérfanas.

### 2. 💻 PERSPECTIVA LÓGICA (Topología, Eficiencia y Estructura)
* **Topología del Directorio:** Define un grafo acíclico de directorios centralizados bajo un manifiesto único (`FOLDER_MANIFEST`), mapeando responsabilidades operativas desde el procesamiento de datos puros (`data/raw`) hasta la persistencia física optimizada (`data/processed` con compresión Delta Parquet).
* **Manejo de Excepciones y Tolerancia a Fallos:** Implementa control preventivo de colisiones y existencia de archivos (utilizando `pathlib.Path.exists()`). Si un archivo de origen no existe, levanta una excepción controlada no crítica impidiendo operaciones de E/S fallidas.
* **Idempotencia Estricta:** Las ejecuciones repetidas del comando `init` son completamente idempotentes: garantizan el estado deseado de la arquitectura de carpetas sin sobrescribir ni alterar información preexistente del usuario.

### 3. 🎨 PERSPECTIVA CREATIVA (Innovación y Diseño de Información)
* **Auto-Documentación (Living Scaffolding):** A diferencia de los estructuradores tradicionales, `FWengine.py` genera un manifiesto de gobernanza centralizado en `Engine/EngineReadme.md` que sirve como única fuente de verdad, explicando el propósito operativo de cada espacio y reduciendo la fricción para los nuevos ingenieros.
* **Integración Nativa con Control de Versiones:** Automatiza la creación de las directrices `.gitignore` directamente en el espacio raíz de desarrollo, asegurando que los entornos virtuales, cachés y archivos de datos masivos no contaminen el control de código fuente.

---

## 🗂️ ESTRUCTURA DEL LAKEHOUSE (FOLDER MANIFEST)

El andamiaje generado consta de los siguientes directorios clave:

* **`src/data_generation/`**: Módulos de simulación matemática y generación de datos sintéticos.
* **`src/fabric_jobs/`**: Scripts productivos de PySpark/Spark SQL para orquestación en Microsoft Fabric.
* **`docs/technical_specs/`**: Contratos de esquemas, linaje de datos y especificaciones técnicas.
* **`docs/engineers_notes/`**: Decisiones de diseño de ingeniería y análisis de causa raíz.
* **`docs/architecture/`**: Diagramas y topología de datos en capas Medallion.
* **`tests/`**: Suite de calidad de datos y pruebas unitarias.
* **`Notebooks/`**: Análisis exploratorio e investigación interactiva.
* **`Artefactos/Planes/`**: Presupuestos cloud, capacidad F-SKUs e hitos.
* **`Tools/`**: Scripts utilitarios locales y linting.
* **`config/`**: Parámetros de entorno desacoplados.
* **`infrastructure/`**: Infraestructura como Código (CDK, Terraform).
* **`data/raw/`**: Zona de aterrizaje local de datos inmutables (Bronze).
* **`data/processed/`**: Datos refinados listos para analítica (Silver/Gold).
* **`data/sandbox/`**: Entorno seguro de experimentación aislada.
* **`schemas/`**: Esquemas estrictos de datos (Avro, JSON Schema).
* **`scripts/`**: Automatización y scripts bash de mantenimiento.
* **`logs/`**: Trazabilidad y auditoría local.
* **`Engine/`**: Núcleo del framework donde reside el motor.

---

## ⚙️ GUÍA DE INSTALACIÓN Y USO

### Requisitos
* Python 3.8 o superior

### Inicialización del Proyecto
Genera la estructura de carpetas de gobernanza en el directorio actual:
```powershell
python FWengine.py init
```

Para inicializar en una ruta externa:
```powershell
python FWengine.py init "ruta/a/tu/proyecto"
```

### Ruteo de Archivos Inteligente
Para auditar a qué carpeta pertenece un archivo según su tipo:
```powershell
python FWengine.py route "datos_ventas.parquet"
```

Para mover físicamente el archivo analizado a su carpeta destino óptima:
```powershell
python FWengine.py route "datos_ventas.parquet" --move
```

---

## 🐙 DIRECTRICES DE GIT (.gitignore)

Para cada nuevo proyecto inicializado, el motor despliega de forma nativa la siguiente política de ignorados en la raíz:

```text
.venv/
__pycache__/
*.pyc
.ipynb_checkpoints/

# Ignorar archivos de datos locales
*.csv
*.parquet
```
