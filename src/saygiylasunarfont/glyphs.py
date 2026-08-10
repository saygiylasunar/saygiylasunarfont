from __future__ import annotations

from collections.abc import Callable

from fontTools.pens.ttGlyphPen import TTGlyphPen

from .config import L, M
from .geometry import axis_segment, dot, open_soft_bowl, polygon, rect, rounded_rect, soft_ring, thick_segment

Draw = Callable[[TTGlyphPen], None]


def _glyph(draw: Draw | None = None):
    pen = TTGlyphPen(None)
    if draw:
        draw(pen)
    return pen.glyph()


def _notdef(pen: TTGlyphPen) -> None:
    rounded_rect(pen, L.x9(1), 0, L.x9(8), M.cap_height, M.round_radius)
    rounded_rect(
        pen,
        L.x9(2), M.stroke,
        L.x9(7), M.cap_height - M.stroke,
        M.round_radius / 2,
        clockwise=False,
    )


# --- Core stems / terminal ambiguities ------------------------------------


def _H(pen: TTGlyphPen) -> None:
    rect(pen, L.x9(1), 0, L.x9(2), M.cap_height)
    rect(pen, L.x9(7), 0, L.x9(8), M.cap_height)
    rect(pen, L.x9(1), M.cap_height / 2 - M.stroke / 2, L.x9(8), M.cap_height / 2 + M.stroke / 2)


def _I(pen: TTGlyphPen) -> None:
    rect(pen, L.x9(2), M.cap_height - M.stroke, L.x9(7), M.cap_height)
    rect(pen, M.center - M.stroke / 2, 0, M.center + M.stroke / 2, M.cap_height)
    rect(pen, L.x9(2), 0, L.x9(7), M.stroke)


def _l(pen: TTGlyphPen) -> None:
    rect(pen, M.center - M.stroke / 2, 0, M.center + M.stroke / 2, M.cap_height)
    rect(pen, M.center - M.stroke / 2, 0, L.x9(6.5), M.stroke)


def _i(pen: TTGlyphPen) -> None:
    rect(pen, M.center - M.stroke / 2, 0, M.center + M.stroke / 2, M.x_height - L.ninth)
    dot(pen, M.center, M.x_height - L.ninth / 6, M.stroke)


def _dotless_i(pen: TTGlyphPen) -> None:
    rect(pen, M.center - M.stroke / 2, 0, M.center + M.stroke / 2, M.x_height)


def _one(pen: TTGlyphPen) -> None:
    rect(pen, M.center - M.stroke / 2, 0, M.center + M.stroke / 2, M.cap_height)
    thick_segment(pen, L.x9(2.8), M.cap_height - L.ninth, M.center, M.cap_height, M.stroke)
    rect(pen, L.x9(2.25), 0, L.x9(6.75), M.stroke)


# --- Primary round system -------------------------------------------------


def _O(pen: TTGlyphPen) -> None:
    soft_ring(
        pen,
        L.x9(1), -M.overshoot,
        L.x9(8), M.cap_height + M.overshoot,
        stroke=M.stroke,
        radius=L.sixth,
    )


def _zero(pen: TTGlyphPen) -> None:
    _O(pen)
    axis_segment(
        pen,
        M.center,
        M.cap_height / 2,
        M.cap_height * 0.72,
        66,
        M.stroke * 0.72,
    )


def _o(pen: TTGlyphPen) -> None:
    soft_ring(
        pen,
        L.x9(1.25), -M.overshoot,
        L.x9(7.75), M.x_height + M.overshoot,
        stroke=M.stroke,
        radius=M.round_radius,
    )


def _a(pen: TTGlyphPen) -> None:
    _o(pen)
    rect(pen, L.x9(6.75), 0, L.x9(7.75), M.x_height)
    thick_segment(pen, L.x9(7.2), L.ninth * 0.35, L.x9(8.2), 0, M.stroke * 0.72)


def _g(pen: TTGlyphPen) -> None:
    _o(pen)
    rect(pen, L.x9(6.75), -L.x9(2.25), L.x9(7.75), M.x_height)
    rect(pen, L.x9(3.4), -L.x9(2.25), L.x9(7.75), -L.x9(1.25))
    thick_segment(pen, L.x9(3.4), -L.x9(2.25), L.x9(2.4), -L.x9(1.7), M.stroke * 0.72)


