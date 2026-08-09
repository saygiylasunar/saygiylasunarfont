from __future__ import annotations

from collections.abc import Callable

from fontTools.pens.ttGlyphPen import TTGlyphPen

from .config import M
from .geometry import dot, octagonal_ring, open_octagonal_bowl, polygon, rect, thick_segment

Draw = Callable[[TTGlyphPen], None]


def _glyph(draw: Draw | None = None):
    pen = TTGlyphPen(None)
    if draw:
        draw(pen)
    return pen.glyph()


def _notdef(pen: TTGlyphPen) -> None:
    polygon(pen, [(60, 0), (540, 0), (540, 700), (60, 700)], clockwise=True)
    polygon(pen, [(140, 80), (460, 80), (460, 620), (140, 620)], clockwise=False)


def _H(pen: TTGlyphPen) -> None:
    s = M.stroke
    rect(pen, M.left, 0, M.left + s, M.cap_height)
    rect(pen, M.right - s, 0, M.right, M.cap_height)
    rect(pen, M.left, 310, M.right, 390)


def _I(pen: TTGlyphPen) -> None:
    s = M.stroke
    rect(pen, 150, M.cap_height - s, 450, M.cap_height)
    rect(pen, M.center - s / 2, 0, M.center + s / 2, M.cap_height)
    rect(pen, 150, 0, 450, s)


def _l(pen: TTGlyphPen) -> None:
    s = M.stroke
    rect(pen, M.center - s / 2, 0, M.center + s / 2, M.cap_height)
    rect(pen, M.center - s / 2, 0, 430, s)


def _i(pen: TTGlyphPen) -> None:
    s = M.stroke
    rect(pen, M.center - s / 2, 0, M.center + s / 2, M.x_height - 85)
    dot(pen, M.center, M.x_height - 15, s)


def _dotless_i(pen: TTGlyphPen) -> None:
    s = M.stroke
    rect(pen, M.center - s / 2, 0, M.center + s / 2, M.x_height)


def _one(pen: TTGlyphPen) -> None:
    s = M.stroke
    rect(pen, M.center - s / 2, 0, M.center + s / 2, M.cap_height)
    thick_segment(pen, 205, 540, M.center, M.cap_height, s)
    rect(pen, 165, 0, 435, s)


def _O(pen: TTGlyphPen) -> None:
    octagonal_ring(
        pen,
        M.left,
        -M.overshoot,
        M.right,
        M.cap_height + M.overshoot,
        stroke=M.stroke,
        corner=115,
    )


def _zero(pen: TTGlyphPen) -> None:
    _O(pen)
    thick_segment(pen, 190, 105, 410, 595, 56)


def _o(pen: TTGlyphPen) -> None:
    octagonal_ring(
        pen,
        95,
        -M.overshoot,
        505,
        M.x_height + M.overshoot,
        stroke=M.stroke,
        corner=M.corner,
    )


def _a(pen: TTGlyphPen) -> None:
    _o(pen)
    rect(pen, 425, 0, 505, M.x_height)
    rect(pen, 425, -10, 540, 70)


def _g(pen: TTGlyphPen) -> None:
    _o(pen)
    rect(pen, 425, -145, 505, M.x_height)
    rect(pen, 270, -200, 505, -120)
    thick_segment(pen, 270, -200, 190, -145, 65)


def _open_bowl(pen: TTGlyphPen, *, top: int, bottom: int, crossbar: bool = False) -> None:
    height = top - bottom
    is_upper = height > 600
    x0, x1 = (75, 525) if is_upper else (95, 505)
    corner = 115 if is_upper else M.corner
    open_octagonal_bowl(
        pen,
        x0,
        bottom,
        x1,
        top,
        stroke=M.stroke,
        corner=corner,
        opening="right",
    )
    if crossbar:
        mid = (top + bottom) / 2
        rect(pen, x0 + M.stroke - 20, mid - M.stroke / 2, x1 - 20, mid + M.stroke / 2)


def _C(pen: TTGlyphPen) -> None:
    _open_bowl(pen, top=M.cap_height + M.overshoot, bottom=-M.overshoot)


def _c(pen: TTGlyphPen) -> None:
    _open_bowl(pen, top=M.x_height + M.overshoot, bottom=-M.overshoot)


def _e(pen: TTGlyphPen) -> None:
    _open_bowl(pen, top=M.x_height + M.overshoot, bottom=-M.overshoot, crossbar=True)


def _G(pen: TTGlyphPen) -> None:
    _C(pen)
    rect(pen, 305, 300, 505, 380)
    rect(pen, 425, 170, 505, 380)


def _T(pen: TTGlyphPen) -> None:
    s = M.stroke
    rect(pen, M.left, M.cap_height - s, M.right, M.cap_height)
    rect(pen, M.center - s / 2, 0, M.center + s / 2, M.cap_height)


def _Z(pen: TTGlyphPen) -> None:
    s = M.stroke
    rect(pen, M.left, M.cap_height - s, M.right, M.cap_height)
    thick_segment(pen, M.right - 30, M.cap_height - 40, M.left + 30, 40, 88)
    rect(pen, M.left, 0, M.right, s)


