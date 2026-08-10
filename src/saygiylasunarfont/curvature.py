from __future__ import annotations

import math
from dataclasses import dataclass, replace

Point = tuple[float, float]
REFERENCE_STROKE_RATIO = 1.0 / 9.0


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _signed_power(value: float, power: float) -> float:
    if value == 0:
        return 0.0
    return math.copysign(abs(value) ** power, value)


@dataclass(frozen=True)
class CharacterDNA:
    """Dimensionless curvature identity shared by all glyph families.

    Absolute units do not belong here. A glyph family derives small deltas from
    this master DNA; an instance then resolves those ratios for a given stroke.
    """

    exponent: float = 3.65
    inner_exponent_delta: float = -0.18
    aperture_ratio: float = 0.245
    terminal_bias: float = 0.045
    axis_bias: float = 0.0
    weight_exponent_gain: float = -0.22
    weight_aperture_gain: float = 0.045

    def derive(
        self,
        *,
        exponent_delta: float = 0.0,
        aperture_delta: float = 0.0,
        terminal_delta: float = 0.0,
        axis_bias_delta: float = 0.0,
    ) -> "CharacterDNA":
        """Create a recognisable family variant without inventing new DNA."""
        return replace(
            self,
            exponent=self.exponent + exponent_delta,
            aperture_ratio=self.aperture_ratio + aperture_delta,
            terminal_bias=self.terminal_bias + terminal_delta,
            axis_bias=self.axis_bias + axis_bias_delta,
        )


@dataclass(frozen=True)
class ResolvedCurve:
    exponent: float
    inner_exponent: float
    aperture_ratio: float
    terminal_bias: float
    axis_bias: float
    stroke_ratio: float


CORE_DNA = CharacterDNA()

# Small, intentional derivatives of one identity. These are not independent
# style presets: changing CORE_DNA should move the whole typeface family.
BOWL_DNA = CORE_DNA.derive(exponent_delta=0.12)
LOWER_BOWL_DNA = CORE_DNA.derive(exponent_delta=-0.12)
OPEN_DNA = CORE_DNA.derive(exponent_delta=-0.06, aperture_delta=0.055)
FLOW_DNA = CORE_DNA.derive(exponent_delta=-0.42, aperture_delta=0.025, terminal_delta=0.018)
NUMERIC_DNA = CORE_DNA.derive(exponent_delta=0.18, aperture_delta=0.012)


def resolve_curve(
    dna: CharacterDNA,
    *,
    cell: float,
    stroke: float,
) -> ResolvedCurve:
    """Resolve dimensionless DNA for an absolute font instance.

    Uniformly scaling both `cell` and `stroke` produces the exact same resolved
    curve. Increasing weight changes only optical compensation terms.
    """
    if cell <= 0 or stroke <= 0:
        raise ValueError("cell and stroke must be positive")

    stroke_ratio = stroke / cell
    relative_weight = stroke_ratio / REFERENCE_STROKE_RATIO
    weight_delta = relative_weight - 1.0

    exponent = clamp(
        dna.exponent + dna.weight_exponent_gain * weight_delta,
        2.05,
        6.5,
    )
    inner_exponent = clamp(
        exponent + dna.inner_exponent_delta,
        2.02,
        exponent,
    )
    aperture_ratio = clamp(
        dna.aperture_ratio + dna.weight_aperture_gain * weight_delta,
        0.12,
        0.48,
    )

    return ResolvedCurve(
        exponent=exponent,
        inner_exponent=inner_exponent,
        aperture_ratio=aperture_ratio,
        terminal_bias=dna.terminal_bias,
        axis_bias=dna.axis_bias,
        stroke_ratio=stroke_ratio,
    )


@dataclass(frozen=True)
class CurveBox:
    x0: float
    y0: float
    x1: float
    y1: float

    @property
    def width(self) -> float:
        return self.x1 - self.x0

    @property
    def height(self) -> float:
        return self.y1 - self.y0

    @property
    def cx(self) -> float:
        return (self.x0 + self.x1) / 2.0

    @property
    def cy(self) -> float:
        return (self.y0 + self.y1) / 2.0

    def inset(self, amount: float) -> "CurveBox":
        if amount * 2 >= min(self.width, self.height):
            raise ValueError("inset collapses curve box")
        return CurveBox(
            self.x0 + amount,
            self.y0 + amount,
            self.x1 - amount,
            self.y1 - amount,
        )


def superellipse_unit_point(
    t: float,
    *,
    exponent: float,
    axis_bias: float = 0.0,
) -> Point:
    """Point on a unit superellipse.

    `axis_bias` allows related families to redistribute curvature between the
    horizontal and vertical shoulders without changing the base exponent.
    """
    nx = clamp(exponent * (1.0 + axis_bias), 2.01, 8.0)
    ny = clamp(exponent * (1.0 - axis_bias), 2.01, 8.0)
    c = math.cos(t)
    s = math.sin(t)
    return (
        _signed_power(c, 2.0 / nx),
        _signed_power(s, 2.0 / ny),
    )


def superellipse_point(
    box: CurveBox,
    t: float,
    *,
    exponent: float,
    axis_bias: float = 0.0,
) -> Point:
    ux, uy = superellipse_unit_point(t, exponent=exponent, axis_bias=axis_bias)
    return (
        box.cx + ux * box.width / 2.0,
        box.cy + uy * box.height / 2.0,
    )


def sample_superellipse(
    box: CurveBox,
    *,
    exponent: float,
    axis_bias: float = 0.0,
    start: float = 0.0,
    end: float = math.tau,
    steps: int = 40,
) -> list[Point]:
    if steps < 4:
        raise ValueError("steps must be at least 4")
    return [
        superellipse_point(
            box,
            start + (end - start) * i / steps,
            exponent=exponent,
            axis_bias=axis_bias,
        )
        for i in range(steps + 1)
    ]


def aperture_angle(profile: ResolvedCurve) -> float:
    """Convert a vertical aperture ratio into the superellipse parameter t.

    On the right shoulder, the desired full opening is `height * ratio`.
    Inverting the superellipse y equation yields the corresponding angle.
    """
    ny = clamp(profile.exponent * (1.0 - profile.axis_bias), 2.01, 8.0)
    normalized_y = clamp(profile.aperture_ratio, 0.001, 0.999)
    sin_t = normalized_y ** (ny / 2.0)
    return math.asin(clamp(sin_t, 0.0, 1.0))
