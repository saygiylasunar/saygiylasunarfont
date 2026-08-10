from __future__ import annotations

import math

Point = tuple[float, float]


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def harmonic_flow_unit(
    t: float,
    *,
    harmonic_mix: float = 0.72,
    stiffness: float = 1.9,
) -> float:
    """Odd serpentine wave used as the S-family centerline.

    The fundamental keeps the terminal direction stable while the third
    harmonic creates the two characteristic shoulders. `tanh` then redistributes
    curvature continuously: low stiffness is rounder, high stiffness holds a
    more engineered shoulder without introducing geometric corners.
    """
    if not 0.0 <= t <= 1.0:
        raise ValueError("t must be in [0, 1]")
    if not 0.0 <= harmonic_mix <= 1.0:
        raise ValueError("harmonic_mix must be in [0, 1]")
    if stiffness <= 0:
        raise ValueError("stiffness must be positive")

    base = (
        (1.0 - harmonic_mix) * math.cos(math.pi * t)
        + harmonic_mix * math.cos(3.0 * math.pi * t)
    )
    scale = math.tanh(stiffness)
    return math.tanh(stiffness * base) / scale


def harmonic_flow_derivative(
    t: float,
    *,
    harmonic_mix: float = 0.72,
    stiffness: float = 1.9,
) -> float:
    """Analytic derivative of :func:`harmonic_flow_unit`."""
    if not 0.0 <= t <= 1.0:
        raise ValueError("t must be in [0, 1]")
    if not 0.0 <= harmonic_mix <= 1.0:
        raise ValueError("harmonic_mix must be in [0, 1]")
    if stiffness <= 0:
        raise ValueError("stiffness must be positive")

    base = (
        (1.0 - harmonic_mix) * math.cos(math.pi * t)
        + harmonic_mix * math.cos(3.0 * math.pi * t)
    )
    base_prime = (
        -(1.0 - harmonic_mix) * math.pi * math.sin(math.pi * t)
        - 3.0 * harmonic_mix * math.pi * math.sin(3.0 * math.pi * t)
    )
    cosh = math.cosh(stiffness * base)
    sech2 = 1.0 / (cosh * cosh)
    return stiffness * sech2 * base_prime / math.tanh(stiffness)


def flow_spine_point(
    t: float,
    *,
    center_x: float,
    top: float,
    bottom: float,
    amplitude: float,
    harmonic_mix: float,
    stiffness: float,
) -> Point:
    if top <= bottom:
        raise ValueError("top must be above bottom")
    if amplitude <= 0:
        raise ValueError("amplitude must be positive")
    return (
        center_x
        + amplitude
        * harmonic_flow_unit(t, harmonic_mix=harmonic_mix, stiffness=stiffness),
        top + (bottom - top) * t,
    )


def flow_spine_tangent(
    t: float,
    *,
    top: float,
    bottom: float,
    amplitude: float,
    harmonic_mix: float,
    stiffness: float,
) -> Point:
    return (
        amplitude
        * harmonic_flow_derivative(t, harmonic_mix=harmonic_mix, stiffness=stiffness),
        bottom - top,
    )


def _smoothstep(value: float) -> float:
    value = clamp(value, 0.0, 1.0)
    return value * value * (3.0 - 2.0 * value)


def stroked_flow_outline(
    *,
    center_x: float,
    top: float,
    bottom: float,
    amplitude: float,
    stroke: float,
    harmonic_mix: float,
    stiffness: float,
    steps: int = 72,
    terminal_relief: float = 0.025,
    diagonal_compensation: float = 0.025,
) -> list[Point]:
    """Expand a harmonic centerline into one closed monoline outline.

    The outline is generated from analytic tangents, not independently drawn
    inner/outer contours. This keeps stroke and curvature related under scaling.
    Small dimensionless optical terms reduce terminal and fast-diagonal pressure.
    """
    if steps < 12:
        raise ValueError("steps must be at least 12")
    if stroke <= 0:
        raise ValueError("stroke must be positive")
    if not 0.0 <= terminal_relief < 0.25:
        raise ValueError("terminal_relief must be in [0, 0.25)")
    if not 0.0 <= diagonal_compensation < 0.25:
        raise ValueError("diagonal_compensation must be in [0, 0.25)")

    left: list[Point] = []
    right: list[Point] = []

    for i in range(steps + 1):
        t = i / steps
        x, y = flow_spine_point(
            t,
            center_x=center_x,
            top=top,
            bottom=bottom,
            amplitude=amplitude,
            harmonic_mix=harmonic_mix,
            stiffness=stiffness,
        )
        dx, dy = flow_spine_tangent(
            t,
            top=top,
            bottom=bottom,
            amplitude=amplitude,
            harmonic_mix=harmonic_mix,
            stiffness=stiffness,
        )
        length = math.hypot(dx, dy)
        if length == 0:
            raise ValueError("degenerate flow tangent")

        nx = -dy / length
        ny = dx / length
        horizontal_motion = abs(dx) / length

        # Relief fades out after the first/last 12.5% of the path.
        edge = min(t, 1.0 - t) / 0.125
        terminal_factor = 1.0 - terminal_relief * (1.0 - _smoothstep(edge))
        diagonal_factor = 1.0 - diagonal_compensation * horizontal_motion
        half = stroke * terminal_factor * diagonal_factor / 2.0

        left.append((x + nx * half, y + ny * half))
        right.append((x - nx * half, y - ny * half))

    return left + list(reversed(right))
