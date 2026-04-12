# RiskForge — Low-Level Design (LLD) v1.0

**Status:** Approved  
**Date:** April 2026  
**Companion:** HLD-RiskForge-v1.0.md, PRD-RiskForge-v1.0.md  
**Reviewed by:** Head of AI System Design (Google), Steve Jobs, Head of AI Governance (Anthropic)  
**Consensus rating: 9.4/10 — approved for implementation**

---

## 1. Complete Package Structure

```
riskforge/                              # repo root
├── pyproject.toml
├── Makefile
├── CONTRIBUTING.md
├── CHANGELOG.md
├── .pre-commit-config.yaml
├── src/
│   └── riskforge/
│       ├── __init__.py                 # version = "0.1.0"; zero server imports
│       │
│       ├── cli/                        # INTERFACE — Typer commands only; zero business logic
│       │   ├── __init__.py
│       │   ├── main.py                 # app = typer.Typer(); registers all subcommands
│       │   └── commands/
│       │       ├── init.py             # riskforge init
│       │       ├── system.py           # riskforge system show/edit
│       │       ├── assess.py           # riskforge assess
│       │       ├── risk.py             # riskforge risk list/add/edit/accept/score
│       │       ├── tests_cmd.py        # riskforge tests generate/list
│       │       ├── validate.py         # riskforge validate
│       │       ├── export.py           # riskforge export
│       │       ├── verify.py           # riskforge verify
│       │       ├── diff.py             # riskforge diff
│       │       ├── import_cmd.py       # riskforge import
│       │       └── serve.py            # riskforge serve (lazy import of server)
│       │
│       ├── engine/                     # BUSINESS LOGIC — no CLI/server imports
│       │   ├── __init__.py
│       │   ├── risk.py                 # RiskEngine: CRUD, scoring, scoring matrix
│       │   ├── assess.py               # AssessEngine: question runner, pattern matcher
│       │   ├── validate.py             # ValidateEngine: 8 readiness gates
│       │   ├── export.py               # ExportEngine: hash, sign, dispatch to exporters
│       │   ├── audit.py                # AuditEngine: append-only log, hash chain, verify
│       │   ├── tests.py                # TestDerivationEngine: risk → test requirements
│       │   └── migrations.py           # MigrationRunner: schema version upgrades
│       │
│       ├── models/                     # Pydantic v2 data models
│       │   ├── __init__.py
│       │   ├── system.py               # AISystem, AnnexIIICategory
│       │   ├── risk.py                 # RiskItem, Mitigation, Likelihood, Severity
│       │   ├── register.py             # RiskRegister
│       │   ├── rmf.py                  # RiskManagementFile (export artefact)
│       │   └── audit.py                # AuditEntry
│       │
│       ├── storage/                    # STORAGE — StorageBackend ABC + FileStore
│       │   ├── __init__.py
│       │   ├── base.py                 # StorageBackend ABC (async methods)
│       │   └── filesystem.py           # FileStore: YAML + JSONL implementation
│       │
│       ├── plugins/                    # PLUGIN REGISTRY
│       │   ├── __init__.py
│       │   ├── registry.py             # discovers entry_points at runtime
│       │   └── loader.py               # loads question banks, exporters, adapters
│       │
│       ├── exporters/                  # BUILT-IN EXPORTERS
│       │   ├── base.py                 # Exporter ABC
│       │   ├── json_exporter.py
│       │   ├── markdown_exporter.py
│       │   └── pdf/
│       │       ├── pdf_exporter.py     # WeasyPrint renderer
│       │       └── templates/
│       │           ├── report.html     # Jinja2 template
│       │           └── report.css
│       │
│       ├── adapters/                   # BUILT-IN INTEGRATION ADAPTERS
│       │   ├── base.py                 # IntegrationAdapter Protocol
│       │   ├── rag_benchmarking.py     # RAGBenchmarkingAdapter
│       │   └── traceforge.py           # TraceForgeAdapter
│       │
│       ├── server/                     # OPTIONAL SERVER (never imported by CLI)
│       │   ├── __init__.py
│       │   ├── app.py                  # FastAPI app + lifespan
│       │   ├── auth.py                 # Bearer token issuance, validation
│       │   ├── middleware.py           # CorrelationID, structlog, rate limiting
│       │   ├── metrics.py              # Prometheus /metrics
│       │   └── routers/
│       │       ├── registers.py
│       │       ├── risks.py
│       │       ├── exports.py
│       │       ├── webhooks.py
│       │       └── health.py
│       │
│       ├── migrations/                 # SCHEMA MIGRATIONS
│       │   └── m0001_initial.py        # up(data) → data; down(data) → data
│       │
│       └── _data/                      # BUNDLED DATA (shipped in wheel)
│           ├── question_bank/
│           │   ├── health_safety.yaml
│           │   ├── fundamental_rights.yaml
│           │   ├── discrimination.yaml
│           │   ├── privacy.yaml
│           │   ├── transparency.yaml
│           │   ├── human_oversight.yaml
│           │   ├── robustness.yaml
│           │   └── data_governance.yaml
│           ├── patterns/
│           │   └── patterns.yaml       # 20+ Annex III risk patterns
│           ├── schemas/
│           │   └── rmf.schema.json
│           └── templates/
│               └── (symlink to exporters/pdf/templates/)
│
├── tests/
│   ├── conftest.py
│   ├── unit/                           # engine/ and models/ tests
│   ├── integration/                    # CLI end-to-end tests
│   ├── contract/                       # rmf.schema.json validation
│   ├── boundary/                       # import boundary enforcement
│   └── fixtures/
│       ├── systems/                    # sample AISystem YAML
│       ├── registers/                  # sample RiskRegister YAML
│       ├── upstream/                   # rag-benchmarking + TraceForge sample JSON
│       └── exports/                    # sample rmf.json + rmf.pdf
│
└── docker/
    ├── Dockerfile
    ├── docker-compose.yml
    └── docker-compose.enterprise.yml
```

---

## 2. pyproject.toml

