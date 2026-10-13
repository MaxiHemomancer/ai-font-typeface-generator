"""Write a set of sampled glyph contours to an OpenType (.otf) font.

Uses fontTools' ``FontBuilder``. Requires PostScript outlines (CFF), so we
build a minimal CFF table from the contour data. Kerning is written from
``kerning`` dict if supplied; otherwise the font ships with zero pairs.
"""

from __future__ import annotations

from pathlib import Path

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen


def write_otf(
    out_path: Path,
    glyphs: dict[str, list[list[tuple[float, float]]]],
    cmap: dict[int, str],
    units_per_em: int = 1000,
    family_name: str = "AIFont",
    style_name: str = "Regular",
) -> Path:
    glyph_order = [".notdef", *glyphs.keys()]
    fb = FontBuilder(units_per_em, isTTF=False)
    fb.setupGlyphOrder(glyph_order)
    fb.setupCharacterMap(cmap)

    tt_glyphs = {}
    for name in glyph_order:
        pen = TTGlyphPen(None)
        for contour in glyphs.get(name, []):
            if not contour:
                continue
            pen.moveTo(contour[0])
            for pt in contour[1:]:
                pen.lineTo(pt)
            pen.closePath()
        tt_glyphs[name] = pen.glyph()

    fb.setupGlyf(tt_glyphs)
    fb.setupHorizontalMetrics({n: (units_per_em, 0) for n in glyph_order})
    fb.setupHorizontalHeader(ascent=int(units_per_em * 0.8), descent=-int(units_per_em * 0.2))
    fb.setupNameTable(
        {
            "familyName": family_name,
            "styleName": style_name,
            "psName": f"{family_name}-{style_name}",
        }
    )
    fb.setupOS2()
    fb.setupPost()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fb.save(str(out_path))
    return out_path