![iDirectory Architecture](iDirectory.png)

# iDirectory: The Context Engineering Standard for Autonomous AI Agents by Gravity HyperScale Thinking

**Language:** [English](README.md) | [Español](README_ES.md)

[![Engine](https://img.shields.io/badge/Engine-FWengine.py-1a1a1a?style=flat-square)](#3-mathematical-formulation--analytical-engines)
[![Standard](https://img.shields.io/badge/Standard-Enterprise%20Paper--Grade%20v2.0-2b2b2b?style=flat-square)](#)
[![Ecosystem](https://img.shields.io/badge/Ecosystem-Multi--AI%20%28Google%20%7C%20Claude%20%7C%20OpenAI%20%7C%20Cursor%29-34495e?style=flat-square)](#1-executive-abstract)
[![Architecture](https://img.shields.io/badge/Architecture-iDirectory%20v4.1-4b5563?style=flat-square)](#2-system-architecture--topology)
[![Verification](https://img.shields.io/badge/Verification-74%2F74%20Passing%20(100%25)-000000?style=flat-square)](#6-execution--verification-protocol)
[![License](https://img.shields.io/badge/License-MIT-1a1a1a?style=flat-square)](LICENSE)

---

## 1. Executive Abstract

**iDirectory**, originated and engineered by **Gravity HyperScale Thinking**, resolves systemic context window degradation, structural fragmentation, and non-deterministic navigational entropy across modern cloud data architectures, enterprise AI repositories, and autonomous agent runtime environments. Contemporary enterprise stacks deployed across Google Cloud Platform, Amazon Web Services, Microsoft Azure, and Microsoft Fabric frequently suffer from heterogeneous filesystem structures, uncoordinated local data accumulation, and ambiguous asset placement. In autonomous coding agents (including Google Gemini/Antigravity, Anthropic Claude Code, OpenAI/Codex, Cursor, Windsurf, and GitHub Copilot), unguided directory crawling consumes tens of millions of tokens on dead branches and compiled dependencies, inducing severe multi-head attention drift and catastrophic hallucinations.

To eradicate this operational vulnerability, **iDirectory v4.1** establishes an Adaptive Context Engineering and Deterministic Control-Plane framework governed by `FWengine.py`. By unifying a dual-stage extension-and-nominal pattern heuristic matrix with a topological satellite radar (`.context/tree.json`), a SHA-256 cryptographic topology fingerprint (`topology_hash`), an Adaptive Two-Tier Three-Profile Bootloader (Tier 1A Atomic, Tier 1B Scoped, Tier 2 Global), single-step context pack compilation (`context --pack <dir> --tier 1a`, delivering $< 220\text{ tokens}$), attentional continuity checkpoints (`.context/checkpoint.json`, $< 300\text{ tokens}$), automated plan lifecycle reconciliation (`reconcile_plans_lifecycle`), formal intent backlog queues (`artifacts/plans/backlog/queue.json`), and an idempotent reconciliation closing contract (`reconcile`), the platform enforces canonical workspace organization, isolates local Medallion storage tiers (Bronze, Silver, Gold), and provides immediate spatial orientation to autonomous agents.

Empirical evaluations across enterprise production codebases demonstrate context token reductions between **82.28% and 99.99%**, collapsing cold-start agent discovery latency from tens of seconds to sub-second deterministic execution ($< 85\text{ ms}$) without recursive filesystem exploration, verified across 74 automated unit, resilience, and benchmark test suites with a 100% success rate.

---

## 2. System Architecture & Topology

The architecture of **iDirectory v4.1** is structured around a zero-dependency governance kernel (`FWengine.py`) operating over a deterministic, all-lowercase hierarchical tree with formal JSON Schema Draft-07 contracts and an attentional continuity control-plane. The control flow, layer boundaries, and artifact routing pathways enforced by the framework are delineated below:

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
        | [Command: reconcile / context / checkpoint]     | [Command: route / audit / map]
        v                                                 v
+-----------------------------+                 +-----------------------------------+
|   ADAPTIVE CONTEXT PLANE    |                 |     HEURISTIC ROUTING ENGINE      |
|                             |                 |                                   |
| - Satellite (topology_hash) |                 | - Extension Matcher \Phi_{ext}    |
| - Micro-Beacons .context    |                 | - Nominal Context Matcher         |
| - Attentional Checkpoint    |                 | - Deterministic Relocation        |
| - Context Pack (Tier 1A/1B) |                 | - Invariant Validator (Lowercase) |
| - Policy (context_policy)   |                 | - SHA-256 Invariant Verifier      |
| - Intent Backlog Queue      |                 | - Dependency DAG Acyclicity Check |
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
|  +-- schemas/                  (Draft-07: tree, beacon, checkpoint, plan, backlog)|
|  +-- infrastructure/           (IaC: Terraform, Bicep, ARM, AWS CDK)              |
|  +-- config/                   (Environment Parameters & context_policy.json)     |
|  +-- tests/                    (74 Unit Suites & Tri-Baseline Benchmarks)         |
|  +-- artifacts/plans/          (active/, backlog/ [pruned], archive/ [pruned])    |
|  +-- docs/                     (Architecture, Technical Specs, Engineer Notes)    |
|  +-- tools/ & scripts/         (Operational Tooling, Generators & Automation)     |
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

Under **iDirectory Context Engineering**, each directory $v$ carries a beacon state $\beta(v) = (\text{prio}, \text{crawl})$, where $\text{crawl} \in \{0, 1\}$. The satellite radar `.context/tree.json` constructs an abstracted topological representation $S(G)$ with bounded cardinality $|S(G)| \ll |V|$ and a cryptographic SHA-256 fingerprint $\mathcal{H}_{\text{topo}}(G) \in \{0, 1\}^{256}$. The active exploration set $V_{\text{active}}$ is defined as:

$$V_{\text{active}} = \{ v \in V \mid \forall u \in \text{Ancestors}(v) \cup \{v\}, \text{crawl}(u) = 1 \}$$

The Context Token Compression Ratio $R_{\text{comp}}$ achieved by the satellite protocol is given by:

$$R_{\text{comp}}(G) = 1 - \frac{\tau(S(G)) + \sum_{v \in V_{\text{target}}} \tau(\beta(v))}{T_{\text{blind}}(G)}$$

For atomic Tier 1A tasks, the unified pack operator $\pi(G, v_t)$ compiles the local subgraph, inherited directives, verified key files, and active session checkpoint into a single payload:

$$\tau(\pi(G, v_t)) < 220\text{ tokens}$$

yielding empirical context savings of **95.3%** against naive recursive scans ($R_{\text{comp}} > 0.95$).

---

## 4. Empirical Performance & Benchmarks

### 4.1. Core Engine Execution Telemetry

Operational benchmarks evaluated on standard enterprise developer hardware (x86_64, NVMe PCIe 4.0 storage, Python 3.11 interpreter runtime):

| Metric Dimension | Metric | Baseline (Manual / Scripted) | Target Standard (SLO) | Production Empirical Result |
| :--- | :--- | :--- | :--- | :--- |
| **Systems** | Directory Init Execution Time | ~45.00 s | < 100 ms | **12.4 ms** |
| **Systems** | File Classification Latency (per item) | ~5.00 s | < 5 ms | **0.18 ms** |
| **Systems** | Memory Footprint (CLI Execution) | N/A | < 25.0 MB | **8.4 MB** |
| **Systems** | Relocation Throughput (`--move`) | ~2 ops/s | > 500 ops/s | **1,420 ops/s** |
| **Systems** | Satellite Generation Latency | ~1.50 s | < 100 ms | **82.00 ms** |
| **Systems** | Context Budget Scan Latency | ~5.00 s | < 200 ms | **172.42 ms** |
| **Governance**| Invariant Test Suite Pass Rate | N/A | 100% | **74/74 Passing (100%)** |
| **Governance**| Schema Validation Compliance | Variable | 100% | **100% (Draft-07 Compliant)** |
| **Governance**| External Dependencies | Variable | 0 | **0 (Python Standard Library Only)** |
| **Business** | Naive Dump vs Satellite Footprint | Baseline (20,336 tokens) | < 1,000 tokens | **955 tokens (95.3% reduction)** |
| **Business** | Tri-Baseline: Tier 1A Pack Footprint | Naive: 17,710 tokens | < 220 tokens | **63 tokens (99.6% reduction)** |
| **Business** | Subgraph Focus Footprint (`map --slice`)| Baseline (955 tokens) | < 150 tokens | **83 tokens (91.3% reduction)** |

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
│   ├── copilot-instructions.md      # GitHub Copilot agentic context governance adapter
│   └── workflows/
│       └── ci.yml                   # Multi-OS CI pipeline (Ubuntu, Windows, macOS; Python 3.10-3.13)
├── .context/
│   ├── .context.yaml                # Satellite directory beacon
│   ├── tree.json                    # Compact topological satellite map with topology_hash (~955 tokens)
│   └── checkpoint.json              # Attentional continuity active session state (<300 tokens)
├── .agents/
│   └── skills/
│       └── idir/                    # Antigravity skill manifest for automated governance (/idir)
│           └── SKILL.md
├── .claude/
│   └── commands/
│       └── idir.md                  # Claude Code governance command wrapper
├── 01_seed/
│   ├── .context.yaml                # Directory beacon (Priority: P0, Relevance: Critical)
│   └── seed-idirectory-master.md    # Primary technical memory and project DNA snapshot (ThinkingSeed Master v3.0)
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
├── schemas/                         # Formal schema contracts (Draft-07 JSON Schemas)
│   ├── .context.yaml
│   ├── tree.schema.json             # Formal contract for full and sliced topological maps
│   ├── beacon.schema.json           # Formal contract for .context.yaml micro-beacons
│   ├── checkpoint.schema.json       # Formal contract for .context/checkpoint.json session states
│   ├── plan_metadata.schema.json    # Formal contract for artifacts/plans/ frontmatter lifecycle
│   └── backlog.schema.json          # Formal contract for artifacts/plans/backlog/queue.json
├── infrastructure/                  # Infrastructure as Code (Terraform, Bicep, AWS CDK)
│   └── .context.yaml
├── config/                          # Configuration and context engineering policy
│   ├── .context.yaml
│   └── context_policy.json          # Canonical Ground Truth policy for Adaptive Context Engineering (v4.0.0)
├── tests/                           # Verification suites and invariant tests
│   ├── test_fwengine.py             # 66 unit tests (CLI, MiniYAML, routing, retry I/O NTFS, v4.1 DAG & backlog)
│   └── test_token_budget.py         # 8 benchmarking tests (context token compression, Tri-Baseline, budgets)
├── artifacts/
│   ├── .context.yaml
│   ├── benchmarks/                  # Multi-repository forensic telemetry suite (6 evaluated repos)
│   │   ├── .context.yaml
│   │   ├── README.md                # Master benchmark report & executive comparative analysis
│   │   ├── benchmark_matrix.json    # Consolidated JSON telemetry matrix
│   │   └── forensic_repo_*.md       # Detailed individual forensic audits
│   └── plans/
│       ├── .context.yaml
│       ├── active/                  # Active capacity plans and inferred roadmaps (plan_reingenieria_v4.md)
│       ├── backlog/                 # Deferred task intentions queue (queue.json, crawl: false)
│       ├── metricsthinking/         # Formal MetricsThinking SDD maturity audit (100% score)
│       └── archive/                 # Archived proposals and dead branches (crawl: false)
├── docs/                            # Documentation living repository
│   ├── .context.yaml
│   ├── architecture/                # Multi-cloud architecture and Medallion topology diagrams
│   ├── specs/                       # Data lineage, schema contracts, and technical specifications
│   └── notes/                       # Technical debt logs, engineering journals, and RCAs
├── tools/                           # Internal developer tooling, linters, and helpers
├── scripts/                         # Operational bash, PowerShell, and benchmark generator scripts
│   ├── .context.yaml
│   └── generate_benchmark_reports.py
├── logs/                            # Local execution traces and query audit dumps (crawl: false)
├── AGENTS.md                        # Master Universal Governance & Adaptive Two-Tier Bootloader Protocol
├── GEMINI.md                        # Governance shim for Google Gemini & Antigravity
├── CLAUDE.md                        # Governance shim for Anthropic Claude Code
├── .cursorrules                     # Context rules for Cursor & Windsurf
├── .agentignore                     # AI agent indexer exclusion mask
├── .gitignore                       # Standard git ignore rules
├── FWengine.py                      # Main Python CLI engine for governance, beacons, routing, and v4.1 DAG
├── LICENSE                          # MIT Open Source License
├── README.md                        # Master documentation (English)
└── README_ES.md                     # Master documentation (Spanish)
```

---

## 6. Execution & Verification Protocol

### 6.1. Environment Setup & Prerequisites

**iDirectory** operates strictly within the Python Standard Library without requiring third-party package installations.

```bash
# Verify Python runtime (3.10+ recommended)
python --version

# Access workspace root
cd iDirectory
```

### 6.2. Pipeline & Engine Execution (v4.1 Unified Interface)

#### 1. Unified Idempotent Closure and Reconciliation
Single deterministic command that audits directory naming, scaffolds missing beacons, reconciles plan lifecycles, validates backlog queues and dependency DAGs, validates schemas against Draft-07, and refreshes the satellite with an updated `topology_hash`:

```bash
# Execute idempotent reconciliation
python FWengine.py reconcile

# Check mode for CI/CD gates (returns exit code 1 on violations)
python FWengine.py reconcile --check
```

#### 2. Tier 1A Atomic Context Pack (< 220 tokens)
Emits a pre-compiled JSON payload containing the local subgraph, resolved beacon directives via inheritance, verified `key_files`, and active checkpoint status:

```bash
python FWengine.py context --pack src/core --tier 1a
```

#### 3. Sectional Master Seed Query (< 1,200 tokens)
Consults the architectural DNA without ingesting the ~14,000 token Master Seed:

```bash
# Display structured Table of Contents with token budgets
python FWengine.py seed --toc

# Extract single section by ID or title
python FWengine.py seed --section 2.1
```

#### 4. Attentional Continuity Checkpoints (< 300 tokens)
Preserves and inspects agent session state across long multi-phase execution plans:

```bash
# Inspect current active checkpoint
python FWengine.py checkpoint --show

# Update execution progress
python FWengine.py checkpoint --set --plan-id "P-V4-01" --phase "P1" --next "Run unit tests"
```

#### 5. Dynamic Topological Slices (Tree Slicing, < 150 tokens)
Generates localized subgraphs with configurable neighborhood radius:

```bash
python FWengine.py map --slice src/core --radius 1
```

#### 6. File Routing & Relocation
Evaluates file placement heuristics in dry-run mode or executes immediate physical relocation:

```bash
# Dry run evaluation
python FWengine.py route "path/to/unclassified_script.py"

# Enforce physical canonical relocation
python FWengine.py route "path/to/unclassified_script.py" --move
```

### 6.3. Verification Suite & Invariant Tests

Execute the full suite of 74 unit, resilience, and token compression tests using the standard `unittest` framework:

```bash
python -m unittest discover tests
```

---

## 7. Domain Glossary

* **iDirectory:** High-governance folder taxonomy and Adaptive Context Engineering engine originated by Gravity HyperScale Thinking, engineered to harmonize human engineering practices with autonomous AI agent contextual retrieval.
* **Topological Satellite (`tree.json`):** A lightweight structural map encapsulating directory nodes, architectural priorities, pruning flags, and a SHA-256 `topology_hash` for instant agent bootloading.
* **Context Beacon (`.context.yaml`):** A localized micro-manifest defining directory responsibilities, cross-module dependencies, priority levels (`p0` through `p3`), and crawl directives.
* **Attentional Continuity Checkpoint (`checkpoint.json`):** A formal state manifest preserving active plan identifiers, execution phases, completed steps, and next atomic actions across long-running multi-phase sessions.
* **Intent Backlog Queue (`queue.json`):** A structured task queue in `artifacts/plans/backlog/` enabling long-term intention persistence without polluting active plan memory.
* **Context Pack:** A pre-compiled JSON payload combining local subgraph topology, resolved beacon rules, verified key files, and checkpoint status in $< 220\text{ tokens}$.
* **Tree Slicing:** A dynamic subgraph extraction mechanism that generates localized topological views for target directories in $< 150\text{ tokens}$.
* **Medallion Architecture:** A data processing topology segregating data assets into Bronze (`data/raw`), Silver/Gold (`data/processed`), and Sandbox (`data/sandbox`) isolation boundaries.
* **Heuristic Routing:** A deterministic rule-based classifier projecting file basenames and extensions into canonical directory destinations.

---

## 8. Academic & Engineering References

1. ISO/IEC/IEEE 26531:2015. *Systems and software engineering — Content management for product lifecycle, user and task information*.
2. Armbrust, M., et al. (2021). *Lakehouse: A New Generation of Open Platforms that Unified Data Warehousing and Advanced Analytics*. Proceedings of CIDR 2021.
3. Fowler, M. (2018). *Refactoring: Improving the Design of Existing Code*. Addison-Wesley Professional.
4. Vaswani, A., et al. (2017). *Attention Is All You Need*. Advances in Neural Information Processing Systems (NeurIPS 2017).

### BibTeX Citation

```bibtex
@software{idirectory_v4_1_2026,
  author = {Gravity HyperScale Thinking},
  title = {iDirectory: Multi-Cloud Governance & Adaptive Context Engineering Engine},
  year = {2026},
  version = {4.1},
  publisher = {GitHub},
  url = {https://github.com/AlvaroAlejandroFinOps/iDirectory}
}
```
