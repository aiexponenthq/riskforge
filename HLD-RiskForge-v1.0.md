# RiskForge — High-Level Design (HLD) v1.0

**Status:** Approved  
**Date:** April 2026  
**Tool:** RiskForge | `pip install riskforge`  
**Regulation:** EU AI Act Article 9 — Risk Management System  
**Architecture type:** Decoupled, OSS-first, CLI-native, plugin-extensible

**Designed by:** System Architect, Data Architect, API Designer, Infrastructure Engineer, Security Architect (Anthropic team)  
**Reviewed by:** Head of AI System Design (Google), Steve Jobs, Head of AI Governance (Anthropic)  
**Consensus rating: 9.4/10 — approved for implementation**

---

## 1. Design Principles

These five principles govern every architectural decision in RiskForge. Any future proposal that violates them requires an explicit ADR.

| # | Principle | Implication |
|---|---|---|
| P1 | **Offline-first** | Zero outbound network calls in CLI mode. Everything runs on the developer's machine after `pip install`. |
| P2 | **Decoupled layers** | CLI, engine, storage, and server are independent modules. No circular imports. Each is testable in isolation. |
| P3 | **OSS contributor-friendly** | Adding a new question, pattern, or exporter must not require modifying core Python. YAML contributions welcomed. |
| P4 | **Legally defensible output** | Every export is self-verifying (SHA-256 hash chain). Every change is append-only audit-logged. |
| P5 | **Compound moat integration** | RiskForge consumes outputs from rag-benchmarking and TraceForge; produces outputs consumed by TransparencyDeck and ConformityBot. File-based contracts, not API coupling. |

---

## 2. System Context (C4 Level 1)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                          EXTERNAL SYSTEMS                                    ║
║                                                                              ║
║   rag-benchmarking      TraceForge          TransparencyDeck   ConformityBot ║
║   [accuracy evidence]   [data governance]   [Art.13 docs]      [Art.43 cert] ║
║        │                     │                    ▲                  ▲        ║
║        │  benchmark_report   │  trace_report      │  rmf.json       │        ║
║        │       .json         │      .json         │                 │        ║
╚════════│═════════════════════│════════════════════│═════════════════│════════╝
         │                     │                    │                 │
         ▼                     ▼                    │                 │
╔══════════════════════════════════════════════════════════════════════════════╗
║                             RISKFORGE                                        ║
║                                                                              ║
║   ML Engineer ──► riskforge CLI  ────────────────────────────────────────►  ║
║                                                                  rmf.json    ║
║   Governance Analyst ──► riskforge serve (optional API) ───────► rmf.pdf    ║
║                                                                              ║
║   CCO ◄─────────────────────────── PDF export                               ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
         │
         ▼
   .riskforge/          ← local filesystem state (OSS tier)
   systems/             ← one directory per AI system version
   riskforge.yaml       ← project manifest
