"""Integration tests — end-to-end CLI pipeline via subprocess.

These tests invoke the installed `riskforge` binary directly, which is the
most reliable way to test a CLI that uses Rich Console (module-level Console()
objects capture the real stdout at import time, bypassing CliRunner's patch).

The assess command requires interactive terminal prompts so it is not tested
here. AssessEngine is covered in unit/test_audit_chain.py.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

# Use sys.executable-relative path for the binary — reliable in all install modes.
# sys.executable gives /path/to/venv/bin/python; the CLI entry point is in the same bin/.
_RF_BIN = str(Path(sys.executable).parent / "riskforge")
if not Path(_RF_BIN).exists():
    _RF_BIN = shutil.which("riskforge") or _RF_BIN


def _run(args: list[str], cwd: str | None = None) -> subprocess.CompletedProcess:
    """Run riskforge <args> and return the completed process.

    Returns a CompletedProcess with a combined .output attribute (stdout + stderr)
    because Rich Console may write to either stream depending on TTY detection.
    """
    result = subprocess.run(
        [_RF_BIN] + args,
        capture_output=True,
        text=True,
        cwd=cwd,
    )
    # Attach combined output for convenience (Rich sometimes writes to stderr in CI)
    result.output = result.stdout + result.stderr  # type: ignore[attr-defined]
    return result


def _init_project(tmp_dir: Path, name: str = "Pipeline Test System") -> str:
    """Run riskforge init and return the system_id."""
    result = _run([
        "init",
        "--name", name,
        "--version", "2.0",
        "--purpose", f"Integration test for {name}.",
        "--provider", "AiExponent LLC",
        "--category", "employment",
        "--project-dir", str(tmp_dir),
    ])
    assert result.returncode == 0, f"init failed:\nSTDOUT:{result.stdout}\nSTDERR:{result.stderr}"
    sid = next(
        (line.split(":", 1)[-1].strip() for line in result.output.splitlines() if "System ID:" in line),
        None,
    )
    assert sid, f"Could not extract system ID from:\n{result.output}"
    return sid


def _seed_register(tmp_dir: Path, sid: str, one_dim: bool = False) -> None:
    """Seed a register directly via the engine (bypasses interactive assess)."""
    import asyncio
    from riskforge.engine.audit import AuditEngine
    from riskforge.engine.risk import RiskEngine
    from riskforge.models.audit import AuditActor
    from riskforge.models.register import RiskRegister
    from riskforge.models.risk import Likelihood, RiskDimension, RiskItem, Severity
    from riskforge.storage.filesystem import FileStore

    async def _run_async():
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
        dims = [RiskDimension.privacy] if one_dim else list(RiskDimension)
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

    asyncio.run(_run_async())


@pytest.mark.enable_socket
def test_version_shows_zero_telemetry() -> None:
    """riskforge --version must include the zero-telemetry trust signal."""
    result = _run(["--version"])
    assert result.returncode == 0, f"--version failed:\n{result.stderr}"
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

        # 1. Init
        sid = _init_project(d)

        # 2. Seed register (replaces interactive assess in CI)
        _seed_register(d, sid)

        # 3. Validate
        validate_result = _run([
            "validate", sid, "--project-dir", str(d),
        ])
        assert validate_result.returncode in (0, 1), (
            f"validate exited {validate_result.returncode}:\n{validate_result.stdout}"
        )

        # 4. Export JSON
        output_json = d / "test_rmf.json"
        export_result = _run([
            "export", sid,
            "--format", "json",
            "--output", str(output_json),
            "--force",
            "--project-dir", str(d),
        ])
        assert export_result.returncode == 0, (
            f"export json failed:\n{export_result.stdout}\n{export_result.stderr}"
        )
        assert output_json.exists(), "rmf.json not created"

        rmf = json.loads(output_json.read_text())
        assert "rmf_schema_version" in rmf
        assert "register" in rmf
        assert len(rmf["register"]["items"]) == 8
        assert rmf["sha256_hash"] != ""

        # 5. Verify audit chain
        verify_result = _run([
            "verify", "--project-dir", str(d),
        ])
        assert verify_result.returncode == 0, (
            f"verify failed (chain corrupt):\n{verify_result.stdout}"
        )
        assert "verified" in (verify_result.stdout + verify_result.stderr).lower()


@pytest.mark.enable_socket
def test_export_markdown_contains_risk_items() -> None:
    """Markdown export must contain actual risk item text."""
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        sid = _init_project(d, "Markdown Test System")
        _seed_register(d, sid, one_dim=True)

        out = d / "test.md"
        result = _run([
            "export", sid,
            "--format", "markdown",
            "--output", str(out),
            "--force",
            "--project-dir", str(d),
        ])
        assert result.returncode == 0, f"markdown export failed:\n{result.stderr}"
        assert out.exists()
        content = out.read_text()
        assert "Risk Management" in content
        assert "Integration test risk" in content


@pytest.mark.enable_socket
def test_risk_list_shows_seeded_items() -> None:
    """riskforge risk list must return seeded items."""
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        sid = _init_project(d, "List Test System")
        _seed_register(d, sid, one_dim=True)

        result = _run(["risk", "list", sid, "--project-dir", str(d)])
        assert result.returncode == 0, f"risk list failed:\n{result.stderr}"
        assert "privacy" in (result.stdout + result.stderr).lower()
