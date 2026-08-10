from __future__ import annotations

from dataclasses import dataclass

from fontTools.pens.ttGlyphPen import TTGlyphPen

from .config import CORE_UNIT, M
from .constraints import PointRole
from .curvature import FLOW_DNA, ResolvedCurve, resolve_curve
from .flowcurve import stroked_flow_outline
from .geometry import polygon
from .moldcaster import TRIHEX_36, Mold, Moldcaster
from .solver import ConstructionSolver


# The S family is not drawn as stacked bowls. It derives a continuous spine from
# FLOW_DNA, then expands that spine by the resolved stroke. Lowercase relaxes the
# same identity rather than introducing a separate curve language.
LOWER_FLOW_DNA = FLOW_DNA.derive(
    exponent_delta=-0.14,
    terminal_delta=0.010,
)


@dataclass(frozen=True)
class FlowInstance:
    kind: str
    cell: float
    body_height: float
    center_x: float
    top: float
    bottom: float
    amplitude: float
    stroke: float
    profile: ResolvedCurve
    harmonic_mix: float
    stiffness: float

    @property
    def right_terminal_x(self) -> float:
        return self.center_x + self.amplitude

    @property
    def left_terminal_x(self) -> float:
        return self.center_x - self.amplitude


@dataclass(frozen=True)
class FlowMaster:
    source_cell: float = M.advance
    source_cap_height: float = M.cap_height
    source_x_height: float = M.x_height
    source_stroke: float = M.stroke
    source_overshoot: float = M.overshoot

    # Optical review showed that the first harmonic S exposed its mathematics
    # too strongly. Keep the third harmonic, but give it less authority while
    # increasing the continuous stiffness transform. Quarter-core amplitude
    # corrections widen the silhouette without abandoning the 36-core mold.
    upper_amplitude: float = 6.25 * CORE_UNIT
    lower_amplitude: float = 5.75 * CORE_UNIT
    upper_harmonic_mix: float = 0.66
    lower_harmonic_mix: float = 0.62
    stiffness_gain: float = 0.76

    def _solver(self) -> ConstructionSolver:
        return ConstructionSolver(Moldcaster(self.source_cell))

    @staticmethod
    def _scale(value: float, source_span: float, target_span: float) -> float:
        return value / source_span * target_span

    def _resolve_amplitude(
        self,
        source_amplitude: float,
        *,
        target_cell: float,
        mold: Mold,
        lowercase: bool,
    ) -> float:
        source_right = self.source_cell / 2.0 + source_amplitude
        solved_right = self._solver().solve_coordinate(
            source_right,
            target_span=target_cell,
            mold=mold,
            role=PointRole.TERMINAL,
            strength_scale=0.22 if lowercase else 0.62,
        )
        return solved_right - target_cell / 2.0

    def resolve(
        self,
        kind: str,
        *,
        target_cell: float | None = None,
        target_body_height: float | None = None,
        mold: Mold = TRIHEX_36,
        quantize_stroke: bool = False,
    ) -> FlowInstance:
        if kind not in {"S", "s"}:
            raise ValueError("kind must be 'S' or 's'")

        lowercase = kind == "s"
        source_height = self.source_x_height if lowercase else self.source_cap_height
        target_cell = self.source_cell if target_cell is None else target_cell
        target_body_height = source_height if target_body_height is None else target_body_height
        if target_cell <= 0 or target_body_height <= 0:
            raise ValueError("target dimensions must be positive")

        caster = Moldcaster(self.source_cell)
        stroke = caster.cast_stroke(
            self.source_stroke,
            target_span=target_cell,
            mold=mold if quantize_stroke else None,
            quantize=quantize_stroke,
        )

        dna = LOWER_FLOW_DNA if lowercase else FLOW_DNA
        profile = resolve_curve(dna, cell=target_cell, stroke=stroke)
        amplitude = self._resolve_amplitude(
            self.lower_amplitude if lowercase else self.upper_amplitude,
            target_cell=target_cell,
            mold=mold,
            lowercase=lowercase,
        )
        overshoot = self._scale(
            self.source_overshoot,
            source_height,
            target_body_height,
        )

        return FlowInstance(
            kind=kind,
            cell=target_cell,
            body_height=target_body_height,
            center_x=target_cell / 2.0,
            top=target_body_height + overshoot,
            bottom=-overshoot,
            amplitude=amplitude,
            stroke=stroke,
            profile=profile,
            harmonic_mix=self.lower_harmonic_mix if lowercase else self.upper_harmonic_mix,
            stiffness=profile.exponent * self.stiffness_gain,
        )

    def outline(self, kind: str, **kwargs: object) -> list[tuple[float, float]]:
        instance = self.resolve(kind, **kwargs)
        return stroked_flow_outline(
            center_x=instance.center_x,
            top=instance.top,
            bottom=instance.bottom,
            amplitude=instance.amplitude,
            stroke=instance.stroke,
            harmonic_mix=instance.harmonic_mix,
            stiffness=instance.stiffness,
            steps=88,
            terminal_relief=0.010,
            diagonal_compensation=0.012,
        )

    def draw(self, pen: TTGlyphPen, kind: str) -> None:
        polygon(pen, self.outline(kind), clockwise=True)


FLOW_MASTER = FlowMaster()


def draw_S(pen: TTGlyphPen) -> None:
    FLOW_MASTER.draw(pen, "S")


def draw_s(pen: TTGlyphPen) -> None:
    FLOW_MASTER.draw(pen, "s")
