"""DDIM sampler for the glyph diffusion model."""

from __future__ import annotations

import torch

from aifont.models.diffusion import GlyphDiffusion


@torch.no_grad()
def sample_glyph(
    model: GlyphDiffusion,
    codepoint: int,
    steps: int = 50,
    grid_size: int = 64,
    device: str = "cpu",
    seed: int = 6767,
) -> torch.Tensor:
    """Return a (1, grid_size, grid_size) coverage grid for ``codepoint``."""
    g = torch.Generator(device=device).manual_seed(seed)
    x = torch.randn(1, 1, grid_size, grid_size, generator=g, device=device)
    cp = torch.tensor([codepoint], device=device)
    model = model.to(device).eval()
    ts = torch.linspace(1.0, 0.0, steps, device=device)
    for i in range(steps - 1):
        t = ts[i].expand(1)
        t_next = ts[i + 1].expand(1)
        pred = model(x, t, cp)
        x = x + (t_next - t)[:, None, None, None] * pred
    return x.squeeze(0).clamp(0.0, 1.0)