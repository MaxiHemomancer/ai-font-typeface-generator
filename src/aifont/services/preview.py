"""Render a PNG specimen sheet of sampled glyphs using Pillow."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


def render_preview_png(
    glyph_grids: dict[int, np.ndarray],
    out_path: Path,
    cell: int = 96,
    columns: int = 16,
) -> Path:
    rows = (len(glyph_grids) + columns - 1) // columns
    canvas = Image.new("L", (columns * cell, rows * cell), color=255)
    draw = ImageDraw.Draw(canvas)
    for i, (cp, grid) in enumerate(glyph_grids.items()):
        r, c = divmod(i, columns)
        img = Image.fromarray((grid * 255).astype(np.uint8)).resize((cell, cell))
        canvas.paste(img, (c * cell, r * cell))
        draw.text((c * cell + 4, r * cell + cell - 16), f"U+{cp:04X}", fill=128)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out_path)
    return out_path