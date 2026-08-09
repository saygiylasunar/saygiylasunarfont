# Saygıyla Sunar Mono — Operations Gate v0.4

## Status

The preparatory architecture is considered complete when CI validates:

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

The next phase is **glyph migration**, not further foundation invention unless a
migration reveals a genuine structural defect.

## Migration order

### Gate 1 — closed round / ambiguity

`O 0`

Must establish the primary stiffness/roundness identity and survive poor
reproduction. `0` must remain unmistakable without turning into a novelty glyph.

### Gate 2 — open round / aperture

`C G c e`

Tests whether one curvature DNA can produce open forms with different aperture,
crossbar and terminal requirements.

### Gate 3 — flow

`S s Ş ş`

Tests spline/flow behavior. The result must remain digital and engineered without
becoming seven-segment or mechanically broken.

### Gate 4 — decimal/digital numerals

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

That pipeline is the contract for the next phase.