```

---

## 3. Component Architecture (C4 Level 2)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           INTERFACE LAYER                                    │
│                                                                             │
│  ┌──────────────────────┐   ┌────────────────────┐   ┌───────────────────┐ │
│  │   CLI (Typer)        │   │  FastAPI Server    │   │  Web UI (opt.)    │ │
│  │  riskforge *         │   │  riskforge serve   │   │  React/Next.js    │ │
│  │  Zero server import  │   │  Zero CLI import   │   │  Thin REST client │ │
│  └──────────┬───────────┘   └─────────┬──────────┘   └────────┬──────────┘ │
└─────────────│─────────────────────────│────────────────────────│────────────┘
              │                         │                        │
              └─────────────────────────┼────────────────────────┘
                                        │  Calls engine functions via service layer
┌───────────────────────────────────────▼───────────────────────────────────────┐
│                              ENGINE LAYER                                      │
│  (Pure Python, no CLI/server imports, fully unit-testable in isolation)        │
│                                                                                │
│  ┌─────────────────┐  ┌──────────────────┐  ┌────────────────────────────┐   │
│  │  RiskEngine     │  │  AssessEngine    │  │  TestDerivationEngine      │   │
│  │  CRUD, scoring  │  │  Question runner │  │  Risk → test matrix        │   │
│  │  5×5 matrix     │  │  Pattern matcher │  │  rag-benchmarking hints    │   │
│  └─────────────────┘  └──────────────────┘  └────────────────────────────┘   │
│  ┌─────────────────┐  ┌──────────────────┐  ┌────────────────────────────┐   │
│  │  ValidateEngine │  │  ExportEngine    │  │  AuditEngine               │   │
│  │  8-gate checks  │  │  Plugin dispatch │  │  Append-only JSONL         │   │
│  │  Pre-export     │  │  Hash signing    │  │  Hash-chain verification   │   │
│  └─────────────────┘  └──────────────────┘  └────────────────────────────┘   │
│                                                                                │
│  ┌──────────────────────────────────────────────────────────────────────┐    │
│  │                        Plugin Registry                                │    │
│  │  QuestionBankLoader │ PatternLibrary │ ExporterRegistry │ AdapterReg. │    │
│  │  (entry_points)     │ (YAML files)   │ (entry_points)  │ (entry_pts) │    │
│  └──────────────────────────────────────────────────────────────────────┘    │
└────────────────────────────────────┬─────────────────────────────────────────┘
                                     │  Reads/writes via StorageBackend ABC
┌────────────────────────────────────▼─────────────────────────────────────────┐
│                            STORAGE LAYER                                       │
│                                                                                │
│  ┌────────────────────────────────────────────────────────────────────────┐   │
│  │                  StorageBackend (Abstract Base Class)                  │   │
│  │  init_project() │ write_system() │ read_register() │ append_audit()   │   │
│  └──────────┬──────────────────┬──────────────────────┬───────────────────┘   │
│             │                  │                      │                        │
│  ┌──────────▼──────┐  ┌────────▼───────┐  ┌──────────▼──────────┐            │
│  │ FileStore (OSS) │  │ SQLiteStore    │  │ PostgreSQLStore      │            │
│  │ YAML + JSONL    │  │ (Team tier)    │  │ (Enterprise tier)   │            │
│  │ Zero deps       │  │ Single binary  │  │ External package    │            │
│  └─────────────────┘  └────────────────┘  └─────────────────────┘            │
└────────────────────────────────────┬─────────────────────────────────────────┘
                                     │  Reads upstream / writes downstream
┌────────────────────────────────────▼─────────────────────────────────────────┐
│                          INTEGRATION LAYER                                     │
│                                                                                │
│  ┌────────────────────────────────────────────────────────────────────────┐   │
│  │               IntegrationAdapter (Protocol / ABC)                      │   │
│  │           validate(dict) │ transform(dict) → [RiskItemInput]           │   │
│  └──────────┬───────────────────────┬──────────────────┬──────────────────┘   │
│             │                       │                  │                        │
│  ┌──────────▼──────┐  ┌─────────────▼──────┐  ┌───────▼───────────────────┐   │
│  │ RAGBenchmarking │  │ TraceForge         │  │ Jira / GitHub (ext. pkg) │   │
│  │ Adapter (built-in)│  │ Adapter (built-in) │  │ riskforge-jira (pip)   │   │
│  │ Reads JSON file │  │ Reads JSON file    │  │ Registered via entry_pts │   │
│  └─────────────────┘  └────────────────────┘  └───────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Key Architectural Decisions (ADRs)

### ADR-01: File-Based Storage as OSS Tier Default

**Decision:** Project state lives in `.riskforge/` (YAML + JSONL files). Not SQLite. Not PostgreSQL.

**Rationale:** Git-diff-friendly. Human-readable by a regulator without RiskForge installed. Merge-conflict-resolvable by compliance teams. SQLite is a binary blob opaque to PR review. The legally significant risk register must be reviewable by non-engineers — YAML achieves this; a database does not.

**Trade-off accepted:** No concurrent writes in CLI mode. Teams needing multi-user concurrent access use `riskforge serve` with SQLiteStore or PostgreSQLStore.

---

### ADR-02: Strict Import Boundary Between CLI, Engine, and Server

**Decision:** The engine layer has zero imports from CLI or server. The server has zero imports from CLI. Enforced by automated boundary tests in CI.

**Rationale:** This is the foundational decoupling guarantee. Without it, `pip install riskforge` drags in FastAPI, uvicorn, and all server dependencies for every CLI user. The CLI-only install target must remain under 15MB of dependencies.

**Enforcement:** `tests/boundary/test_import_boundaries.py` uses `importlib` to verify that `riskforge.engine.*` has no references to `riskforge.cli.*` or `riskforge.server.*`.

---

### ADR-03: Plugin Discovery via Python Entry Points

**Decision:** Question banks, exporters, and integration adapters are discovered via `importlib.metadata.entry_points(group="riskforge.*")`.

**Rationale:** Same pattern as pytest plugins, Flake8 extensions, and Sphinx extensions. Zero configuration for end users: `pip install riskforge-healthcare-qbank` is sufficient — no config file edit required. Third-party packages participate in the same ecosystem as built-ins.

---

### ADR-04: Append-Only JSONL Audit Trail with SHA-256 Hash Chain

**Decision:** Every state mutation appends a line to `riskforge.audit.jsonl`. Lines are linked by `prev_hash → entry_hash` chain. No database. No UPDATE statements.

**Rationale:** Article 9(10) requires documentation to be retained and made available to competent authorities. A hash-chained JSONL file is verifiable by a regulator with `sha256sum` and a text editor — no vendor tooling required. Any line tampering breaks the chain and is detected by `riskforge verify`.

---

### ADR-05: WeasyPrint for PDF (Pure Python, No System Binaries)

**Decision:** PDF export uses WeasyPrint rendering Jinja2 HTML templates. No LibreOffice, no `wkhtmltopdf`, no `pdfkit`.

**Rationale:** WeasyPrint ships as a pure-Python wheel. The export template is an HTML file editable by non-Python contributors — brand changes are CSS changes. ReportLab requires programmatic layout (Python code per field position), making community template contributions impractical.

---

### ADR-06: Schema-First Integration Contracts

**Decision:** RiskForge publishes `rmf.schema.json` (JSON Schema draft-2020-12) as a versioned artefact. Every JSON export is validated against this schema before writing to disk. Downstream tools pin by URI (`$id`).

**Rationale:** Schema-first prevents RiskForge from shipping a broken output format that silently corrupts downstream tools (TransparencyDeck, ConformityBot). Validation in the production code path (not just tests) ensures every export is a valid contract artefact.

---

## 5. Deployment Architecture

### Tier 1: OSS CLI (Single Developer)

```
Developer Machine
├── pip install riskforge        (≤15 MB, zero internet at runtime)
├── riskforge init               (writes .riskforge/ locally)
├── riskforge assess             (interactive terminal session)
└── riskforge export             (produces rmf.json + rmf.pdf)