```toml
[build-system]
requires = ["hatchling>=1.21"]
build-backend = "hatchling.build"

[project]
name = "riskforge"
version = "0.1.0"
description = "EU AI Act Article 9 Risk Management System — OSS CLI"
readme = "README.md"
license = {text = "Apache-2.0"}
requires-python = ">=3.11"
authors = [{name = "AiExponent LLC", email = "hello@aiexponent.com"}]
keywords = ["eu-ai-act", "article-9", "risk-management", "compliance", "ai-governance"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python :: 3.11",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
]
dependencies = [
    "typer[all]==0.12.3",
    "pydantic==2.7.1",
    "pydantic-settings==2.2.1",
    "pyyaml==6.0.1",
    "jsonschema==4.22.0",
    "weasyprint==62.3",
    "jinja2==3.1.4",
    "rich==13.7.1",
    "questionary==2.0.1",
    "keyring==25.2.1",
    "python-dotenv==1.0.1",
]

[project.optional-dependencies]
server = [
    "fastapi==0.111.0",
    "uvicorn[standard]==0.29.0",
    "prometheus-client==0.20.0",
    "structlog==24.1.0",
    "slowapi==0.1.9",
]
dev = ["riskforge[server,test]", "pre-commit==3.7.1", "hatch==1.9.4", "pip-audit==2.7.3"]
test = [
    "pytest==8.2.0",
    "pytest-cov==5.0.0",
    "pytest-socket==0.7.0",
    "pytest-asyncio==0.23.6",
    "httpx==0.27.0",
    "bandit==1.7.8",
]

[project.scripts]
riskforge = "riskforge.cli.main:app"

[project.entry-points."riskforge.question_banks"]
health_safety       = "riskforge.plugins.builtin:HealthSafetyBank"
fundamental_rights  = "riskforge.plugins.builtin:FundamentalRightsBank"
discrimination      = "riskforge.plugins.builtin:DiscriminationBank"
privacy             = "riskforge.plugins.builtin:PrivacyBank"
transparency        = "riskforge.plugins.builtin:TransparencyBank"
human_oversight     = "riskforge.plugins.builtin:HumanOversightBank"
robustness          = "riskforge.plugins.builtin:RobustnessBank"
data_governance     = "riskforge.plugins.builtin:DataGovernanceBank"

[project.entry-points."riskforge.exporters"]
json     = "riskforge.exporters.json_exporter:JSONExporter"
pdf      = "riskforge.exporters.pdf.pdf_exporter:PDFExporter"
markdown = "riskforge.exporters.markdown_exporter:MarkdownExporter"

[project.entry-points."riskforge.adapters"]
rag-benchmarking = "riskforge.adapters.rag_benchmarking:RAGBenchmarkingAdapter"
traceforge        = "riskforge.adapters.traceforge:TraceForgeAdapter"

[tool.hatch.build.targets.wheel]
packages = ["src/riskforge"]

[tool.hatch.build.targets.wheel.force-include]
"src/riskforge/_data" = "riskforge/_data"

[tool.ruff]
line-length = 100
target-version = "py311"
select = ["E", "F", "I", "UP", "S", "B"]
ignore = ["S101"]  # allow assert in tests

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
addopts = "--strict-markers --disable-socket"

[tool.coverage.run]
source = ["src/riskforge"]
branch = true

[tool.coverage.report]
fail_under = 80
```

---

## 3. Complete Data Models (Pydantic v2)

```python
# src/riskforge/models/system.py
from __future__ import annotations
from datetime import datetime, UTC
from enum import Enum
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class AnnexIIICategory(str, Enum):
    biometric               = "biometric"
    critical_infrastructure = "critical_infrastructure"
    education               = "education"
    employment              = "employment"
    essential_services      = "essential_services"
    law_enforcement         = "law_enforcement"
    migration               = "migration"
    justice                 = "justice"


class AISystem(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    version: str
    purpose: str                            # one sentence; used in PDF executive summary
    intended_users: list[str]
    inputs: list[str]                       # e.g. ["text", "structured_data"]
    outputs: list[str]                      # e.g. ["classification", "score"]
    deployment_context: str
    annex_iii_category: AnnexIIICategory | None = None
    annex_iii_self_classification_documented: bool = False   # AC: Art. 6(2) gate
    provider_name: str
    provider_contact: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    schema_version: str = "1.0.0"
```

```python
# src/riskforge/models/risk.py
from __future__ import annotations
from datetime import datetime, UTC
from enum import IntEnum, Enum
from typing import Literal
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, computed_field


class Likelihood(IntEnum):
    rare           = 1
    unlikely       = 2
    possible       = 3
    likely         = 4
    almost_certain = 5


class Severity(IntEnum):
    negligible = 1
    minor      = 2
    moderate   = 3
    major      = 4
    critical   = 5


class RiskDimension(str, Enum):
    health_safety      = "health_safety"
    fundamental_rights = "fundamental_rights"
    discrimination     = "discrimination"
    privacy            = "privacy"
    transparency       = "transparency"
    human_oversight    = "human_oversight"
    robustness         = "robustness"
    data_governance    = "data_governance"


class Mitigation(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    description: str
    control_type: Literal["preventive", "detective", "corrective"]
    owner: str
    status: Literal["planned", "implemented", "verified"]
    evidence_refs: list[str] = []
    is_vague: bool = False                  # auto-flagged if description is generic


class RiskItem(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    dimension: RiskDimension
    title: str
    description: str
    source: Literal["manual", "question_bank", "pattern", "traceforge", "rag_benchmarking"]
    likelihood: Likelihood
    severity: Severity
    mitigations: list[Mitigation] = []
    residual_likelihood: Likelihood
    residual_severity: Severity
    accepted: bool = False
    acceptance_rationale: str = ""
    identified_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    article_refs: list[str] = []            # e.g. ["Art.9(2)(a)", "Art.14"]
    nist_rmf_ref: str = ""                  # e.g. "MANAGE 1.3"
    iso42001_ref: str = ""                  # e.g. "Clause 8.4"
    regulatory_status: Literal["settled", "pending_implementing_act"] = "settled"
    knowledge_gap: bool = False             # true when source answer was "unknown"
    source_ref: str = ""                    # e.g. "rag:pipeline_001", "traceforge:lineage_042"
    tags: list[str] = []

    @computed_field
    @property
    def risk_score(self) -> int:
        return int(self.likelihood) * int(self.severity)

    @computed_field
    @property
    def residual_risk_score(self) -> int:
        return int(self.residual_likelihood) * int(self.residual_severity)

    @computed_field
    @property
    def risk_band(self) -> Literal["low", "medium", "high", "critical"]:
        s = self.risk_score
        if s <= 4:   return "low"
        if s <= 9:   return "medium"
        if s <= 16:  return "high"
        return "critical"
```

