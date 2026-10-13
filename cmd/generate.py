"""Standalone script entry — same as `aifont run` but callable without install."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from aifont.cli import app  # noqa: E402

if __name__ == "__main__":
    app(["run", *sys.argv[1:]])