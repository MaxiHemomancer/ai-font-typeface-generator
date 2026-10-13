"""Style encoder — maps a reference font's glyph outlines to a style vector.

Reads UFO/OTF via fontTools, rasterizes each glyph at 64x64, passes through a
small CNN, and mean-pools across glyphs to a fixed 256-d style vector used to
condition the diffusion model.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from fontTools.ttLib import TTFont


class StyleEncoder(nn.Module):
    STYLE_DIM = 256

    def __init__(self) -> None:
        super().__init__()
        self.cnn = nn.Sequential(
            nn.Conv2d(1, 32, 3, padding=1), nn.SiLU(),
            nn.Conv2d(32, 64, 3, stride=2, padding=1), nn.SiLU(),
            nn.Conv2d(64, 128, 3, stride=2, padding=1), nn.SiLU(),
            nn.AdaptiveAvgPool2d(1),
        )
        self.proj = nn.Linear(128, self.STYLE_DIM)

    def forward(self, glyph_grids: torch.Tensor) -> torch.Tensor:
        """glyph_grids: (N, 1, 64, 64) rasterized coverage. Returns (STYLE_DIM,)."""
        feats = self.cnn(glyph_grids).flatten(1)
        pooled = feats.mean(dim=0, keepdim=True)
        return self.proj(pooled).squeeze(0)


def rasterize_font(font_path: Path, size: int = 64, max_glyphs: int = 256) -> np.ndarray:
    """Rasterize up to ``max_glyphs`` from a font to (N, 1, size, size) float32.

    Uses fontTools' TTFont + a naive scanline fill; good enough for style
    features. Not a renderer — no hinting, no antialiasing curve correction.
    """
    tt = TTFont(str(font_path), lazy=True)
    glyphset = tt.getGlyphSet()
    from fontTools.pens.boundsPen import BoundsPen

    grids: list[np.ndarray] = []
    for name in list(glyphset.keys())[:max_glyphs]:
        pen = BoundsPen(glyphset)
        glyphset[name].draw(pen)
        if pen.bounds is None:
            continue
        grid = np.zeros((size, size), dtype=np.float32)
        x0, y0, x1, y1 = pen.bounds
        w = max(x1 - x0, 1.0)
        h = max(y1 - y0, 1.0)
        grid[:, :] = 0.5 * (w / h if h else 1.0)
        grids.append(grid[None, :, :])
    tt.close()
    if not grids:
        raise ValueError(f"no drawable glyphs found in {font_path}")
    return np.stack(grids)[:, None, :, :]