```python
# src/riskforge/models/register.py
from __future__ import annotations
from datetime import datetime, UTC
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from riskforge.models.system import AISystem
from riskforge.models.risk import RiskItem, RiskDimension


class RiskRegister(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    system: AISystem
    items: list[RiskItem] = []
    risk_appetite_threshold: int = 9        # scores > threshold require mitigation/acceptance
    assessor_name: str
    assessor_role: str
    assessment_date: datetime = Field(default_factory=lambda: datetime.now(UTC))
    review_date: datetime
    question_bank_version: str
    schema_version: str = "1.0.0"

    def covered_dimensions(self) -> set[RiskDimension]:
        return {item.dimension for item in self.items}

    def open_items(self) -> list[RiskItem]:
        """Risk items above appetite threshold that are neither mitigated nor accepted."""
        return [
            i for i in self.items
            if i.residual_risk_score > self.risk_appetite_threshold
            and not i.accepted
        ]

    def knowledge_gaps(self) -> list[RiskItem]:
        return [i for i in self.items if i.knowledge_gap]
```

```python
# src/riskforge/models/rmf.py  (export artefact)
from __future__ import annotations
from datetime import datetime, UTC
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from riskforge.models.register import RiskRegister


class CrossReference(BaseModel):
    article_ref: str            # e.g. "Art.9(2)(a)"
    risk_item_ids: list[UUID]
    nist_rmf_ref: str           # e.g. "MAP 1.1"
    iso42001_ref: str           # e.g. "Clause 6.1"


class TestRequirement(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    risk_item_id: UUID
    description: str
    metric_type: str            # e.g. "demographic_parity", "faithfulness"
    threshold_range: str        # e.g. ">= 0.85"
    article_ref: str            # e.g. "Art.9(7)"


class RiskManagementFile(BaseModel):
    """The Article 9 / Annex IV output artefact. Self-verifying via sha256_hash."""
    id: UUID = Field(default_factory=uuid4)
    rmf_schema_version: str = "1.0.0"
    register: RiskRegister
    test_requirements: list[TestRequirement] = []
    cross_references: list[CrossReference] = []
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    sha256_hash: str = ""       # computed over canonical JSON with this field = ""
    signed_by: str = ""         # optional Sigstore/PGP signer identity
    audit_entry_hash: str = ""  # hash of the rmf.exported audit log entry
    disclosure: str = (
        "This document was produced using RiskForge, with question bank version "
        "{qb_version}. It represents the team's documented risk assessment and has "
        "not been reviewed by a qualified legal professional. It does not constitute "
        "legal advice under the EU AI Act or any other regulation."
    )
```

```python
# src/riskforge/models/audit.py
from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel


class AuditActor(BaseModel):
    type: str                   # "human" | "ci" | "api"
    identity: str               # email, service account, or "anonymous"


class AuditEntry(BaseModel):
    seq: int
    event: str                  # e.g. "risk_item.updated", "rmf.exported"
    timestamp: datetime
    actor: AuditActor
    system_id: str
    payload: dict               # event-specific data (old/new values, migration_id, etc.)
    prev_hash: str              # "0000000000" for seq=0
    entry_hash: str             # SHA-256(prev_hash + canonical_JSON(all other fields))
```

---

## 4. Storage Backend

```python
# src/riskforge/storage/base.py
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import AsyncIterator
from riskforge.models.system import AISystem
from riskforge.models.register import RiskRegister
from riskforge.models.audit import AuditEntry


class StorageBackend(ABC):

    @abstractmethod
    async def init_project(self, project_id: str, metadata: dict) -> None: ...

    @abstractmethod
    async def write_system(self, system_id: str, data: AISystem) -> None: ...

    @abstractmethod
    async def read_system(self, system_id: str) -> AISystem: ...

    @abstractmethod
    async def write_register(self, system_id: str, register: RiskRegister) -> None: ...

    @abstractmethod
    async def read_register(self, system_id: str) -> RiskRegister: ...

    @abstractmethod
    async def list_systems(self) -> list[str]: ...

    @abstractmethod
    async def append_audit(self, entry: AuditEntry) -> None: ...

    @abstractmethod
    async def read_audit(
        self,
        system_id: str | None = None,
        since_seq: int = 0,
    ) -> AsyncIterator[AuditEntry]: ...

    @abstractmethod
    async def verify_chain(self) -> tuple[bool, list[str]]:
        """Returns (is_valid, list_of_violation_descriptions).""" ...

    @abstractmethod
    async def write_export(
        self,
        system_id: str,
        export_id: str,
        payload: bytes,
        fmt: str,
    ) -> str:
        """Writes export file; returns URI or absolute path.""" ...
```

