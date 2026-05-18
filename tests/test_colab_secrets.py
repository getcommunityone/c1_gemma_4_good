"""Secret-loading behavior for Colab notebooks."""

from __future__ import annotations

import os
import sys
import types
from pathlib import Path

_COLAB = Path(__file__).resolve().parents[1] / "scripts" / "colab" / "utils"
if str(_COLAB) not in sys.path:
    sys.path.insert(0, str(_COLAB))

from colab_secrets import default_local_secrets_mode, in_colab_runtime  # noqa: E402


def test_default_local_secrets_mode_uses_env_only_locally(monkeypatch) -> None:
    monkeypatch.delenv("GOVERNANCE_NOTEBOOK_SECRETS", raising=False)
    monkeypatch.setattr("colab_secrets.in_colab_runtime", lambda: False)

    default_local_secrets_mode()

    assert os.environ["GOVERNANCE_NOTEBOOK_SECRETS"] == "env_only"


def test_default_local_secrets_mode_keeps_colab_secrets_in_judge_mode(monkeypatch) -> None:
    monkeypatch.delenv("GOVERNANCE_NOTEBOOK_SECRETS", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.setenv("GOVERNANCE_JUDGE_MODE", "1")
    monkeypatch.setattr("colab_secrets.in_colab_runtime", lambda: True)

    default_local_secrets_mode()

    assert "GOVERNANCE_NOTEBOOK_SECRETS" not in os.environ


def test_in_colab_runtime_accepts_real_colab_without_release_tag(monkeypatch) -> None:
    monkeypatch.delenv("GOVERNANCE_FORCE_COLAB_SECRETS", raising=False)
    monkeypatch.delenv("COLAB_RELEASE_TAG", raising=False)
    monkeypatch.setattr("colab_secrets.Path.is_dir", lambda self: str(self) == "/content")
    monkeypatch.setitem(sys.modules, "google", types.ModuleType("google"))
    monkeypatch.setitem(sys.modules, "google.colab", types.ModuleType("google.colab"))

    assert in_colab_runtime() is True