def _open_bowl(
    pen: TTGlyphPen,
    *,
    top: float,
    bottom: float,
    lowercase: bool = False,
    crossbar: bool = False,
) -> None:
    x0, x1 = (L.x9(1.25), L.x9(7.75)) if lowercase else (L.x9(1), L.x9(8))
    radius = M.round_radius if lowercase else L.sixth
    aperture = L.third * 1.05 if not lowercase else M.x_height * 0.46
    open_soft_bowl(
        pen,
        x0, bottom, x1, top,
        stroke=M.stroke,
        radius=radius,
        aperture=aperture,
        opening="right",
    )
    if crossbar:
        mid = (top + bottom) / 2
        rect(pen, x0 + M.stroke * 0.75, mid - M.stroke / 2, x1 - M.stroke * 0.9, mid + M.stroke / 2)


def _C(pen: TTGlyphPen) -> None:
    _open_bowl(pen, top=M.cap_height + M.overshoot, bottom=-M.overshoot)


def _c(pen: TTGlyphPen) -> None:
    _open_bowl(pen, top=M.x_height + M.overshoot, bottom=-M.overshoot, lowercase=True)


def _e(pen: TTGlyphPen) -> None:
    _open_bowl(
        pen,
        top=M.x_height + M.overshoot,
        bottom=-M.overshoot,
        lowercase=True,
        crossbar=True,
    )


def _G(pen: TTGlyphPen) -> None:
    _C(pen)
    y = M.cap_height * 0.42
    rect(pen, L.x9(4.5), y, L.x9(8), y + M.stroke)
    rect(pen, L.x9(7), L.x9(2.1), L.x9(8), y + M.stroke)


def _rounded_s(pen: TTGlyphPen, top: float, lowercase: bool = False) -> None:
    mid = top / 2
    x0, x1 = (L.x9(1.4), L.x9(7.6)) if lowercase else (L.x9(1.1), L.x9(7.9))
    radius = M.round_radius * 0.9 if lowercase else L.sixth * 0.9
    stroke = M.stroke * (0.92 if lowercase else 1.0)
    overlap = M.stroke * 0.28
    aperture = top / 2.65
    open_soft_bowl(
        pen, x0, mid - overlap, x1, top + M.overshoot,
        stroke=stroke, radius=radius, aperture=aperture, opening="right",
    )
    open_soft_bowl(
        pen, x0, -M.overshoot, x1, mid + overlap,
        stroke=stroke, radius=radius, aperture=aperture, opening="left",
    )


def _S(pen: TTGlyphPen) -> None:
    _rounded_s(pen, M.cap_height)


def _s(pen: TTGlyphPen) -> None:
    _rounded_s(pen, M.x_height, lowercase=True)


# --- Stiff diagonal family ------------------------------------------------


def _T(pen: TTGlyphPen) -> None:
    rect(pen, L.x9(1), M.cap_height - M.stroke, L.x9(8), M.cap_height)
    rect(pen, M.center - M.stroke / 2, 0, M.center + M.stroke / 2, M.cap_height)


def _Z(pen: TTGlyphPen) -> None:
    rect(pen, L.x9(1), M.cap_height - M.stroke, L.x9(8), M.cap_height)
    thick_segment(pen, L.x9(7.55), M.cap_height - M.stroke / 2, L.x9(1.45), M.stroke / 2, M.stroke * 1.05)
    rect(pen, L.x9(1), 0, L.x9(8), M.stroke)


def _V(pen: TTGlyphPen) -> None:
    thick_segment(pen, L.x9(1.35), M.cap_height, M.center, 0, M.stroke * 1.08)
    thick_segment(pen, M.center, 0, L.x9(7.65), M.cap_height, M.stroke * 1.08)


def _W(pen: TTGlyphPen) -> None:
    w = M.stroke
    thick_segment(pen, L.x9(0.85), M.cap_height, L.x9(2.8), 0, w)
    thick_segment(pen, L.x9(2.8), 0, M.center, L.x9(3.8), w)
    thick_segment(pen, M.center, L.x9(3.8), L.x9(6.2), 0, w)
    thick_segment(pen, L.x9(6.2), 0, L.x9(8.15), M.cap_height, w)


# --- U family -------------------------------------------------------------


