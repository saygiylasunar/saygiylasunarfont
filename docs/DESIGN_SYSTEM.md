# Saygıyla Sunar Mono — Design System v0.3

## Intent

Saygıyla Sunar Mono is a documentary/technical monospaced typeface with a
digital, field-engineering character. It should feel credible in a terminal,
maintenance manual, schematic label, inventory sheet or military-adjacent
technical document without becoming a stencil, gamer face or seven-segment
display.

The visual equation is:

**parametric family DNA × triadic/hexagonal construction × controlled roundness × engineered stiffness × documentary legibility**

## Identity hierarchy

The font is not defined by one visible gimmick, one radius or one grid. The
order of authority is:

1. recognition and documentary legibility;
2. shared parametric family DNA;
3. stiffness/roundness character;
4. family-specific curvature derivatives;
5. 30°/60° and 3/6/9 construction influence;
6. final optical correction.

See `CURVATURE_MODEL.md` for the equations and scaling model.

## 3 → 6 → 9 lattice

The current construction cell is **648 units** wide.

- 1/3 = **216**
- 1/6 = **108**
- 1/9 = **72**

These are preferred landmarks, not mandatory coordinates. Geometry can use
exact lattice points, half-steps or soft attraction toward the lattice. If an
exact 3/6/9 placement damages recognition, optical placement wins.

The OpenType container remains 1000 UPM for interoperability. The internal
design logic does not inherit the decimal structure of the UPM.

## Parametric curvature

Rounded families are generated from a superellipse-based model. The controlling
stiffness exponent and related parameters are dimensionless, so the same family
character can be re-resolved under changes in scale, stroke and local glyph box.

Absolute values such as `radius=90` are implementation outputs, not identity.
The important values are ratios and functions: curvature exponent, stroke ratio,
aperture ratio, terminal bias and axis bias.

Different glyph groups use small derivatives of one `CORE_DNA` rather than
unrelated curve presets. O, e, S and 9 are allowed to distribute curvature
differently while remaining visibly related.

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
- large bowls are stiff but not polygonal;
- lowercase and flow families may redistribute curvature;
- heavier weights receive optical counter/aperture compensation;
- terminal cuts and diagonals retain documentary precision.

Reference feeling: the stiffness/technology balance associated with Bender and
Exo, without copying their glyph outlines.

## Family grammar

### Bowl family
`O 0 o a g 6 8 9`

Closed forms derive from the same core curvature DNA. `0` receives an explicit
slash because documentary disambiguation outranks stylistic purity.

### Open family
`C G c e`

Open forms derive from the core with controlled aperture and terminal changes.
The aperture is a ratio/function, not a fixed unit value.

### Flow family
`S s Ş ş 3`

Flow forms may use a softer curvature derivative and asymmetric terminal bias,
but must remain recognisably part of the same typeface.

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
- ornamental sacred-geometry tricks
- sacrificing recognition to mathematical purity

## Review string

The identity is considered unstable until this string works as one system:

`O0 1Ilı aoe cg CGSŞş TVWZ 0123456789 ÇĞİÖŞÜ çğıöşü ₺ ² []{}()<>`

Do not expand the alphabet merely to increase glyph count before this string is
optically coherent.
