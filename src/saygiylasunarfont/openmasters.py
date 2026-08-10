from __future__ import annotations

from dataclasses import dataclass

from fontTools.pens.ttGlyphPen import TTGlyphPen

from .config import CORE_UNIT, M
from .constraints import PointRole
from .curvature import OPEN_DNA, ResolvedCurve, resolve_curve
from .geometry import profiled_open_bowl, rect
from .moldcaster import TRIHEX_36, Mold, Moldcaster
from .solver import ConstructionSolver


# Open forms remain derivatives of one OPEN_DNA. Lowercase gets a little more
# flow and aperture; e adds a further recognition-oriented aperture adjustment.
LOWER_OPEN_DNA = OPEN_DNA.derive(
    exponent_delta=-0.12,
    aperture_delta=0.020,
    terminal_delta=0.010,
)
E_DNA = LOWER_OPEN_DNA.derive(aperture_delta=0.030)
G_DNA = OPEN_DNA.derive(aperture_delta=-0.010, terminal_delta=-0.008)


@dataclass(frozen=True)
class OpenRoundInstance:
    kind: str
    cell: float
    body_height: float
    x0: float
    x1: float
    y0: float
    y1: float
    stroke: float
    profile: ResolvedCurve
    crossbar_y: float | None = None
    crossbar_x0: float | None = None
    crossbar_x1: float | None = None
    spur_y0: float | None = None

    @property
    def center(self) -> float:
        return (self.x0 + self.x1) / 2.0


@dataclass(frozen=True)
class OpenRoundMaster:
    source_cell: float = M.advance
    source_cap_height: float = M.cap_height
    source_x_height: float = M.x_height
    source_stroke: float = M.stroke
    source_overshoot: float = M.overshoot
    upper_inset: float = 2 * CORE_UNIT
    lower_inset: float = 2.5 * CORE_UNIT

    def _solver(self) -> ConstructionSolver:
        return ConstructionSolver(Moldcaster(self.source_cell))

    def _resolve_inset(
        self,
        source_inset: float,
        *,
        target_cell: float,
        mold: Mold,
        lowercase: bool,
    ) -> tuple[float, float]:
        # Lowercase bowls get more optical freedom than cap forms.
        scale = 0.38 if lowercase else 1.0
        left = self._solver().solve_coordinate(
            source_inset,
            target_span=target_cell,
            mold=mold,
            role=PointRole.BOWL_EXTREMUM,
            strength_scale=scale,
        )
        return left, target_cell - left

    @staticmethod
    def _scale(value: float, source_span: float, target_span: float) -> float:
        return value / source_span * target_span

    def resolve(
        self,
        kind: str,
        *,
        target_cell: float | None = None,
        target_body_height: float | None = None,
        mold: Mold = TRIHEX_36,
        quantize_stroke: bool = False,
    ) -> OpenRoundInstance:
        if kind not in {"C", "G", "c", "e"}:
            raise ValueError("kind must be one of C, G, c, e")

        lowercase = kind.islower()
        source_height = self.source_x_height if lowercase else self.source_cap_height
        target_cell = self.source_cell if target_cell is None else target_cell
        target_body_height = source_height if target_body_height is None else target_body_height
        if target_cell <= 0 or target_body_height <= 0:
            raise ValueError("target dimensions must be positive")

        x0, x1 = self._resolve_inset(
            self.lower_inset if lowercase else self.upper_inset,
            target_cell=target_cell,
            mold=mold,
            lowercase=lowercase,
        )
        caster = Moldcaster(self.source_cell)
        stroke = caster.cast_stroke(
            self.source_stroke,
            target_span=target_cell,
            mold=mold if quantize_stroke else None,
            quantize=quantize_stroke,
        )

        if kind == "G":
            dna = G_DNA
        elif kind == "e":
            dna = E_DNA
        elif lowercase:
            dna = LOWER_OPEN_DNA
        else:
            dna = OPEN_DNA
        profile = resolve_curve(dna, cell=target_cell, stroke=stroke)

        overshoot = self._scale(
            self.source_overshoot,
            source_height,
            target_body_height,
        )
        instance = OpenRoundInstance(
            kind=kind,
            cell=target_cell,
            body_height=target_body_height,
            x0=x0,
            x1=x1,
            y0=-overshoot,
            y1=target_body_height + overshoot,
            stroke=stroke,
            profile=profile,
        )

        if kind == "e":
            # The eye sits on the mathematical midline, while its right terminal
            # stops before the outer extremum so the aperture stays visible.
            return OpenRoundInstance(
                **{
                    **instance.__dict__,
                    "crossbar_y": target_body_height * 0.50,
                    "crossbar_x0": x0 + stroke * 0.72,
                    "crossbar_x1": x1 - target_cell * (0.45 / 18.0),
                }
            )

        if kind == "G":
            # G uses one integrated documentary shelf plus a short downward spur.
            # The shelf is intentionally below center so it reads as G, not C+dash.
            crossbar_y = target_body_height * 0.42
            return OpenRoundInstance(
                **{
                    **instance.__dict__,
                    "crossbar_y": crossbar_y,
                    "crossbar_x0": target_cell * 0.47,
                    "crossbar_x1": x1 - target_cell * (0.20 / 18.0),
                    "spur_y0": crossbar_y - target_body_height * 0.20,
                }
            )

        return instance

    def draw(self, pen: TTGlyphPen, kind: str) -> None:
        instance = self.resolve(kind)
        profiled_open_bowl(
            pen,
            instance.x0,
            instance.y0,
            instance.x1,
            instance.y1,
            stroke=instance.stroke,
            profile=instance.profile,
            opening="right",
            steps=56,
        )

        if instance.crossbar_y is not None:
            assert instance.crossbar_x0 is not None
            assert instance.crossbar_x1 is not None
            y = instance.crossbar_y
            rect(
                pen,
                instance.crossbar_x0,
                y - instance.stroke / 2.0,
                instance.crossbar_x1,
                y + instance.stroke / 2.0,
            )

        if kind == "G":
            assert instance.spur_y0 is not None
            assert instance.crossbar_x1 is not None
            rect(
                pen,
                instance.crossbar_x1 - instance.stroke,
                instance.spur_y0,
                instance.crossbar_x1,
                instance.crossbar_y + instance.stroke / 2.0,  # type: ignore[operator]
            )


OPEN_MASTER = OpenRoundMaster()


def draw_C(pen: TTGlyphPen) -> None:
    OPEN_MASTER.draw(pen, "C")


def draw_G(pen: TTGlyphPen) -> None:
    OPEN_MASTER.draw(pen, "G")


def draw_c(pen: TTGlyphPen) -> None:
    OPEN_MASTER.draw(pen, "c")


def draw_e(pen: TTGlyphPen) -> None:
    OPEN_MASTER.draw(pen, "e")
