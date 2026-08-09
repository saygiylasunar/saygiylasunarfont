# Saygıyla Sunar Mono — Moldcaster v0.4

## Purpose

The **36-unit core** is the native construction quantum of the current font
instance, not a demand that every future medium use units divisible by 36.
Moldcaster preserves normalized design relationships and reinterprets them in a
target construction system.

The native monospaced cell is:

- core = **36**
- cell = **18 cores = 648**
- regular stroke = **2 cores = 72**
- cap height = **20 cores = 720**
- x-height = **15 cores = 540**

Half-core and optical departures are allowed. The core is a harmonic reference,
not a pixel prison.

## Normalized casting

Every source coordinate first becomes dimensionless:

`u = x / source_span`

A target medium receives the same geometry by affine casting:

`x_target = u × target_span`

This is the identity-preserving step. Snapping is optional and happens only
after the normalized geometry exists.

## Mold hierarchy

### Trihex-36

Native construction hierarchy:

`2 / 3 / 6 / 9 / 18`

The 18-way layer exposes the 36-unit core. Coarser 3/6/9 anchors carry more
characteristic authority than the fine 18-way layer.

### Decimal-10

Decimal production favors factors of ten:

`2 / 5 / 10`

Halves and fifths are stronger structural anchors than arbitrary tenths. This
lets documentation, charts and decimal measurement systems feel native without
rewriting the font DNA around base 10.

### Dyadic-32

Digital/bitmap production favors powers of two:

`2 / 4 / 8 / 16 / 32`

This mold supports pixel and terminal experiments. The finest 32-way layer may
quantize strokes or coordinates when a discrete medium requires it, while
coarser powers of two retain stronger structural weight.

## Attractor rule

A mold is an **attractor hierarchy**, not a hard grid. For a normalized point
`u`, candidate grid points are scored by geometric distance and hierarchy
weight. A role-specific strength then interpolates toward the selected target:

`u' = u + strength × (target - u)`

`strength = 0` keeps the optical solution. `strength = 1` fully casts to the
selected mold anchor. Most glyph geometry should live between these extremes.

## Constraint roles

Snapping authority depends on what the point means:

- metric: effectively hard;
- stem: strong structural attraction;
- symmetry: strong relational constraint;
- bowl extremum: curvature/family outrank grid;
- aperture: recognition and counter openness outrank grid;
- terminal: angle/family character outrank exact position;
- curve handle: highly free, curvature-led;
- optical: almost unconstrained.

Therefore two points at the same coordinate can respond differently to the
same mold because their typographic roles differ.

## Angle systems

Position molds are complemented by angle families:

- documentary: `0° / 90°`
- trihex: `30° / 60°` and mirrors
- dyadic: `45°` and mirror

Angles are also soft attractors. A diagonal may remain at an optically superior
value when exact canonical alignment harms recognition.

## Priority order

When constraints conflict, use this design hierarchy:

1. legibility / glyph recognition
2. family identity
3. curvature and stroke continuity
4. symmetry / rhythm
5. medium-specific mold attraction
6. pure grid exactness

The goal is mathematically related forms, not mathematically obedient forms.

## Production implication

The same normalized glyph skeleton can be interpreted as:

- vector font geometry in the 648-unit native cell;
- decimal technical diagrams or measurement layouts;
- 16/32/64-pixel digital assets;
- future condensed/expanded widths;
- future weight instances.

Moldcaster changes the **production mold**, not the character DNA.
