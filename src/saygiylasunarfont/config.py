from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Metrics:
    upm: int = 1000
    advance: int = 600
    ascender: int = 800
    descender: int = -200
    cap_height: int = 700
    x_height: int = 500
    stroke: int = 80
    overshoot: int = 12
    sidebearing: int = 50
    round_inset: int = 72
    corner: int = 92
    accent_gap: int = 55

    @property
    def left(self) -> int:
        return self.sidebearing

    @property
    def right(self) -> int:
        return self.advance - self.sidebearing

    @property
    def center(self) -> int:
        return self.advance // 2


M = Metrics()

# Deliberately explicit. These are design invariants, not incidental constants.
FAMILY_NAME = "Saygıyla Sunar Mono"
STYLE_NAME = "Regular"
POSTSCRIPT_NAME = "SaygiylaSunarMono-Regular"
VERSION = "0.1.0"
