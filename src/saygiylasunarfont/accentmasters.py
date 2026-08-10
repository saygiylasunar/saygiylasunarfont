from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from fontTools.pens.ttGlyphPen import TTGlyphPen

from .config import CORE_UNIT, M
from .curveprimitives import stroked_quadratic_outline
from .geometry import polygon, rounded_rect

Draw = Callable[[TTGlyphPen], None]


@dataclass(frozen=True)
class AccentMaster:
    core: float = CORE_UNIT
    dot_size: float = 1.5 * CORE_UNIT
    diaeresis_offset: float = 2.0 * CORE_UNIT
    dot_gap: float = 1.25 * CORE_UNIT
    breve_half_span: float = 2.6 * CORE_UNIT
    breve_low_gap: float = 0.85 * CORE_UNIT
    breve_high_gap: float = 1.55 * CORE_UNIT
    breve_stroke: float = 0.58 * M.stroke
    cedilla_stroke: float = 0.58 * M.stroke

    def draw_dot(self, pen: TTGlyphPen, *, cx: float, cy: float) -> None:
        half = self.dot_size / 2.0
        rounded_rect(
            pen,
            cx - half,
            cy - half,
            cx + half,
            cy + half,
            self.dot_size * 0.28,
            clockwise=True,
        )

    def draw_diaeresis(self, pen: TTGlyphPen, *, base_top: float) -> None:
        cy = base_top + self.dot_gap
        self.draw_dot(pen, cx=M.center - self.diaeresis_offset, cy=cy)
        self.draw_dot(pen, cx=M.center + self.diaeresis_offset, cy=cy)

    def draw_breve(self, pen: TTGlyphPen, *, base_top: float) -> None:
        high = base_top + self.breve_high_gap
        low = base_top + self.breve_low_gap
        # For a symmetric quadratic, midpoint=(high+control)/2. Solve the
        # control point so the visible center lands exactly on `low`.
        control_y = 2.0 * low - high
        points = stroked_quadratic_outline(
            (M.center - self.breve_half_span, high),
            (M.center, control_y),
            (M.center + self.breve_half_span, high),
            stroke=self.breve_stroke,
            steps=32,
        )
        polygon(pen, points, clockwise=True)

    def draw_cedilla(self, pen: TTGlyphPen) -> None:
        points = stroked_quadratic_outline(
            (M.center, 0.10 * self.core),
            (M.center - 0.90 * self.core, -1.55 * self.core),
            (M.center + 1.15 * self.core, -2.70 * self.core),
            stroke=self.cedilla_stroke,
            steps=28,
        )
        polygon(pen, points, clockwise=True)

    def draw_dot_above(self, pen: TTGlyphPen, *, base_top: float) -> None:
        self.draw_dot(pen, cx=M.center, cy=base_top + self.dot_gap)


ACCENT_MASTER = AccentMaster()


def compose(base: Draw, accent: Callable[[TTGlyphPen], None]) -> Draw:
    def draw(pen: TTGlyphPen) -> None:
        base(pen)
        accent(pen)
    return draw


def upper_diaeresis(base: Draw) -> Draw:
    return compose(base, lambda pen: ACCENT_MASTER.draw_diaeresis(pen, base_top=M.cap_height))


def lower_diaeresis(base: Draw) -> Draw:
    return compose(base, lambda pen: ACCENT_MASTER.draw_diaeresis(pen, base_top=M.x_height))


def upper_breve(base: Draw) -> Draw:
    return compose(base, lambda pen: ACCENT_MASTER.draw_breve(pen, base_top=M.cap_height))


def lower_breve(base: Draw) -> Draw:
    return compose(base, lambda pen: ACCENT_MASTER.draw_breve(pen, base_top=M.x_height))


def with_cedilla(base: Draw) -> Draw:
    return compose(base, ACCENT_MASTER.draw_cedilla)


def upper_dot(base: Draw) -> Draw:
    return compose(base, lambda pen: ACCENT_MASTER.draw_dot_above(pen, base_top=M.cap_height))
