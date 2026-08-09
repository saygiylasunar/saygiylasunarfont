from __future__ import annotations

import math
from collections.abc import Iterable

from fontTools.pens.ttGlyphPen import TTGlyphPen

Point = tuple[float, float]


def _signed_area(points: list[Point]) -> float:
    return sum(
        x1 * y2 - x2 * y1
        for (x1, y1), (x2, y2) in zip(points, points[1:] + points[:1])
    ) / 2


def polygon(pen: TTGlyphPen, points: Iterable[Point], *, clockwise: bool = True) -> None:
    pts = list(points)
    if len(pts) < 3:
        raise ValueError("polygon needs at least three points")
    is_clockwise = _signed_area(pts) < 0
    if is_clockwise != clockwise:
        pts.reverse()
    pen.moveTo(pts[0])
    for point in pts[1:]:
        pen.lineTo(point)
    pen.closePath()


def rect(pen: TTGlyphPen, x0: float, y0: float, x1: float, y1: float) -> None:
    polygon(pen, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)])


def octagon_points(x0: float, y0: float, x1: float, y1: float, corner: float) -> list[Point]:
    c = min(corner, (x1 - x0) / 2, (y1 - y0) / 2)
    return [
        (x0 + c, y0),
        (x1 - c, y0),
        (x1, y0 + c),
        (x1, y1 - c),
        (x1 - c, y1),
        (x0 + c, y1),
        (x0, y1 - c),
        (x0, y0 + c),
    ]


def octagonal_ring(
    pen: TTGlyphPen,
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    *,
    stroke: float,
    corner: float,
) -> None:
    polygon(pen, octagon_points(x0, y0, x1, y1, corner), clockwise=True)
    polygon(
        pen,
        octagon_points(
            x0 + stroke,
            y0 + stroke,
            x1 - stroke,
            y1 - stroke,
            max(0, corner - stroke / 2),
        ),
        clockwise=False,
    )


def thick_segment(
    pen: TTGlyphPen,
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    width: float,
) -> None:
    dx = x1 - x0
    dy = y1 - y0
    length = math.hypot(dx, dy)
    if not length:
        raise ValueError("segment endpoints must differ")
    px = -dy / length * width / 2
    py = dx / length * width / 2
    polygon(
        pen,
        [
            (x0 + px, y0 + py),
            (x1 + px, y1 + py),
            (x1 - px, y1 - py),
            (x0 - px, y0 - py),
        ],
    )


def chevron(
    pen: TTGlyphPen,
    x_center: float,
    y_center: float,
    width: float,
    height: float,
    stroke: float,
    *,
    up: bool = True,
) -> None:
    direction = 1 if up else -1
    y_edge = y_center - direction * height / 2
    y_tip = y_center + direction * height / 2
    thick_segment(pen, x_center - width / 2, y_edge, x_center, y_tip, stroke)
    thick_segment(pen, x_center, y_tip, x_center + width / 2, y_edge, stroke)


def dot(pen: TTGlyphPen, cx: float, cy: float, size: float) -> None:
    half = size / 2
    rect(pen, cx - half, cy - half, cx + half, cy + half)
