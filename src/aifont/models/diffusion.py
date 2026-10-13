"""Glyph diffusion model — U-Net over contour grids.

Input:  (B, 1, 64, 64) coverage grid of a glyph bitmap, plus a
        (B, glyph_embed_dim) class embedding for the codepoint.
Output: (B, 1, 64, 64) denoised coverage grid.

Concurrency: model is not thread-safe; wrap calls in a lock if you fan out
across a ThreadPoolExecutor. GPU memory at batch=64, 64x64 is ~1.8GB on
fp32; OOMs above batch=96 on a 12GB card.
"""

from __future__ import annotations

import torch
import torch.nn as nn


class SinusoidalPosEmb(nn.Module):
    def __init__(self, dim: int) -> None:
        super().__init__()
        self.dim = dim

    def forward(self, t: torch.Tensor) -> torch.Tensor:
        half = self.dim // 2
        freqs = torch.exp(
            -torch.arange(half, device=t.device) * (torch.log(torch.tensor(10000.0)) / half)
        )
        args = t[:, None].float() * freqs[None]
        return torch.cat([args.sin(), args.cos()], dim=-1)


class ConvBlock(nn.Module):
    def __init__(self, cin: int, cout: int, emb: int) -> None:
        super().__init__()
        self.conv = nn.Conv2d(cin, cout, 3, padding=1)
        self.norm = nn.GroupNorm(8, cout)
        self.act = nn.SiLU()
        self.emb_proj = nn.Linear(emb, cout)

    def forward(self, x: torch.Tensor, emb: torch.Tensor) -> torch.Tensor:
        h = self.conv(x)
        h = h + self.emb_proj(emb)[:, :, None, None]
        return self.act(self.norm(h))


class GlyphDiffusion(nn.Module):
    """Denoiser conditioned on timestep + glyph class embedding."""

    def __init__(self, hidden_dim: int = 256, num_layers: int = 8, glyph_embed_dim: int = 128) -> None:
        super().__init__()
        self.hidden_dim = hidden_dim
        self.time_emb = nn.Sequential(
            SinusoidalPosEmb(hidden_dim),
            nn.Linear(hidden_dim, hidden_dim),
            nn.SiLU(),
        )
        self.glyph_emb = nn.Embedding(0x10FFFF, glyph_embed_dim)
        self.in_conv = nn.Conv2d(1, hidden_dim, 3, padding=1)
        self.blocks = nn.ModuleList(
            [ConvBlock(hidden_dim, hidden_dim, hidden_dim + glyph_embed_dim) for _ in range(num_layers)]
        )
        self.out_conv = nn.Conv2d(hidden_dim, 1, 3, padding=1)

    def forward(self, x: torch.Tensor, t: torch.Tensor, codepoint: torch.Tensor) -> torch.Tensor:
        temb = self.time_emb(t)
        cemb = self.glyph_emb(codepoint)
        emb = torch.cat([temb, cemb], dim=-1)
        h = self.in_conv(x)
        for block in self.blocks:
            h = block(h, emb)
        return self.out_conv(h)