def _U(pen: TTGlyphPen) -> None:
    rect(pen, L.x9(1), L.ninth, L.x9(2), M.cap_height)
    rect(pen, L.x9(7), L.ninth, L.x9(8), M.cap_height)
    rounded_rect(pen, L.x9(1), 0, L.x9(8), L.x9(2), L.ninth, clockwise=True)
    rounded_rect(pen, L.x9(2), M.stroke, L.x9(7), L.x9(2), M.round_radius / 2, clockwise=False)


def _u(pen: TTGlyphPen) -> None:
    rect(pen, L.x9(1.25), L.ninth, L.x9(2.25), M.x_height)
    rect(pen, L.x9(6.75), 0, L.x9(7.75), M.x_height)
    rect(pen, L.x9(2), 0, L.x9(7.25), M.stroke)
    thick_segment(pen, L.x9(1.75), L.ninth, L.x9(2.4), M.stroke / 2, M.stroke * 0.8)


# --- Numerals -------------------------------------------------------------


def _digit_two(pen: TTGlyphPen) -> None:
    open_soft_bowl(
        pen, L.x9(1.2), M.cap_height * 0.48, L.x9(7.8), M.cap_height + M.overshoot,
        stroke=M.stroke, radius=M.round_radius, aperture=L.third * 0.9, opening="left",
    )
    thick_segment(pen, L.x9(7.2), M.cap_height * 0.48, L.x9(1.4), M.stroke, M.stroke)
    rect(pen, L.x9(1), 0, L.x9(8), M.stroke)


def _digit_three(pen: TTGlyphPen) -> None:
    mid = M.cap_height / 2
    open_soft_bowl(
        pen, L.x9(1.4), mid - M.stroke * 0.2, L.x9(7.8), M.cap_height + M.overshoot,
        stroke=M.stroke, radius=M.round_radius, aperture=L.third * 0.75, opening="left",
    )
    open_soft_bowl(
        pen, L.x9(1.4), -M.overshoot, L.x9(7.8), mid + M.stroke * 0.2,
        stroke=M.stroke, radius=M.round_radius, aperture=L.third * 0.75, opening="left",
    )


def _digit_four(pen: TTGlyphPen) -> None:
    thick_segment(pen, L.x9(2), M.cap_height, L.x9(1.1), M.cap_height * 0.42, M.stroke)
    rect(pen, L.x9(1.1), M.cap_height * 0.38, L.x9(8), M.cap_height * 0.38 + M.stroke)
    rect(pen, L.x9(6.7), 0, L.x9(7.7), M.cap_height)


def _digit_five(pen: TTGlyphPen) -> None:
    rect(pen, L.x9(1), M.cap_height - M.stroke, L.x9(8), M.cap_height)
    rect(pen, L.x9(1), M.cap_height / 2, L.x9(2), M.cap_height)
    open_soft_bowl(
        pen, L.x9(1), -M.overshoot, L.x9(8), M.cap_height / 2 + M.stroke,
        stroke=M.stroke, radius=M.round_radius, aperture=L.third * 0.8, opening="left",
    )


def _digit_six(pen: TTGlyphPen) -> None:
    soft_ring(
        pen, L.x9(1), -M.overshoot, L.x9(8), M.cap_height * 0.58,
        stroke=M.stroke, radius=L.ninth,
    )
    rect(pen, L.x9(1), M.cap_height * 0.3, L.x9(2), M.cap_height * 0.86)
    thick_segment(pen, L.x9(1.5), M.cap_height * 0.84, L.x9(2.7), M.cap_height, M.stroke * 0.8)


def _digit_seven(pen: TTGlyphPen) -> None:
    rect(pen, L.x9(1), M.cap_height - M.stroke, L.x9(8), M.cap_height)
    thick_segment(pen, L.x9(7.55), M.cap_height - M.stroke / 2, L.x9(3.0), 0, M.stroke * 1.02)


def _digit_eight(pen: TTGlyphPen) -> None:
    mid = M.cap_height / 2
    soft_ring(pen, L.x9(1.45), mid - M.stroke * 0.1, L.x9(7.55), M.cap_height + M.overshoot, stroke=M.stroke * 0.9, radius=M.round_radius)
    soft_ring(pen, L.x9(1.25), -M.overshoot, L.x9(7.75), mid + M.stroke * 0.1, stroke=M.stroke * 0.9, radius=M.round_radius)


