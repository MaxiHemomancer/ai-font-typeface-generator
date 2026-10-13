"""Batch generator — sample a whole charset and export in one pass."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from aifont.config.schema import FontRunConfig
from aifont.export.otf_writer import write_otf
from aifont.export.ufo_writer import write_ufo
from aifont.glyph_synth.contour import grid_to_contours
from aifont.models.diffusion import GlyphDiffusion

LATIN_BASIC = list(range(0x20, 0x7F))


class BatchGenerator:
    def __init__(self, config: FontRunConfig) -> None:
        self.config = config
        self.model = GlyphDiffusion(
            hidden_dim=config.model.hidden_dim,
            num_layers=config.model.num_layers,
            glyph_embed_dim=config.model.glyph_embed_dim,
        )

    def generate(self, codepoints: Iterable[int] | None = None) -> Path:
        from aifont.glyph_synth.sampler import sample_glyph

        cps = list(codepoints) if codepoints is not None else LATIN_BASIC
        glyphs: dict[str, list[list[tuple[float, float]]]] = {}
        cmap: dict[int, str] = {}
        for cp in cps:
            grid = sample_glyph(
                self.model,
                codepoint=cp,
                seed=self.config.seed,
                device="cuda" if _cuda_available() else "cpu",
            ).squeeze(0).numpy()
            name = f"uni{cp:04X}"
            glyphs[name] = grid_to_contours(grid, self.config.export.units_per_em)
            cmap[cp] = name

        out_dir = self.config.output_dir / self.config.run_name
        written: list[Path] = []
        if "otf" in self.config.export.formats:
            written.append(
                write_otf(
                    out_dir / f"{self.config.export.family_name}-{self.config.export.style_name}.otf",
                    glyphs,
                    cmap,
                    units_per_em=self.config.export.units_per_em,
                    family_name=self.config.export.family_name,
                    style_name=self.config.export.style_name,
                )
            )
        if "ufo" in self.config.export.formats:
            written.append(
                write_ufo(
                    out_dir / f"{self.config.export.family_name}.ufo",
                    glyphs,
                    units_per_em=self.config.export.units_per_em,
                    family_name=self.config.export.family_name,
                )
            )
        return written[0] if written else out_dir


def _cuda_available() -> bool:
    try:
        import torch

        return torch.cuda.is_available()
    except Exception:
        return False