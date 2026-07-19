"""Path-traversal hardening for FileStore system-id handling.

system_id flows into filesystem paths via _system_dir (register, system, exports,
mitigations). A crafted id must not escape the systems/ directory.
"""

from __future__ import annotations

import uuid
from pathlib import Path

import pytest
from riskforge.storage.filesystem import FileStore


@pytest.mark.parametrize(
    "bad",
    ["../etc", "../../etc/passwd", "a/b", "..", ".", "", "x\\y", "/abs/path"],
)
def test_system_dir_rejects_traversal(tmp_path: Path, bad: str) -> None:
    store = FileStore(tmp_path)
    with pytest.raises(ValueError):
        store._system_dir(bad)


def test_system_dir_accepts_uuid(tmp_path: Path) -> None:
    store = FileStore(tmp_path)
    sid = str(uuid.uuid4())
    resolved = store._system_dir(sid)
    assert resolved.name == sid
    assert resolved.parent == store._systems_dir
