# RiskForge — Product Requirements Document v1.0

**Status:** Approved for Development  
**Date:** April 2026  
**Owner:** Ajay Pundhir, Founder & CEO, AiExponent LLC  
**Tool name:** RiskForge  
**PyPI package:** `riskforge`  
**GitHub:** github.com/aiexponenthq/riskforge  
**License (OSS):** Apache 2.0  
**Regulation:** EU AI Act Article 9 (Risk Management System)  
**Priority:** P0 — build now. August 2026 enforcement is 4 months away.

**Reviewed by:** AI Governance Analyst (Anthropic), Market Researcher, Competitive Analyst, System Architect, API Designer, UX Researcher, UX Designer, Security Architect, Responsible AI Lead, Steve Jobs, Head of AI Governance (Anthropic)  
**Consensus rating after review cycle:** 9.2/10 — approved for development commissioning

---

## Document Conventions

- **FR-n** = Functional Requirement
- **NFR-n** = Non-Functional Requirement
- **AC-n** = Acceptance Criterion
- Article references: **Regulation (EU) 2024/1689** (EU AI Act) unless otherwise stated
- **Article 9 compliance file** = the primary output artefact — the regulator-ready risk management file
- **RMS** = Risk Management System (the process; Article 9 obligation)
- **RMF** = Risk Management File (the documentary artefact; Annex IV requirement)

---

## 1. Strategic Context

### Why This Exists

AiExponent builds compliance infrastructure for engineering teams. The portfolio moat is a tool chain where every layer produces structured evidence consumed by the next:

```
TraceForge (Art.10) → LCC (Art.53) → rag-benchmarking (Art.15)
         ↓
    RiskForge (Art.9)  ← THIS TOOL
         ↓
TransparencyDeck (Art.13) → ConformityBot (Art.43) → Sigil (Art.14/17) → VigilanceDash (Art.72)
```

**RiskForge is the structural centre of this chain.** Every upstream tool (TraceForge, LCC, rag-benchmarking) produces inputs that feed the risk register. Every downstream tool (TransparencyDeck, ConformityBot) consumes the risk management file RiskForge exports.

Article 9 is the most important article for high-risk AI systems. August 2026 enforcement is 4 months away. There is currently **no open-source tool** that helps engineering teams build a compliant Article 9 risk management system. The Big 4 charge €80K–€350K to do this manually. RiskForge does it in 25 minutes.

### The Gap No One Else Fills

| Tool | Article 9 coverage | Verdict |
|---|---|---|
| ServiceNow AI Governance | Generic IT risk register; no Article 9 structure | No |
| IBM OpenPages | Manual configuration; no EU AI Act taxonomy | No |
| Credo AI | Strong on model eval; weak on procedural RMS documentation | Partial |
| Holistic AI | EU AI Act audit service; enterprise-only, £80K+ entry | No (scale) |
| Any OSS tool (as of April 2026) | None exists | **Gap** |

**RiskForge fills this gap.** It is the only open-source, developer-native, Article 9-specific risk management system builder.

---

## 2. Problem Statement

### The Problem

EU AI Act Article 9 requires providers of high-risk AI systems to establish, implement, document, and maintain a risk management system covering the entire lifecycle. The obligations are operational, iterative, and legally significant — they produce a documented artefact (the risk management file) that must be retained and made available to national competent authorities on request.

Engineering teams responsible for high-risk AI systems cannot meet this obligation because:

1. **They don't know what Article 9 actually requires.** The regulation is dense. Article 9(2) lists six sub-obligations. Article 9(7) requires testing against "previously determined metrics and probabilistic thresholds appropriate to the intended purpose." Most engineers have never read it.

2. **They have no structured workflow.** Existing GRC tools are designed for risk officers, not engineers. They model risks as tickets with owner fields — not as likelihood × severity matrices linked to EU AI Act dimensions and testing requirements.

3. **They cannot connect their engineering artefacts to legal documentary requirements.** A rag-benchmarking result showing accuracy at 0.61 needs to become an Article 9(7) testing entry with a threshold rationale. That translation is manual today.

4. **They can't afford the manual alternative.** A single Article 9 risk management file prepared by Big 4 consultants costs €8K–€42K for initial preparation and €8K–€20K per model version update.

5. **August 2026 is 4 months away.** Companies without a documented RMS cannot legally deploy covered systems from that date. The urgency is a deployment gate, not a compliance tick-box.

### Who Is In Scope

Under Article 9, the primary obligated party is the **provider** — any natural or legal person that develops or places a high-risk AI system on the market. **Deployers** who substantially modify a system become providers under Article 3(3) and inherit full Article 9 obligations.

**Annex III high-risk system categories most common in enterprise AI (target customers):**
- Category 4: Employment and worker management (hiring, performance, task allocation)
- Category 5: Access to essential private and public services (credit scoring, insurance, benefits)
- Category 3: Education and vocational training (assessment tools, admissions)
- Category 1: Biometric identification (face recognition, emotion recognition)

### The Cost of Inaction

Non-compliance with Article 9 exposes providers to fines up to **€30M or 6% of global annual turnover** (whichever is higher). National market surveillance authorities in Germany, France, and the Netherlands have signalled active enforcement posture for August 2026. Inability to produce an Article 9 risk management file on inspection is a primary enforcement trigger.

---

## 3. Business Model

### Decision: OSS Core + Enterprise Tier

