# Saygıyla Sunar Mono — Operations Gate v0.4

## Status

The preparatory architecture is complete. CI validates:

- 36-unit native core;
- dimensionless curvature DNA;
- family derivatives;
- weight/scale invariance;
- Trihex-36, Decimal-10 and Dyadic-32 Moldcaster paths;
- role-based constraint hierarchy;
- documentary / trihex / dyadic angle families;
- strict monospaced metrics;
- Turkish source-level repertoire;
- deterministic TTF build and audit.

The current phase is **glyph migration**, not further foundation invention unless
a migration reveals a genuine structural defect.

## Migration order

### Gate 1 — closed round / ambiguity — MASTER CANDIDATE PASSED

`O 0` (+ `Ö` through source-level composition)

Gate 1 uses the parametric superellipse master through the migration registry.
The O is the pure round-family carrier. `0` is a controlled derivative with a
slightly narrower silhouette, slightly stiffer numeric curvature and a mold-aware
documentary slash.

Validated in CI and raster review:

- strict shared advance width;
- centered/symmetric closed forms;
- distinct O/0 silhouettes without family break;
- Trihex-native slash attraction;
- Decimal-10 normalized casting;
- Dyadic-32 stroke quantization and angle reinterpretation;
- Turkish `Ö` composition from the migrated O.

This is a **master candidate**, not a release freeze. Later family review may
apply a coordinated CORE/BOWL DNA adjustment, but Gate 1 should not receive
isolated cosmetic edits unless a new legibility issue appears.

### Gate 2 — open round / aperture — MASTER CANDIDATE PASSED

`C G c e` (+ `Ç Ğ ç` through source-level composition)

Gate 2 derives all four forms from OPEN_DNA. Lowercase forms receive controlled
extra optical freedom and aperture; `e` is a recognition-oriented derivative of
`c`, while `G` uses a restrained documentary shelf/spur rather than a separate
outline language.

Validated in CI and raster review:

- shared open-bowl curvature ancestry with Gate 1;
- C/G and c/e paired geometry remains centered and monospaced;
- `e` aperture is more open than `c` while retaining the same family body;
- `G` remains recognisable without collapsing into C+dash;
- Decimal-10 scaling preserves stroke ratio;
- Dyadic-32 quantization preserves open-family relationships;
- `Ç`, `Ğ`, `ç` compose from migrated bodies.

Accent shapes themselves are still legacy-era geometry and are **not optically
locked** by this gate. They will receive a dedicated family normalization pass;
Gate 2 only guarantees that their base bodies now come from the new system.

### Gate 3 — flow — MASTER CANDIDATE PASSED

`S s Ş ş`

Gate 3 replaces the previous stacked-open-bowl construction with one continuous
harmonic spine. The spine combines a fundamental and third harmonic, then uses a
smooth stiffness transform before a role-independent stroke expansion:

`((1-m) cos(pi t) + m cos(3 pi t)) -> tanh(k f) / tanh(k)`

The third harmonic creates the two shoulders near the 1/3 and 2/3 regions while
preserving mirrored flow. Uppercase uses a stronger harmonic/stiffness setting;
lowercase relaxes the same family instead of scaling the capital mechanically.

Validated in CI and raster review:

- odd mirror symmetry around the glyph center;
- mathematically generated shoulder turns near thirds;
- continuous centerline/stroke expansion instead of segment assembly;
- `S` and `s` share one flow family with lowercase optical relaxation;
- Dyadic-32 stroke quantization remains valid;
- `Ş` and `ş` compose from the migrated flow bodies;
- mixed O/C/G/S specimens retain one family character after a second stiffness
  tuning pass.

As in Gate 2, cedilla geometry is still a legacy accent and remains outside the
optical lock of this gate.

### Gate 4 — decimal/digital numerals — NEXT

`2 3 5 6 9`

This gate explicitly tests decimal familiarity (2/5 structure) and dyadic/digital
reinterpretation. Numerals must share family DNA with letters while retaining
fast documentary recognition.

### Gate 5 — diagonal/projective

`V W Z`

Tests 30/60°, documentary axes and optical departure. Exact angle snapping is
never allowed to damage rhythm.

### Gate 6 — lowercase closed family

`a o g`

Tests whether lowercase character survives a more open, text-oriented curvature
without becoming a separate typeface.

## Three-mold review

Every migrated family is reviewed in three representations:

1. **Native vector:** 648-unit cell, 36-unit core.
2. **Decimal interpretation:** normalized geometry viewed through Decimal-10.
3. **Digital interpretation:** normalized geometry viewed through Dyadic-32,
   including quantized stroke where appropriate.

A family does not need identical coordinates across molds. It must preserve:

- recognition;
- characteristic stiffness/roundness;
- terminal behavior;
- stroke hierarchy;
- family relationship.

## Constraint priority

When a migration exposes a conflict:

1. recognition / legibility;
2. family identity;
3. curvature and stroke continuity;
4. symmetry and rhythm;
5. mold attraction;
6. exact grid purity.

## Change discipline

During migration:

- change `CORE_DNA` only when the entire typeface should move;
- change a family derivative when a whole glyph family should move;
- use glyph-local deltas only for recognition-critical exceptions;
- never hard-code a coordinate merely to match one specimen size;
- add a regression test whenever a mathematical invariant is introduced;
- keep `main` untouched until the diagnostic core is visually coherent.

## Definition of ready

Foundation work is ready for glyph operations when CI is green and the current
architecture can express a glyph through:

`normalized geometry → family DNA → role constraints → mold interpretation → optical correction → outline`

That pipeline is the contract for the migration phase.
