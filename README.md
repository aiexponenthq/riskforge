# RiskForge

[![PyPI version](https://img.shields.io/pypi/v/riskforge.svg)](https://pypi.org/project/riskforge/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![CI](https://github.com/aiexponent/riskforge/actions/workflows/ci.yml/badge.svg)](https://github.com/aiexponent/riskforge/actions)
[![Zero telemetry](https://img.shields.io/badge/telemetry-zero-green.svg)](https://github.com/aiexponent/riskforge#privacy)

**RiskForge** is an open-source CLI tool that guides AI system builders through a structured, legally-defensible EU AI Act Article 9 risk management process — producing a signed, audit-trailed Risk Management File (RMF) that satisfies Annex IV documentation requirements.

Built by [AiExponent LLC](https://aiexponent.com). Zero telemetry. Runs entirely offline after `pip install`.

---

## Quick Start

```bash
pip install riskforge

# Initialise a new risk register for your AI system
riskforge init

# Run the interactive 8-dimension risk assessment (50+ guided questions)
riskforge assess

# Validate completeness before export (8 readiness gates)
riskforge validate

# Export a signed PDF + JSON artefact for your compliance team
riskforge export --format pdf
```

In under 30 minutes, you have a PDF your legal team can review and a `rmf.json` your downstream compliance toolchain can consume.

---

## What RiskForge Does

EU AI Act Article 9 requires providers of high-risk AI systems to establish, implement, document, and maintain a risk management system. Article 9 is not optional — it is a prerequisite for CE marking and market access in the EU.

RiskForge operationalises Article 9 as a CLI workflow:

- **8 risk dimensions** mapped to Article 9 requirements: health & safety, fundamental rights, discrimination, privacy, transparency, human oversight, robustness, and data governance
- **50+ guided questions** drawn from the question bank, with per-question Article references (Art.9, Art.10, Art.13, Art.14, Art.15) and NIST AI RMF and ISO/IEC 42001 cross-references
- **5x5 scoring matrix** (likelihood × severity) with automatic risk band classification (low / medium / high / critical)
- **8 validation gates** that block export if the register is incomplete — G1 dimension coverage, G2 Article 6(2) classification, G3 high-risk mitigation, G4 knowledge gap tests, G5 metadata completeness, G6 assessor identity, G7 score plausibility, G8 vague mitigation detection
- **SHA-256 hash-chained audit trail** — every state mutation appends to `audit.jsonl` with a verifiable hash chain; any tampering is detected by `riskforge verify`
- **PDF, JSON, and Markdown export** — WeasyPrint-rendered PDF requires no system binaries; JSON is schema-validated against `rmf.schema.json` (JSON Schema draft-2020-12) before every write
- **AiExponent compound moat integration** — import evidence directly from [rag-benchmarking](https://github.com/aiexponent/rag-benchmarking) accuracy reports and [TraceForge](https://github.com/aiexponent/traceforge) data lineage reports; export RMFs consumed by TransparencyDeck and ConformityBot

---

## Features

| Feature | Detail |
|---|---|
| Offline-first | Zero outbound network calls after `pip install` |
| Legally defensible | SHA-256 hash chain; self-verifying exports; `riskforge verify` exits code 2 for CI |
| Article 9 complete | All 8 dimensions, 50+ questions, 8 export gates |
| PDF export | WeasyPrint + Jinja2; no LibreOffice or wkhtmltopdf required |
| Plugin extensible | Add question banks, exporters, adapters via pip — no config edit required |
| Schema-versioned | `rmf.schema.json` published as stable artefact for downstream tools |
| Git-friendly | YAML + JSONL state; human-readable by regulators, diff-resolvable by teams |
| Zero telemetry | `pytest-socket` CI gate ensures no outbound calls; stated in `--version` |

---

## Architecture

RiskForge has four strictly-decoupled layers with enforced import boundaries:

```
CLI (Typer)          — thin interface; no business logic
    |
Engine               — all business logic; no CLI/server imports (enforced in CI)
    |
Storage (FileStore)  — YAML + JSONL; pluggable backend ABC
    |
Integration adapters — read upstream JSON; emit RiskItems
```

The engine is independently testable. The server (FastAPI) is a separate optional install — `pip install riskforge[server]` — and is never imported by the CLI.

State lives in `.riskforge/` (local filesystem, zero dependencies), making projects git-committable and regulator-readable without RiskForge installed.

For team and enterprise deployment, see the [Docker Compose setup](docker/docker-compose.yml).

---

## EU AI Act Article 9 Context

Article 9 of the EU AI Act mandates that providers of high-risk AI systems (Annex III categories) establish a **risk management system** covering:

- **Art.9(2)** — Identification and analysis of known and foreseeable risks
- **Art.9(4)** — Adoption of suitable risk management measures
- **Art.9(7)** — Testing of AI systems against intended purpose, including validation data and metrics
- **Art.9(9)** — Particular consideration of impacts on children and vulnerable groups
- **Art.9(10)** — Documentation to be retained and made available to national competent authorities

RiskForge maps each of these obligations to specific questions, validation gates, and output fields in the exported RMF. Cross-references to NIST AI RMF and ISO/IEC 42001 are included in every risk item to support multi-framework compliance programmes.

---

## Integration with AiExponent Tools

RiskForge is designed to work with the AiExponent compound moat:

```
[rag-benchmarking] --benchmark_report.json--> riskforge import --adapter rag-benchmarking
[TraceForge]       --trace_report.json------> riskforge import --adapter traceforge
                                                      |
                                               riskforge export
                                                      |
                                 +-----------rmf.json-+--------rmf.pdf---------+
                                 |                                              |
                    [TransparencyDeck]                              [Compliance Officer]
                    [ConformityBot]
```

All integration contracts are file-based. RiskForge never calls external APIs.

---

## Contributing

Contributions are welcome. The easiest contribution requires zero Python:

**Add a question** — edit `src/riskforge/_data/question_bank/<dimension>.yaml` and submit a PR. See [docs/contributing/add-question.md](docs/contributing/add-question.md).

**Add a risk pattern** — edit `src/riskforge/_data/patterns/patterns.yaml`. See [docs/contributing/add-pattern.md](docs/contributing/add-pattern.md).

**Add an exporter** — implement the `Exporter` ABC and register an entry point. See [docs/contributing/add-exporter.md](docs/contributing/add-exporter.md).

For development setup:

```bash
git clone https://github.com/aiexponent/riskforge
cd riskforge
make dev-setup
make test
```

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting a pull request.

---

## Privacy

RiskForge makes **zero outbound network connections** in CLI mode. This is enforced in CI using `pytest-socket --disable-socket`. The `--version` output states this explicitly:

```
RiskForge v0.1.0 | Apache 2.0 | Zero telemetry | aiexponent.com
```

Your AI system's risk data never leaves your machine unless you explicitly deploy the optional server.

---

## License

Apache-2.0 — see [LICENSE](LICENSE).

Built by [AiExponent LLC](https://aiexponent.com) | `hello@aiexponent.com`