**OSS core is free. Enterprise tier is paid.**

This follows the proven dbt / Terraform / Airbyte model: individual and team use is free, enterprise workflow, portfolio management, and compliance reporting features are paid.

**Rationale:**
- Engineering teams adopt tools that appear in their workflow; they do not buy governance software through procurement. OSS distribution is the only viable path to the first 1,000 users.
- The regulatory landscape is uncertain enough that enterprises want to inspect and modify risk frameworks before committing to a vendor.
- Network effects from community contributions update the question bank and risk patterns faster than any single vendor maintains.
- The OSS install base is the enterprise sales pipeline. Users who adopt the CLI become the internal champions who close enterprise deals.

### OSS Core (Free, Apache 2.0)

Available via `pip install riskforge`. Includes:
- Complete Article 9 RMS CLI workflow
- 200+ question bank covering all 8 EU AI Act risk dimensions
- 5×5 risk scoring engine with configurable thresholds
- Integration ingestion (rag-benchmarking, TraceForge)
- JSON export (Article 9 compliant, with SHA-256 integrity hash)
- PDF export (regulator-ready, WeasyPrint)
- Cross-framework mapping: NIST AI RMF, ISO 42001 Clause 8.4
- Docker Compose optional stack with web UI
- All under Apache 2.0 — no CLA required

### Enterprise Tier ($18K–$48K/year)

| Feature | OSS | Enterprise |
|---|---|---|
| Article 9 RMS for single system | ✅ | ✅ |
| CLI + Docker Compose | ✅ | ✅ |
| JSON + PDF export | ✅ | ✅ |
| Question bank + risk patterns | ✅ | ✅ |
| Multi-system portfolio dashboard | ❌ | ✅ |
| Team collaboration (multi-user) | ❌ | ✅ |
| RBAC + audit trail for regulator access | ❌ | ✅ |
| Notified body submission package | ❌ | ✅ |
| Sigil runtime integration | ❌ | ✅ |
| GitHub/Jira evidence linking | ❌ | ✅ |
| Dedicated SLA + support | ❌ | ✅ |
| Private cloud deployment | ❌ | ✅ |

**Pricing tiers:**
- **Team** ($18K/year): up to 5 systems, 10 users, Sigil integration
- **Professional** ($32K/year): up to 25 systems, unlimited users, notified body package
- **Enterprise** (custom, $48K+/year): unlimited systems, private cloud, SI partner support, custom question banks with legal review

### Revenue Target

Year 1: £100K (conservative: 6 Team + 2 Professional conversions from OSS community)  
Year 2: £380K (enterprise contracts, SI partner referrals)

---

## 4. User Personas

### Persona 1 — Alex, ML Engineer (primary user)

**Role:** ML Engineer at a UK fintech building an automated credit scoring model (Annex III, Category 5).  
**Context:** First heard about Article 9 from legal counsel three months before August 2026 deadline. Has never done a risk management assessment. Assumes it will take weeks.  
**Goals:** Complete the assessment quickly. Get a document that makes legal stop asking questions. Never do it manually again.  
**Frustrations:** Documentation overhead. Vague guidance. Tools that require an enterprise account to see anything.  
**Success:** Ran `riskforge assess` in 20 minutes, got a PDF that passed legal review the first time.

### Persona 2 — Sarah, Chief Compliance Officer (primary buyer)

**Role:** CCO at a European insurance company deploying AI for underwriting decisions.  
**Context:** Responsible for EU AI Act compliance across 12 AI systems. Has budget. Needs defensible evidence, not beautiful dashboards.  
**Goals:** Board-reportable compliance posture. Evidence that would survive a competent authority inspection. Zero surprises.  
**Frustrations:** Engineering tools that produce outputs only engineers can interpret. Tools that can't produce a PDF she can put in front of a regulator.  
**Success:** Received an RMF PDF that was accepted as Article 9 evidence by the company's legal counsel and filed in the regulatory evidence library.

### Persona 3 — Marcus, AI Governance Analyst (bridge user)

**Role:** AI Governance Analyst at a global consultancy helping clients achieve Article 9 compliance.  
**Context:** Runs 5–15 Article 9 assessments per year. Currently does them in a 40-tab Excel spreadsheet.  
**Goals:** Faster assessments. Reproducible methodology. Outputs that don't need reformatting before client delivery.  
**Frustrations:** No standard tooling. Every engagement reinvents the risk taxonomy. Clients can't self-serve updates between engagements.  
**Success:** Uses RiskForge as the standard assessment tool across all engagements; clients maintain their own registers between assessments.

---

## 5. User Stories

**Core workflow (must have for v1.0):**

1. As an ML engineer, I want to run `riskforge init` so that I can register my AI system and begin a risk assessment in under 5 minutes without reading documentation.
2. As an ML engineer, I want `riskforge assess` to guide me through risk identification with targeted questions so that I never have to interpret Article 9 legal text myself.
3. As an ML engineer, I want to import my rag-benchmarking output so that accuracy findings below threshold automatically become scored risk items without manual translation.
4. As an ML engineer, I want to run `riskforge export --format pdf` and receive a regulator-ready document so that my compliance officer can review and file it without changes.
5. As a compliance officer, I want the PDF export to include a cover page, executive summary, risk register table, and audit metadata so that I can present it to regulators without additional formatting.
6. As an AI governance analyst, I want to run `riskforge validate` before exporting so that I can see exactly which obligations are unmet before the document is finalised.
7. As an ML engineer, I want `riskforge assess --non-interactive --answers answers.yaml` so that I can integrate risk assessment into CI/CD pipelines for automated re-assessment on model updates.
8. As a compliance officer, I want multi-system portfolio support (Enterprise) so that I can track Article 9 compliance status across all systems in a single dashboard.
9. As a governance analyst, I want the risk register to show cross-references to NIST AI RMF and ISO 42001 controls so that a single assessment satisfies multiple framework obligations.
10. As an ML engineer, I want `riskforge risk accept <id> --rationale "..."` so that I can formally record the decision to accept residual risks with a dated, attributed rationale.