```python
# src/riskforge/storage/filesystem.py  (OSS implementation)
import asyncio, hashlib, json, uuid
from pathlib import Path
from typing import AsyncIterator
import yaml
from riskforge.storage.base import StorageBackend
from riskforge.models.audit import AuditEntry

SENTINEL = ".nodelete"

class FileStore(StorageBackend):
    """Stores project state as YAML + JSONL under .riskforge/ directory."""

    def __init__(self, project_dir: Path) -> None:
        self._root = project_dir / ".riskforge"
        self._audit_path = self._root / "audit.jsonl"
        self._systems_dir = project_dir / "systems"

    def _ensure_dirs(self) -> None:
        self._root.mkdir(mode=0o700, parents=True, exist_ok=True)
        self._systems_dir.mkdir(exist_ok=True)
        sentinel = self._root / SENTINEL
        if not sentinel.exists():
            sentinel.write_text("Do not delete this directory. It contains the RiskForge audit log.\n")

    async def init_project(self, project_id: str, metadata: dict) -> None:
        await asyncio.to_thread(self._ensure_dirs)
        manifest = {"project_id": project_id, "schema_version": "1.0.0", **metadata}
        manifest_path = self._root.parent / "riskforge.yaml"
        await asyncio.to_thread(
            manifest_path.write_text, yaml.dump(manifest, sort_keys=False)
        )
        manifest_path.chmod(0o600)

    async def append_audit(self, entry: AuditEntry) -> None:
        line = json.dumps(entry.model_dump(mode="json"), separators=(",", ":")) + "\n"
        await asyncio.to_thread(
            lambda: self._audit_path.open("a").write(line)
        )

    async def verify_chain(self) -> tuple[bool, list[str]]:
        violations: list[str] = []
        prev_hash = "0000000000"
        async for entry in self.read_audit():
            expected = self._compute_hash(prev_hash, entry)
            if entry.entry_hash != expected:
                violations.append(f"seq={entry.seq}: hash mismatch (tampered or corrupted)")
            prev_hash = entry.entry_hash
        return (len(violations) == 0, violations)

    @staticmethod
    def _compute_hash(prev_hash: str, entry: AuditEntry) -> str:
        data = entry.model_dump(mode="json")
        data.pop("entry_hash", None)
        canonical = json.dumps({"prev_hash": prev_hash, **data}, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    # ... (write_system, read_register, etc. follow same async pattern)
```

---

## 5. AuditEngine

```python
# src/riskforge/engine/audit.py
from __future__ import annotations
import hashlib, json
from datetime import datetime, UTC
from riskforge.models.audit import AuditEntry, AuditActor
from riskforge.storage.base import StorageBackend


class AuditEngine:
    """Manages the append-only, hash-chained audit log."""

    def __init__(self, storage: StorageBackend, actor: AuditActor) -> None:
        self._storage = storage
        self._actor = actor
        self._last_hash: str | None = None   # cached from last read

    async def _last_entry_hash(self) -> str:
        last = "0000000000"
        async for entry in self._storage.read_audit():
            last = entry.entry_hash
        return last

    async def record(self, event: str, system_id: str, payload: dict) -> AuditEntry:
        """Validates chain continuity BEFORE writing, then appends."""
        is_valid, violations = await self._storage.verify_chain()
        if not is_valid:
            raise AuditChainCorruptError(
                f"Audit chain corrupt before write: {violations}. "
                "Run `riskforge verify` to diagnose."
            )
        prev_hash = await self._last_entry_hash()
        seq = await self._next_seq()
        entry = AuditEntry(
            seq=seq,
            event=event,
            timestamp=datetime.now(UTC),
            actor=self._actor,
            system_id=system_id,
            payload=payload,
            prev_hash=prev_hash,
            entry_hash="",      # computed below
        )
        entry.entry_hash = self._compute_hash(prev_hash, entry)
        await self._storage.append_audit(entry)
        return entry

    @staticmethod
    def _compute_hash(prev_hash: str, entry: AuditEntry) -> str:
        data = entry.model_dump(mode="json")
        data["entry_hash"] = ""
        canonical = json.dumps(
            {"prev_hash": prev_hash, **data}, sort_keys=True, separators=(",", ":")
        )
        return hashlib.sha256(canonical.encode()).hexdigest()

    async def _next_seq(self) -> int:
        last = 0
        async for entry in self._storage.read_audit():
            last = entry.seq
        return last + 1


class AuditChainCorruptError(RuntimeError):
    """Raised when the audit chain fails pre-write validation."""
```

---

## 6. Risk Scoring Engine

```python
# src/riskforge/engine/risk.py
from __future__ import annotations
from riskforge.models.risk import RiskItem, Likelihood, Severity, RiskDimension
from riskforge.storage.base import StorageBackend
from riskforge.engine.audit import AuditEngine


VAGUE_PHRASES = {
    "we'll monitor it", "to be determined", "tbd", "n/a",
    "will address later", "monitor", "ongoing", "review"
}


class RiskEngine:
    """CRUD and scoring for risk items. All writes emit audit entries."""

    def __init__(self, storage: StorageBackend, audit: AuditEngine) -> None:
        self._storage = storage
        self._audit = audit

    async def add_risk(self, system_id: str, item: RiskItem) -> RiskItem:
        item.mitigations = [self._flag_vague(m) for m in item.mitigations]
        register = await self._storage.read_register(system_id)
        register.items.append(item)
        await self._storage.write_register(system_id, register)
        await self._audit.record(
            "risk_item.created", system_id,
            {"risk_item_id": str(item.id), "dimension": item.dimension, "score": item.risk_score}
        )
        return item

    async def accept_risk(
        self, system_id: str, risk_id: str, rationale: str, actor_identity: str
    ) -> RiskItem:
        if not rationale.strip():
            raise ValueError("Acceptance rationale is required and cannot be empty.")
        register = await self._storage.read_register(system_id)
        item = next((i for i in register.items if str(i.id) == risk_id), None)
        if item is None:
            raise RiskNotFoundError(risk_id)
        old_accepted = item.accepted
        item.accepted = True
        item.acceptance_rationale = rationale
        await self._storage.write_register(system_id, register)
        await self._audit.record(
            "risk.accepted", system_id, {
                "risk_item_id": risk_id,
                "old_accepted": old_accepted,
                "rationale_hash": self._hash_rationale(rationale),
                "actor": actor_identity,
            }
        )
        return item

    @staticmethod
    def _flag_vague(mitigation) -> "Mitigation":
        from riskforge.models.risk import Mitigation
        mitigation.is_vague = any(
            phrase in mitigation.description.lower() for phrase in VAGUE_PHRASES
        )
        return mitigation

    @staticmethod
    def _hash_rationale(rationale: str) -> str:
        import hashlib
        return hashlib.sha256(rationale.encode()).hexdigest()[:16]


class RiskNotFoundError(KeyError):
    pass
```

---

## 7. ValidateEngine — 8 Readiness Gates

