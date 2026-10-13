"""Pydantic schema for a single font-generation run.

Inputs are YAML files under ``config/``. Every field is validated at load
time so a bad run fails before the model is instantiated.
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class ModelSpec(BaseModel):
    family: Literal["diffusion", "vae", "autoregressive"] = "diffusion"
    hidden_dim: int = Field(256, ge=32, le=2048)
    num_layers: int = Field(8, ge=2, le=64)
    glyph_embed_dim: int = Field(128, ge=16, le=1024)
    checkpoint: Path | None = None


class ExportSpec(BaseModel):
    formats: list[Literal["otf", "ttf", "woff2", "ufo"]] = ["otf", "woff2"]
    units_per_em: int = Field(1000, ge=16, le=16384)
    family_name: str = "AIFont"
    style_name: str = "Regular"


class FontRunConfig(BaseModel):
    run_name: str
    seed: int = 6767
    charset: str = "latin-basic"
    model: ModelSpec = ModelSpec()
    export: ExportSpec = ExportSpec()
    style_reference: Path | None = None
    output_dir: Path = Path("out")

    @field_validator("run_name")
    @classmethod
    def _slug(cls, v: str) -> str:
        if not v or any(c in v for c in " /\\"):
            raise ValueError("run_name must be a non-empty slug without spaces or slashes")
        return v