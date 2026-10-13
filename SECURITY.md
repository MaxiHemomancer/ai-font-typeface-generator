# Security Policy

## Supported versions

| Version | Supported |
| ------- | --------- |
| 0.6.x   | yes       |
| 0.5.x   | security fixes only |

## Reporting a vulnerability

Email `security@aifont-typeface-generator.dev` with:
- affected version (commit hash preferred)
- minimal repro (font file, config, or CLI invocation)
- expected vs observed behavior

We aim to respond within 72 hours. Please do not open public issues for
memory-safety bugs in the C++ rasterizer shim or for arbitrary-code-execution
issues when loading untrusted `.ttf`/`.otf` inputs.

## Threat model

The generator parses untrusted font files during style transfer. The
following are in scope:

- Out-of-bounds reads in `lib/ttf_parser.py` when parsing malformed `glyf`
  tables.
- Code execution via pickle in `models/checkpoints/` — we now load with
  `weights_only=True` by default; report any bypass.
- Path traversal in the CLI `--output` flag.

Font rendering exploits in upstream FreeType are out of scope; report
those upstream.