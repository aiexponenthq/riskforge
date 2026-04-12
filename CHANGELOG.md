# Changelog

All notable changes to RiskForge are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
Versioning: [Semantic Versioning](https://semver.org/)

## [Unreleased]

## [0.1.2] - 2026-04-12

### Added
- `LICENSE` file (Apache 2.0 full text) — previously only in pyproject.toml
- Root-level `CONTRIBUTING.md` — was missing despite README linking to it
- `CODE_OF_CONDUCT.md` (Contributor Covenant 2.1)
- `SECURITY.md` — vulnerability disclosure policy, scope, security design notes
- `.github/ISSUE_TEMPLATE/` — bug report and question bank contribution templates
- `.github/PULL_REQUEST_TEMPLATE.md`
- `src/riskforge/__main__.py` — enables `python -m riskforge` invocation
- `pyproject.toml`: Python 3.12 classifier, `[project.urls]` (Homepage, Repository, Issues, Changelog)
- Full integration test suite — `init → seed → validate → export json → verify → export markdown`

### Fixed
- `RiskManagementFile.register` property — `rmf.register` was raising `AttributeError`
  (Python attribute is `risk_register`; alias only applies to serialisation)
- `ExportEngine` and `JSONExporter` — added `by_alias=True` to `model_dump()` so
  `risk_register` serialises as `register` per the published schema
- README — corrected GitHub org URLs (`aiexponent` → `aiexponenthq`); fixed quick start
  to show actual required args for `riskforge init` and `riskforge assess`
- Test count: 53 → 57

## [0.1.1] - 2026-04-12

### Fixed
- **`riskforge assess` implemented** — interactive 8-dimension risk assessment fully wired:
  question bank loop, pattern matching, likelihood/severity scoring via questionary,
  knowledge gap flagging, progress bar, session summary. The core user workflow now works end-to-end.
- **PDF exporter bug** — `items=rmf.register.system` corrected to `items=rmf.register.items`
- **Audit chain** — three bugs fixed: `read_audit` converted to a true async generator;
  genesis `prev_hash` initialisation aligned between `AuditEngine` and `FileStore.verify_chain`;
  `_compute_hash` made consistent (`entry_hash=""` not `pop`)
- **Sequence numbering** — first audit entry now has `seq=0` (was incorrectly `seq=1`)
- **`RiskDimension` enum** — trimmed to 8 PRD-specified dimensions; removed 5 extra values
  with no corresponding question bank YAML files
- **Typer compatibility** — replaced `str | None` union syntax with `Optional[str]` across all CLI commands

### Added
- 8 new tests covering: audit chain integrity, tamper detection, sequence numbering,
  assess engine question loading, knowledge gap flagging, PDF exporter regression guard
- Total: 53 tests passing

## [0.1.0] - 2026-04-12

### Added
- Initial release of RiskForge
- Article 9 risk management system CLI
- 8 risk dimensions with 50+ questions
- 5x5 likelihood x severity scoring matrix
- JSON, PDF, and Markdown export formats
- SHA-256 hash-chain audit trail
- Integration adapters for rag-benchmarking and TraceForge
- `riskforge init`, `assess`, `validate`, `export`, `verify` commands
- `riskforge risk list/add/edit/accept/score` subcommands
- `riskforge system show/edit` subcommands
- `riskforge tests generate/list` subcommands
- `riskforge diff` and `riskforge import` commands
- Optional FastAPI server (`pip install riskforge[server]`)
- 8 export readiness gates (G1-G8)
- Plugin system via Python entry points (question banks, exporters, adapters)
- WeasyPrint PDF rendering with Jinja2 HTML templates
- `rmf.schema.json` (JSON Schema draft-2020-12) as versioned output contract
- FileStore storage backend (YAML + JSONL, git-friendly)
- Exit code 2 for `riskforge verify` failures (CI-detectable)
- Zero-telemetry guarantee enforced via pytest-socket in CI
- Docker Compose setup for team deployment
- Sigstore OIDC signing on all PyPI releases
- CycloneDX SBOM attached to every GitHub Release
- Build provenance attestation via GitHub Actions