---

## 6. Functional Requirements

### FR-1 — System Registration

`riskforge init` runs an interactive wizard that captures:
- System name, version, purpose statement
- Annex III category (numbered list; tool provides descriptions to aid self-classification)
- Intended users and deployment context
- Primary inputs (text, images, structured data, audio, video)
- Primary outputs (classification, score, decision, recommendation)
- Provider name and assessment date

Outputs a `riskforge.yaml` project file. The wizard completes in under 90 seconds. System metadata is confirmed back to the user before proceeding.

### FR-2 — Guided Risk Identification (`riskforge assess`)

Interactive session covering 8 risk dimensions derived from Article 9 and Annex III harm categories:
1. Health and Safety
2. Fundamental Rights
3. Discrimination and Fairness
4. Privacy and Data Protection
5. Transparency and Explainability
6. Human Oversight and Control
7. Robustness and Accuracy
8. Data Governance

Each dimension: 3–5 targeted questions. Maximum session length: 25 minutes for a first assessment. Questions are answerable from the engineer's existing system knowledge — no external research required mid-session.

`unknown` / `?` is a valid answer for any question, recorded as a `knowledge_gap` entry. Knowledge gaps auto-generate test requirements and do not invalidate the assessment.

Progress display shows: `[Dim 3/8 — Fairness] 2 risks found | 1 unknown | ██████░░░░ 60%`.

A session summary at completion shows: total risks by severity, dimensions with open items, knowledge gaps, auto-generated test requirements count, and next action prompt.

### FR-3 — Risk Scoring Engine

5×5 likelihood × severity matrix. Likelihood scale: rare (1) through almost certain (5). Severity scale: negligible (1) through critical (5). Risk score = likelihood × severity (range 1–25).

Risk appetite threshold: configurable per project (default: 9). Risk items above threshold are flagged as requiring mitigation or explicit acceptance.

Risk bands: low (1–4), medium (5–9), high (10–16), critical (17–25).

### FR-4 — Mitigation Documentation

Each risk item carries one or more mitigations:
- Description of the mitigation measure
- Control type: preventive / detective / corrective
- Owner (name or role)
- Status: planned / implemented / verified
- Evidence references (free text — links to rag-benchmarking reports, monitoring dashboards, code commits)

Mitigations with description "we'll monitor it" or equivalents are flagged with a `vague_mitigation` warning.

Residual likelihood and severity are scored after mitigations are entered to produce a residual risk score.

### FR-5 — Risk Pattern Library

A versioned YAML pattern library (`patterns/v1.yaml`) bundled with the package. Pattern matching runs at session start based on system metadata. Pre-populated risk items are presented for user confirmation/modification, not silently injected.

Minimum 20 patterns at v1.0, covering the 8 most common Annex III deployment scenarios (credit scoring, hiring CV screening, facial recognition, medical imaging, criminal risk assessment, content moderation, driving assistance, student assessment).

### FR-6 — Test Requirement Generation

`riskforge tests generate` derives test requirements from open (unmitigated or knowledge-gap) risk items.

Each test requirement includes: the risk item it addresses, the Article 9(7) testing rationale, a suggested metric type (accuracy, precision/recall, demographic parity, adversarial robustness), and a recommended threshold range.

Test requirements are exported in the Article 9 compliance file and in a machine-readable format that rag-benchmarking can ingest as a benchmark configuration.

### FR-7 — Integration Ingestion

**`riskforge assess --import-rag <path>`:** Reads a `benchmark_report.json` from rag-benchmarking. Maps accuracy metrics below the configured threshold to `RiskItem` entries in the Robustness dimension, with `source="rag_benchmarking"` and a reference to the report file. The engineer reviews and scores; the tool does not auto-accept.

**`riskforge assess --import-trace <path>`:** Reads a `trace_report.json` from TraceForge. Maps data quality findings to `RiskItem` entries in the Data Governance dimension.

### FR-8 — Validation

`riskforge validate` checks:
- All 8 dimensions have at least one entry (risk item, not-applicable record, or deferred with rationale)
- All high-scoring risk items (above threshold) are either mitigated or explicitly accepted with rationale
- No knowledge gaps remain without a test requirement
- All required system metadata fields are populated
- Assessor identity is recorded

Outputs a colour-coded table: PASS / WARN / FAIL per check. Export is blocked if any FAIL exists (can be overridden with `--force` and a mandatory reason).

### FR-9 — Export: JSON (Article 9 Compliance File)

`riskforge export --format json` produces a `RiskManagementFile` JSON document containing:
- Schema version, generation timestamp, question bank version
- AISystem metadata
- Complete risk register (all items, scores, mitigations, residual risks)
- Test requirements derived
- Cross-reference table (Art. 9 clause → risk items → NIST RMF → ISO 42001)
- Audit metadata (SHA-256 hash, assessor identity, change log)
- Mandatory disclosure statement

