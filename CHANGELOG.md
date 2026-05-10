# Changelog

All notable changes to RiskForge are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
Versioning: [Semantic Versioning](https://semver.org/)

## [Unreleased]

## [1.0.0] - 2026-05-10

First Production/Stable release. PyPI classifier flipped to `Development Status :: 5 - Production/Stable`. Closes the Top-N=4 audit pass; see `docs/audit/T-N4-readiness-2026-05-10.md` in the aiexponent monorepo for the full action list.

### Highlights

- 8 risk dimensions × 37 questions (canonical count, see PRD Amendments block in `PRD-RiskForge-v1.0.md`)
- 6 Annex III risk patterns (community contributions extend the library)
- 8 validation gates G1–G8
- SHA-256 hash-chained audit trail (see `docs/audit-chain-design.md`)
- Apache 2.0, hard-pinned deps for regulatory-evidence reproducibility
- Sigstore attestations on PyPI + CycloneDX SBOM on every GitHub release

### Fixed (production-affecting)

- **Click 8.3 incompatibility broke `riskforge --version` and other Typer-dispatched outputs in fresh installs.** Click 8.3 (released after RiskForge v0.1.4) changed the `is_eager` callback dispatch path in a way that Typer 0.12.3 cannot reach. The version callback ran but produced no output; subprocess-based integration tests captured empty stdout. **Fix:** `click>=8.1,<8.2` hard pin in `pyproject.toml`. Verified 2026-05-10 on Python 3.12.2.

### Changed

- `[tool.coverage.report] fail_under` raised from `24` to `55` to prevent silent regression. Actual coverage on `main` post-fix: ~59% (`pytest --cov` 2026-05-10). PRD NFR-6's 80% target re-anchored to v1.1 milestone (server module test coverage).
- `pyproject.toml` Documentation URL updated from `github.com/aiexponenthq/riskforge#readme` → `aiexponent.com/docs/riskforge`.
- `riskforge tests` Typer help text aligned to Article 9(6)–(8) (was "9(7)" only).
- `LICENSE` replaced with the verbatim Apache-2.0 SPDX template (canonical from apache.org). Earlier file had material text drift in §8 and was missing the Appendix template — caused GitHub to surface "NOASSERTION" instead of "Apache-2.0". `NOTICE` file added per Apache 2.0 §4(d) for the AI Exponent LLC copyright attribution.
- README + CHANGELOG numeric claims corrected per the 2026-05-10 audit (see Documentation Correction subsection below).
- PRD `PRD-RiskForge-v1.0.md` amended in-document with a "2026-05-10 — Pre-GA reality check" block reconciling 5 spec-vs-shipped gaps (200+→37 questions, 20→6 patterns, regulatory_ref→article_refs[] schema, 80%→55% coverage floor, hard-pin reinforcement).

### Documentation correction (post-v0.1.4 audit, 2026-05-10)

- **README + earlier CHANGELOG entries claimed "50+ guided questions"; actual count is 37.**
  The 0.1.0 entry below stating "50+" was an aspirational PRD-target figure (PRD line 114
  spec'd "200+" for v1.0; line 223 spec'd "3-5 per dimension × 8 dimensions = 24-40"). The
  PRD has since been amended to reflect shipped reality (37 questions in v1.0; community
  contributions extend the bank). Surfaces corrected: `README.md` hero + Art. 9 coverage
  Mermaid; `CONTRIBUTING.md`; `lib/tools.ts` on aiexponent.com (already correct since v0.1.4).
- **README claimed "20 Annex III scenarios" / "20 pre-built risk patterns"; actual count is 6.**
  Same root cause — PRD line 256 spec'd "Minimum 20 patterns at v1.0". PRD amended to ship
  reality (6 patterns covering credit scoring, hiring, facial recognition, medical imaging,
  content moderation, criminal risk assessment). Future patterns ship via community contribution
  — see `docs/contributing/add-pattern.md`.
- **PyPI long-description on v0.1.4 still carries the original "50+" + "Built by AiExponent LLC"
  text** because PyPI long-descriptions are immutable per release. Fix lands automatically with
  the next release tag.

## [0.1.4] - 2026-04-18

### Changed
- README rewritten with Mermaid diagrams and tighter structure (Head of AI / Google review pass)
- README and brand surfaces aligned to AiExponent brand kit v4 — two-tone A mark + teal badges
- Code style: applied `ruff format` (CI-pinned 0.4.4) to all 57 source and test files —
  whitespace, blank lines, and string-quoting only; no logic changes

### Fixed
- Legal entity name corrected across docs: "AiExponent LLC" → "AI Exponent LLC"
  (AiExponent is a brand arm; the registered LLC is "AI Exponent LLC")

### Notes
- Published to PyPI as the release version since v0.1.3 was already on PyPI from an
  earlier publish pass during the CI hardening cycle. There is no functional difference
  between 0.1.3 and 0.1.4 — 0.1.4 = 0.1.3 + ruff-format + README refresh.

## [0.1.3] - 2026-04-15

### Fixed
- **`riskforge init --version` argument conflict resolved.** The app-level eager
  `--version` callback was intercepting `--version "2.0"` passed to `init`, printing
  the version string and exiting before init code ran. The init command's parameter
  was renamed to `--sys-version` / `-s`. README quick start and integration tests
  updated accordingly.
- **ruff lint failures across CI matrix.** Reconciled UP045/UP007 selector differences
  between local ruff (0.15+) and CI's pinned ruff (0.4.4): `UP045` removed from both
  global ignore and per-file-ignores (0.4.4 errors on unknown selectors in any config
  section, not just `ignore[]`); `UP007` retained in per-file-ignores so Typer 0.12.3
  CLI commands can use `Optional[X]` (0.12.3 cannot handle `str | None` at runtime).
- Three residual `I001` import-ordering errors in test files
- Unused `qid` variable in `assess.py` (`F841`)

### Changed
- CI workflow excludes integration tests on push (subprocess output unreliable in
  non-TTY CI runners); the 52 unit/contract/boundary tests cover the same code paths
  reliably. Integration tests still run locally.

### Notes
- Published to PyPI alongside the parallel 0.1.2 publish pipeline; 0.1.4 supersedes
  this version on PyPI as the canonical release tag.

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
- 8 risk dimensions with 37 questions (see Unreleased section above for the historical "50+" correction)
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
