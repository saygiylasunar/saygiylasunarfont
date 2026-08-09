# Saygıyla Sunar Mono — Design System v0.2

## Intent

Saygıyla Sunar Mono is a documentary/technical monospaced typeface with a
digital, field-engineering character. It should feel credible in a terminal,
maintenance manual, schematic label, inventory sheet or military-adjacent
technical document without becoming a stencil, gamer face or seven-segment
display.

The visual equation is:

**triadic construction × hexagonal axes × controlled roundness × engineered stiffness × documentary legibility**

## 3 → 6 → 9 lattice

The construction cell is **648 units** wide.

- 1/3 = **216**
- 1/6 = **108**
- 1/9 = **72**

These values are design coordinates, not decorative numerology. Major stems,
bowls, apertures, diagonals, terminals and spacing decisions should prefer this
lattice or simple half-steps derived from it.

The OpenType container remains 1000 UPM for interoperability. The design logic
inside the container does not need to inherit the decimal structure of the UPM.

## Dimensional model

The primary 2D axes are orthogonal document axes. Secondary construction axes
are 30° / 60° and their mirrors. `IsoBasis` exposes a three-axis isometric
projection so future glyph details, icons and symbols can be derived from the
same geometry rather than merely looking '3D'.

3D projection is a construction tool, not a rendering effect: the released font
remains flat and highly legible.

## Stiffness vs roundness

Roundness exists to release optical pressure at corners and joints, not to make
the face friendly or soft.

- strokes remain mechanically straight;
- large bowls use stiff rounded corners;
- lowercase bowls receive slightly more radius than hard rectangular symbols;
- terminal cuts and diagonals retain documentary precision.

Reference feeling: the stiffness/technology balance associated with Bender and
Exo, without copying their glyph outlines.

## Family grammar

### Round family
`O 0 o a g C G c e 6 8 9`

All use the same soft-ring/open-bowl vocabulary. `0` receives an explicit slash
because documentary disambiguation outranks stylistic purity.

### Ambiguity family
`1 I l ı i 0 O S 5 Z 2`

Each pair must remain distinguishable at terminal sizes and in poor reproduction.

### Diagonal family
`V W Z 2 4 7 / \\ < >`

Diagonals should feel engineered and related. 30°/60° axes are canonical
construction references, but optical correction may move a final endpoint.

### Turkish family
`Ç Ğ İ Ö Ş Ü ç ğ ı ö ş ü`

Turkish is source-level repertoire. Accents are generated from shared geometric
primitives, never patched onto exported outlines.

## Tone guardrails

Wanted:
- digital
- documentary
- engineering
- controlled military/field-equipment character
- compact authority
- distinct serial-number rhythm

Avoid:
- cyberpunk neon styling
- generic sci-fi cuts
- seven-segment imitation
- stencil clichés
- rounded SaaS friendliness
- ornamental 'sacred geometry'

## Review string

The identity is considered unstable until this string works as one system:

`O0 1Ilı aoe cg CGSŞş TVWZ 0123456789 ÇĞİÖŞÜ çğıöşü ₺ ² []{}()< >`

Do not expand the alphabet merely to increase glyph count before this string is
optically coherent.