The SHA-256 hash is computed over the canonical JSON (sorted keys, normalised whitespace) with the hash field set to `""` before computation, then written back — giving a self-verifying document.

### FR-10 — Export: PDF (Regulator-Ready)

`riskforge export --format pdf` produces a WeasyPrint-rendered PDF containing:

**Cover page:** System name, version, assessment date, assessed by (name + role), EU AI Act Annex III category, status badge (COMPLETE / INCOMPLETE / PENDING), risk summary (3 numbers: total risks / open mitigations / knowledge gaps).

**Section 1 — Executive Summary:** Three paragraphs: system description, identified risks and severity distribution, residual risk posture. Written in plain English. Ends with the mandatory RiskForge tool disclosure.

**Section 2 — Assessment Methodology:** Article 9 clauses addressed, question bank version used, scoring methodology, risk appetite threshold applied.

**Section 3 — Risk Register:** Full table of all risk items with: dimension, description, source, likelihood, severity, score band, mitigations, residual score, accepted status.

**Section 4 — Residual Risk Summary:** Accepted risks with rationale, listed for regulator review.

**Section 5 — Test Requirements:** Derived test requirements with metric types and thresholds, cross-referenced to risk items.

**Section 6 — Cross-Reference Table:** Art. 9 clause ↔ risk item ↔ NIST RMF ↔ ISO 42001 mapping.

**Section 7 — Audit Metadata:** SHA-256 hash, schema version, question bank version, generation timestamp, change log (if re-assessment).

### FR-11 — Non-Interactive / CI Mode

`riskforge assess --non-interactive --answers answers.yaml` accepts a structured YAML answers file for automated execution in CI/CD pipelines. Enables scheduled re-assessment triggered on model version updates.

### FR-12 — Output Contract for Downstream Tools

Publishes a versioned JSON Schema at `riskforge/schemas/v1/rmf.schema.json`. TransparencyDeck and ConformityBot pin against this schema. Any breaking schema change increments the major version with documented migration path.

### FR-13 — API Server (Optional)

`riskforge serve` starts a FastAPI server on port 8090 with full CRUD for registers, risk items, and export. Requires `RISKFORGE_SECRET_KEY` (256-bit minimum). See NFR-Security for full server requirements.

---

## 7. Non-Functional Requirements

### NFR-1 — Performance

- `riskforge init`: completes in under 90 seconds
- `riskforge assess` (full 8-dimension session): under 25 minutes for a first assessment, under 10 minutes for a re-assessment
- `riskforge export --format json`: completes in under 3 seconds for registers with up to 100 risk items
- `riskforge export --format pdf`: completes in under 10 seconds
- CLI startup time (to first prompt): under 1 second

### NFR-2 — Security (CLI mode)

- Project files written with `chmod 600` (owner read/write only) on Unix
- On `riskforge init` in a git repo, `riskforge.yaml` automatically added to `.gitignore`
- Before every export, check `git check-ignore -q` and emit a blocking WARNING if project file would be tracked
- API keys handled via OS keychain (`keyring`) or environment variables only — never in project files
- Zero outbound network calls in CLI mode (enforced; verified by `pytest-socket` CI gate)

### NFR-3 — Security (Server mode)

- Server refuses to bind unless `RISKFORGE_SECRET_KEY` (≥256-bit entropy) is set
- Rejects launch on `0.0.0.0` without explicit `--allow-external` flag
- Bearer token authentication on all endpoints (HMAC-SHA256, configurable TTL)
- Payload size limit: 2MB maximum
- Strict JSON input validation; no executable MIME types; allowlist field types

### NFR-4 — Audit Trail Integrity

- Append-only change log: every mutation to a risk entry records `{timestamp_utc, field_changed, old_value_hash, new_value_hash, author_identity}` in a separate `riskforge.audit.jsonl` file
- Hash chain: each log entry includes SHA-256 of the previous entry
- `riskforge verify` command checks chain integrity; exits non-zero on any gap or hash mismatch
- For regulated submission: `--sign-with key.pem` produces a detached Sigstore/PGP signature block embedded in the export envelope

### NFR-5 — Privacy (Zero Telemetry)

- No network calls in CLI mode — zero outbound connections
- Privacy policy states: "In CLI mode, RiskForge makes zero outbound network connections. No usage data, error reporting, or telemetry."
- `pytest-socket` test with `disable_socket()` must pass on every build

### NFR-6 — Supply Chain Security

- All dependencies pinned to exact versions in `requirements.txt`
- `pip-audit` as required CI gate — blocks release on any CVSS ≥7.0 finding
- CycloneDX SBOM generated on every release; attached to GitHub Release
- PyPI packages signed with Sigstore using GitHub Actions OIDC
- Required CI gates before any release tag: `pip-audit` clean, `bandit -ll` clean, test coverage ≥80%, SBOM attached

### NFR-7 — Portability

- CLI runs on Linux, macOS, and Windows (Python 3.11+)
- PDF export does not require LibreOffice or any system binary (WeasyPrint only)
- Docker Compose optional stack requires only Docker 24+
- No internet connection required in CLI mode after installation

### NFR-8 — Compliance of RiskForge Itself

