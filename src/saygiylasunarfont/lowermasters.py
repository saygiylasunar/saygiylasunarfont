from __future__ import annotations

from dataclasses import dataclass

from fontTools.pens.ttGlyphPen import TTGlyphPen

from .config import CORE_UNIT, M
from .constraints import PointRole
from .curvature import LOWER_BOWL_DNA, ResolvedCurve, resolve_curve
from .curveprimitives import stroked_quadratic_outline
from .geometry import polygon, profiled_ring, rect, thick_segment
from .moldcaster import TRIHEX_36, Mold, Moldcaster
from .solver import ConstructionSolver


@dataclass(frozen=True)
class LowerClosedInstance:
    kind: str
    cell: float
    body_height: float
    x0: float
    x1: float
    y0: float
    y1: float
    stroke: float
    profile: ResolvedCurve
    stem_x0: float | None = None
    descender_bottom: float | None = None
    hook_start_y: float | None = None
    terminal_left: float | None = None
    foot_right: float | None = None

    @property
    def body_width(self) -> float:
        return self.x1 - self.x0


@dataclass(frozen=True)
class LowerClosedMaster:
    """Shared single-storey o/a/g body with documentary derivatives."""

    source_cell: float = M.advance
    source_height: float = M.x_height
    source_stroke: float = M.stroke
    source_overshoot: float = M.overshoot
    source_inset: float = 2.5 * CORE_UNIT
    descender_depth: float = 4.5 * CORE_UNIT
    g_terminal_core: float = 21.0 / 4.0
    g_hook_start_strokes: float = 9.0 / 8.0
    g_terminal_rise_strokes: float = 3.0 / 4.0
    g_hook_stroke_ratio: float = 13.0 / 16.0

    def _solver(self) -> ConstructionSolver:
        return ConstructionSolver(Moldcaster(self.source_cell))

    @staticmethod
    def _scale(value: float, source_span: float, target_span: float) -> float:
        return value / source_span * target_span

    def _resolve_x(
        self,
        source_value: float,
        *,
        target_cell: float,
        mold: Mold,
        role: PointRole,
        strength_scale: float,
    ) -> float:
        return self._solver().solve_coordinate(
            source_value,
            target_span=target_cell,
            mold=mold,
            role=role,
            strength_scale=strength_scale,
        )

    def resolve(
        self,
        kind: str,
        *,
        target_cell: float | None = None,
        target_body_height: float | None = None,
        mold: Mold = TRIHEX_36,
        quantize_stroke: bool = False,
    ) -> LowerClosedInstance:
        if kind not in {"o", "a", "g"}:
            raise ValueError("kind must be one of o, a, g")

        target_cell = self.source_cell if target_cell is None else target_cell
        target_body_height = self.source_height if target_body_height is None else target_body_height
        if target_cell <= 0 or target_body_height <= 0:
            raise ValueError("target dimensions must be positive")

        left = self._resolve_x(
            self.source_inset,
            target_cell=target_cell,
            mold=mold,
            role=PointRole.BOWL_EXTREMUM,
            strength_scale=0.38,
        )
        right = target_cell - left

        caster = Moldcaster(self.source_cell)
        stroke = caster.cast_stroke(
            self.source_stroke,
            target_span=target_cell,
            mold=mold if quantize_stroke else None,
            quantize=quantize_stroke,
        )
        profile = resolve_curve(LOWER_BOWL_DNA, cell=target_cell, stroke=stroke)
        overshoot = self._scale(self.source_overshoot, self.source_height, target_body_height)

        instance = LowerClosedInstance(
            kind=kind,
            cell=target_cell,
            body_height=target_body_height,
            x0=left,
            x1=right,
            y0=-overshoot,
            y1=target_body_height + overshoot,
            stroke=stroke,
            profile=profile,
        )
        if kind == "o":
            return instance

        stem_x0 = right - stroke
        if kind == "a":
            foot_right = self._resolve_x(
                16.4 * CORE_UNIT,
                target_cell=target_cell,
                mold=mold,
                role=PointRole.TERMINAL,
                strength_scale=0.18,
            )
            return LowerClosedInstance(
                **{
                    **instance.__dict__,
                    "stem_x0": stem_x0,
                    "foot_right": foot_right,
                }
            )

        descender_bottom = -self._scale(
            self.descender_depth,
            self.source_height,
            target_body_height,
        )
        terminal_left = self._resolve_x(
            self.g_terminal_core * CORE_UNIT,
            target_cell=target_cell,
            mold=mold,
            role=PointRole.TERMINAL,
            strength_scale=0.14,
        )
        hook_start_y = descender_bottom + stroke * self.g_hook_start_strokes
        return LowerClosedInstance(
            **{
                **instance.__dict__,
                "stem_x0": stem_x0,
                "descender_bottom": descender_bottom,
                "hook_start_y": hook_start_y,
                "terminal_left": terminal_left,
            }
        )

    def draw(self, pen: TTGlyphPen, kind: str) -> None:
        inst = self.resolve(kind)
        profiled_ring(
            pen,
            inst.x0,
            inst.y0,
            inst.x1,
            inst.y1,
            stroke=inst.stroke,
            profile=inst.profile,
            steps=56,
        )
        if kind == "o":
            return

        assert inst.stem_x0 is not None
        if kind == "a":
            assert inst.foot_right is not None
            rect(pen, inst.stem_x0, 0.0, inst.x1, inst.body_height)
            thick_segment(
                pen,
                inst.x1 - inst.stroke * 0.52,
                inst.stroke * 0.34,
                inst.foot_right,
                0.0,
                inst.stroke * 0.68,
            )
            return

        assert inst.descender_bottom is not None
        assert inst.hook_start_y is not None
        assert inst.terminal_left is not None

        stem_center = (inst.stem_x0 + inst.x1) / 2.0
        rect(
            pen,
            inst.stem_x0,
            inst.hook_start_y - inst.stroke * (9.0 / 16.0),
            inst.x1,
            inst.body_height,
        )
        hook = stroked_quadratic_outline(
            (stem_center, inst.hook_start_y),
            (stem_center, inst.descender_bottom),
            (
                inst.terminal_left,
                inst.descender_bottom + inst.stroke * self.g_terminal_rise_strokes,
            ),
            stroke=inst.stroke * self.g_hook_stroke_ratio,
            steps=32,
        )
        polygon(pen, hook, clockwise=True)


LOWER_CLOSED_MASTER = LowerClosedMaster()


def draw_o(pen: TTGlyphPen) -> None:
    LOWER_CLOSED_MASTER.draw(pen, "o")


def draw_a(pen: TTGlyphPen) -> None:
    LOWER_CLOSED_MASTER.draw(pen, "a")


def draw_g(pen: TTGlyphPen) -> None:
    LOWER_CLOSED_MASTER.draw(pen, "g")
