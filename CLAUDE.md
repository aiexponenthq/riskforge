# RiskForge — Project Instructions

> Inherits from `~/.claude/CLAUDE.md` (global). This file is project-specific context only.

## What this is

RiskForge is an **open-source CLI for EU AI Act Article 9 Risk Management Systems**. It helps organizations build, maintain, and export the risk documentation required under EU AI Act Art. 9. Apache-2.0 licensed. Currently v0.1.4 (alpha).

One of AI Exponent LLC's top-3 OSS tools. Ships to regulators, enterprise AI teams, compliance officers.

## Directory map

```
riskforge/
├── src/riskforge/
│   ├── __init__.py
│   ├── __main__.py              # Entry point
│   ├── cli/                     # Typer CLI commands
│   ├── engine/                  # Assessment + scoring engines
│   ├── exporters/               # PDF, JSON, schema outputs
│   ├── models/                  # Pydantic data models (AISystem, RiskItem, etc.)
│   ├── storage/                 # Filesystem + future backends
│   ├── migrations/              # Schema migrations
│   ├── adapters/                # External integrations
│   ├── plugins/
│   ├── server/                  # Optional API server
│   └── _data/                   # Bundled data: question bank (YAML)
├── tests/                       # unit, integration, contract, boundary
├── docs/
├── docker/
├── PRD-RiskForge-v1.0.md
├── HLD-RiskForge-v1.0.md
├── LLD-RiskForge-v1.0.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── LICENSE                      # Apache-2.0
├── README.md
├── Makefile
└── pyproject.toml
```

## Stack

- **Language**: Python **3.11+** (also tested on 3.12)
- **Build**: hatchling (pyproject.toml native)
- **CLI**: Typer 0.12.3 + questionary (interactive prompts)
- **Models**: Pydantic 2.7.1 + pydantic-settings
- **Templating**: Jinja2 3.1.4 → WeasyPrint 62.3 for PDF exports
- **Config**: python-dotenv, keyring (for secrets)
- **Data**: YAML question bank, JSON schema validation (jsonschema 4.22.0)
- **Tests**: pytest (unit/integration/contract/boundary split)
- **Lint/format**: ruff

## Commands

```
pip install -e .                              # Dev install
python -m pytest tests/ -v                    # Run all tests
python -m pytest tests/unit/ -q               # Fast unit tests only
python -m pytest tests/ --cov --cov-report=term-missing    # Coverage
ruff check . && ruff format .                 # Lint + format
python -m build                               # Build wheel/sdist
riskforge --help                              # After install — top-level CLI
riskforge init …                              # Initialize a new RMF project
riskforge assess …                            # Run an assessment
```

## Hard rules (project-specific)

1. **Regulatory accuracy is the product.** Every EU AI Act reference in code, docs, docstrings, or user-facing text must cite the exact article/annex and match the authoritative text. Dates must match the `reference_eu_ai_act_dates` authority (Art. 4: Feb 2025, Art. 5: Feb 2025, Art. 6+: Aug 2026). **No paraphrasing from memory.**

2. **Zero telemetry by design.** RiskForge does not call home. It does not ship data to any server unless the user explicitly configures an export destination. This is a trust commitment to users whose risk data is highly sensitive. `vp-responsible-ai` vetoes any change that adds background telemetry.

3. **Every risk-related claim must be auditable.** The export formats (JSON, PDF) must be reproducible — same input → same output, including signing / hashing. Any non-deterministic output in an export is a bug.

4. **Question bank is authoritative.** `src/riskforge/_data/question_bank/*.yaml` is the source of truth for the assessment engine. Changes to questions = version bump + migration. Do not hardcode questions in Python.

5. **Python idioms**:
   - Prefer `Optional[X]` over `X | None` in public APIs (see existing pattern in `cli/`)
   - Pydantic v2 everywhere; avoid v1 patterns
   - Typer commands use rich output (`rich` is already a dep)
   - No bare `except:`; catch specific exceptions

6. **Apache-2.0 compliance**: every new dep must be license-compatible. When in doubt, check with `vp-responsible-ai` → `compliance-engineer`.

## Non-goals

- Not a SaaS. Stays CLI-first. An API server exists (`server/`) but remains optional, self-hosted.
- Not a consulting deliverable. It's a tool — the output is the user's responsibility.
- Not a legal advice engine. Output says "this is your risk register"; the user/lawyer decides regulatory implications.
- Not coupled to any single cloud provider.

## Test strategy

| Layer | Directory | What it tests |
|---|---|---|
| Unit | `tests/unit/` | Pure functions, models, engine logic |
| Integration | `tests/integration/` | CLI flows, multi-component interactions |
| Contract | `tests/contract/` | Schema validation, export format compatibility |
| Boundary | `tests/boundary/` | External integrations, I/O edges |

Fast inner loop: `python -m pytest tests/unit/ -q`. Full sweep before any release.

## How to pick agents/skills here

- **New CLI command** → `vp-product-engineering` → `backend-engineer` (Python context) + `api-designer` for contract
- **New assessment dimension** → update question bank YAML → `ml-system-designer` for scoring logic → `ml-evaluation-engineer` for validation
- **Regulatory text interpretation** → `vp-responsible-ai` → `ai-governance-analyst` skill (authoritative EU AI Act mapping)
- **New export format** → `backend-engineer` + Jinja2 templates → contract tests required
- **Pre-release security review** → `vp-infra-security` → `application-security-engineer` agent
- **PRD / spec changes** → edit `PRD-RiskForge-v1.0.md` / `LLD-RiskForge-v1.0.md` via `prd-writer` skill

## Release discipline

- Version bump: `src/riskforge/__init__.py` + `pyproject.toml` + `CHANGELOG.md` — all three in the same commit
- `python -m build --no-isolation` to produce wheel + sdist
- Tag with semver; GitHub release notes from `CHANGELOG.md` section
- `gh release create` is in the `ask` list in `~/.claude/settings.json` — approved per release, not in blanket auto-allow