- RiskForge's own Article 9 risk management file (generated by `riskforge assess` on itself) must be included in the GitHub repository
- RiskForge's own dependency tree must pass `pip install license-compliance-checker && lcc scan . --policy eu-ai-act-compliance` at every release

---

## 8. Responsible AI Requirements

### RAI-1 — Mandatory Export Disclosure

Every exported JSON and PDF must contain the following non-removable statement (injected at export time):

> *"This document was produced using RiskForge [version], with question bank version [qb_version]. It has not been reviewed by a qualified legal professional and does not constitute legal advice under the EU AI Act or any other regulation. It represents the outputs of a structured risk identification process conducted by the team listed above."*

### RAI-2 — Question Bank Integrity

- Question bank is versioned and published alongside every release
- Changes to the question bank require a CHANGELOG entry explaining what was added, removed, and why
- Anchoring bias mitigation: where questions offer severity hints, these are clearly labelled as non-binding defaults
- No question can be marked "not applicable" without a mandatory free-text justification field
- Questions in areas of regulatory uncertainty are tagged `status: "pending_implementing_act"` and export includes a caveat

### RAI-3 — False Confidence Prevention

- No aggregate score may be labelled "compliant" or "passed Article 9"
- Any aggregate display must carry: *"Scores indicate coverage of documented considerations, not legal compliance"*
- If all risks are scored low (risk score ≤ 4), `riskforge validate` emits: `All risks scored low. This may reduce regulator confidence. Review scoring criteria before exporting.`
- `riskforge validate` must not produce a green PASS status unless all 8 dimensions have entries

### RAI-4 — Regulatory Uncertainty Handling

- Each question carries a `regulatory_ref` tag (e.g., `EU_AI_ACT:Article9:2(a)`)
- When implementing acts update scope, a question bank patch is released; exports record the question bank version used at assessment time
- The tool never claims to determine whether a system "is high-risk" — it helps document the risk management process for systems the provider has already classified as high-risk

---

## 9. Technical Specification

### 9.1 Core Domain Model (Pydantic v2)

```python
from pydantic import BaseModel, Field, computed_field
from typing import Literal
from datetime import datetime, UTC
from uuid import UUID, uuid4
from enum import Enum, IntEnum

class AnnexIIICategory(str, Enum):
    biometric = "biometric"
    critical_infrastructure = "critical_infrastructure"
    education = "education"
    employment = "employment"
    essential_services = "essential_services"
    law_enforcement = "law_enforcement"
    migration = "migration"
    justice = "justice"

class AISystem(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    version: str
    purpose: str
    intended_users: list[str]
    inputs: list[str]
    outputs: list[str]
    deployment_context: str
    annex_iii_category: AnnexIIICategory | None = None
    provider_name: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

class Likelihood(IntEnum):
    rare = 1; unlikely = 2; possible = 3; likely = 4; almost_certain = 5

class Severity(IntEnum):
    negligible = 1; minor = 2; moderate = 3; major = 4; critical = 5

class RiskDimension(str, Enum):
    health_safety = "health_safety"
    fundamental_rights = "fundamental_rights"
    discrimination = "discrimination"
    privacy = "privacy"
    transparency = "transparency"
    human_oversight = "human_oversight"
    robustness = "robustness"
    data_governance = "data_governance"

class Mitigation(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    description: str
    control_type: Literal["preventive", "detective", "corrective"]
    owner: str
    status: Literal["planned", "implemented", "verified"]
    evidence_refs: list[str] = []

class RiskItem(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    dimension: RiskDimension
    description: str
    source: Literal["manual", "question_bank", "pattern", "traceforge", "rag_benchmarking"]
    likelihood: Likelihood
    severity: Severity
    mitigations: list[Mitigation] = []
    residual_likelihood: Likelihood
    residual_severity: Severity
    accepted: bool = False
    acceptance_rationale: str = ""
    article_refs: list[str] = []       # e.g. ["Art.9(2)(a)", "Art.14"]
    nist_rmf_ref: str = ""             # e.g. "MANAGE 1.3"
    iso42001_ref: str = ""             # e.g. "Clause 8.4"
    regulatory_status: Literal["settled", "pending_implementing_act"] = "settled"

    @computed_field
    @property
    def risk_score(self) -> int:
        return int(self.likelihood) * int(self.severity)

    @computed_field
    @property
    def residual_risk_score(self) -> int:
        return int(self.residual_likelihood) * int(self.residual_severity)

class RiskRegister(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    system: AISystem
    items: list[RiskItem] = []
    risk_appetite_threshold: int = 9
    assessor_name: str
    assessor_role: str
    assessment_date: datetime = Field(default_factory=lambda: datetime.now(UTC))
    review_date: datetime
    question_bank_version: str

class RiskManagementFile(BaseModel):
    """Article 9 / Annex IV output artefact"""
    id: UUID = Field(default_factory=uuid4)
    schema_version: str = "1.0.0"
    register: RiskRegister
    test_requirements: list[dict] = []
    cross_references: list[dict] = []    # Art.9 clause ↔ risk ↔ NIST ↔ ISO
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    sha256_hash: str = ""
    signed_by: str = ""
    disclosure: str = ""                 # mandatory RAI-1 disclosure, injected at export
```

### 9.2 CLI Command Tree

