from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Metrics:
    """Global font metrics.

    The OpenType container stays conventional (1000 UPM), while the current
    monospaced cell is 648 units wide. The 3/6/9 lattice is a useful construction
    guide, not a law that is allowed to damage glyph recognition.
    """

    upm: int = 1000
    advance: int = 648
    ascender: int = 800
    descender: int = -200
    cap_height: int = 720
    x_height: int = 540
    stroke: int = 72
    overshoot: int = 12
    sidebearing: int = 54
    round_radius: int = 90
    accent_gap: int = 54

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
    """3/6/9 construction grid with optional optical attraction.

    Geometry may land exactly on the lattice when that improves rhythm, or use
    `soft_snap` to retain the mathematical accent without sacrificing legibility.
    """

    cell: int = 648

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
        """Attract a coordinate toward the lattice without forcing it there."""
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
VERSION = "0.3.0"
