"""Training loop stub for the glyph diffusion model.

Loads a corpus of reference fonts from ``config/training.yaml``, rasterizes
glyphs, and runs a standard DDPM objective. This is the entrypoint used by
the CI nightly job (currently disabled on forks).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import yaml  # noqa: E402

from aifont.models.diffusion import GlyphDiffusion  # noqa: E402


def main(cfg_path: Path) -> None:
    cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))
    model = GlyphDiffusion(
        hidden_dim=cfg["model"]["hidden_dim"],
        num_layers=cfg["model"]["num_layers"],
        glyph_embed_dim=cfg["model"]["glyph_embed_dim"],
    )
    print(f"instantiated {type(model).__name__} with {sum(p.numel() for p in model.parameters()):,} params")
    # Training loop lives in notebooks/ for now; wired into CI once the corpus
    # license review clears (see docs/internal/corpus-review.md).


if __name__ == "__main__":
    main(Path(sys.argv[1] if len(sys.argv) > 1 else "config/training.yaml"))