```
riskforge init                              # scaffold project, 90-second wizard
riskforge init --from-template <category>   # pre-load Annex III question subset

riskforge system show                       # display registered system metadata
riskforge system edit                       # update system metadata interactively

riskforge assess                            # guided 8-dimension risk session (main workflow)
riskforge assess --dimension <name>         # scope to single dimension
riskforge assess --import-rag <path.json>   # ingest rag-benchmarking output
riskforge assess --import-trace <path.json> # ingest TraceForge output
riskforge assess --non-interactive --answers <answers.yaml>  # CI/CD mode

riskforge risk list                         # tabular register view
riskforge risk show <id>                    # detailed single item view
riskforge risk add                          # manual item entry
riskforge risk edit <id>                    # edit item interactively
riskforge risk accept <id> --rationale "..." # record acceptance decision
riskforge risk score <id> --likelihood 3 --severity 4

riskforge tests generate                    # derive test requirements from open risks
riskforge tests list                        # show all test requirements

riskforge validate                          # pre-export readiness check (8 gates)
riskforge status                            # dashboard: open risks, coverage, export readiness

riskforge export --format json [--output rmf.json]
riskforge export --format pdf  [--output rmf.pdf]
riskforge export --format markdown [--output RISK_SUMMARY.md]
riskforge export --sign-with <key.pem>      # attach Sigstore/PGP signature

riskforge verify [--file rmf.json]          # verify hash chain integrity
riskforge diff <rmf_v1.json> <rmf_v2.json>  # show changes between two versions

riskforge serve [--host HOST] [--port 8090] # start API server (requires RISKFORGE_SECRET_KEY)
```

### 9.3 API Endpoints (Server Mode)

```
POST   /api/v1/registers                        # create new register
GET    /api/v1/registers                        # list registers
GET    /api/v1/registers/{id}                   # fetch register
PATCH  /api/v1/registers/{id}                   # update system metadata
DELETE /api/v1/registers/{id}                   # delete register (audit log preserved)

POST   /api/v1/registers/{id}/risks             # add risk item
GET    /api/v1/registers/{id}/risks             # list all risks
PATCH  /api/v1/registers/{id}/risks/{risk_id}   # update risk item
DELETE /api/v1/registers/{id}/risks/{risk_id}   # remove risk item

POST   /api/v1/registers/{id}/import/rag        # ingest rag-benchmarking JSON
POST   /api/v1/registers/{id}/import/trace      # ingest TraceForge JSON

POST   /api/v1/registers/{id}/export/json       # returns RMF JSON
POST   /api/v1/registers/{id}/export/pdf        # returns PDF blob
POST   /api/v1/registers/{id}/validate          # run validation checks

GET    /api/v1/schemas/rmf                      # published JSON Schema (pinned by downstream tools)
GET    /api/v1/health                           # health check
```

### 9.4 Question Bank Schema

```yaml
# question_bank/v1.yaml
version: "1.0.0"
questions:
  - id: HS-001
    dimension: health_safety
    text: "Could the system's outputs directly influence a clinical, safety, or physical decision without mandatory human review?"
    annex_iii_categories: [essential_services, biometric]
    default_severity_hint: 4
    article_refs: ["Art.9(2)(a)", "Art.14"]
    nist_rmf_ref: "MAP 1.5"
    iso42001_ref: "Clause 6.1"
    regulatory_status: settled
```

### 9.5 Integration Contract (Downstream Tools)

RiskForge exports `rmf.schema.json` at a stable URL. Downstream tools pin to this schema version.

**TransparencyDeck** reads: `register.items[].article_refs`, `register.items[].description` (for Art. 13 limitation disclosure), `register.items[dimension=health_safety]` (for intended use restrictions).

**ConformityBot** reads: the full `RiskManagementFile` to generate Annex IV evidence checklist coverage.

**Sigil** reads: `register.items[dimension=human_oversight]` to configure runtime oversight policies.

### 9.6 Key Dependencies

```
# requirements.txt (pinned at release)
click==8.1.7
fastapi==0.111.0
uvicorn[standard]==0.30.1
pydantic>=2.7,<3
pydantic-settings==2.2.1
rich==13.7.1
questionary==2.0.1
weasyprint==62.3
keyring==25.2.1
python-dotenv==1.0.1
httpx==0.27.0         # API server client calls only; never imported in CLI mode
pytest==8.2.0
pytest-socket==0.7.0
pip-audit==2.7.3
```

---

## 10. UX Requirements

### UX-1 — Time Budget

`riskforge assess` first run: 25 minutes maximum. Re-assessment after model update: 10 minutes maximum. Every question must be answerable from the engineer's existing knowledge. No external research should be required mid-session.

### UX-2 — First Run Confidence

After the first `riskforge assess` session, the user must see a non-zero number of identified risks. A zero-risk first run triggers: `No risks identified — this is unusual for a deployed system. Review dimension coverage before exporting.`

### UX-3 — "I Don't Know" is a Valid Answer

`unknown` / `?` records a `knowledge_gap` entry. Session is not invalidated. Knowledge gaps appear prominently in the session summary and in the export as items requiring resolution.

### UX-4 — Progress Display

Single-line status bar during session: `[Dim 3/8 — Fairness] 2 risks found | 1 unknown | ██████░░░░ 60%`. Updates after every question.

### UX-5 — Session Summary

Terminal output at session end:
- Total risks by severity band
- Dimensions with open items
- Knowledge gaps count
- Auto-generated test requirements count
- File path of project file
- Single next-action prompt

