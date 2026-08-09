from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Metrics:
    """Global font metrics.

    The OpenType container stays conventional (1000 UPM), while the glyph cell
    is deliberately 648 units wide so it divides exactly into 3, 6 and 9.
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
    """3/6/9 construction grid for the monospaced cell."""

    cell: int = 648

    @property
    def third(self) -> int:
        return self.cell // 3  # 216

    @property
    def sixth(self) -> int:
        return self.cell // 6  # 108

    @property
    def ninth(self) -> int:
        return self.cell // 9  # 72

    def x3(self, i: float) -> float:
        return i * self.third

    def x6(self, i: float) -> float:
        return i * self.sixth

    def x9(self, i: float) -> float:
        return i * self.ninth


M = Metrics()
L = Lattice(M.advance)

FAMILY_NAME = "Saygıyla Sunar Mono"
STYLE_NAME = "Regular"
POSTSCRIPT_NAME = "SaygiylaSunarMono-Regular"
VERSION = "0.2.0"
