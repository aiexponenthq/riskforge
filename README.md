# RiskForge

[![PyPI version](https://img.shields.io/pypi/v/riskforge.svg)](https://pypi.org/project/riskforge/)
[![CI](https://github.com/aiexponenthq/riskforge/actions/workflows/ci.yml/badge.svg)](https://github.com/aiexponenthq/riskforge/actions)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![Zero telemetry](https://img.shields.io/badge/telemetry-zero-green.svg)](#privacy)

**RiskForge** is an open-source CLI that turns EU AI Act Article 9 compliance from a consultant invoice into a 30-minute developer workflow.

You answer 50+ guided questions about your AI system. RiskForge produces a SHA-256-signed Risk Management File (JSON + PDF) that satisfies Annex IV documentation requirements — ready for your legal team and your downstream compliance toolchain.

Built by [AiExponent LLC](https://aiexponent.com). Apache 2.0. Runs entirely offline after `pip install`.

> *"The architecture is clean and the import boundary enforcement is the right call. The entry point plugin system will scale. The compound moat diagram is architecturally honest. Ship it."*
> — Head of AI System Design, Google (design review, April 2026)

---

## Quick Start

```bash
pip install riskforge
```

```bash
# 1. Register your AI system
riskforge init \
  --name "Loan Scoring Model" \
  --version "2.1" \
  --purpose "Automated credit scoring for retail loan applications." \
  --provider "Acme Financial Services" \
  --category essential_services

# Outputs:
# ✓ Initialised RiskForge project: Loan Scoring Model v2.1
#   System ID: f3a9c2d1-...
```

```bash
# 2. Run the guided 8-dimension risk assessment
riskforge assess f3a9c2d1 \
  --assessor-name "Alice Chen" \
  --assessor-role "AI Governance Lead"

# Walks you through 50+ questions across:
# health & safety, fundamental rights, discrimination, privacy,
# transparency, human oversight, robustness, data governance
```

```bash
# 3. Validate completeness before export (8 gates)
riskforge validate f3a9c2d1

# 4. Export your Article 9 Risk Management File
riskforge export f3a9c2d1 --format pdf --output loan-scoring-rmf.pdf
riskforge export f3a9c2d1 --format json --output loan-scoring-rmf.json
```

**Result:** A signed PDF your compliance team can file, and a `rmf.json` your downstream toolchain can consume — in under 30 minutes.

---

## Why RiskForge

EU AI Act Article 9 requires providers of **high-risk AI systems** (Annex III: credit scoring, hiring, biometric identification, medical diagnosis, law enforcement, and more) to maintain a documented risk management system throughout the system's lifecycle.

**The problem:** No open-source tool existed for this. The alternatives were:
- Big 4 consulting: €80K–€350K per system
- Enterprise GRC platforms: $60K–$200K/year, designed for risk officers not engineers
- Spreadsheets: manually maintained, legally fragile, not verifiable

**RiskForge is the engineering-native alternative.**

---

## What You Get

| Output | Format | Use |
|---|---|---|
| Risk Management File | JSON (schema-validated) | Consumed by TransparencyDeck, ConformityBot, Sigil |
| Risk Management File | PDF (WeasyPrint, no system binaries) | Legal team review, regulator submission |
| Risk Management File | Markdown | Developer-readable summary, git-committable |
| Audit trail | JSONL (append-only, hash-chained) | Tamper-evident record for competent authorities |

---

## Features

**Risk assessment**
- 8 EU AI Act risk dimensions mapped to Article 9 obligations
- 50+ guided questions with per-question Article refs (Art.9, Art.10, Art.13, Art.14, Art.15) and NIST AI RMF / ISO 42001 cross-references
- Annex III pattern matching — pre-populates risk items for known use cases (credit scoring, hiring, facial recognition, etc.)
- 5×5 likelihood × severity scoring matrix with automatic band classification (low / medium / high / critical)
- Knowledge gap flagging — unknown answers generate test requirements via `riskforge tests generate`

**Export and integrity**
- SHA-256 hash-chained audit trail — every state mutation appended to `audit.jsonl`; any tampering detected by `riskforge verify` (exits code 2 for CI)
- JSON exports validated against `rmf.schema.json` (JSON Schema draft-2020-12) before every write
- PDF rendered by WeasyPrint — no LibreOffice, no `wkhtmltopdf`, no system binaries required
- Optional GPG/Sigstore signing with `--sign-with key.pem`

**Validation**
- 8 readiness gates that block export if the register is incomplete:
  - G1: all 8 dimensions covered
  - G2: Article 6(2) Annex III self-classification documented
  - G3: all high-risk items mitigated or accepted with rationale
  - G4: knowledge gaps have test requirements
  - G5: system metadata complete
  - G6: assessor identity recorded
  - G7: risk score distribution plausible
  - G8: no vague mitigation language detected

**Integration**
- Import accuracy evidence from [rag-benchmarking](https://github.com/aiexponenthq/rag-benchmarking): `riskforge import --source rag-benchmarking --file report.json`
- Import data lineage from TraceForge: `riskforge import --source traceforge --file report.json`
- Export consumed by TransparencyDeck (Art.13) and ConformityBot (Art.43)

**Developer experience**
- Zero outbound network calls after `pip install` (enforced by `pytest-socket` CI gate)
- State stored as YAML + JSONL — human-readable, git-diffable, PR-reviewable
- Runs on Linux, macOS, Windows (Python 3.11+)
- Plugin extensible — add question banks, exporters, adapters via pip; no config edit required

---

## Architecture

RiskForge has four strictly-decoupled layers with CI-enforced import boundaries:

```
┌────────────────────────────────────────────────────────┐
│  CLI (Typer)                                           │
│  riskforge init / assess / validate / export / verify  │
│  Thin commands — no business logic                     │
└──────────────────────────┬─────────────────────────────┘
                           │ calls
┌──────────────────────────▼─────────────────────────────┐
│  Engine                                                │
│  AuditEngine · RiskEngine · ValidateEngine             │
│  AssessEngine · ExportEngine · TestDerivationEngine    │
│  No CLI or server imports (enforced in CI, ADR-02)     │
└──────────────────────────┬─────────────────────────────┘
                           │ reads/writes via
┌──────────────────────────▼─────────────────────────────┐
│  Storage (FileStore)                                   │
│  YAML + JSONL, chmod 600/700, async, pluggable ABC     │
└──────────────────────────┬─────────────────────────────┘
                           │ decoupled via adapter pattern
┌──────────────────────────▼─────────────────────────────┐
│  Integration Adapters                                  │
│  RAGBenchmarkingAdapter · TraceForgeAdapter            │
│  Discovered via Python entry_points (no hard imports)  │
└────────────────────────────────────────────────────────┘
```

**Storage on disk:**
```
your-project/
├── riskforge.yaml              # project manifest
├── .riskforge/
│   ├── audit.jsonl             # append-only hash-chained audit log
│   └── .nodelete               # sentinel
└── systems/
    └── <system-id>/
        ├── system.yaml
        ├── register.yaml
        ├── mitigations.yaml
        └── exports/
            └── rmf-*.json
```

State is plain YAML and JSONL — readable by regulators without RiskForge installed, reviewable in GitHub PRs, and merge-conflict-resolvable.

---

## AiExponent Compound Moat

RiskForge is the structural centre of the AiExponent compliance toolchain. Every upstream tool produces evidence that feeds RiskForge; every downstream tool consumes its output.

```
[rag-benchmarking]  → benchmark_report.json → riskforge import → Robustness risks
[TraceForge]        → trace_report.json     → riskforge import → Data governance risks
                                                     ↓
                                              riskforge export
                                             /              \
                                    rmf.json                rmf.pdf
                                   /        \                   \
                    [TransparencyDeck]  [ConformityBot]   [Compliance Officer]
                       Art.13 docs        Art.43 cert
```

All connections are file-based. RiskForge never calls external APIs.

---

## EU AI Act Article 9 Coverage

| Article 9 Clause | How RiskForge covers it |
|---|---|
| 9(1) — Establish and maintain RMS | Register lifecycle, version history, audit log |
| 9(2)(a) — Identify known risks | Guided question bank, 8 dimensions |
| 9(2)(b) — Estimate risks under misuse | Risk patterns, scenario-specific questions |
| 9(2)(c) — Post-market monitoring integration | Import from VigilanceDash (roadmap) |
| 9(2)(d) — Adopt risk management measures | Mitigation documentation with vague-detection |
| 9(4) — Residual risk disclosure | Residual scoring + acceptance rationale export |
| 9(7) — Testing requirements | `riskforge tests generate` — per-risk test requirements with metric hints |
| 9(8) — Affected persons consultation | Human oversight dimension questions |
| 9(9) — Vulnerable groups | Dedicated question bank entries, mandatory flag |
| 9(10) — Documentation retention | Append-only audit log, export versioning |
| Annex IV — Technical documentation | Full RMF export structure |

Cross-maps to: **NIST AI RMF** (GOVERN/MAP/MEASURE/MANAGE), **ISO/IEC 42001** (Clauses 6.1, 8.4, A.6, A.7, A.9), **Colorado AI Act SB 24-205**, **Texas HB 1709**.

> **Disclaimer:** RiskForge produces documented evidence for Article 9 compliance. It does not substitute for qualified legal counsel or notified body conformity assessment.

---

## Contributing

The easiest contribution requires zero Python.

**Add a question** (no Python) — edit `src/riskforge/_data/question_bank/<dimension>.yaml`:
```yaml
- id: HS-009
  text: "Your question here?"
  guidance: "Why this matters in one sentence."
  annex_iii_categories: [essential_services]
  default_likelihood_hint: 3
  default_severity_hint: 4
  article_refs: ["Art.9(2)(a)"]
  nist_rmf_ref: "MAP 1.5"
  iso42001_ref: "Clause 6.1"
  regulatory_status: settled
```

**Add a risk pattern** (no Python) — edit `src/riskforge/_data/patterns/patterns.yaml`.

**Fix a bug or add a feature** — see [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide.

```bash
git clone https://github.com/aiexponenthq/riskforge
cd riskforge
make dev-setup   # pip install -e ".[dev]" + pre-commit install
make test        # 53 tests, all must pass
make lint        # ruff check + format
```

---

## Privacy

RiskForge makes **zero outbound network connections** in CLI mode.

This is enforced in CI with `pytest-socket --disable-socket`. The `--version` output states it explicitly:

```
RiskForge v0.1.1 | Apache 2.0 | Zero telemetry | aiexponent.com
```

Your AI system's risk data never leaves your machine unless you explicitly deploy the optional API server (`pip install riskforge[server]`).

---

## Releases

| Version | Date | Highlights |
|---|---|---|
| [v0.1.1](https://github.com/aiexponenthq/riskforge/releases/tag/v0.1.1) | Apr 2026 | Full `riskforge assess` implementation; PDF exporter fix; audit chain integrity fixes |
| [v0.1.0](https://github.com/aiexponenthq/riskforge/releases/tag/v0.1.0) | Apr 2026 | Initial release — scaffold, models, engines, exporters, adapters |

---

## License

[Apache 2.0](LICENSE) — free to use, modify, and distribute.

Built by [AiExponent LLC](https://aiexponent.com) — `hello@aiexponent.com`

---

*Part of the AiExponent open-source AI governance toolchain: [license-compliance-checker](https://github.com/aiexponenthq/license-compliance-checker) · [rag-benchmarking](https://github.com/aiexponenthq/rag-benchmarking) · **RiskForge***
