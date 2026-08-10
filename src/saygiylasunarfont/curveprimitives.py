from __future__ import annotations

import math

Point = tuple[float, float]


def quadratic_point(p0: Point, p1: Point, p2: Point, t: float) -> Point:
    if not 0.0 <= t <= 1.0:
        raise ValueError("t must be in [0, 1]")
    mt = 1.0 - t
    return (
        mt * mt * p0[0] + 2.0 * mt * t * p1[0] + t * t * p2[0],
        mt * mt * p0[1] + 2.0 * mt * t * p1[1] + t * t * p2[1],
    )


def quadratic_tangent(p0: Point, p1: Point, p2: Point, t: float) -> Point:
    if not 0.0 <= t <= 1.0:
        raise ValueError("t must be in [0, 1]")
    return (
        2.0 * (1.0 - t) * (p1[0] - p0[0]) + 2.0 * t * (p2[0] - p1[0]),
        2.0 * (1.0 - t) * (p1[1] - p0[1]) + 2.0 * t * (p2[1] - p1[1]),
    )


def stroked_quadratic_outline(
    p0: Point,
    p1: Point,
    p2: Point,
    *,
    stroke: float,
    steps: int = 28,
) -> list[Point]:
    """Expand one quadratic centerline into a constant-width closed outline."""
    if stroke <= 0:
        raise ValueError("stroke must be positive")
    if steps < 6:
        raise ValueError("steps must be at least 6")

    left: list[Point] = []
    right: list[Point] = []
    half = stroke / 2.0
    for i in range(steps + 1):
        t = i / steps
        x, y = quadratic_point(p0, p1, p2, t)
        dx, dy = quadratic_tangent(p0, p1, p2, t)
        length = math.hypot(dx, dy)
        if length == 0.0:
            raise ValueError("degenerate quadratic tangent")
        nx = -dy / length
        ny = dx / length
        left.append((x + nx * half, y + ny * half))
        right.append((x - nx * half, y - ny * half))
    return left + list(reversed(right))
