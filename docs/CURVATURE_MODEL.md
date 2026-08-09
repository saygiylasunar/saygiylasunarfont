# Saygıyla Sunar Mono — Parametric Curvature Model

## Principle

The typeface identity must survive changes in size, width, stroke and glyph
category. Absolute radii and hand-picked coordinates are therefore outputs,
not design DNA.

The hierarchy is:

1. **Character DNA** — dimensionless identity.
2. **Family derivative** — small deltas for bowls, apertures, flow and numerals.
3. **Instance resolution** — optical compensation for stroke/weight.
4. **Geometry realisation** — scale into the glyph box.
5. **Lattice attraction** — optional 3/6/9 alignment where it helps rhythm.
6. **Optical correction** — recognition always outranks grid purity.

## Master curvature

The primary rounded geometry uses a superellipse:

```text
x(t) = a · sgn(cos t) · |cos t|^(2/n)
y(t) = b · sgn(sin t) · |sin t|^(2/n)
```

`a` and `b` are dimensions of the local glyph box. `n` is dimensionless and
acts as the stiffness parameter:

- `n = 2` approaches an ellipse;
- moderate `n > 2` gives controlled mechanical roundness;
- larger `n` approaches a stiff rounded rectangle.

The family does not use one universal `n`. Instead all curvature groups are
small derivatives of one `CORE_DNA` value.

## Family derivatives

The current model exposes related profiles:

- `BOWL_DNA` — O/o/0-like closed forms;
- `LOWER_BOWL_DNA` — smaller lowercase bowls;
- `OPEN_DNA` — C/c/e/G-like forms with more aperture;
- `FLOW_DNA` — S/s and future continuous transitions;
- `NUMERIC_DNA` — 2/3/6/8/9 families.

These are additive deltas from `CORE_DNA`, not unrelated presets. If the core
stiffness changes, all families move with it.

## Scaling invariant

Let cell size be `C` and stroke be `S`.

```text
rho = S / C
```

`rho` is the weight ratio. Uniform scaling by any factor `k` leaves it unchanged:

```text
(kS) / (kC) = S / C
```

Therefore the resolved curve remains identical under uniform scaling. Geometry
is generated in a local box and then mapped into absolute font units.

## Weight compensation

A heavier stroke is not produced by blindly expanding the Regular outline.
The curve is re-resolved from the same DNA.

With reference weight `rho0 = 1/9`:

```text
w = rho / rho0 - 1
n_weight = clamp(n0 + gain_n · w)
aperture_weight = clamp(a0 + gain_a · w)
```

The current DNA slightly reduces the exponent as weight increases and opens the
aperture. The intent is to release optical pressure and protect counters while
keeping the same mechanical identity.

The inner counter also receives its own exponent delta:

```text
n_inner = n_weight + delta_inner
```

This lets outer stiffness remain authoritative without making inner counters
look pinched.

## Curvature redistribution

`axis_bias` modifies the horizontal and vertical superellipse powers around the
same master exponent:

```text
nx = n · (1 + bias)
ny = n · (1 - bias)
```

This allows an O-like bowl, an e-like shoulder and an S-like transition to
share the same family character while distributing curvature differently.

## Apertures and terminals

Aperture is stored as a ratio of local glyph height, never as a fixed number of
font units. The right-shoulder aperture angle is obtained by inverting the
superellipse equation, so a C/e/G opening stays structurally related when the
box changes size.

`terminal_bias` then permits a small asymmetric terminal shift. This is useful
for documentary/digital character and recognition without inventing an
unrelated terminal system for each glyph.

## 3 / 6 / 9 lattice

The current monospace cell is 648 units:

```text
1/3 = 216
1/6 = 108
1/9 = 72
```

These values are preferred construction landmarks, not mandatory coordinates.
The lattice supports **soft snapping**:

```text
p' = p + strength · (nearest_grid(p) - p)
```

where `strength` is between 0 and 1.

- `0` means pure optical placement;
- `1` means exact grid placement;
- values between them preserve a mathematical accent while allowing readable
  imperfections.

This makes 3/6/9 a characteristic influence rather than a numerological cage.

## Design invariant

A successful derivative may change:

- width;
- height;
- stroke;
- curvature distribution;
- aperture;
- terminal position;
- optical grid deviation.

It must not lose:

- the core stiffness/roundness balance;
- documentary disambiguation;
- digital/mechanical rhythm;
- shared family curvature;
- controlled 30°/60° diagonal language;
- Turkish source-level consistency.

The mathematical system exists to preserve character under transformation, not
to make every glyph obey the same visible trick.