def _digit_nine(pen: TTGlyphPen) -> None:
    soft_ring(
        pen, L.x9(1), M.cap_height * 0.42, L.x9(8), M.cap_height + M.overshoot,
        stroke=M.stroke, radius=L.ninth,
    )
    rect(pen, L.x9(7), M.cap_height * 0.14, L.x9(8), M.cap_height * 0.7)
    thick_segment(pen, L.x9(7.5), M.cap_height * 0.16, L.x9(6.3), 0, M.stroke * 0.8)


# --- Accents --------------------------------------------------------------


def _diaeresis(pen: TTGlyphPen, y: float) -> None:
    dot(pen, L.x9(3.45), y, M.stroke * 0.82)
    dot(pen, L.x9(5.55), y, M.stroke * 0.82)


def _breve(pen: TTGlyphPen, y: float) -> None:
    w = M.stroke * 0.62
    thick_segment(pen, L.x9(3.0), y + L.ninth * 0.45, L.x9(4.0), y, w)
    thick_segment(pen, L.x9(4.0), y, L.x9(5.0), y, w)
    thick_segment(pen, L.x9(5.0), y, L.x9(6.0), y + L.ninth * 0.45, w)


def _cedilla(pen: TTGlyphPen) -> None:
    w = M.stroke * 0.65
    thick_segment(pen, M.center, M.stroke * 0.18, L.x9(4.2), -L.ninth * 1.05, w)
    thick_segment(pen, L.x9(4.2), -L.ninth * 1.05, L.x9(5.2), -L.ninth * 1.65, w)


def _with(base: Draw, accent: Callable[[TTGlyphPen], None]) -> Draw:
    def draw(pen: TTGlyphPen) -> None:
        base(pen)
        accent(pen)
    return draw


def _upper_diaeresis(base: Draw) -> Draw:
    return _with(base, lambda pen: _diaeresis(pen, M.cap_height + M.accent_gap))


def _lower_diaeresis(base: Draw) -> Draw:
    return _with(base, lambda pen: _diaeresis(pen, M.x_height + M.accent_gap))


def _upper_breve(base: Draw) -> Draw:
    return _with(base, lambda pen: _breve(pen, M.cap_height + M.accent_gap * 0.65))


def _lower_breve(base: Draw) -> Draw:
    return _with(base, lambda pen: _breve(pen, M.x_height + M.accent_gap * 0.65))


# --- Punctuation / documentary symbols ----------------------------------


def _period(pen: TTGlyphPen) -> None:
    dot(pen, M.center, M.stroke / 2, M.stroke)


def _comma(pen: TTGlyphPen) -> None:
    _period(pen)
    thick_segment(pen, M.center + M.stroke * 0.15, 0, M.center - M.stroke * 0.35, -L.ninth, M.stroke * 0.52)


def _colon(pen: TTGlyphPen) -> None:
    dot(pen, M.center, M.x_height * 0.24, M.stroke * 0.86)
    dot(pen, M.center, M.x_height * 0.72, M.stroke * 0.86)


def _semicolon(pen: TTGlyphPen) -> None:
    _colon(pen)
    thick_segment(pen, M.center + M.stroke * 0.12, M.x_height * 0.21, M.center - M.stroke * 0.35, M.x_height * 0.08, M.stroke * 0.5)


def _hyphen(pen: TTGlyphPen) -> None:
    rect(pen, L.x9(2.25), M.x_height * 0.48, L.x9(6.75), M.x_height * 0.48 + M.stroke * 0.8)


def _underscore(pen: TTGlyphPen) -> None:
    rect(pen, L.x9(0.75), -M.stroke, L.x9(8.25), -M.stroke * 0.25)


def _slash(pen: TTGlyphPen) -> None:
    thick_segment(pen, L.x9(2), -L.ninth, L.x9(7), M.cap_height + L.ninth, M.stroke * 0.7)


def _backslash(pen: TTGlyphPen) -> None:
    thick_segment(pen, L.x9(2), M.cap_height + L.ninth, L.x9(7), -L.ninth, M.stroke * 0.7)


def _plus(pen: TTGlyphPen) -> None:
    rect(pen, L.x9(2), M.x_height * 0.55, L.x9(7), M.x_height * 0.55 + M.stroke * 0.82)
    rect(pen, M.center - M.stroke * 0.41, M.x_height * 0.3, M.center + M.stroke * 0.41, M.x_height * 0.82)


