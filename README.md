# Saygıyla Sunar Font

A geometric, terminal-minded monospaced typeface built programmatically.

The project treats the font as a small geometry system rather than a folder of unrelated drawings. Shared metrics, terminals, bowls, diagonals and apertures are defined once and reused across glyph families.

## Design contract

- Strict monospaced advance width across printable glyphs.
- Geometric / technical voice: somewhere between terminal utility and engineered display type.
- Turkish is first-class: `Ç Ğ İ Ö Ş Ü ç ğ ı ö ş ü` are part of the core set, not later patches.
- Similar glyphs must remain distinguishable in code and tabular use: `0/O`, `1/I/l/ı`, `5/S`, `2/Z`, `8/B`.
- Lowercase must read naturally at text sizes; novelty never wins over recognition.
- Repeated forms come from shared primitives and shared optical rules.
- Build output is generated. Source-of-truth lives in Python geometry and metrics.

## Current phase

`v0` is a diagnostic core. It intentionally starts with the glyphs that expose the design system fastest: round forms, lowercase apertures, diagonals, Turkish accents and ambiguous terminal characters. Once those families are stable, the remaining alphabet is expanded from the same primitives.

## Repository layout

```text
src/saygiylasunarfont/
  config.py      global metrics and design tokens
  geometry.py    reusable contour helpers
  glyphs.py      glyph construction and family rules
  build.py       deterministic TTF build
scripts/
  audit.py       metric / coverage audit
build/           generated files (ignored)
tests/           invariant tests
```

## Build

Requires Python 3.11+.

```bash
python -m venv .venv
. .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e .
syf-build
syf-audit
```

The font is written to `build/SaygiylaSunarMono-Regular.ttf`.

## Locked metrics

The font uses a 1000 UPM grid and a single 600-unit advance width. Shape width may vary optically inside the cell, but the advance width does not.

Do not fix a difficult glyph by changing its advance width. Fix the drawing, sidebearings, family primitive or optical correction instead.