def _rounded_s(pen: TTGlyphPen, top: int) -> None:
    mid = top / 2
    if top > 600:
        x0, x1, stroke, corner, overlap = 95, 505, 72, 92, 28
    else:
        x0, x1, stroke, corner, overlap = 105, 495, 68, 78, 22
    open_octagonal_bowl(
        pen,
        x0,
        mid - overlap,
        x1,
        top + M.overshoot,
        stroke=stroke,
        corner=corner,
        opening="right",
    )
    open_octagonal_bowl(
        pen,
        x0,
        -M.overshoot,
        x1,
        mid + overlap,
        stroke=stroke,
        corner=corner,
        opening="left",
    )


def _S(pen: TTGlyphPen) -> None:
    _rounded_s(pen, M.cap_height)


def _s(pen: TTGlyphPen) -> None:
    _rounded_s(pen, M.x_height)


def _V(pen: TTGlyphPen) -> None:
    thick_segment(pen, 105, M.cap_height, M.center, 0, 90)
    thick_segment(pen, M.center, 0, 495, M.cap_height, 90)


def _W(pen: TTGlyphPen) -> None:
    w = 84
    thick_segment(pen, 70, M.cap_height, 195, 0, w)
    thick_segment(pen, 195, 0, M.center, 280, w)
    thick_segment(pen, M.center, 280, 405, 0, w)
    thick_segment(pen, 405, 0, 530, M.cap_height, w)


def _U(pen: TTGlyphPen) -> None:
    s = M.stroke
    rect(pen, M.left, 105, M.left + s, M.cap_height)
    rect(pen, M.right - s, 105, M.right, M.cap_height)
    rect(pen, 150, 0, 450, s)
    thick_segment(pen, M.left + 40, 115, 165, 40, s)
    thick_segment(pen, 435, 40, M.right - 40, 115, s)


def _u(pen: TTGlyphPen) -> None:
    rect(pen, 95, 90, 175, M.x_height)
    rect(pen, 425, 0, 505, M.x_height)
    rect(pen, 175, 0, 425, 80)
    thick_segment(pen, 135, 105, 190, 45, 65)


# --- Numerals -------------------------------------------------------------


def _digit_two(pen: TTGlyphPen) -> None:
    rect(pen, 120, 620, 470, 700)
    rect(pen, 425, 350, 505, 625)
    rect(pen, 130, 310, 470, 390)
    rect(pen, 95, 75, 175, 340)
    rect(pen, 130, 0, 480, 80)


def _digit_three(pen: TTGlyphPen) -> None:
    rect(pen, 120, 620, 465, 700)
    rect(pen, 135, 310, 465, 390)
    rect(pen, 120, 0, 465, 80)
    rect(pen, 425, 350, 505, 625)
    rect(pen, 425, 75, 505, 350)


def _digit_four(pen: TTGlyphPen) -> None:
    rect(pen, 95, 335, 175, 700)
    rect(pen, 130, 300, 505, 380)
    rect(pen, 425, 0, 505, 700)


def _digit_five(pen: TTGlyphPen) -> None:
    rect(pen, 120, 620, 480, 700)
    rect(pen, 95, 350, 175, 625)
    rect(pen, 130, 310, 470, 390)
    rect(pen, 425, 75, 505, 340)
    rect(pen, 120, 0, 465, 80)


def _digit_six(pen: TTGlyphPen) -> None:
    rect(pen, 120, 620, 465, 700)
    rect(pen, 95, 75, 175, 625)
    rect(pen, 130, 310, 470, 390)
    rect(pen, 425, 75, 505, 340)
    rect(pen, 130, 0, 470, 80)


def _digit_seven(pen: TTGlyphPen) -> None:
    rect(pen, 105, 620, 495, 700)
    thick_segment(pen, 455, 635, 225, 0, 86)


def _digit_eight(pen: TTGlyphPen) -> None:
    octagonal_ring(pen, 120, 340, 480, 710, stroke=72, corner=78)
    octagonal_ring(pen, 120, -10, 480, 360, stroke=72, corner=78)


def _digit_nine(pen: TTGlyphPen) -> None:
    octagonal_ring(pen, 105, 310, 505, 710, stroke=M.stroke, corner=88)
    rect(pen, 425, 60, 505, 350)
    rect(pen, 130, 0, 465, 80)


# --- Accents --------------------------------------------------------------


def _diaeresis(pen: TTGlyphPen, y: int) -> None:
    dot(pen, 235, y, 66)
    dot(pen, 365, y, 66)


def _breve(pen: TTGlyphPen, y: int) -> None:
    s = 54
    thick_segment(pen, 205, y + 35, 265, y, s)
    thick_segment(pen, 265, y, 335, y, s)
    thick_segment(pen, 335, y, 395, y + 35, s)


def _cedilla(pen: TTGlyphPen) -> None:
    thick_segment(pen, 310, 15, 275, -80, 54)
    thick_segment(pen, 275, -80, 345, -125, 54)


