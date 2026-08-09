from __future__ import annotations

from dataclasses import dataclass


# Native construction quantum. The current mono cell is 18 cores wide.
# Half-core values are allowed for optical/spacing roles; the core is a moldable
# geometric reference, not a hard pixel grid.
CORE_UNIT = 36


@dataclass(frozen=True)
class Metrics:
    """Global font metrics derived from the 36-unit construction core.

    OpenType remains conventional at 1000 UPM. Design dimensions are expressed
    as rational multiples of CORE_UNIT so the geometry can be recast by the
    Moldcaster into decimal, dyadic and future production media.
    """

    upm: int = 1000
    core: int = CORE_UNIT
    advance: int = 18 * CORE_UNIT
    ascender: int = 800
    descender: int = -200
    cap_height: int = 20 * CORE_UNIT
    x_height: int = 15 * CORE_UNIT
    stroke: int = 2 * CORE_UNIT
    overshoot: int = CORE_UNIT // 3
    sidebearing: int = 3 * CORE_UNIT // 2
    round_radius: int = 5 * CORE_UNIT // 2
    accent_gap: int = 3 * CORE_UNIT // 2

    @property
    def left(self) -> int:
        return self.sidebearing

    @property
    def right(self) -> int:
        return self.advance - self.sidebearing

    @property
    def center(self) -> int:
        return self.advance // 2


@dataclass(frozen=True)
class Lattice:
    """Trihex construction guide retained for backwards-compatible glyph code.

    New geometry should prefer Moldcaster + role constraints. `soft_snap` remains
    a small convenience for existing diagnostic glyphs during migration.
    """

    cell: int = 18 * CORE_UNIT

    @property
    def core(self) -> int:
        return self.cell // 18

    @property
    def third(self) -> int:
        return self.cell // 3

    @property
    def sixth(self) -> int:
        return self.cell // 6

    @property
    def ninth(self) -> int:
        return self.cell // 9

    def step(self, division: int) -> float:
        if division <= 0:
            raise ValueError("division must be positive")
        return self.cell / division

    def x3(self, i: float) -> float:
        return i * self.third

    def x6(self, i: float) -> float:
        return i * self.sixth

    def x9(self, i: float) -> float:
        return i * self.ninth

    def soft_snap(self, value: float, *, division: int = 9, strength: float = 0.35) -> float:
        if not 0.0 <= strength <= 1.0:
            raise ValueError("strength must be between 0 and 1")
        step = self.step(division)
        target = round(value / step) * step
        return value + (target - value) * strength


M = Metrics()
L = Lattice(M.advance)

FAMILY_NAME = "Saygıyla Sunar Mono"
STYLE_NAME = "Regular"
POSTSCRIPT_NAME = "SaygiylaSunarMono-Regular"
VERSION = "0.4.0"
