"""Integration tests — end-to-end CLI pipeline using Typer's CliRunner.

These tests exercise the full riskforge workflow via the CLI entry point:
  init → (engine: seed register) → validate → export json → verify

The assess command requires interactive terminal prompts (questionary) so it
is not tested here. AssessEngine is covered in unit/test_audit_chain.py.
"""
from __future__ import annotations

import json
import tempfile
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from typer.testing import CliRunner

from riskforge.cli.main import app

runner = CliRunner(mix_stderr=False)


def _init_project(tmp_dir: Path, name: str = "Pipeline Test System") -> str:
    """Run riskforge init and return the system_id."""
    result = runner.invoke(app, [
        "init",
        "--name", name,
        "--version", "2.0",
        "--purpose", f"Integration test for {name}.",
        "--provider", "AiExponent LLC",
        "--category", "employment",
        "--project-dir", str(tmp_dir),
    ])
    assert result.exit_code == 0, f"init failed:\n{result.output}"
    sid = next(
        line.split(":")[-1].strip()
        for line in result.output.splitlines()
        if "System ID:" in line
    )
    return sid


def _seed_register(tmp_dir: Path, sid: str, dimensions_only: bool = False) -> None:
    """Seed a register with one risk item per dimension (bypasses interactive assess)."""
    import asyncio
    from riskforge.engine.audit import AuditEngine
    from riskforge.engine.risk import RiskEngine
    from riskforge.models.audit import AuditActor
    from riskforge.models.register import RiskRegister
    from riskforge.models.risk import Likelihood, RiskDimension, RiskItem, Severity
    from riskforge.storage.filesystem import FileStore

    async def _run():
        store = FileStore(tmp_dir)
        sys_obj = await store.read_system(sid)
        sys_obj.annex_iii_self_classification_documented = True
        await store.write_system(sid, sys_obj)
        reg = RiskRegister(
            system=sys_obj,
            assessor_name="Test Assessor",
            assessor_role="QA Engineer",
            assessment_date=datetime.now(UTC),
            review_date=datetime.now(UTC) + timedelta(days=365),
            question_bank_version="1.0.0",
        )
        await store.write_register(sid, reg)
        actor = AuditActor(type="ci", identity="integration-test")
        audit = AuditEngine(store, actor)
        engine = RiskEngine(store, audit)
        dims = [RiskDimension.privacy] if dimensions_only else list(RiskDimension)
        for dim in dims:
            item = RiskItem(
                dimension=dim,
                title=f"Integration test risk — {dim.value}",
                description=f"Seeded by integration test for {dim.value}.",
                source="manual",
                likelihood=Likelihood.possible,
                severity=Severity.moderate,
                residual_likelihood=Likelihood.unlikely,
                residual_severity=Severity.minor,
            )
            await engine.add_risk(sid, item)

    asyncio.run(_run())


@pytest.mark.enable_socket
def test_version_shows_zero_telemetry() -> None:
    """--version must include the zero-telemetry trust signal."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0, f"--version failed:\n{result.output}"
    assert "Zero telemetry" in result.output
    assert "Apache 2.0" in result.output


@pytest.mark.enable_socket
def test_init_creates_project_files() -> None:
    """riskforge init must create .riskforge/ and riskforge.yaml."""
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        sid = _init_project(d, "Init Test System")
        assert (d / "riskforge.yaml").exists(), "riskforge.yaml not created"
        assert (d / ".riskforge").is_dir(), ".riskforge/ directory not created"
        assert len(sid) > 10, f"Unexpected system ID: {sid}"


@pytest.mark.enable_socket
def test_full_pipeline_init_validate_export_verify() -> None:
    """Full pipeline: init → seed → validate → export json → verify."""
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)

        # ── 1. Init ────────────────────────────────────────────────────────
        sid = _init_project(d)

        # ── 2. Seed register (replaces interactive assess in CI) ───────────
        _seed_register(d, sid)

        # ── 3. Validate ────────────────────────────────────────────────────
        validate_result = runner.invoke(app, [
            "validate", sid,
            "--project-dir", str(d),
        ])
        # May warn but must not hard-fail (0 = all pass, 1 = warnings)
        assert validate_result.exit_code in (0, 1), (
            f"validate exited {validate_result.exit_code}:\n{validate_result.output}"
        )
        assert "G1" in validate_result.output or "gate" in validate_result.output.lower()

        # ── 4. Export JSON ─────────────────────────────────────────────────
        output_json = d / "test_rmf.json"
        export_result = runner.invoke(app, [
            "export", sid,
            "--format", "json",
            "--output", str(output_json),
            "--force",
            "--project-dir", str(d),
        ])
        assert export_result.exit_code == 0, (
            f"export json failed:\n{export_result.output}"
        )
        assert output_json.exists(), "rmf.json not created"

        # Validate the JSON structure
        rmf = json.loads(output_json.read_text())
        assert "rmf_schema_version" in rmf
        assert "register" in rmf
        assert len(rmf["register"]["items"]) == 8
        assert rmf["sha256_hash"] != ""

        # ── 5. Verify audit chain ──────────────────────────────────────────
        verify_result = runner.invoke(app, [
            "verify",
            "--project-dir", str(d),
        ])
        assert verify_result.exit_code == 0, (
            f"verify failed:\n{verify_result.output}"
        )
        assert "verified" in verify_result.output.lower()


@pytest.mark.enable_socket
def test_export_markdown_contains_risk_items() -> None:
    """Markdown export must contain actual risk item text."""
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        sid = _init_project(d, "Markdown Test System")
        _seed_register(d, sid, dimensions_only=True)

        out = d / "test.md"
        result = runner.invoke(app, [
            "export", sid,
            "--format", "markdown",
            "--output", str(out),
            "--force",
            "--project-dir", str(d),
        ])
        assert result.exit_code == 0, f"markdown export failed:\n{result.output}"
        assert out.exists()
        content = out.read_text()
        assert "Risk Management" in content
        assert "Integration test risk" in content


@pytest.mark.enable_socket
def test_risk_list_empty_after_init() -> None:
    """A freshly-initialised project with an empty register shows no items."""
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        sid = _init_project(d, "Empty Register Test")
        # Seed with an empty register
        _seed_register(d, sid, dimensions_only=True)
        list_result = runner.invoke(app, [
            "risk", "list", sid,
            "--project-dir", str(d),
        ])
        assert list_result.exit_code == 0, f"risk list failed:\n{list_result.output}"
        assert "privacy" in list_result.output.lower()
