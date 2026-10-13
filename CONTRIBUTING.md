# Contributing to ai-font-typeface-generator

Thanks for wanting to help forge typefaces with us. This repo is a modular
Python toolkit for training, sampling, and exporting AI-generated typefaces
to OpenType (OTF/TTF), UFO, and web formats.

## Dev setup

```
python -m venv .venv
. .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pre-commit install
```

## Layout

- `src/aifont/` — core package (models, samplers, exporters)
- `src/aifont/glyph_synth/` — glyph-shape synthesis modules
- `src/aifont/style_transfer/` — style encoder + transfer pipeline
- `src/aifont/export/` — OTF/UFO/WOFF2 writers
- `cmd/` — CLI entry points
- `lib/` — shared low-level font utilities (kerning, metrics)
- `config/` — YAML configs for training and sampling runs
- `tests/` — pytest suite

## Style

- Ruff for lint+format, line length 100.
- Type hints required on public functions.
- New samplers go under `src/aifont/samplers/` with a pytest fixture.
- Every exporter must round-trip against a golden UFO in `tests/fixtures/`.

## PR checklist

- [ ] `ruff check src cmd lib tests`
- [ ] `pytest -q`
- [ ] New model config added to `config/models/`
- [ ] CHANGELOG entry under `## Unreleased`

## Discussion

Open an issue tagged `rfc` before adding a new architectural family
(diffusion, VAE, autoregressive). We keep the sampler interface stable.