def _with(base: Draw, accent: Callable[[TTGlyphPen], None]) -> Draw:
    def draw(pen: TTGlyphPen) -> None:
        base(pen)
        accent(pen)
    return draw


def _upper_diaeresis(base: Draw) -> Draw:
    return _with(base, lambda pen: _diaeresis(pen, M.cap_height + 105))


def _lower_diaeresis(base: Draw) -> Draw:
    return _with(base, lambda pen: _diaeresis(pen, M.x_height + 105))


def _upper_breve(base: Draw) -> Draw:
    return _with(base, lambda pen: _breve(pen, M.cap_height + 80))


def _lower_breve(base: Draw) -> Draw:
    return _with(base, lambda pen: _breve(pen, M.x_height + 80))


# --- Punctuation / symbols ----------------------------------------------


def _period(pen: TTGlyphPen) -> None:
    dot(pen, M.center, 40, 80)


def _comma(pen: TTGlyphPen) -> None:
    _period(pen)
    thick_segment(pen, M.center + 15, 15, M.center - 30, -90, 42)


def _colon(pen: TTGlyphPen) -> None:
    dot(pen, M.center, 120, 72)
    dot(pen, M.center, 380, 72)


def _semicolon(pen: TTGlyphPen) -> None:
    dot(pen, M.center, 380, 72)
    dot(pen, M.center, 120, 72)
    thick_segment(pen, M.center + 15, 95, M.center - 30, -10, 42)


def _hyphen(pen: TTGlyphPen) -> None:
    rect(pen, 170, 225, 430, 295)


def _underscore(pen: TTGlyphPen) -> None:
    rect(pen, 70, -90, 530, -30)


def _slash(pen: TTGlyphPen) -> None:
    thick_segment(pen, 155, -70, 445, 770, 58)


def _backslash(pen: TTGlyphPen) -> None:
    thick_segment(pen, 155, 770, 445, -70, 58)


def _plus(pen: TTGlyphPen) -> None:
    rect(pen, 130, 275, 470, 345)
    rect(pen, 265, 140, 335, 480)


def _equal(pen: TTGlyphPen) -> None:
    rect(pen, 140, 205, 460, 270)
    rect(pen, 140, 350, 460, 415)


def _paren_left(pen: TTGlyphPen) -> None:
    thick_segment(pen, 360, 690, 235, 520, 62)
    rect(pen, 205, 180, 275, 520)
    thick_segment(pen, 235, 180, 360, 10, 62)


def _paren_right(pen: TTGlyphPen) -> None:
    thick_segment(pen, 240, 690, 365, 520, 62)
    rect(pen, 325, 180, 395, 520)
    thick_segment(pen, 365, 180, 240, 10, 62)


def _bracket_left(pen: TTGlyphPen) -> None:
    rect(pen, 200, 0, 280, 700)
    rect(pen, 200, 620, 410, 700)
    rect(pen, 200, 0, 410, 80)


def _bracket_right(pen: TTGlyphPen) -> None:
    rect(pen, 320, 0, 400, 700)
    rect(pen, 190, 620, 400, 700)
    rect(pen, 190, 0, 400, 80)


def _brace_left(pen: TTGlyphPen) -> None:
    thick_segment(pen, 380, 700, 285, 610, 60)
    rect(pen, 245, 390, 315, 610)
    thick_segment(pen, 280, 390, 205, 350, 60)
    thick_segment(pen, 205, 350, 280, 310, 60)
    rect(pen, 245, 90, 315, 310)
    thick_segment(pen, 285, 90, 380, 0, 60)


def _brace_right(pen: TTGlyphPen) -> None:
    thick_segment(pen, 220, 700, 315, 610, 60)
    rect(pen, 285, 390, 355, 610)
    thick_segment(pen, 320, 390, 395, 350, 60)
    thick_segment(pen, 395, 350, 320, 310, 60)
    rect(pen, 285, 90, 355, 310)
    thick_segment(pen, 315, 90, 220, 0, 60)


def _less(pen: TTGlyphPen) -> None:
    thick_segment(pen, 420, 500, 180, 310, 65)
    thick_segment(pen, 180, 310, 420, 120, 65)


def _greater(pen: TTGlyphPen) -> None:
    thick_segment(pen, 180, 500, 420, 310, 65)
    thick_segment(pen, 420, 310, 180, 120, 65)


def _lira(pen: TTGlyphPen) -> None:
    thick_segment(pen, 235, 40, 285, 700, 72)
    thick_segment(pen, 165, 500, 420, 585, 50)
    thick_segment(pen, 160, 375, 410, 460, 50)
    rect(pen, 235, 35, 345, 105)
    thick_segment(pen, 335, 70, 470, 195, 68)


def _sup_two(pen: TTGlyphPen) -> None:
    rect(pen, 245, 625, 410, 680)
    rect(pen, 190, 470, 410, 525)
    thick_segment(pen, 390, 620, 215, 510, 52)


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
    "İ": _with(_I, lambda pen: dot(pen, M.center, M.cap_height + 95, 64)),
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