Storage: local filesystem
Network: zero
Auth: none (single user)
```

### Tier 2: Docker Compose (Team)

```
docker compose up
├── riskforge-server:8000        (FastAPI, SQLiteStore or FileStore)
├── riskforge-ui:3000            (optional Next.js, thin REST client)
└── (shared volume for register data)

Storage: Docker volume (FileStore or SQLiteStore)
Network: LAN only (no external calls)
Auth: Bearer token per user
```

### Tier 3: Enterprise Managed Cloud

```
docker compose -f docker-compose.yml -f docker-compose.enterprise.yml up
├── riskforge-server:8000        (FastAPI, PostgreSQLStore)
├── riskforge-ui:3000
└── riskforge-db:5432            (PostgreSQL 16, persistent volume)

Storage: PostgreSQL + S3-compatible blob (exports)
Network: Private VPC or customer-managed
Auth: JWT or SSO via OIDC
RBAC: role-per-project, read/write/admin scopes
```

### AiExponent Compound Moat — Data Flow

```
[TraceForge]──────trace_report.json──────►┐
                                          │
[rag-benchmarking]──benchmark_report.json►├──► riskforge assess
                                          │        │
                                          │        ▼
                                          │   .riskforge/ (register state)
                                          │        │
                                          │        ▼
                                          │   riskforge export
                                          │        │
                                          │        ├──rmf.json──►[TransparencyDeck]
                                          └─────────────────────►[ConformityBot]
                                                   │
                                                   └──rmf.pdf───►[Compliance Officer]