def _equal(pen: TTGlyphPen) -> None:
    y = M.x_height * 0.42
    rect(pen, L.x9(2), y, L.x9(7), y + M.stroke * 0.72)
    rect(pen, L.x9(2), y + L.ninth * 1.8, L.x9(7), y + L.ninth * 1.8 + M.stroke * 0.72)


def _paren_left(pen: TTGlyphPen) -> None:
    thick_segment(pen, L.x9(5.6), M.cap_height, L.x9(3.7), M.cap_height * 0.72, M.stroke * 0.7)
    rect(pen, L.x9(3.2), M.cap_height * 0.28, L.x9(4.2), M.cap_height * 0.72)
    thick_segment(pen, L.x9(3.7), M.cap_height * 0.28, L.x9(5.6), 0, M.stroke * 0.7)


def _paren_right(pen: TTGlyphPen) -> None:
    thick_segment(pen, L.x9(3.4), M.cap_height, L.x9(5.3), M.cap_height * 0.72, M.stroke * 0.7)
    rect(pen, L.x9(4.8), M.cap_height * 0.28, L.x9(5.8), M.cap_height * 0.72)
    thick_segment(pen, L.x9(5.3), M.cap_height * 0.28, L.x9(3.4), 0, M.stroke * 0.7)


def _bracket_left(pen: TTGlyphPen) -> None:
    rect(pen, L.x9(3), 0, L.x9(4), M.cap_height)
    rect(pen, L.x9(3), M.cap_height - M.stroke, L.x9(6), M.cap_height)
    rect(pen, L.x9(3), 0, L.x9(6), M.stroke)


def _bracket_right(pen: TTGlyphPen) -> None:
    rect(pen, L.x9(5), 0, L.x9(6), M.cap_height)
    rect(pen, L.x9(3), M.cap_height - M.stroke, L.x9(6), M.cap_height)
    rect(pen, L.x9(3), 0, L.x9(6), M.stroke)


def _brace_left(pen: TTGlyphPen) -> None:
    w = M.stroke * 0.7
    thick_segment(pen, L.x9(5.8), M.cap_height, L.x9(4.3), M.cap_height * 0.82, w)
    rect(pen, L.x9(3.8), M.cap_height * 0.56, L.x9(4.8), M.cap_height * 0.82)
    thick_segment(pen, L.x9(4.3), M.cap_height * 0.56, L.x9(3.2), M.cap_height * 0.5, w)
    thick_segment(pen, L.x9(3.2), M.cap_height * 0.5, L.x9(4.3), M.cap_height * 0.44, w)
    rect(pen, L.x9(3.8), M.cap_height * 0.18, L.x9(4.8), M.cap_height * 0.44)
    thick_segment(pen, L.x9(4.3), M.cap_height * 0.18, L.x9(5.8), 0, w)


def _brace_right(pen: TTGlyphPen) -> None:
    w = M.stroke * 0.7
    thick_segment(pen, L.x9(3.2), M.cap_height, L.x9(4.7), M.cap_height * 0.82, w)
    rect(pen, L.x9(4.2), M.cap_height * 0.56, L.x9(5.2), M.cap_height * 0.82)
    thick_segment(pen, L.x9(4.7), M.cap_height * 0.56, L.x9(5.8), M.cap_height * 0.5, w)
    thick_segment(pen, L.x9(5.8), M.cap_height * 0.5, L.x9(4.7), M.cap_height * 0.44, w)
    rect(pen, L.x9(4.2), M.cap_height * 0.18, L.x9(5.2), M.cap_height * 0.44)
    thick_segment(pen, L.x9(4.7), M.cap_height * 0.18, L.x9(3.2), 0, w)


def _less(pen: TTGlyphPen) -> None:
    thick_segment(pen, L.x9(6.4), M.x_height * 0.82, L.x9(2.6), M.x_height * 0.5, M.stroke * 0.72)
    thick_segment(pen, L.x9(2.6), M.x_height * 0.5, L.x9(6.4), M.x_height * 0.18, M.stroke * 0.72)


def _greater(pen: TTGlyphPen) -> None:
    thick_segment(pen, L.x9(2.6), M.x_height * 0.82, L.x9(6.4), M.x_height * 0.5, M.stroke * 0.72)
    thick_segment(pen, L.x9(6.4), M.x_height * 0.5, L.x9(2.6), M.x_height * 0.18, M.stroke * 0.72)


