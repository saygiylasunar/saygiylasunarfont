# Saygıyla Sunar Mono — Operations Gate v0.5

## Status

The preparatory architecture is complete, the **six diagnostic DNA gates are
master candidates**, and Turkish accent normalization has passed. This is not a
release freeze; it is the clean checkpoint from which the alphabet can expand by
structural family rather than by ad-hoc glyph drawing.

CI currently validates:

- 36-unit native core;
- dimensionless curvature DNA and family derivatives;
- weight/scale invariance;
- Trihex-36, Decimal-10 and Dyadic-32 Moldcaster paths;
- documentary, trihex, decimal-factor and dyadic angle families;
- role-based constraint hierarchy and fit constraints;
- strict monospaced metrics;
- Turkish source-level repertoire and normalized accent bounds;
- deterministic TTF build and audit.

## Diagnostic gates

### Gate 1 — closed round / ambiguity — MASTER CANDIDATE PASSED

`O 0` (+ `Ö` by composition)

- O is the pure BOWL_DNA carrier.
- `0` is slightly narrower/stiffer and receives a mold-aware documentary slash.
- Native, Decimal-10 and Dyadic-32 interpretations retain one family identity.
- O/0 separation survives small raster sizes without novelty styling.

### Gate 2 — open round / aperture — MASTER CANDIDATE PASSED

`C G c e` (+ `Ç Ğ ç` by composition)

- all derive from OPEN_DNA;
- lowercase receives controlled aperture/optical freedom;
- `e` is an open-family recognition derivative rather than a miniature E;
- `G` uses a restrained documentary shelf/spur;
- base-body relationships survive Decimal-10 and Dyadic-32 casts.

### Gate 3 — harmonic flow — MASTER CANDIDATE PASSED

`S s Ş ş`

The S spine is continuous rather than stacked/segmented:

`f(t) = (1-m) cos(pi t) + m cos(3 pi t)`

followed by:

`tanh(k f) / tanh(k)`

The third harmonic produces the two shoulders near the one-third/two-third
regions. Analytic tangent/normal expansion produces the stroke. A second raster
tuning pass increased harmonic stiffness without reintroducing seven-segment
behavior.

### Gate 4 — decimal / digital numerals — MASTER CANDIDATE PASSED

`2 3 5 6 9`

- Decimal angle attractors are derived from integer slopes `1:2` and `2:5`, not
  decorative base-10 angles.
- `2` keeps one source construction while trihex, decimal and dyadic media pull
  its diagonal differently.
- `6/9` inherit the closed-ring grammar.
- `5` inherits open-family behavior.
- the first two-bowl `3` was rejected in raster review; final `3` is one
  continuous two-lobe periodic flow with sequence `-1,+1,-1,+1,-1` and a
  six-core half-width aligned to the S-family rhythm.

### Gate 5 — diagonal / projective — MASTER CANDIDATE PASSED

`V W Z`

- mold angle attraction is subordinate to a geometric fit constraint, so an
  attractive 45-degree dyadic axis cannot push a diagonal outside the mono cell;
- `V` is a symmetric two-stroke skeleton;
- `W` is a mirrored five-point skeleton with its center at `9 × 36 = 324`, or
  `9/20` of cap height;
- the first raster exposed a reversed Z diagonal and a low W center; both were
  corrected before the gate was accepted;
- final Z/2 separation remains immediate at small sizes.

### Gate 6 — lowercase closed family — MASTER CANDIDATE PASSED

`a o g` (+ `ö ğ` by composition)

- all three use exactly one resolved LOWER_BOWL_DNA body;
- `a` preserves the successful single-storey silhouette and adds only a right
  stem plus restrained technical foot;
- `g` extends that same stem into a compact documentary descender/hook;
- lowercase body sharing is tested directly, not merely judged visually;
- Decimal-10 symmetry and Dyadic-32 stroke quantization remain valid.

## Accent normalization — PASSED

`Ç Ğ İ Ö Ş Ü ç ğ ö ş ü`

- diaeresis and dotted-I use one core-derived rounded-dot system;
- breve is a stroked quadratic centerline rather than a three-segment legacy
  approximation;
- cedilla is one stroked quadratic hook rather than two disconnected segments;
- cap accents are mathematically bounded below the global ascender;
- cedilla geometry is mathematically bounded above the global descender;
- accented glyph clipping is checked against the built TTF in CI;
- normalized accents can already compose with legacy bodies such as I/U/u while
  those bodies wait for their own family migration.

## Expansion — NEXT

Expand by structural families rather than alphabetic order:

1. stem/document family;
2. diagonal/projective family extensions;
3. bowl/stem uppercase family;
4. lowercase stem/arch family;
5. remaining numerals and punctuation/symbol normalization.

## Three-mold review

Every promoted family is reviewed in:

1. **Native vector:** 648-unit cell, 36-unit core.
2. **Decimal interpretation:** Decimal-10.
3. **Digital interpretation:** Dyadic-32 with quantized stroke where appropriate.

Coordinates need not match across molds. Recognition, family character,
curvature/stroke hierarchy and terminal behavior must.

## Constraint priority

When rules conflict:

1. recognition / legibility;
2. family identity;
3. curvature and stroke continuity;
4. symmetry and rhythm;
5. mold attraction;
6. exact grid purity.

## Change discipline

- change CORE_DNA only when the whole typeface should move;
- change a family derivative when the whole family should move;
- use glyph-local deltas only for recognition-critical exceptions;
- never hard-code a coordinate merely to match one specimen size;
- add a regression test whenever a mathematical invariant is introduced;
- keep `main` untouched until the diagnostic core and first expanded alphabet
  are visually coherent.
