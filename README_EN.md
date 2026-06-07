# 🚀 Engine v1.0: Automation, Governance, and Data Routing

**Engine v1.0** is the core data infrastructure utility designed to establish, audit, and govern the Lakehouse repository structure. It automates the directory scaffolding aligned with multi-cloud medallion standards (Bronze, Silver, Gold) and manages incoming files via an intelligent routing matrix based on metadata and file extensions.

---

## 📐 TRIPLE ARCHITECTURAL PERSPECTIVE

### 1. 🧮 MATHEMATICAL PERSPECTIVE (Rigor, Algorithmics, and Integrity)
* **Decisional Routing Algorithm:** The engine implements a deterministic mapping function $f(ext) \to subfolder$ via the `ROUTING_MAP` dictionary, executing with a constant time complexity $O(1)$.
* **Pattern-Based Heuristic Classification:** Ambiguous or generic files are analyzed using a rule-based lexicographical classifier that inspects lowercase string tokens (such as `"test"`, `"spec"`, `"plan"`, `"gen"`, `"mock"`), providing robust categorization with minimal overhead ($O(N)$ where $N$ represents filename length).
* **Structural Integrity:** The utility asserts the target directory structure before executing file movements, preventing data loss or the creation of orphaned system paths.

### 2. 💻 LOGICAL PERSPECTIVE (Topology, Efficiency, and Structure)
* **Directory Topology:** Defines an acyclic directory graph controlled by a single centralized configuration source (`FOLDER_MANIFEST`), mapping operations from raw entry zones (`data/raw`) to physical storage formats (`data/processed` using Delta Parquet compression).
* **Exception Handling & Fault Tolerance:** Prevents I/O collision using validation check patterns (`pathlib.Path.exists()`). If a source file does not exist, it raises a controlled non-crashing warning, blocking bad filesystem operations.
* **Strict Idempotency:** Consecutive invocations of the `init` command yield identical results without altering or overwriting existing user data.

### 3. 🎨 CREATIVE PERSPECTIVE (Innovation and Information Design)
* **Self-Documenting Architecture (Living Scaffolding):** Unlike standard boilerplate generators, `FWengine.py` deploys a centralized master file (`Engine/EngineReadme.md`), offering a single point of truth regarding directory policies and accelerating onboarding.
* **Native Version Control Integration:** Automatically drafts and deploys `.gitignore` templates directly into the project root directory, keeping Python virtual environments, cache folders, and heavy datasets off the repository.

---

## 🗂️ LAKEHOUSE FOLDER MANIFEST

The generated scaffolding comprises the following key directories:

* **`src/data_generation/`**: Mathematical simulation models and synthetic data generators.
* **`src/fabric_jobs/`**: PySpark/Spark SQL scripts for production orchestrations in Microsoft Fabric.
* **`docs/technical_specs/`**: Data lineage sheets, schema contracts, and specifications.
* **`docs/engineers_notes/`**: Architecture design decisions, runbooks, and root-cause analysis.
* **`docs/architecture/`**: Topology maps and Medallion layer structures.
* **`tests/`**: Unit testing suites and quality assurance (Great Expectations).
* **`Notebooks/`**: Exploratory data analysis (EDA) and prototype notebooks.
* **`Artefactos/Planes/`**: Capacity planning (F-SKUs), cloud budgets, and milestones.
* **`Tools/`**: Local utility scripts and linting tools.
* **`config/`**: Decoupled environmental variable schemas.
* **`infrastructure/`**: Infrastructure as Code templates (CDK, Terraform).
* **`data/raw/`**: Raw landing zone for immutable source files (Bronze).
* **`data/processed/`**: Processed schemas optimized for analytics (Silver/Gold).
* **`data/sandbox/`**: Sandbox testing directories for isolated development.
* **`schemas/`**: Strict schema definitions (Avro, SQL DDL).
* **`scripts/`**: System maintenance scripts (bash/make).
* **`logs/`**: Logging and auditing dumps.
* **`Engine/`**: Framework core files where the engine script resides.

---

## ⚙️ INSTALLATION AND DEPLOYMENT GUIDE

### Prerequisites
* Python 3.8 or higher

### Project Scaffolding Initialization
Create the directory structure under your current working folder:
```powershell
python FWengine.py init
```

To initialize the structure in an external project path:
```powershell
python FWengine.py init "path/to/your/project"
```

### Smart File Routing
Audit where a specific file belongs in the directory structure:
```powershell
python FWengine.py route "sales_data.parquet"
```

To physically move the file into its designated target subfolder:
```powershell
python FWengine.py route "sales_data.parquet" --move
```

---

## 🐙 GIT POLICIES (.gitignore)

For every new repository initialized, the engine deploys the following ignore policy in the root folder:

```text
.venv/
__pycache__/
*.pyc
.ipynb_checkpoints/

# Ignore local datasets
*.csv
*.parquet
```
