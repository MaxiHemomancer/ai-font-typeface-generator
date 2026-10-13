"""Style transfer: condition glyph sampling on a reference font vector."""

from __future__ import annotations

from pathlib import Path

import torch

from aifont.models.style_encoder import StyleEncoder, rasterize_font


def load_style_vector(font_path: Path, device: str = "cpu") -> torch.Tensor:
    grids = rasterize_font(font_path)
    tensor = torch.from_numpy(grids).to(device)
    encoder = StyleEncoder().to(device).eval()
    with torch.no_grad():
        return encoder(tensor)


def apply_style(
    base_grid: torch.Tensor,
    style_vector: torch.Tensor,
    strength: float = 0.75,
) -> torch.Tensor:
    """Blend a base glyph grid toward a style-conditioned modulation.

    ``strength`` in [0, 1]; 0 = identity, 1 = full style. The modulation here
    is a cheap affine on the grid's high-frequency residual — the diffusion
    model does the heavy lifting, this just steers the final pass.
    """
    if not 0.0 <= strength <= 1.0:
        raise ValueError("strength must be in [0, 1]")
    mean = base_grid.mean()
    residual = base_grid - mean
    style_bias = style_vector.mean().tanh()
    modulated = mean + residual * (1.0 + strength * style_bias)
    return modulated.clamp(0.0, 1.0)