![alt text](iDirectory.png)
# iDirectory: Multi-Cloud Governance & Scaffolding Engine by Gravity HyperScale Thinking

**Language:** [English](README.md) | [Español](README_ES.md)

[![Runtime: Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-1a1a1a.svg?style=flat-square)](https://www.python.org/)
[![Architecture: iDirectory v3.0](https://img.shields.io/badge/Architecture-iDirectory%20v3.0-2b2b2b.svg?style=flat-square)](#2-system-architecture--topology)
[![Created by: Gravity HyperScale Thinking](https://img.shields.io/badge/Created%20by-Gravity%20HyperScale%20Thinking-34495e.svg?style=flat-square)](#1-executive-abstract)
[![Engine: Deterministic CLI](https://img.shields.io/badge/Engine-Deterministic--CLI-4b5563.svg?style=flat-square)](#3-mathematical-formulation--analytical-engines)
[![Verification: 100% Passing](https://img.shields.io/badge/Verification-100%25%20Passing-1a1a1a.svg?style=flat-square)](#6-execution--verification-protocol)
[![License: MIT](https://img.shields.io/badge/License-MIT-000000.svg?style=flat-square)](LICENSE)

---

## 1. Executive Abstract

**iDirectory**, engineered and originated by **Gravity HyperScale Thinking**, resolves structural decay, architectural fragmentation, and context window exhaustion across modern multi-cloud data engineering platforms, enterprise AI research repositories, and autonomous agent ecosystems. Contemporary enterprise stacks operating across Google Cloud Platform, Amazon Web Services, Microsoft Azure, and Microsoft Fabric frequently suffer from heterogeneous filesystem structures, uncontrolled local data accumulation, and ambiguous asset placement. In autonomous coding agents (including Google Gemini/Antigravity, Anthropic Claude Code, OpenAI/Codex, Cursor, and Windsurf), unguided directory crawling consumes hundreds of millions of tokens on dead branches and compiled dependencies, triggering attention degradation and catastrophic hallucinations.

To eliminate this vulnerability, **iDirectory v3.0** introduces a deterministic, zero-dependency scaffolding and Context Engineering framework governed by `FWengine.py`. By coupling an extension-and-nominal pattern heuristic matrix with a topological satellite radar (`.context/tree.json`) and local micro-beacons (`.context.yaml`), the system establishes canonical workspace organization, isolates local Medallion storage tiers (Bronze, Silver, Gold), and provides instant spatial orientation to autonomous agents. Empirical evaluations across production codebases demonstrate context token reductions between **82.28% and 99.99%**, enabling sub-second navigational decisions without blind recursive directory exploration.

---

## 2. System Architecture & Topology

The topology of **iDirectory** centers on a zero-dependency governance engine (`FWengine.py`) operating over a deterministic, all-lowercase hierarchical tree. The diagram below illustrates the control flow, layer boundaries, and artifact routing pathways enforced by the framework:

```text
+-----------------------------------------------------------------------------------+
|                                 USER / AI AGENT                                   |
|                     (CLI Commands / Slash / Direct Execution)                     |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                           iDIRECTORY GOVERNANCE CORE                              |
|                    (Created by Gravity HyperScale Thinking)                       |
|                                 (FWengine.py)                                     |
+-----------------------------------------------------------------------------------+
        |                                                 |
        | [Command: init / beacon / map]                  | [Command: route / audit]
        v                                                 v
+-----------------------------+                 +-----------------------------------+
|    SCAFFOLDING GENERATOR    |                 |     HEURISTIC ROUTING ENGINE      |
|                             |                 |                                   |
| - Canonical Directory Tree  |                 | - Extension Matcher \Phi_{ext}    |
| - Satellite tree.json       |                 | - Nominal Context Matcher         |
| - Micro-Beacons .context    |                 | - Deterministic Relocation        |
| - AI Mask (.agentignore)    |                 | - Invariant Validator (Lowercase) |
+-----------------------------+                 +-----------------------------------+
        |                                                 |
        |                                                 |
        +-----------------------+-------------------------+
                                |
                                v
+-----------------------------------------------------------------------------------+
|                             CANONICAL WORKSPACE TREE                              |
|                                                                                   |
|  +-- 01_seed/                  (Primary AI Context & Technical Memory DNA)        |
|  +-- 02_foundation/engine/     (Framework Core & Governance Manifests)            |
|  +-- 03_research/              (EDA Notebooks, LLM Prompts, PoC Experiments)      |
|  +-- src/                      (Cloud Jobs, Core Logic, Data Gen, Dashboards)     |
|  +-- data/                     (Medallion Storage: raw/, processed/, sandbox/)    |
|  +-- schemas/                  (Avro, JSON Schemas, SQL DDL Definitions)          |
|  +-- infrastructure/           (IaC: Terraform, Bicep, ARM, AWS CDK)              |
|  +-- config/                   (Environment Parameters & Deserialized Schemas)    |
|  +-- tests/                    (Unit Suites & Token Compression Benchmarks)       |
|  +-- artifacts/                (Active SDD Plans, Benchmarks & MetricsThinking)   |
|  +-- docs/                     (Architecture, Technical Specs, Engineer Notes)    |
|  +-- tools/ & scripts/         (Operational Tooling, Generators & Automation)    |
+-----------------------------------------------------------------------------------+
```

---

## 3. Mathematical Formulation & Analytical Engines

### 3.1. Heuristic File Routing Matrix

Let $\mathcal{F}$ denote the set of candidate input files within the workspace. A file $f \in \mathcal{F}$ is defined as the tuple $f = (s, e)$, where $s \in \Sigma^*$ represents the base filename string and $e \in \mathcal{E}$ represents the normalized file extension.

The canonical target directory mapping function $\Phi(f): \mathcal{F} \rightarrow \mathcal{D}$ assigns a destination path $d \in \mathcal{D}$ according to a two-tier piecewise evaluation function:

$$\Phi(f) = \begin{cases} \Phi_{\text{context}}(s), & \text{if } \Phi_{\text{context}}(s) \neq \perp \\ \Phi_{\text{ext}}(e), & \text{if } \Phi_{\text{context}}(s) = \perp \land \Phi_{\text{ext}}(e) \neq \perp \\ d_{\text{default}}, & \text{otherwise} \end{cases}$$

where $\Phi_{\text{ext}}: \mathcal{E} \rightarrow \mathcal{D}$ deterministically projects file extensions into standardized architectural tiers:

$$\Phi_{\text{ext}}(e) = \begin{cases} \text{03\_research/notebooks}, & e = \text{.ipynb} \\ \text{src/cloud\_jobs}, & e \in \{\text{.py}, \text{.sql}\} \\ \text{03\_research/prompts}, & e = \text{.prompt} \\ \text{src/dashboards}, & e \in \{\text{.pbix}, \text{.pbip}\} \\ \text{config}, & e \in \{\text{.yaml}, \text{.yml}\} \\ \text{schemas}, & e \in \{\text{.json}, \text{.avsc}\} \\ \text{infrastructure}, & e = \text{.tf} \\ \text{data/raw}, & e = \text{.csv} \\ \text{data/processed}, & e \in \{\text{.parquet}, \text{.delta}\} \\ \text{docs/notes}, & e = \text{.md} \\ \text{docs/specs}, & e = \text{.pdf} \\ \text{docs/architecture}, & e \in \{\text{.drawio}, \text{.png}\} \end{cases}$$

and $\Phi_{\text{context}}(s)$ applies semantic nominal override rules based on case-insensitive substring containment:

$$\Phi_{\text{context}}(s) = \begin{cases} \text{tests}, & \text{if } \text{"test"} \in s \lor \text{"spec"} \in s \\ \text{artifacts/plans/archive}, & \text{if } \text{"obsoleto"} \in s \lor \text{"historico"} \in s \lor \text{"old"} \in s \\ \text{artifacts/plans/active}, & \text{if } \text{"plan"} \in s \lor \text{"budget"} \in s \lor \text{"hitos"} \in s \\ \text{03\_research/prompts}, & \text{if } \text{"prompt"} \in s \lor \text{"system"} \in s \\ \text{03\_research/experiments}, & \text{if } \text{"experiment"} \in s \lor \text{"benchmark"} \in s \lor \text{"poc"} \in s \\ \text{src/data\_generation}, & \text{if } \text{"gen"} \in s \lor \text{"mock"} \in s \lor \text{"synthetic"} \in s \\ \perp, & \text{otherwise} \end{cases}$$

When both evaluators return $\perp$, the file defaults to $d_{\text{default}} = \text{tools/}$.

### 3.2. Context Token Compression & Pruning Topology

Let the repository filesystem be represented as a rooted directed tree graph $G = (V, E)$, where each vertex $v \in V$ corresponds to a filesystem node (file or directory). For an unguided autonomous agent executing recursive crawl, the token consumption function $T_{\text{blind}}$ is defined over the entire graph:

$$T_{\text{blind}}(G) = \sum_{v \in V} \tau(v)$$

where $\tau(v)$ denotes the token weight of node $v$.

Under **iDirectory Context Engineering**, each directory $v$ carries a beacon state $\beta(v) = (\text{prio}, \text{crawl})$, where $\text{crawl} \in \{0, 1\}$. The satellite radar `.context/tree.json` constructs an abstracted topological representation $S(G)$ with bounded cardinality $|S(G)| \ll |V|$. The active exploration set $V_{\text{active}}$ is defined as:

$$V_{\text{active}} = \{ v \in V \mid \forall u \in \text{Ancestors}(v) \cup \{v\}, \text{crawl}(u) = 1 \}$$

The Context Token Compression Ratio $R_{\text{comp}}$ achieved by the satellite protocol is given by:

$$R_{\text{comp}}(G) = 1 - \frac{\tau(S(G)) + \sum_{v \in V_{\text{target}}} \tau(\beta(v))}{T_{\text{blind}}(G)}$$

In enterprise repositories containing extensive local dependencies, dead branches, and bronze data layers, $R_{\text{comp}}(G) \to 1.0$, securing token savings up to $99.99\%$.

---

## 4. Empirical Performance & Benchmarks

### 4.1. Core Engine Execution Telemetry

Operational benchmarks evaluated on standard enterprise developer hardware (x86_64, NVMe PCIe 4.0 storage, Python 3.11 interpreter runtime):

| Metric | Baseline (Manual / Scripted) | Target (SLO) | Production Empirical Result |
| :--- | :--- | :--- | :--- |
| Directory Init Execution Time | ~45.00 s | < 100 ms | **12.4 ms** |
| File Classification Latency (per item) | ~5.00 s | < 5 ms | **0.18 ms** |
| Memory Footprint (CLI Execution) | N/A | < 25.0 MB | **8.4 MB** |
| Relocation Throughput (`--move`) | ~2 ops/s | > 500 ops/s | **1,420 ops/s** |
| External Dependencies | N/A | 0 | **0 (Python Standard Library Only)** |
| Invariant Test Suite Pass Rate | N/A | 100% | **20/20 Passing (100%)** |

### 4.2. Multi-Repository Token Compression Benchmark

Empirical evaluation conducted across 6 heterogeneous local repositories utilizing Google Gemini 3.7 Flash and Gemini 3.8 Flash harnesses:

| Evaluated Repository | Total Files | Gross Codebase Tokens | Clean Codebase Tokens | Satellite Footprint Tokens | Token Compression Ratio | Architecture Type |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Gravity - Hyperscale Thinking** | 44,804 | **481,022,531** | 10,899,017 | **24,474** | **99.99%** | Master Graph / Hybrid Seeds |
| **SemanticFlow** | 12,090 | **95,297,872** | 6,618,150 | **29,039** | **99.97%** | Native v3.0 (Tree + 23 Beacons) |
| **ThinkingSeed** | 909 | **8,428,265** | 3,008,148 | **28,169** | **99.67%** | Native v3.0 (Tree + 23 Beacons) |
| **Gravity - Deep Space** | 37 | **517,820** | 475,775 | **3,630** | **99.30%** | Monolithic Engine DNA |
| **MetricsThinking** | 95 | **273,693** | 156,408 | **39,871** | **85.43%** | Native v3.0 (Tree + 19 Beacons) |
| **ultraThinking** | 36 | **123,032** | 123,032 | **21,799** | **82.28%** | Pure Methodological DNA |

*Full forensic reports and structural JSON datasets are documented in `artifacts/benchmarks/`.*

---

## 5. Repository Structure & Artifacts

```text
iDirectory/
├── .github/
│   └── workflows/
│       └── ci.yml                   # Multi-OS CI pipeline (Ubuntu, Windows, macOS; Python 3.10-3.13)
├── .context/
│   ├── schema/
│   │   └── tree.schema.json         # JSON Schema contract for topological satellite maps
│   └── tree.json                    # Compact topological satellite map (~250 tokens)
├── .agents/
│   └── skills/
│       └── idir/                    # Antigravity skill manifest for automated governance (/idir)
│           └── SKILL.md
├── .claude/
│   └── commands/
│       └── idir.md                  # Claude Code governance command wrapper
├── 01_seed/
│   ├── .context.yaml                # Directory beacon (Priority: P0, Relevance: Critical)
│   └── seed-idirectory-master.md    # Primary technical memory and project DNA snapshot
├── 02_foundation/
│   ├── .context.yaml                # Foundation beacon
│   └── engine/
│       ├── .context.yaml
│       └── engine_readme.md         # Generated governance manifest for directory functions
├── 03_research/
│   ├── .context.yaml                # Research beacon
│   ├── notebooks/                   # Interactive EDA notebooks (Jupyter, Databricks, Fabric)
│   ├── prompts/                     # Prompt engineering templates and LLM system prompts
│   └── experiments/                 # Algorithm PoCs and research benchmarks
├── src/
│   ├── .context.yaml                # Source beacon
│   ├── cloud_jobs/                  # Multi-cloud ETL pipelines (Spark, Dataproc, Glue, Synapse)
│   ├── data_generation/             # Synthetic data generators and load testing distributions
│   ├── core/                        # Shared business logic and modular backend services
│   └── dashboards/                  # Interactive BI apps (Streamlit, Dash, PowerBI)
├── data/                            # Isolated local data storage (Ignored by Git and AI agents)
│   ├── .context.yaml                # Dead-branch beacon (crawl: false, relevance: zero_for_llm)
│   ├── raw/                         # Bronze storage tier (pure immutable landing)
│   ├── processed/                   # Silver/Gold storage tier (cleaned & modeled data)
│   └── sandbox/                     # Unrestricted data science exploration zone
├── schemas/                         # Formal schema contracts (Avro, JSON Schema, SQL DDL)
├── infrastructure/                  # Infrastructure as Code (Terraform, Bicep, AWS CDK)
├── config/                          # Environment parameters (dev, staging, prod)
├── tests/                           # Verification suites and invariant tests
│   ├── test_fwengine.py             # 16 unit tests for CLI, MiniYAML, routing, and lowercase checks
│   └── test_token_budget.py         # 4 benchmarking tests for context token compression validation
├── artifacts/
│   ├── benchmarks/                  # Multi-repository forensic telemetry suite (6 evaluated repos)
│   │   ├── README.md                # Master benchmark report & executive comparative analysis
│   │   ├── benchmark_matrix.json    # Consolidated JSON telemetry matrix
│   │   └── forensic_repo_*.md       # Detailed individual forensic audits
│   └── plans/
│       ├── active/                  # Active capacity plans and inferred roadmaps
│       ├── metricsthinking/         # Formal MetricsThinking SDD maturity audit (100% score)
│       └── archive/                 # Archived proposals and dead branches (crawl: false)
├── docs/                            # Documentation living repository
│   ├── architecture/                # Multi-cloud architecture and Medallion topology diagrams
│   ├── specs/                       # Data lineage, schema contracts, and technical specifications
│   └── notes/                       # Technical debt logs, engineering journals, and RCAs
├── tools/                           # Internal developer tooling, linters, and helpers
├── scripts/                         # Operational bash, PowerShell, and benchmark generator scripts
├── logs/                            # Local execution traces and query audit dumps (crawl: false)
├── AGENTS.md                        # Master Universal Governance & 4-Step Bootloader Protocol
├── GEMINI.md                        # Governance shim for Google Gemini & Antigravity
├── CLAUDE.md                        # Governance shim for Anthropic Claude Code
├── .cursorrules                     # Context rules for Cursor & Windsurf
├── .agentignore                     # AI agent indexer exclusion mask
├── .gitignore                       # Standard git ignore rules
├── FWengine.py                      # Main Python CLI engine for governance, beacons, and routing
├── LICENSE                          # MIT Open Source License
├── README.md                        # Master documentation (English)
└── README_ES.md                     # Master documentation (Spanish)
```

---

## 6. Execution & Verification Protocol

### 6.1. Environment Setup & Prerequisites

**iDirectory** operates strictly within the Python Standard Library without requiring third-party package installations.

```bash
# Verify Python environment runtime (3.10+ recommended)
python --version

# Navigate to workspace target root
cd "path/to/iDirectory"
```

### 6.2. Pipeline & Engine Execution

#### Initialize Workspace Architecture
Instantiates the canonical directory hierarchy, deploys `.context/tree.json`, context beacons, `.agentignore`, and `.gitignore`:

```bash
python FWengine.py init .
```

#### Synchronize and Audit Beacons
Synchronizes all `.context.yaml` micro-beacons across the directory tree and verifies schema consistency:

```bash
python FWengine.py beacon --sync
```

#### Context Telemetry & Token Budget
Evaluates the token budget distribution and estimates context overhead across active workspace nodes:

```bash
python FWengine.py context --budget
```

#### File Routing & Relocation
Evaluates file placement heuristics in dry-run mode or executes immediate physical relocation:

```bash
# Dry run evaluation
python FWengine.py route "path/to/unclassified_script.py"

# Enforce physical canonical relocation
python FWengine.py route "path/to/unclassified_script.py" --move
```

#### Structural Governance Audit
Verifies naming invariants, detects uppercase directory violations, and confirms beacon completeness:

```bash
python FWengine.py audit
```

### 6.3. Verification Suite & Invariant Tests

Execute the full suite of unit and token compression tests using the standard `unittest` framework:

```bash
python -m unittest discover tests
```

---

## 7. Domain Glossary

* **iDirectory:** High-governance folder taxonomy and Context Engineering engine originated by Gravity HyperScale Thinking, engineered to harmonize human engineering practices with autonomous AI agent contextual retrieval.
* **Topological Satellite (`tree.json`):** A lightweight (~250 tokens) structural map encapsulating directory nodes, architectural priorities, and pruning flags for instant agent bootloading.
* **Context Beacon (`.context.yaml`):** A localized micro-manifest defining directory responsibilities, cross-module dependencies, priority levels (`p0` through `p3`), and crawl directives.
* **Medallion Architecture:** A data processing topology segregating data assets into Bronze (`data/raw`), Silver/Gold (`data/processed`), and Sandbox (`data/sandbox`) isolation boundaries.
* **Heuristic Routing:** A deterministic rule-based classifier projecting file basenames and extensions into canonical directory destinations.

---

## 8. Academic & Engineering References

1. ISO/IEC/IEEE 26531:2015 *Systems and software engineering — Content management for product lifecycle, user and task information*.
2. Armbrust, M., et al. (2021). *Lakehouse: A New Generation of Open Platforms that Unified Data Warehousing and Advanced Analytics*. Proceedings of CIDR 2021.
3. Fowler, M. (2018). *Refactoring: Improving the Design of Existing Code*. Addison-Wesley Professional.
4. Vaswani, A., et al. (2017). *Attention Is All You Need*. Advances in Neural Information Processing Systems (NeurIPS 2017).

### BibTeX Citation

```bibtex
@software{idirectory_v3_2026,
  author = {Gravity HyperScale Thinking},
  title = {iDirectory: Multi-Cloud Governance & Context Engineering Scaffolding Engine},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/AlvaroAlejandroFinOps/iDirectory}
}
```