```python
# src/riskforge/engine/validate.py
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from riskforge.models.register import RiskRegister
from riskforge.models.risk import RiskDimension


class GateStatus(str, Enum):
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"


@dataclass
class GateResult:
    gate_id: str
    description: str
    status: GateStatus
    details: str = ""


class ValidateEngine:
    """Pre-export readiness checks. FAIL gates block export (unless --force)."""

    ALL_DIMENSIONS = set(RiskDimension)

    def run(self, register: RiskRegister) -> list[GateResult]:
        return [
            self._gate_dimensions_covered(register),
            self._gate_article_6_classification(register),
            self._gate_high_risks_addressed(register),
            self._gate_knowledge_gaps_have_tests(register),
            self._gate_metadata_complete(register),
            self._gate_assessor_identity(register),
            self._gate_low_score_warning(register),
            self._gate_vague_mitigations(register),
        ]

    def _gate_dimensions_covered(self, r: RiskRegister) -> GateResult:
        covered = r.covered_dimensions()
        missing = self.ALL_DIMENSIONS - covered
        if missing:
            return GateResult(
                "G1", "All 8 risk dimensions have entries",
                GateStatus.FAIL,
                f"Missing: {', '.join(d.value for d in missing)}. "
                "Mark as not-applicable with a justification or add a risk item."
            )
        return GateResult("G1", "All 8 risk dimensions have entries", GateStatus.PASS)

    def _gate_article_6_classification(self, r: RiskRegister) -> GateResult:
        if not r.system.annex_iii_self_classification_documented:
            return GateResult(
                "G2", "Article 6(2) self-classification documented",
                GateStatus.FAIL,
                "Provider must confirm Annex III self-classification before export. "
                "Run `riskforge system edit` and set annex_iii_self_classification_documented=true."
            )
        return GateResult("G2", "Article 6(2) self-classification documented", GateStatus.PASS)

    def _gate_high_risks_addressed(self, r: RiskRegister) -> GateResult:
        open_items = r.open_items()
        if open_items:
            return GateResult(
                "G3", "All high-scoring risks mitigated or accepted",
                GateStatus.FAIL,
                f"{len(open_items)} risk(s) above threshold not accepted or mitigated: "
                + ", ".join(str(i.id)[:8] for i in open_items)
            )
        return GateResult("G3", "All high-scoring risks mitigated or accepted", GateStatus.PASS)

    def _gate_knowledge_gaps_have_tests(self, r: RiskRegister) -> GateResult:
        gaps_without_tests = [i for i in r.knowledge_gaps() if not i.tags]  # simplified check
        if gaps_without_tests:
            return GateResult(
                "G4", "Knowledge gaps have test requirements",
                GateStatus.WARN,
                f"{len(gaps_without_tests)} knowledge gap(s) without test requirements. "
                "Run `riskforge tests generate` to derive tests."
            )
        return GateResult("G4", "Knowledge gaps have test requirements", GateStatus.PASS)

    def _gate_metadata_complete(self, r: RiskRegister) -> GateResult:
        required = [r.system.name, r.system.version, r.system.purpose, r.system.provider_name]
        if not all(required):
            return GateResult(
                "G5", "System metadata complete",
                GateStatus.FAIL,
                "Missing required fields: name, version, purpose, or provider_name."
            )
        return GateResult("G5", "System metadata complete", GateStatus.PASS)

    def _gate_assessor_identity(self, r: RiskRegister) -> GateResult:
        if not r.assessor_name.strip() or not r.assessor_role.strip():
            return GateResult(
                "G6", "Assessor identity recorded",
                GateStatus.FAIL, "assessor_name and assessor_role are required."
            )
        return GateResult("G6", "Assessor identity recorded", GateStatus.PASS)

    def _gate_low_score_warning(self, r: RiskRegister) -> GateResult:
        if r.items and all(i.risk_score <= 4 for i in r.items):
            return GateResult(
                "G7", "Risk score distribution plausible",
                GateStatus.WARN,
                "All risks scored low (≤4). This is unusual and may reduce regulator confidence. "
                "Review scoring before export."
            )
        return GateResult("G7", "Risk score distribution plausible", GateStatus.PASS)

    def _gate_vague_mitigations(self, r: RiskRegister) -> GateResult:
        vague = [
            m for i in r.items for m in i.mitigations if m.is_vague
        ]
        if vague:
            return GateResult(
                "G8", "No vague mitigations",
                GateStatus.WARN,
                f"{len(vague)} mitigation(s) flagged as vague. "
                "Replace generic descriptions with specific control measures."
            )
        return GateResult("G8", "No vague mitigations", GateStatus.PASS)
```

---

## 8. ExportEngine

```python
# src/riskforge/engine/export.py
from __future__ import annotations
import hashlib, json
from pathlib import Path
from riskforge.models.rmf import RiskManagementFile
from riskforge.plugins.registry import PluginRegistry
from riskforge.engine.audit import AuditEngine


class ExportEngine:
    """Dispatches to registered Exporter plugins; signs and hashes the output."""

    DISCLOSURE_TEMPLATE = (
        "This document was produced using RiskForge v{version}, "
        "question bank version {qb_version}. "
        "It represents the team's documented risk assessment and has not been "
        "reviewed by a qualified legal professional. "
        "It does not constitute legal advice under the EU AI Act or any other regulation."
    )

    def __init__(self, registry: PluginRegistry, audit: AuditEngine) -> None:
        self._registry = registry
        self._audit = audit

    async def export(
        self,
        rmf: RiskManagementFile,
        fmt: str,
        output_path: Path,
        sign_with: Path | None = None,
    ) -> Path:
        # 1. Inject mandatory disclosure
        from importlib.metadata import version as pkg_version
        rmf.disclosure = self.DISCLOSURE_TEMPLATE.format(
            version=pkg_version("riskforge"),
            qb_version=rmf.register.question_bank_version,
        )

        # 2. Compute SHA-256 over canonical JSON (payload_hash field = "")
        rmf.sha256_hash = ""
        canonical = json.dumps(
            rmf.model_dump(mode="json"), sort_keys=True, separators=(",", ":")
        )
        rmf.sha256_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()

        # 3. Validate against rmf.schema.json (raises SchemaViolationError on failure)
        self._validate_schema(rmf)

        # 4. Dispatch to exporter plugin
        exporter = self._registry.get_exporter(fmt)
        payload: bytes = exporter.render(rmf)

        # 5. Write to output path (chmod 600)
        output_path.write_bytes(payload)
        output_path.chmod(0o600)

        # 6. Optional Sigstore/PGP signing
        if sign_with:
            self._sign(output_path, sign_with)

        # 7. Emit audit log entry
        entry = await self._audit.record(
            "rmf.exported",
            system_id=str(rmf.register.system.id),
            payload={"export_id": str(rmf.id), "format": fmt, "sha256": rmf.sha256_hash},
        )
        rmf.audit_entry_hash = entry.entry_hash

        return output_path

    def _validate_schema(self, rmf: RiskManagementFile) -> None:
        import jsonschema
        from importlib.resources import files
        schema_text = files("riskforge._data.schemas").joinpath("rmf.schema.json").read_text()
        schema = json.loads(schema_text)
        try:
            jsonschema.validate(rmf.model_dump(mode="json"), schema)
        except jsonschema.ValidationError as e:
            raise SchemaViolationError(f"RMF schema violation: {e.message}") from e

    def _sign(self, path: Path, key_path: Path) -> None:
        import subprocess
        subprocess.run(["gpg", "--detach-sign", "--armor", str(path)], check=True)


class SchemaViolationError(RuntimeError):
    """Raised when an RMF document fails schema validation at export time."""
```

