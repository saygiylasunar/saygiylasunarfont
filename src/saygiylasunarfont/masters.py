from __future__ import annotations

from dataclasses import dataclass, replace

from fontTools.pens.ttGlyphPen import TTGlyphPen

from .config import CORE_UNIT, M
from .constraints import DYADIC_AXES, TRIHEX_AXES, PointRole
from .curvature import BOWL_DNA, ResolvedCurve, resolve_curve
from .geometry import axis_segment, profiled_ring
from .moldcaster import DYADIC_32, TRIHEX_36, Mold, Moldcaster
from .solver import ConstructionSolver


# Zero remains a derivative of the round family. It is only slightly stiffer
# and vertically biased; the slash and a restrained width difference carry most
# of the documentary disambiguation.
ZERO_DNA = BOWL_DNA.derive(exponent_delta=0.10, axis_bias_delta=0.015)


@dataclass(frozen=True)
class O0Instance:
    """Resolved O/0 construction in one output medium."""

    kind: str
    cell: float
    cap_height: float
    x0: float
    x1: float
    y0: float
    y1: float
    stroke: float
    profile: ResolvedCurve
    slash_angle: float | None = None
    slash_length: float | None = None
    slash_width: float | None = None

    @property
    def width(self) -> float:
        return self.x1 - self.x0

    @property
    def center(self) -> float:
        return (self.x0 + self.x1) / 2.0


@dataclass(frozen=True)
class O0Master:
    """First master mold of the typeface.

    Geometry is authored once in the native 36-core cell, then interpreted by a
    target mold. The O is the pure round-family carrier; zero is a documentary
    derivative, not a separate design language.
    """

    source_cell: float = M.advance
    source_cap_height: float = M.cap_height
    source_stroke: float = M.stroke
    source_overshoot: float = M.overshoot
    o_inset: float = 2 * CORE_UNIT
    zero_inset: float = 2.25 * CORE_UNIT
    slash_seed_angle: float = 54.0
    slash_length_ratio: float = 0.78
    slash_width_ratio: float = 0.68

    def _solver(self) -> ConstructionSolver:
        return ConstructionSolver(Moldcaster(self.source_cell))

    def _solve_symmetric_inset(
        self,
        inset: float,
        *,
        target_cell: float,
        mold: Mold,
        strength_scale: float,
    ) -> tuple[float, float]:
        left = self._solver().solve_coordinate(
            inset,
            target_span=target_cell,
            mold=mold,
            role=PointRole.BOWL_EXTREMUM,
            strength_scale=strength_scale,
        )
        return left, target_cell - left

    def _cast_vertical(self, value: float, *, target_cap_height: float) -> float:
        # Vertical overshoot may sit outside the nominal [0, cap] interval, so it
        # is scaled affinely rather than sent through bounded mold attraction.
        return value / self.source_cap_height * target_cap_height

    def resolve(
        self,
        kind: str,
        *,
        target_cell: float | None = None,
        target_cap_height: float | None = None,
        mold: Mold = TRIHEX_36,
        quantize_stroke: bool = False,
    ) -> O0Instance:
        if kind not in {"O", "0"}:
            raise ValueError("kind must be 'O' or '0'")

        target_cell = self.source_cell if target_cell is None else target_cell
        target_cap_height = (
            self.source_cap_height if target_cap_height is None else target_cap_height
        )
        if target_cell <= 0 or target_cap_height <= 0:
            raise ValueError("target dimensions must be positive")

        is_zero = kind == "0"
        inset = self.zero_inset if is_zero else self.o_inset
        # O is allowed to sit firmly on the native lattice. Zero keeps some
        # optical freedom so its narrower silhouette does not collapse back into O.
        strength_scale = 0.38 if is_zero else 1.0
        x0, x1 = self._solve_symmetric_inset(
            inset,
            target_cell=target_cell,
            mold=mold,
            strength_scale=strength_scale,
        )

        caster = Moldcaster(self.source_cell)
        stroke = caster.cast_stroke(
            self.source_stroke,
            target_span=target_cell,
            mold=mold if quantize_stroke else None,
            quantize=quantize_stroke,
        )
        dna = ZERO_DNA if is_zero else BOWL_DNA
        profile = resolve_curve(dna, cell=target_cell, stroke=stroke)

        overshoot = self._cast_vertical(
            self.source_overshoot,
            target_cap_height=target_cap_height,
        )
        instance = O0Instance(
            kind=kind,
            cell=target_cell,
            cap_height=target_cap_height,
            x0=x0,
            x1=x1,
            y0=-overshoot,
            y1=target_cap_height + overshoot,
            stroke=stroke,
            profile=profile,
        )
        if not is_zero:
            return instance

        angle_families = (DYADIC_AXES,) if mold == DYADIC_32 else (TRIHEX_AXES,)
        slash_angle = self._solver().solve_angle(
            self.slash_seed_angle,
            role=PointRole.TERMINAL,
            families=angle_families,
        )
        slash_length = target_cap_height * self.slash_length_ratio
        slash_width = stroke * self.slash_width_ratio
        if quantize_stroke:
            quantum = target_cell / mold.finest_division
            slash_width = max(quantum, round(slash_width / quantum) * quantum)

        return replace(
            instance,
            slash_angle=slash_angle,
            slash_length=slash_length,
            slash_width=slash_width,
        )

    def draw(self, pen: TTGlyphPen, kind: str) -> None:
        instance = self.resolve(kind)
        profiled_ring(
            pen,
            instance.x0,
            instance.y0,
            instance.x1,
            instance.y1,
            stroke=instance.stroke,
            profile=instance.profile,
            steps=64,
        )
        if kind == "0":
            assert instance.slash_angle is not None
            assert instance.slash_length is not None
            assert instance.slash_width is not None
            axis_segment(
                pen,
                instance.cell / 2.0,
                instance.cap_height / 2.0,
                instance.slash_length,
                instance.slash_angle,
                instance.slash_width,
            )


O0_MASTER = O0Master()


def draw_O(pen: TTGlyphPen) -> None:
    O0_MASTER.draw(pen, "O")


def draw_zero(pen: TTGlyphPen) -> None:
    O0_MASTER.draw(pen, "0")
