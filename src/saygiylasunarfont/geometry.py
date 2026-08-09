from __future__ import annotations

import math
from collections.abc import Iterable
from dataclasses import dataclass

from fontTools.pens.reverseContourPen import ReverseContourPen
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


def _rounded_rect_ccw(
    pen: TTGlyphPen,
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    radius: float,
) -> None:
    r = min(radius, (x1 - x0) / 2, (y1 - y0) / 2)
    pen.moveTo((x0 + r, y0))
    pen.lineTo((x1 - r, y0))
    pen.qCurveTo((x1, y0), (x1, y0 + r))
    pen.lineTo((x1, y1 - r))
    pen.qCurveTo((x1, y1), (x1 - r, y1))
    pen.lineTo((x0 + r, y1))
    pen.qCurveTo((x0, y1), (x0, y1 - r))
    pen.lineTo((x0, y0 + r))
    pen.qCurveTo((x0, y0), (x0 + r, y0))
    pen.closePath()


def rounded_rect(
    pen: TTGlyphPen,
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    radius: float,
    *,
    clockwise: bool = True,
) -> None:
    target = ReverseContourPen(pen) if clockwise else pen
    _rounded_rect_ccw(target, x0, y0, x1, y1, radius)


def soft_ring(
    pen: TTGlyphPen,
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    *,
    stroke: float,
    radius: float,
) -> None:
    """Stiff rounded rectangular ring: round enough to breathe, never pill-like."""
    rounded_rect(pen, x0, y0, x1, y1, radius, clockwise=True)
    rounded_rect(
        pen,
        x0 + stroke,
        y0 + stroke,
        x1 - stroke,
        y1 - stroke,
        max(0, radius - stroke * 0.45),
        clockwise=False,
    )


def _open_bowl_ccw(
    pen: TTGlyphPen,
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    *,
    stroke: float,
    radius: float,
    aperture: float,
) -> None:
    """Single C-shaped contour, opening to the right, drawn CCW."""
    r = min(radius, (x1 - x0) / 2, (y1 - y0) / 2)
    ir = max(0, r - stroke * 0.45)
    mid = (y0 + y1) / 2
    half_gap = min((y1 - y0) * 0.38, aperture / 2)
    outer_hi = mid + half_gap
    outer_lo = mid - half_gap
    ix0, iy0 = x0 + stroke, y0 + stroke
    ix1, iy1 = x1 - stroke, y1 - stroke
    inner_hi = min(iy1 - ir, outer_hi)
    inner_lo = max(iy0 + ir, outer_lo)

    pen.moveTo((x1, outer_lo))
    pen.lineTo((x1, y0 + r))
    pen.qCurveTo((x1, y0), (x1 - r, y0))
    pen.lineTo((x0 + r, y0))
    pen.qCurveTo((x0, y0), (x0, y0 + r))
    pen.lineTo((x0, y1 - r))
    pen.qCurveTo((x0, y1), (x0 + r, y1))
    pen.lineTo((x1 - r, y1))
    pen.qCurveTo((x1, y1), (x1, y1 - r))
    pen.lineTo((x1, outer_hi))
    pen.lineTo((ix1, inner_hi))
    pen.lineTo((ix1, iy1 - ir))
    pen.qCurveTo((ix1, iy1), (ix1 - ir, iy1))
    pen.lineTo((ix0 + ir, iy1))
    pen.qCurveTo((ix0, iy1), (ix0, iy1 - ir))
    pen.lineTo((ix0, iy0 + ir))
    pen.qCurveTo((ix0, iy0), (ix0 + ir, iy0))
    pen.lineTo((ix1 - ir, iy0))
    pen.qCurveTo((ix1, iy0), (ix1, iy0 + ir))
    pen.lineTo((ix1, inner_lo))
    pen.closePath()


def open_soft_bowl(
    pen: TTGlyphPen,
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    *,
    stroke: float,
    radius: float,
    aperture: float,
    opening: str = "right",
) -> None:
    if opening not in {"right", "left"}:
        raise ValueError("opening must be 'right' or 'left'")
    if opening == "right":
        _open_bowl_ccw(
            ReverseContourPen(pen),
            x0, y0, x1, y1,
            stroke=stroke, radius=radius, aperture=aperture,
        )
        return

    from fontTools.pens.recordingPen import RecordingPen
    from fontTools.pens.transformPen import TransformPen

    rec = RecordingPen()
    _open_bowl_ccw(
        rec, x0, y0, x1, y1,
        stroke=stroke, radius=radius, aperture=aperture,
    )
    axis = x0 + x1
    mirrored = TransformPen(ReverseContourPen(pen), (-1, 0, 0, 1, axis, 0))
    rec.replay(mirrored)


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


def axis_segment(
    pen: TTGlyphPen,
    cx: float,
    cy: float,
    length: float,
    angle_degrees: float,
    width: float,
) -> None:
    """Segment on a deliberate construction axis (0/30/60/90 are canonical)."""
    angle = math.radians(angle_degrees)
    dx = math.cos(angle) * length / 2
    dy = math.sin(angle) * length / 2
    thick_segment(pen, cx - dx, cy - dy, cx + dx, cy + dy, width)


@dataclass(frozen=True)
class IsoBasis:
    """2D projection of a simple 3-axis construction space."""

    scale: float = 72.0
    angle: float = 30.0

    def project(self, x: float, y: float, z: float = 0.0) -> Point:
        a = math.radians(self.angle)
        ux = math.cos(a) * self.scale
        uy = math.sin(a) * self.scale
        vx = -math.cos(a) * self.scale
        vy = math.sin(a) * self.scale
        return (x * ux + y * vx, x * uy + y * vy + z * self.scale)


def dot(pen: TTGlyphPen, cx: float, cy: float, size: float) -> None:
    half = size / 2
    rounded_rect(
        pen,
        cx - half, cy - half, cx + half, cy + half,
        min(size * 0.18, half),
        clockwise=True,
    )