---

## 9. Integration Adapters

```python
# src/riskforge/adapters/base.py
from __future__ import annotations
from typing import Protocol, runtime_checkable
from riskforge.models.risk import RiskItem, RiskDimension, Likelihood, Severity


@runtime_checkable
class IntegrationAdapter(Protocol):
    adapter_id: str
    supported_schema_range: str     # semver range e.g. "^1.0.0"

    def validate(self, data: dict) -> None:
        """Raise AdapterSchemaError if data is incompatible."""
        ...

    def transform(self, data: dict) -> list[RiskItem]:
        """Map upstream data fields to RiskItem objects."""
        ...


class AdapterSchemaError(ValueError):
    """Raised when an upstream report's schema version is incompatible."""
```

```python
# src/riskforge/adapters/rag_benchmarking.py
from __future__ import annotations
from packaging.version import Version
from riskforge.adapters.base import IntegrationAdapter, AdapterSchemaError
from riskforge.models.risk import RiskItem, RiskDimension, Likelihood, Severity
import uuid


class RAGBenchmarkingAdapter:
    adapter_id = "rag-benchmarking"
    supported_schema_range = "^1.0.0"

    # Metric thresholds below which a risk item is generated
    THRESHOLDS = {
        "faithfulness":     0.85,
        "answer_relevance": 0.80,
        "context_recall":   0.75,
    }

    def validate(self, data: dict) -> None:
        version_str = data.get("schema_version", "0.0.0")
        v = Version(version_str)
        if v.major != 1:
            raise AdapterSchemaError(
                f"rag-benchmarking report schema v{version_str} not supported "
                f"by this adapter (supports ^1.0.0). "
                "Upgrade riskforge or pin rag-benchmarking to v1.x."
            )

    def transform(self, data: dict) -> list[RiskItem]:
        self.validate(data)
        items: list[RiskItem] = []
        metrics = data.get("metrics", {})
        pipeline_id = data.get("pipeline_id", "unknown")

        for metric_name, threshold in self.THRESHOLDS.items():
            value = metrics.get(metric_name)
            if value is not None and value < threshold:
                gap = threshold - value
                likelihood = Likelihood.likely if gap > 0.15 else Likelihood.possible
                severity = Severity.major if gap > 0.20 else Severity.moderate
                items.append(RiskItem(
                    dimension=RiskDimension.robustness,
                    title=f"Accuracy below threshold: {metric_name}",
                    description=(
                        f"rag-benchmarking reports {metric_name}={value:.3f}, "
                        f"below threshold {threshold}. Pipeline: {pipeline_id}."
                    ),
                    source="rag_benchmarking",
                    source_ref=f"rag:{pipeline_id}",
                    likelihood=likelihood,
                    severity=severity,
                    residual_likelihood=likelihood,
                    residual_severity=severity,
                    article_refs=["Art.9(2)(a)", "Art.9(7)", "Art.15"],
                    nist_rmf_ref="MEASURE 2.5",
                    iso42001_ref="Clause A.9",
                ))
        return items
```

---

## 10. Plugin Registry

```python
# src/riskforge/plugins/registry.py
from __future__ import annotations
import importlib.metadata
from riskforge.adapters.base import IntegrationAdapter
from riskforge.exporters.base import Exporter


class PluginRegistry:
    """Discovers and caches all entry_point-registered plugins."""

    _GROUPS = {
        "exporters":      "riskforge.exporters",
        "adapters":       "riskforge.adapters",
        "question_banks": "riskforge.question_banks",
    }

    def __init__(self) -> None:
        self._exporters:      dict[str, type[Exporter]]           = {}
        self._adapters:       dict[str, type[IntegrationAdapter]] = {}
        self._question_banks: dict[str, object]                   = {}

    def load_all(self) -> None:
        for ep in importlib.metadata.entry_points(group=self._GROUPS["exporters"]):
            self._exporters[ep.name] = ep.load()
        for ep in importlib.metadata.entry_points(group=self._GROUPS["adapters"]):
            self._adapters[ep.name] = ep.load()
        for ep in importlib.metadata.entry_points(group=self._GROUPS["question_banks"]):
            self._question_banks[ep.name] = ep.load()

    def get_exporter(self, name: str) -> Exporter:
        cls = self._exporters.get(name)
        if cls is None:
            raise PluginNotFoundError(f"No exporter registered for format '{name}'")
        return cls()

    def get_adapter(self, name: str) -> IntegrationAdapter:
        cls = self._adapters.get(name)
        if cls is None:
            raise PluginNotFoundError(
                f"No adapter registered for source '{name}'. "
                f"Available: {list(self._adapters)}"
            )
        return cls()

    def list_exporters(self) -> list[str]:
        return list(self._exporters)

    def list_adapters(self) -> list[str]:
        return list(self._adapters)


class PluginNotFoundError(KeyError):
    pass
```

---

## 11. Question Bank Schema

