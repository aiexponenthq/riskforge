"""Regression tests for `--sign` key handling (B5).

`_sign` invoked `gpg --detach-sign --armor <file>` with no `--local-user`, so the
caller-supplied key was ignored (GPG used its default key) and a GPG failure raised
an uncaught CalledProcessError traceback. Signing now passes the key and fails clean.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest
from riskforge.engine.export import ExportEngine, SigningError


def _engine() -> ExportEngine:
    # _sign uses neither the registry nor the audit engine.
    return ExportEngine(None, None)


def test_sign_passes_supplied_key_to_gpg(monkeypatch, tmp_path: Path) -> None:
    recorded: dict[str, list[str]] = {}

    def fake_run(cmd, **kwargs):
        recorded["cmd"] = cmd
        return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")

    monkeypatch.setattr(shutil, "which", lambda name: "/usr/bin/gpg")
    monkeypatch.setattr(subprocess, "run", fake_run)

    f = tmp_path / "rmf.json"
    f.write_text("{}")
    _engine()._sign(f, "alice@example.com")

    assert "--local-user" in recorded["cmd"]
    assert "alice@example.com" in recorded["cmd"]
    assert str(f) in recorded["cmd"]


def test_sign_missing_gpg_raises_clean_error(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(shutil, "which", lambda name: None)
    f = tmp_path / "rmf.json"
    f.write_text("{}")
    with pytest.raises(SigningError):
        _engine()._sign(f, "alice@example.com")


def test_sign_gpg_failure_raises_clean_error(monkeypatch, tmp_path: Path) -> None:
    def fake_run(cmd, **kwargs):
        raise subprocess.CalledProcessError(2, cmd, stderr="no secret key")

    monkeypatch.setattr(shutil, "which", lambda name: "/usr/bin/gpg")
    monkeypatch.setattr(subprocess, "run", fake_run)

    f = tmp_path / "rmf.json"
    f.write_text("{}")
    with pytest.raises(SigningError, match="badkey"):
        _engine()._sign(f, "badkey")
