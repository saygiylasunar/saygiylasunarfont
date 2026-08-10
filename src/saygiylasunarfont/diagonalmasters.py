from __future__ import annotations

import math
from dataclasses import dataclass

from fontTools.pens.ttGlyphPen import TTGlyphPen

from .config import CORE_UNIT, M
from .constraints import DECIMAL_AXES, DYADIC_AXES, TRIHEX_AXES, PointRole
from .geometry import axis_segment, rect, thick_segment
from .moldcaster import DECIMAL_10, DYADIC_32, TRIHEX_36, Mold, Moldcaster
from .solver import ConstructionSolver


@dataclass(frozen=True)
class DiagonalContext:
    cell: float
    body_height: float
    stroke: float
    mold: Mold
    v_angle: float
    z_angle: float
    w_points: tuple[tuple[float, float], ...]


@dataclass(frozen=True)
class DiagonalMaster:
    source_cell: float = M.advance
    source_height: float = M.cap_height
    source_stroke: float = M.stroke

    def _solver(self) -> ConstructionSolver:
        return ConstructionSolver(Moldcaster(self.source_cell))

    @staticmethod
    def _angle_family(mold: Mold):
        if mold == DYADIC_32:
            return DYADIC_AXES
        if mold == DECIMAL_10:
            return DECIMAL_AXES
        return TRIHEX_AXES

    def _x(
        self,
        core_units: float,
        *,
        target_cell: float,
        mold: Mold,
        role: PointRole = PointRole.STEM,
        strength_scale: float = 0.55,
    ) -> float:
        return self._solver().solve_coordinate(
            core_units * CORE_UNIT,
            target_span=target_cell,
            mold=mold,
            role=role,
            strength_scale=strength_scale,
        )

    @staticmethod
    def _fit_angle(
        proposed: float,
        *,
        vertical_span: float,
        max_horizontal_run: float,
    ) -> float:
        """Keep a mold-attracted diagonal inside its monospaced construction box."""
        if vertical_span <= 0 or max_horizontal_run <= 0:
            raise ValueError("fit spans must be positive")
        minimum = math.degrees(math.atan2(vertical_span, max_horizontal_run))
        return max(minimum, min(89.0, proposed))

    def resolve(
        self,
        *,
        target_cell: float | None = None,
        target_body_height: float | None = None,
        mold: Mold = TRIHEX_36,
        quantize_stroke: bool = False,
    ) -> DiagonalContext:
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
        family = self._angle_family(mold)

        # V starts from a 7-core horizontal run over the 20-core cap height.
        v_seed = math.degrees(math.atan2(20.0, 7.0))
        v_proposed = self._solver().solve_angle(
            v_seed,
            role=PointRole.STEM,
            families=(family,),
            strength_scale=0.42,
        )
        v_angle = self._fit_angle(
            v_proposed,
            vertical_span=target_body_height,
            max_horizontal_run=target_cell / 2.0 - CORE_UNIT * target_cell / self.source_cell,
        )

        # Z has more room to respond to the target mold. Its seed comes from a
        # 12-core horizontal run over an 18-core effective vertical stroke span.
        z_seed = math.degrees(math.atan2(18.0, 12.0))
        z_proposed = self._solver().solve_angle(
            z_seed,
            role=PointRole.STEM,
            families=(family,),
            strength_scale=0.68,
        )
        z_vertical = target_body_height - stroke
        z_angle = self._fit_angle(
            z_proposed,
            vertical_span=z_vertical,
            max_horizontal_run=target_cell - 4.0 * CORE_UNIT * target_cell / self.source_cell,
        )

        outer_left = self._x(1.0, target_cell=target_cell, mold=mold, strength_scale=0.30)
        inner_left = self._x(5.0, target_cell=target_cell, mold=mold, strength_scale=0.36)
        center = target_cell / 2.0
        center_y = 8.0 / 20.0 * target_body_height
        w_points = (
            (outer_left, target_body_height),
            (inner_left, 0.0),
            (center, center_y),
            (target_cell - inner_left, 0.0),
            (target_cell - outer_left, target_body_height),
        )

        return DiagonalContext(
            cell=target_cell,
            body_height=target_body_height,
            stroke=stroke,
            mold=mold,
            v_angle=v_angle,
            z_angle=z_angle,
            w_points=w_points,
        )

    def draw_V(self, pen: TTGlyphPen, ctx: DiagonalContext) -> None:
        run = ctx.body_height / math.tan(math.radians(ctx.v_angle))
        center = ctx.cell / 2.0
        thick_segment(pen, center - run, ctx.body_height, center, 0.0, ctx.stroke)
        thick_segment(pen, center, 0.0, center + run, ctx.body_height, ctx.stroke)

    def draw_W(self, pen: TTGlyphPen, ctx: DiagonalContext) -> None:
        width = ctx.stroke * 0.92
        for a, b in zip(ctx.w_points, ctx.w_points[1:]):
            thick_segment(pen, a[0], a[1], b[0], b[1], width)

    def draw_Z(self, pen: TTGlyphPen, ctx: DiagonalContext) -> None:
        left = self._x(2.0, target_cell=ctx.cell, mold=ctx.mold)
        right = self._x(16.0, target_cell=ctx.cell, mold=ctx.mold)
        rect(pen, left, ctx.body_height - ctx.stroke, right, ctx.body_height)
        rect(pen, left, 0.0, right, ctx.stroke)
        vertical_span = ctx.body_height - ctx.stroke
        length = vertical_span / math.sin(math.radians(ctx.z_angle))
        axis_segment(
            pen,
            ctx.cell / 2.0,
            ctx.body_height / 2.0,
            length,
            180.0 - ctx.z_angle,
            ctx.stroke,
        )

    def draw(self, pen: TTGlyphPen, kind: str) -> None:
        ctx = self.resolve()
        if kind == "V":
            self.draw_V(pen, ctx)
        elif kind == "W":
            self.draw_W(pen, ctx)
        elif kind == "Z":
            self.draw_Z(pen, ctx)
        else:
            raise ValueError("kind must be one of V, W, Z")


DIAGONAL_MASTER = DiagonalMaster()


def draw_V(pen: TTGlyphPen) -> None:
    DIAGONAL_MASTER.draw(pen, "V")


def draw_W(pen: TTGlyphPen) -> None:
    DIAGONAL_MASTER.draw(pen, "W")


def draw_Z(pen: TTGlyphPen) -> None:
    DIAGONAL_MASTER.draw(pen, "Z")