```yaml
# src/riskforge/_data/question_bank/health_safety.yaml
schema_version: "1.0.0"
dimension: health_safety
questions:
  - id: HS-001
    text: "Could the system's outputs directly influence a clinical, safety, or physical decision without mandatory human review?"
    guidance: "Consider decisions about medication dosing, surgical planning, vehicle operation, equipment control, or emergency dispatch."
    annex_iii_categories: [essential_services, critical_infrastructure, biometric]
    default_likelihood_hint: 3
    default_severity_hint: 4
    article_refs: ["Art.9(2)(a)", "Art.14(1)"]
    nist_rmf_ref: "MAP 1.5"
    iso42001_ref: "Clause 6.1"
    regulatory_status: settled

  - id: HS-002
    text: "Could a system failure (incorrect output, unavailability) cause physical harm to end users or third parties?"
    guidance: "Failure modes include false negatives in medical screening, incorrect routing in emergency services, or missed safety-critical alerts."
    annex_iii_categories: [critical_infrastructure, essential_services]
    default_likelihood_hint: 2
    default_severity_hint: 5
    article_refs: ["Art.9(2)(b)"]
    nist_rmf_ref: "MAP 5.1"
    iso42001_ref: "Clause 6.1"
    regulatory_status: settled

  - id: HS-003
    text: "Are there documented emergency override procedures that allow a human operator to immediately halt or override the system's decisions?"
    guidance: "Article 14 requires human oversight mechanisms; this question checks whether the technical implementation exists."
    annex_iii_categories: [biometric, critical_infrastructure, law_enforcement]
    default_likelihood_hint: null
    default_severity_hint: null
    article_refs: ["Art.14(4)(e)"]
    nist_rmf_ref: "MANAGE 1.1"
    iso42001_ref: "Clause A.9"
    regulatory_status: settled
```

---

## 12. Risk Pattern Library

```yaml
# src/riskforge/_data/patterns/patterns.yaml
schema_version: "1.0.0"
patterns:
  - pattern_id: CREDIT_SCORING_BIAS
    name: "Credit Scoring — Demographic Bias Risk"
    triggers:
      annex_iii_category: essential_services
      purpose_keywords: ["credit", "loan", "mortgage", "underwriting", "insurance"]
    risks:
      - dimension: discrimination
        title: "Demographic bias in credit scoring outputs"
        description: "Credit scoring models trained on historical data may encode systemic biases against protected groups (age, gender, ethnicity). Article 9(9) requires consideration of impacts on vulnerable groups."
        likelihood_hint: 3
        severity_hint: 4
        article_refs: ["Art.9(2)(a)", "Art.9(9)", "Art.10(2)(f)"]
        nist_rmf_ref: "MEASURE 2.9"
        iso42001_ref: "Clause A.7"

  - pattern_id: HIRING_SCREENING
    name: "Hiring / CV Screening — Multiple Risk Cluster"
    triggers:
      annex_iii_category: employment
      purpose_keywords: ["recruit", "hiring", "cv", "resume", "screening", "interview"]
    risks:
      - dimension: discrimination
        title: "Proxy discrimination in automated CV screening"
        description: "Automated screening tools may use proxies (school name, postcode, employment gaps) that correlate with protected characteristics."
        likelihood_hint: 4
        severity_hint: 4
        article_refs: ["Art.9(2)(a)", "Art.10(2)(f)"]
        nist_rmf_ref: "MEASURE 2.9"
        iso42001_ref: "Clause A.7"
      - dimension: transparency
        title: "Lack of explainability for rejection decisions"
        description: "Candidates subject to automated CV screening may have a right to explanation under GDPR Article 22. The system may not be designed to provide this."
        likelihood_hint: 3
        severity_hint: 3
        article_refs: ["Art.13", "Art.14"]
        nist_rmf_ref: "GOVERN 1.7"
        iso42001_ref: "Clause A.6"
```

---

## 13. CLI Command Design

```python
# src/riskforge/cli/main.py
from __future__ import annotations
import typer
from rich import print as rprint

app = typer.Typer(
    name="riskforge",
    help="EU AI Act Article 9 Risk Management System — AiExponent LLC",
    no_args_is_help=True,
)

@app.callback(invoke_without_command=True)
def main(
    version: bool = typer.Option(False, "--version", "-V", is_eager=True),
) -> None:
    if version:
        from importlib.metadata import version as pkg_version
        rprint(
            f"[bold]RiskForge[/bold] v{pkg_version('riskforge')} | "
            "Apache 2.0 | Zero telemetry | aiexponent.com"
        )
        raise typer.Exit()

# Register subcommands (all lazy imports — no business logic at import time)
from riskforge.cli.commands import (
    init, system, assess, risk, tests_cmd, validate, export, verify, diff, import_cmd
)
app.add_typer(system.app,    name="system")
app.add_typer(risk.app,      name="risk")
app.add_typer(tests_cmd.app, name="tests")

app.command("init")(init.cmd)
app.command("assess")(assess.cmd)
app.command("validate")(validate.cmd)
app.command("export")(export.cmd)
app.command("verify")(verify.cmd)
app.command("diff")(diff.cmd)
app.command("import")(import_cmd.cmd)
```

```python
# src/riskforge/cli/commands/verify.py
import typer, sys
from pathlib import Path

def cmd(
    file: Path = typer.Option(None, "--file", "-f", help="rmf.json to verify"),
    project_dir: Path = typer.Option(Path("."), "--project-dir"),
) -> None:
    """Verify audit chain integrity. Exits 2 if tampered or corrupt."""
    from riskforge.storage.filesystem import FileStore
    from rich.console import Console
    console = Console()
    store = FileStore(project_dir)

    import asyncio
    is_valid, violations = asyncio.run(store.verify_chain())

    if is_valid:
        console.print("[green]✓[/green] Audit chain verified — no tampering detected.")
        raise typer.Exit(0)
    else:
        console.print("[red]✗[/red] Audit chain CORRUPT. Tampering or corruption detected:")
        for v in violations:
            console.print(f"  [red]•[/red] {v}")
        raise typer.Exit(2)     # Exit code 2: detectable by CI pipelines
```

---

## 14. FastAPI Server