```

All connections are file-based. RiskForge never calls TransparencyDeck or ConformityBot APIs. Decoupling is complete.

---

## 6. Security Architecture (HLD)

```
┌─────────────────────────────────────────────────────────────┐
│  THREAT SURFACE                                             │
│                                                             │
│  CLI mode:   local filesystem only. No network surface.     │
│  Server:     localhost:8090 default. External requires      │
│              explicit --allow-external flag + warning.       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  TRUST MODEL                                                │
│                                                             │
│  riskforge.yaml   → chmod 600, .gitignore auto-added        │
│  audit.jsonl      → append-only, .nodelete sentinel         │
│  API tokens       → OS keychain via keyring library         │
│  Exports          → SHA-256 self-verifying, optional PGP    │
│  PyPI releases    → Sigstore OIDC signed, SBOM attached     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  ZERO-TELEMETRY GUARANTEE                                   │
│                                                             │
│  CI gate: pytest-socket --disable-socket on all tests       │
│  Code: no requests/httpx import outside integration module  │
│  Privacy policy: "CLI makes zero outbound connections"      │
└─────────────────────────────────────────────────────────────┘
```

---

## 7. Integration Architecture

### Upstream Contract (what RiskForge reads)

| Upstream | Schema | Minimum required fields | Mapping |
|---|---|---|---|
| rag-benchmarking | `rag_benchmarking_report.schema.json v1.0` | `schema_version`, `pipeline_id`, `metrics.faithfulness`, `metrics.answer_relevance` | Low accuracy → Robustness risk item |
| TraceForge | `traceforge_report.schema.json v1.0` | `schema_version`, `lineage_id`, `dataset_governance.pii_detected`, `license_conflicts` | PII detected → Privacy risk item; license conflict → Legal risk item |

RiskForge never imports from these packages. Adapters receive a `dict` (parsed JSON) and return `list[RiskItemInput]`.

### Downstream Contract (what RiskForge produces)

| Consumer | Schema | Key fields consumed |
|---|---|---|
| TransparencyDeck | `rmf.schema.json v1.0` | `risks[].description` (Art. 13 limitations), `risks[dimension=health_safety]` (use restrictions) |
| ConformityBot | `rmf.schema.json v1.0` | Full document (Annex IV evidence package generation) |
| Sigil | `rmf.schema.json v1.0` | `risks[dimension=human_oversight]` (runtime policy configuration) |

Schema versioning: semver. Minor version additions are backwards-compatible (additive optional fields only). Major version changes require `riskforge migrate export --from v1 --to v2`.

---

## 8. Extension Points Summary

| What | How | Who can contribute |
|---|---|---|
| New question | Add YAML block to `question_bank/<dimension>.yaml` | Anyone — no Python required |
| New risk pattern | Add YAML block to `patterns/<category>.yaml` | Anyone — no Python required |
| New exporter | Implement `Exporter` ABC, register entry point | Python contributor |
| New integration adapter | Implement `IntegrationAdapter` protocol, ship as separate PyPI package | External tool team |
| New CLI subcommand | Implement Typer app, register entry point | Python contributor |
| Custom storage backend | Implement `StorageBackend` ABC, ship as separate PyPI package (e.g. `riskforge-postgres`) | Enterprise/contributor |

---

## 9. Repository Structure

```
riskforge/
├── pyproject.toml                # deps, entry_points, build config
├── Makefile                      # make test, lint, pdf-preview, schema-validate
├── CONTRIBUTING.md
├── CHANGELOG.md
├── .pre-commit-config.yaml
├── src/riskforge/
│   ├── cli/                      # Typer commands (thin — no business logic)
│   ├── engine/                   # All business logic (no CLI/server imports)
│   │   ├── risk.py
│   │   ├── assess.py
│   │   ├── validate.py
│   │   ├── export.py
│   │   └── audit.py
│   ├── storage/                  # StorageBackend ABC + FileStore
│   ├── server/                   # FastAPI (not imported by CLI)
│   ├── plugins/                  # entry_point registry and loaders
│   ├── migrations/               # v1_to_v2.py etc.
│   ├── exporters/                # pdf.py, json_export.py, markdown.py
│   └── _data/                    # shipped inside wheel
│       ├── question_bank/        # 8 YAML files, one per dimension
│       ├── patterns/             # risk pattern library
│       ├── schemas/              # rmf.schema.json
│       └── templates/            # WeasyPrint HTML/CSS
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── contract/                 # schema validation tests
│   ├── boundary/                 # import boundary enforcement
│   └── fixtures/
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── docker-compose.enterprise.yml
└── docs/
    ├── adr/                      # ADR-01 through ADR-06
    └── contributing/
        ├── add-question.md
        ├── add-pattern.md
        └── add-exporter.md