def _lira(pen: TTGlyphPen) -> None:
    thick_segment(pen, L.x9(3.7), M.stroke * 0.5, L.x9(4.4), M.cap_height, M.stroke)
    axis_segment(pen, M.center, M.cap_height * 0.68, L.third * 1.2, 18, M.stroke * 0.62)
    axis_segment(pen, M.center, M.cap_height * 0.51, L.third * 1.2, 18, M.stroke * 0.62)
    thick_segment(pen, L.x9(4.0), M.stroke, L.x9(6.9), M.cap_height * 0.25, M.stroke * 0.82)


def _sup_two(pen: TTGlyphPen) -> None:
    y0 = M.cap_height * 0.63
    rect(pen, L.x9(3.1), M.cap_height - M.stroke * 0.65, L.x9(6.1), M.cap_height)
    thick_segment(pen, L.x9(5.8), M.cap_height - M.stroke * 0.3, L.x9(3.1), y0, M.stroke * 0.62)
    rect(pen, L.x9(3.0), y0, L.x9(6.2), y0 + M.stroke * 0.62)


def glyph_name(ch: str) -> str:
    digit_names = {
        "0": "zero", "1": "one", "2": "two", "3": "three", "4": "four",
        "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine",
    }
    punctuation = {
        " ": "space", ".": "period", ",": "comma", ":": "colon", ";": "semicolon",
        "-": "hyphen", "_": "underscore", "/": "slash", "\\": "backslash",
        "+": "plus", "=": "equal", "(": "parenleft", ")": "parenright",
        "[": "bracketleft", "]": "bracketright", "{": "braceleft", "}": "braceright",
        "<": "less", ">": "greater", "₺": "uni20BA", "²": "twosuperior",
    }
    if ch in digit_names:
        return digit_names[ch]
    if ch in punctuation:
        return punctuation[ch]
    if ch.isascii() and ch.isalpha():
        return ch
    return f"uni{ord(ch):04X}"


DRAWERS: dict[str, Draw | None] = {
    " ": None,
    "H": _H, "I": _I, "O": _O, "C": _C, "G": _G, "S": _S,
    "T": _T, "U": _U, "V": _V, "W": _W, "Z": _Z,
    "a": _a, "c": _c, "e": _e, "g": _g, "i": _i, "ı": _dotless_i,
    "l": _l, "o": _o, "s": _s, "u": _u,
    "0": _zero, "1": _one, "2": _digit_two, "3": _digit_three, "4": _digit_four,
    "5": _digit_five, "6": _digit_six, "7": _digit_seven, "8": _digit_eight,
    "9": _digit_nine,
    ".": _period, ",": _comma, ":": _colon, ";": _semicolon,
    "-": _hyphen, "_": _underscore, "/": _slash, "\\": _backslash,
    "+": _plus, "=": _equal, "(": _paren_left, ")": _paren_right,
    "[": _bracket_left, "]": _bracket_right, "{": _brace_left, "}": _brace_right,
    "<": _less, ">": _greater, "₺": _lira, "²": _sup_two,

    "Ç": _with(_C, _cedilla),
    "Ğ": _upper_breve(_G),
    "İ": _with(_I, lambda pen: dot(pen, M.center, M.cap_height + M.accent_gap, M.stroke * 0.82)),
    "Ö": _upper_diaeresis(_O),
    "Ş": _with(_S, _cedilla),
    "Ü": _upper_diaeresis(_U),
    "ç": _with(_c, _cedilla),
    "ğ": _lower_breve(_g),
    "ö": _lower_diaeresis(_o),
    "ş": _with(_s, _cedilla),
    "ü": _lower_diaeresis(_u),
}


def build_glyphs() -> tuple[list[str], dict[str, object], dict[int, str]]:
    order = [".notdef"]
    glyphs: dict[str, object] = {".notdef": _glyph(_notdef)}
    cmap: dict[int, str] = {}

    for ch, draw in DRAWERS.items():
        name = glyph_name(ch)
        if name in glyphs:
            raise ValueError(f"duplicate glyph name: {name}")
        order.append(name)
        glyphs[name] = _glyph(draw)
        cmap[ord(ch)] = name

    return order, glyphs, cmap