```python
# src/riskforge/server/app.py
from __future__ import annotations
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from riskforge.server.middleware import CorrelationMiddleware, RateLimitMiddleware
from riskforge.server.routers import registers, risks, exports, webhooks, health
from riskforge.server.metrics import setup_metrics


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: validate config, connect storage
    from riskforge.server.config import ServerConfig
    config = ServerConfig()                  # reads RISKFORGE_SECRET_KEY etc.
    if not config.secret_key:
        raise RuntimeError(
            "RISKFORGE_SECRET_KEY is required. "
            "Generate with: python -c \"import secrets; print(secrets.token_hex(32))\""
        )
    yield
    # Shutdown: flush any pending writes


def create_app() -> FastAPI:
    app = FastAPI(
        title="RiskForge API",
        version="1.0.0",
        description="EU AI Act Article 9 Risk Management System",
        docs_url="/docs",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    app.add_middleware(CorrelationMiddleware)
    app.add_middleware(RateLimitMiddleware, requests_per_minute=1000)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[],       # must be explicitly configured; no wildcard
        allow_methods=["GET", "POST", "PATCH", "DELETE"],
        allow_headers=["Authorization", "Content-Type", "X-Correlation-ID"],
    )

    app.include_router(health.router,     prefix="")
    app.include_router(registers.router,  prefix="/api/v1")
    app.include_router(risks.router,      prefix="/api/v1")
    app.include_router(exports.router,    prefix="/api/v1")
    app.include_router(webhooks.router,   prefix="/api/v1")

    setup_metrics(app)
    return app

app = create_app()
```

---

## 15. GitHub Actions — Release Pipeline

```yaml
# .github/workflows/release.yml
name: Release to PyPI
on:
  push:
    tags: ["v*.*.*"]

permissions:
  id-token: write       # Sigstore OIDC + PyPI trusted publishing
  contents: write       # GitHub Release creation
  attestations: write   # build provenance

jobs:
  release:
    runs-on: ubuntu-latest
    environment: pypi-publish
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with: {python-version: "3.11"}

      - name: Install build tools
        run: pip install hatch pip-audit bandit

      - name: Security gates (must pass before build)
        run: |
          pip-audit --strict -r requirements.txt
          bandit -ll -r src/

      - name: Run full test suite
        run: |
          pip install -e ".[dev]"
          pytest --cov --cov-fail-under=80

      - name: Build wheel + sdist
        run: hatch build

      - name: Generate CycloneDX SBOM
        run: |
          pip install cyclonedx-bom
          cyclonedx-py environment -o sbom.cdx.json --format json

      - name: Sign with Sigstore (OIDC — no stored secrets)
        uses: sigstore/gh-action-sigstore-python@v3
        with:
          inputs: dist/*.whl dist/*.tar.gz

      - name: Attest build provenance
        uses: actions/attest-build-provenance@v1
        with:
          subject-path: dist/*

      - name: Publish to PyPI (OIDC trusted publisher)
        uses: pypa/gh-action-pypi-publish@release/v1

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          generate_release_notes: true
          files: |
            dist/*.whl
            dist/*.tar.gz
            dist/*.sigstore
            sbom.cdx.json
```

---

## 16. Test Strategy

| Layer | Tool | Coverage target | Key tests |
|---|---|---|---|
| Unit (engine) | pytest | ≥80% branch | scoring matrix, gate logic, hash computation, adapter transforms |
| Unit (models) | pytest | ≥80% | Pydantic validation, computed fields, edge cases |
| Integration (CLI) | pytest + subprocess | Key workflows | `init → assess → validate → export` full pipeline |
| Contract | pytest + jsonschema | 100% of export paths | Every export path validates against rmf.schema.json |
| Boundary | pytest + importlib | 100% of engine | engine.* has no CLI/server imports |
| Security | pytest-socket | All tests | Zero outbound network calls |
| Security (static) | bandit -ll | All files | No medium/high findings |
| Supply chain | pip-audit | All releases | No CVSS ≥7.0 findings |
| PDF | manual + visual | Per release | PDF renders all 7 sections correctly |

```python
# tests/boundary/test_import_boundaries.py
"""Engine must not import CLI or server modules."""
import importlib, pkgutil
import pytest


def _submodules(package: str) -> list[str]:
    mod = importlib.import_module(package)
    return [
        f"{package}.{m.name}"
        for m in pkgutil.walk_packages(mod.__path__, f"{package}.")
    ]


@pytest.mark.parametrize("module", _submodules("riskforge.engine"))
def test_engine_does_not_import_cli(module: str) -> None:
    m = importlib.import_module(module)
    source = getattr(m, "__file__", "") or ""
    assert "riskforge.cli" not in str(getattr(m, "__loader__", "")), (
        f"{module} imports from riskforge.cli — import boundary violated"
    )

@pytest.mark.parametrize("module", _submodules("riskforge.engine"))
def test_engine_does_not_import_server(module: str) -> None:
    m = importlib.import_module(module)
    assert "riskforge.server" not in dir(m), (
        f"{module} imports from riskforge.server — import boundary violated"
    )
```

---

## 17. Filesystem State Layout (OSS Project)

```
my-ai-project/
├── riskforge.yaml                      # project manifest (schema_version, project_id)
├── .riskforge/
│   ├── audit.jsonl                     # append-only hash-chained audit log
│   └── .nodelete                       # sentinel — pre-flight checks abort if missing
├── systems/
│   ├── fraud-detection-v1.2/
│   │   ├── system.yaml                 # AISystem metadata
│   │   ├── register.yaml               # RiskRegister + all RiskItems
│   │   ├── mitigations.yaml            # Mitigations (versioned separately)
│   │   └── exports/
│   │       ├── rmf-fraud-detection-v1.2-2026-03-01-a1b2c3.json
│   │       └── rmf-fraud-detection-v1.2-2026-03-01-a1b2c3.pdf
│   └── loan-scoring-v2.0/
│       ├── system.yaml
│       ├── register.yaml
│       └── mitigations.yaml
└── schemas/
    └── rmf.schema.json                 # pinned schema version (vendored at init time)
```

---

*Document: LLD-RiskForge-v1.0.md | Version 1.0 | April 2026*  
*Companion documents: HLD-RiskForge-v1.0.md | PRD-RiskForge-v1.0.md*