### UX-6 — Export: Compliance Officer View

Cover page contains: system name/version, assessment date, assessed by, Annex III category, status badge (COMPLETE / INCOMPLETE), three summary numbers (total risks, open mitigations, knowledge gaps). No jargon above the fold. Page 2 executive summary is readable aloud in a board meeting.

### UX-7 — Trust Signals in Export

- Version-locked methodology reference (RiskForge version + question bank version)
- SHA-256 hash embedded in PDF footer
- Immutable timestamp
- Change log on re-assessments showing what changed since prior version

---

## 11. EU AI Act Cross-Framework Mapping

| Article 9 Clause | RiskForge Feature | NIST AI RMF | ISO 42001 |
|---|---|---|---|
| Art. 9(1) — establish and maintain RMS | RiskRegister lifecycle, version history | GOVERN 1.1–1.7 | Clause 6.1 |
| Art. 9(2)(a) — identify known risks | `riskforge assess` question bank | MAP 1.1–1.6 | Clause A.6 |
| Art. 9(2)(b) — estimate risks under misuse | Risk patterns + dimension coverage | MAP 5.1–5.2 | Clause A.7 |
| Art. 9(2)(c) — post-market monitoring integration | Import from VigilanceDash (future) | MANAGE 4.1 | Clause A.10 |
| Art. 9(2)(d) — adopt risk management measures | Mitigation documentation (FR-4) | MANAGE 1.1–3.2 | Clause 8.4 |
| Art. 9(4) — residual risk disclosure | Residual risk export section | MANAGE 2.2 | Clause 8.4 |
| Art. 9(5)–(7) — testing requirements | `riskforge tests generate` | MEASURE 2.1–2.9 | Clause A.9 |
| Art. 9(8) — affected persons consultation | Knowledge gap entry type | MAP 1.6 | Clause A.7 |
| Art. 9(9) — vulnerable groups | Dimension question HS-V-* | MAP 2.3 | Clause A.7 |
| Art. 9(10) — documentation retention | Append-only audit log, export versioning | GOVERN 6.2 | Clause 7.5 |
| Annex IV — technical documentation | Full RMF export structure | — | — |

**Colorado AI Act (SB 24-205):** A properly completed RiskForge assessment satisfies the Colorado impact assessment obligation with the addition of a `colorado_disclosure` field (provided as a template extension in v1.1).

**Texas HB 1709:** Algorithmic impact assessment and bias audit obligations are substantially covered by the `discrimination` dimension question bank. Full Texas compliance requires the addition of a demographic disparity analysis (integration with rag-benchmarking fairness metrics in v1.2).

---

## 12. Acceptance Criteria

**AC-1** `riskforge init` on a new project completes in under 90 seconds and produces a valid `riskforge.yaml`.

**AC-2** `riskforge assess` on a credit scoring system (Annex III Category 5) auto-loads risk patterns for financial services use cases and presents them for user confirmation.

**AC-3** `riskforge assess --import-rag benchmark_report.json` (where `retrieval_precision: 0.61` and threshold is `0.75`) automatically creates a scored risk item in the Robustness dimension with `source="rag_benchmarking"`.

**AC-4** `riskforge validate` fails (exits non-zero) when any of the 8 dimensions has no entries and has not been explicitly marked not-applicable.

**AC-5** `riskforge export --format json` produces a JSON document that validates against `riskforge/schemas/v1/rmf.schema.json` and contains a non-empty `sha256_hash` field.

**AC-6** `riskforge export --format pdf` produces a PDF containing all 7 required sections (cover, executive summary, methodology, risk register, residual risks, test requirements, audit metadata).

**AC-7** `riskforge verify --file rmf.json` exits 0 when the file is unmodified and exits non-zero when any field has been tampered with after export.

**AC-8** `riskforge assess --non-interactive --answers answers.yaml` completes without interactive prompts and produces the same output as an interactive session with equivalent answers.

**AC-9** The `pytest-socket` test with `disable_socket()` passes in CLI mode — verifying zero outbound network calls.

**AC-10** Running `lcc scan .` on the RiskForge project itself produces zero violations under the `eu-ai-act-compliance` policy.

**AC-11** A compliance officer with no prior RiskForge experience can navigate from cover page to a specific risk item and its associated mitigation in the PDF export without referring to any documentation.

**AC-12** RiskForge's own `riskforge.yaml` and completed `RiskManagementFile` are committed to the GitHub repository as self-attestation.

---

## 13. Success Metrics

| Metric | Target | Window |
|---|---|---|
| PyPI weekly downloads | >1,000 | 90 days after v1.0 |
| GitHub stars | >300 | 6 months |
| Community question bank contributions (PRs) | >20 | 6 months |
| First enterprise conversion | ≥1 paying customer | 4 months after v1.0 |
| PDF export accepted as Article 9 evidence by legal counsel | Documented case study | 6 months |
| Assessment completion time (median) | <20 minutes | measured from telemetry opt-in users |
| Zero critical CVEs in RiskForge dependency tree | Always | ongoing |

---

## 14. Build Plan

### Phase 1 — MVP (6 weeks, 1 engineer)

**Scope:** Complete CLI workflow for a single system; JSON + PDF export; 50-question question bank covering all 8 dimensions; 5×5 scoring; `riskforge validate`; basic `--import-rag` ingestion.

