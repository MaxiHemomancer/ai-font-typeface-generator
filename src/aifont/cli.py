"""Typer CLI entry point. `aifont run <config.yaml>` is the hot path."""

from __future__ import annotations

from pathlib import Path

import typer
import yaml

from aifont.config.schema import FontRunConfig
from aifont.pipeline import FontPipeline

app = typer.Typer(help="AI font / typeface generator", no_args_is_help=True)


@app.command()
def run(config: Path = typer.Argument(..., exists=True, dir_okay=False)) -> None:
    """Generate a font from a YAML config."""
    data = yaml.safe_load(config.read_text(encoding="utf-8"))
    cfg = FontRunConfig.model_validate(data)
    FontPipeline(cfg).run()


@app.command()
def version() -> None:
    from aifont import __version__

    typer.echo(__version__)


if __name__ == "__main__":
    app()