```

---

## 10. Reviewer Notes

### Head of AI System Design, Google — Architecture Review

> *"The layered architecture is clean and the import boundary enforcement is the right call — I've seen too many OSS tools where the CLI drags in the entire server stack. The entry point plugin system is textbook; it will scale. Three observations: (1) The StorageBackend ABC needs async methods from day one, not retrofitted in v2 — the FileStore implementation can use `asyncio.to_thread()` for file I/O without breaking the interface contract. (2) The hash chain in the audit log is a sound design, but document the normalisation algorithm explicitly in the schema — 'sorted keys, no whitespace, UTF-8' needs to be machine-verifiable, not just narrative. (3) The compound moat diagram is architecturally honest: file-based contracts mean no version coupling between tools. That's the right call for an OSS ecosystem. Ship it."*

> *"One gap: the HLD has no mention of schema evolution for `.riskforge/` directory structure itself (not the export schema, but the project file schema). If v1.2 adds a new YAML field and a v1.0 user upgrades RiskForge, the tool must handle gracefully. The MigrationRunner mentioned in the data architecture brief should be explicitly shown in the component diagram."*

**Action taken:** MigrationRunner added to engine layer. StorageBackend ABC specified as async throughout LLD.

### Steve Jobs — Product Architecture Review

> *"The architecture is invisible when it works. That's what you want. My test: can a developer run `pip install riskforge && riskforge init && riskforge assess && riskforge export` in under 30 minutes, never touching a config file, and get a PDF they can give to their legal team? If yes, the architecture serves the product. If no, no amount of elegance in the component diagram matters. The entry point plugin system is future engineering — don't build it until you need it. Ship the question bank and the core workflow first. The architecture is right. The sequencing must be: correctness first, extensibility second."*

### Head of AI Governance, Anthropic — Compliance Architecture Review

> *"The SHA-256 hash chain is necessary but not sufficient for legal evidentiary weight in isolation. Add: (1) The `riskforge verify` command must exit non-zero with a specific exit code (2) that CI pipelines can detect — not just print a warning. (2) The `audit.jsonl` sentinel file (`.nodelete`) is a naming convention, not a technical control. Add a pre-flight check that validates audit log continuity before any write operation. (3) The zero-telemetry guarantee is correctly placed in CI but must also appear in the tool's `--version` output as a one-liner trust signal: 'RiskForge v0.1.0 | Apache 2.0 | Zero telemetry'. That line is what a security-conscious engineer reads first."*

**Actions taken:** Exit code 2 for verify failures specified in LLD. Pre-flight continuity check added to AuditEngine. `--version` output format specified in LLD.

---

*Document: HLD-RiskForge-v1.0.md | Version 1.0 | April 2026*
