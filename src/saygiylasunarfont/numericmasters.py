from __future__ import annotations

import math
from dataclasses import dataclass

from fontTools.pens.ttGlyphPen import TTGlyphPen

from .config import CORE_UNIT, M
from .constraints import DECIMAL_AXES, DYADIC_AXES, TRIHEX_AXES, PointRole
from .curvature import NUMERIC_DNA, ResolvedCurve, resolve_curve
from .curveprimitives import stroked_quadratic_outline
from .flowcurve import stroked_periodic_flow_outline
from .geometry import polygon, profiled_open_bowl, profiled_ring, rect, thick_segment
from .moldcaster import DECIMAL_10, DYADIC_32, TRIHEX_36, Mold, Moldcaster
from .solver import ConstructionSolver


NUMERIC_OPEN_DNA = NUMERIC_DNA.derive(
    exponent_delta=-0.12,
    aperture_delta=0.045,
    terminal_delta=0.010,
)
NUMERIC_RING_DNA = NUMERIC_DNA.derive(exponent_delta=0.05)


@dataclass(frozen=True)
class NumericContext:
    cell: float
    body_height: float
    stroke: float
    mold: Mold
    open_profile: ResolvedCurve
    ring_profile: ResolvedCurve
    two_diagonal_angle: float


@dataclass(frozen=True)
class NumericMaster:
    source_cell: float = M.advance
    source_height: float = M.cap_height
    source_stroke: float = M.stroke
    source_overshoot: float = M.overshoot

    def _solver(self) -> ConstructionSolver:
        return ConstructionSolver(Moldcaster(self.source_cell))

    def _x(
        self,
        core_units: float,
        *,
        ctx: NumericContext,
        role: PointRole = PointRole.STEM,
        strength_scale: float = 0.72,
    ) -> float:
        source = core_units * CORE_UNIT
        return self._solver().solve_coordinate(
            source,
            target_span=ctx.cell,
            mold=ctx.mold,
            role=role,
            strength_scale=strength_scale,
        )

    def _y(self, core_units: float, *, ctx: NumericContext) -> float:
        return core_units / 20.0 * ctx.body_height

    def _overshoot(self, *, ctx: NumericContext) -> float:
        return self.source_overshoot / self.source_height * ctx.body_height

    @staticmethod
    def _angle_family(mold: Mold):
        if mold == DYADIC_32:
            return DYADIC_AXES
        if mold == DECIMAL_10:
            return DECIMAL_AXES
        return TRIHEX_AXES

    def resolve(
        self,
        *,
        target_cell: float | None = None,
        target_body_height: float | None = None,
        mold: Mold = TRIHEX_36,
        quantize_stroke: bool = False,
    ) -> NumericContext:
        target_cell = self.source_cell if target_cell is None else target_cell
        target_body_height = self.source_height if target_body_height is None else target_body_height
        if target_cell <= 0 or target_body_height <= 0:
            raise ValueError("target dimensions must be positive")

        caster = Moldcaster(self.source_cell)
        stroke = caster.cast_stroke(
            self.source_stroke,
            target_span=target_cell,
            mold=mold if quantize_stroke else None,
            quantize=quantize_stroke,
        )
        open_profile = resolve_curve(NUMERIC_OPEN_DNA, cell=target_cell, stroke=stroke)
        ring_profile = resolve_curve(NUMERIC_RING_DNA, cell=target_cell, stroke=stroke)

        seed_angle = math.degrees(math.atan2(8.0, 12.0))
        two_angle = self._solver().solve_angle(
            seed_angle,
            role=PointRole.STEM,
            families=(self._angle_family(mold),),
            strength_scale=0.72,
        )

        return NumericContext(
            cell=target_cell,
            body_height=target_body_height,
            stroke=stroke,
            mold=mold,
            open_profile=open_profile,
            ring_profile=ring_profile,
            two_diagonal_angle=two_angle,
        )

    def draw_two(self, pen: TTGlyphPen, ctx: NumericContext) -> None:
        x0 = self._x(2.0, ctx=ctx, role=PointRole.BOWL_EXTREMUM)
        x1 = self._x(16.0, ctx=ctx, role=PointRole.BOWL_EXTREMUM)
        over = self._overshoot(ctx=ctx)
        profiled_open_bowl(
            pen,
            x0,
            self._y(10.0, ctx=ctx),
            x1,
            ctx.body_height + over,
            stroke=ctx.stroke,
            profile=ctx.open_profile,
            opening="left",
            steps=52,
        )

        # A quadratic transition replaces the former independent diagonal. It
        # leaves the bowl's lower-right shoulder almost vertically and then
        # turns toward the baseline, visually approaching G1 continuity while
        # preserving the moldable source proportions.
        diagonal = stroked_quadratic_outline(
            (x1 - ctx.stroke * 0.32, self._y(13.0, ctx=ctx)),
            (x1 - ctx.stroke * 0.16, self._y(10.4, ctx=ctx)),
            (self._x(3.0, ctx=ctx, role=PointRole.TERMINAL, strength_scale=0.34), self._y(2.0, ctx=ctx)),
            stroke=ctx.stroke * 0.96,
            steps=36,
        )
        polygon(pen, diagonal, clockwise=True)
        rect(pen, self._x(2.0, ctx=ctx), 0.0, self._x(16.0, ctx=ctx), ctx.stroke)

    def draw_three(self, pen: TTGlyphPen, ctx: NumericContext) -> None:
        # Optical review showed that the first periodic 3 inherited too much of
        # the S gesture. Keep one continuous two-lobe equation, but reduce the
        # stiffness and pull the left terminals/notch inward. Right lobes remain
        # dominant, which restores numeric recognition without abandoning flow.
        left = self._x(4.0, ctx=ctx, role=PointRole.TERMINAL, strength_scale=0.30)
        right = self._x(15.0, ctx=ctx, role=PointRole.BOWL_EXTREMUM, strength_scale=0.42)
        over = self._overshoot(ctx=ctx)
        points = stroked_periodic_flow_outline(
            center_x=(left + right) / 2.0,
            top=ctx.body_height + over,
            bottom=-over,
            amplitude=(right - left) / 2.0,
            stroke=ctx.stroke,
            lobes=2,
            polarity=-1.0,
            stiffness=ctx.open_profile.exponent * 0.34,
            steps=112,
            terminal_relief=0.025,
            diagonal_compensation=0.012,
        )
        polygon(pen, points, clockwise=True)

    def draw_five(self, pen: TTGlyphPen, ctx: NumericContext) -> None:
        left = self._x(2.0, ctx=ctx)
        stem_right = self._x(4.0, ctx=ctx)
        right = self._x(16.0, ctx=ctx)
        rect(pen, left, ctx.body_height - ctx.stroke, right, ctx.body_height)
        rect(pen, left, self._y(10.0, ctx=ctx), stem_right, ctx.body_height)
        profiled_open_bowl(
            pen,
            left,
            -self._overshoot(ctx=ctx),
            right,
            self._y(11.0, ctx=ctx),
            stroke=ctx.stroke,
            profile=ctx.open_profile,
            opening="left",
            steps=52,
        )

    def draw_six(self, pen: TTGlyphPen, ctx: NumericContext) -> None:
        left = self._x(2.0, ctx=ctx)
        stem_right = self._x(4.0, ctx=ctx)
        right = self._x(16.0, ctx=ctx)
        over = self._overshoot(ctx=ctx)
        profiled_ring(
            pen,
            left,
            -over,
            right,
            self._y(12.0, ctx=ctx),
            stroke=ctx.stroke,
            profile=ctx.ring_profile,
            steps=52,
        )
        rect(pen, left, self._y(6.0, ctx=ctx), stem_right, self._y(17.0, ctx=ctx))
        thick_segment(
            pen,
            (left + stem_right) / 2.0,
            self._y(17.0, ctx=ctx),
            self._x(6.0, ctx=ctx, role=PointRole.TERMINAL, strength_scale=0.35),
            ctx.body_height,
            ctx.stroke * 0.82,
        )

    def draw_nine(self, pen: TTGlyphPen, ctx: NumericContext) -> None:
        left = self._x(2.0, ctx=ctx)
        stem_left = self._x(14.0, ctx=ctx)
        right = self._x(16.0, ctx=ctx)
        over = self._overshoot(ctx=ctx)
        profiled_ring(
            pen,
            left,
            self._y(8.0, ctx=ctx),
            right,
            ctx.body_height + over,
            stroke=ctx.stroke,
            profile=ctx.ring_profile,
            steps=52,
        )
        rect(pen, stem_left, self._y(3.0, ctx=ctx), right, self._y(14.0, ctx=ctx))
        thick_segment(
            pen,
            (stem_left + right) / 2.0,
            self._y(3.0, ctx=ctx),
            self._x(12.0, ctx=ctx, role=PointRole.TERMINAL, strength_scale=0.35),
            0.0,
            ctx.stroke * 0.82,
        )

    def draw(self, pen: TTGlyphPen, kind: str) -> None:
        ctx = self.resolve()
        drawers = {
            "2": self.draw_two,
            "3": self.draw_three,
            "5": self.draw_five,
            "6": self.draw_six,
            "9": self.draw_nine,
        }
        try:
            draw = drawers[kind]
        except KeyError as exc:
            raise ValueError("kind must be one of 2, 3, 5, 6, 9") from exc
        draw(pen, ctx)


NUMERIC_MASTER = NumericMaster()


def draw_2(pen: TTGlyphPen) -> None:
    NUMERIC_MASTER.draw(pen, "2")


def draw_3(pen: TTGlyphPen) -> None:
    NUMERIC_MASTER.draw(pen, "3")


def draw_5(pen: TTGlyphPen) -> None:
    NUMERIC_MASTER.draw(pen, "5")


def draw_6(pen: TTGlyphPen) -> None:
    NUMERIC_MASTER.draw(pen, "6")


def draw_9(pen: TTGlyphPen) -> None:
    NUMERIC_MASTER.draw(pen, "9")