**Deliverables:**
- `riskforge init`, `assess`, `risk list/add/accept/score`, `tests generate`, `validate`, `export json/pdf`
- Question bank v1.0 covering all 8 dimensions (minimum 50 questions)
- PDF export via WeasyPrint (all 7 sections)
- SHA-256 self-verifying export
- `pytest-socket` zero-telemetry gate
- `riskforge.yaml` self-assessment committed to repo

**Key risk:** WeasyPrint PDF layout on complex risk register tables. Validate against a real Annex IV template in Week 2, not Week 6.

### Phase 2 — Integration Layer (4 weeks)

**Scope:** `--import-trace` from TraceForge, pattern library (20 patterns), published `rmf.schema.json`, `riskforge diff`, hash-chain audit log, `riskforge verify`.

**Deliverables:**
- Pattern library v1.0 (20 patterns, 8 Annex III scenarios)
- TraceForge integration
- Published schema for TransparencyDeck / ConformityBot to pin against
- Append-only audit log with hash chain
- `riskforge verify` command

### Phase 3 — API and Web UI (6 weeks)

**Scope:** FastAPI server, Docker Compose stack with lightweight React UI, optional PGP signing.

**Deliverables:**
- `riskforge serve` (FastAPI, port 8090, authenticated)
- Docker Compose: server + optional UI at port 3000
- `--sign-with key.pem` Sigstore/PGP signature block

### Phase 4 — Compliance Hardening and Enterprise (ongoing)

**Scope:** Question bank expanded to 200+ items with legal review, Colorado/Texas extension fields, ISO 42001 automation, NIST AI RMF tagging, Enterprise features (multi-system portfolio, RBAC, Sigil integration).

**Legal review milestone:** Before question bank v2.0 ships, EU AI Act counsel must review all Article 9(2)(a)–(b) questions. This is not optional. The tool generates legally significant documents.

### Build Estimate Summary

| Phase | Duration | Engineer effort |
|---|---|---|
| Phase 1 — MVP | 6 weeks | 1 FTE |
| Phase 2 — Integrations | 4 weeks | 1 FTE |
| Phase 3 — API + UI | 6 weeks | 1–2 FTE |
| Phase 4 — Enterprise | Ongoing | 2 FTE |

---

## 15. What's Out of Scope (Non-Goals)

- RiskForge does **not** determine whether a system is high-risk under Annex III. Self-classification is the provider's obligation under Article 6(2). RiskForge helps document the risk management process for systems already classified.
- RiskForge does **not** certify compliance. It produces documented evidence. Legal compliance determination requires qualified legal counsel and, for notified-body categories, a third-party conformity assessment.
- RiskForge does **not** replace the Article 10 training data governance tool (TraceForge). Data quality risks surface in RiskForge as imported findings, but the primary Article 10 tooling is separate.
- RiskForge does **not** include a vulnerability scanner, penetration tester, or adversarial robustness evaluator. These feed in via rag-benchmarking and external tools.
- RiskForge does **not** generate legal templates (privacy policies, instructions for use). These are outputs of TransparencyDeck.

---

## Appendix A — Stakeholder Review Notes

### Steve Jobs — Final Review

> *"This is the right product. You've made compliance feel like engineering, not paperwork. The 25-minute time budget is ambitious and honest — hold to it. Two things I'd push harder: First, the first run experience is everything. The moment someone runs `riskforge init` for the first time is your only chance to prove the tool understands their problem. Make that wizard feel like it was designed by someone who has actually tried to comply with Article 9, not by someone who read the regulation. Second: the mandatory disclosure is right, but the language is defensive and legal. Rewrite it to be honest and human: 'This document represents your team's best current understanding of the risks in your system. It is a starting point for compliance, not a finish line.' That's the tone that makes compliance officers trust it."*

> *"One more thing: name the patterns. When the tool says 'I found a risk pattern: Facial Recognition in Public Space — Art. 5 Proximity Risk' and explains in plain English why that pattern is serious, that moment is when the engineer stops treating this as a checkbox and starts treating it as a tool that understands their work. Design that moment."*

### Head of AI Governance, Anthropic — Regulatory Validation

> *"The regulatory mapping is accurate. The Article 9 clause-by-clause coverage in FR-6 through FR-10 and the cross-framework table are correct as of April 2026. Two additions required before v1.0 ships: (1) The tool must handle the Article 6(2) self-classification step explicitly — add a pre-assessment check that asks 'Have you determined this system falls under Annex III?' with a Y/N and a documentation field. Do not assume the user has done this. (2) The question bank must include at least 3 questions specifically addressing Article 9(8) (affected persons consultation) and Article 9(9) (vulnerable groups including children). These are the two most frequently missed obligations in practitioner assessments I have reviewed. They are not optional."*

> *"On the legal review requirement for the question bank: this is non-negotiable. Every question in the question bank is implicitly telling a provider what the regulation requires them to consider. An incomplete or inaccurate question could result in a risk being missed and a provider being exposed to enforcement they believed they had addressed. Build the legal review gate into Phase 1, not Phase 4."*

**Consensus rating: 9.2/10 — approved for development commissioning with two conditions:**
1. Article 6(2) self-classification check added to `riskforge init` before v1.0 ships
2. Legal counsel review of question bank v1.0 before PyPI release

---

*Document version: 1.0 | Last updated: April 2026 | Next review: on Phase 1 completion*
