"""Write sampled glyphs to a UFO 3 source directory (for Glyphs/FontForge)."""

from __future__ import annotations

from pathlib import Path

import defcon


def write_ufo(
    out_dir: Path,
    glyphs: dict[str, list[list[tuple[float, float]]]],
    units_per_em: int = 1000,
    family_name: str = "AIFont",
) -> Path:
    font = defcon.Font()
    font.info.unitsPerEm = units_per_em
    font.info.familyName = family_name
    font.info.styleName = "Regular"

    for name, contours in glyphs.items():
        glyph = font.newGlyph(name)
        pen = glyph.getPen()
        for contour in contours:
            if not contour:
                continue
            pen.moveTo(contour[0])
            for pt in contour[1:]:
                pen.lineTo(pt)
            pen.closePath()

    out_dir.parent.mkdir(parents=True, exist_ok=True)
    font.save(str(out_dir))
    return out_dir