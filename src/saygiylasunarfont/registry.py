from __future__ import annotations

from .diagonalmasters import draw_V, draw_W, draw_Z
from .flowmasters import draw_S, draw_s
from .glyphs import (
    DRAWERS as LEGACY_DRAWERS,
    _cedilla,
    _glyph,
    _lower_breve,
    _lower_diaeresis,
    _notdef,
    _upper_breve,
    _upper_diaeresis,
    _with,
    glyph_name,
)
from .lowermasters import draw_a, draw_g, draw_o
from .masters import draw_O, draw_zero
from .numericmasters import draw_2, draw_3, draw_5, draw_6, draw_9
from .openmasters import draw_C, draw_G, draw_c, draw_e


# Staged migration registry. Legacy glyph definitions remain intact until their
# family gate is promoted. This keeps each geometric migration isolated and easy
# to audit or revert.
DRAWERS = dict(LEGACY_DRAWERS)
DRAWERS.update(
    {
        # Gate 1 — closed round / ambiguity
        "O": draw_O,
        "0": draw_zero,
        "Ö": _upper_diaeresis(draw_O),
        # Gate 2 — open round / aperture
        "C": draw_C,
        "G": draw_G,
        "c": draw_c,
        "e": draw_e,
        "Ç": _with(draw_C, _cedilla),
        "Ğ": _upper_breve(draw_G),
        "ç": _with(draw_c, _cedilla),
        # Gate 3 — continuous harmonic flow
        "S": draw_S,
        "s": draw_s,
        "Ş": _with(draw_S, _cedilla),
        "ş": _with(draw_s, _cedilla),
        # Gate 4 — decimal / digital numeric derivatives
        "2": draw_2,
        "3": draw_3,
        "5": draw_5,
        "6": draw_6,
        "9": draw_9,
        # Gate 5 — diagonal / projective family
        "V": draw_V,
        "W": draw_W,
        "Z": draw_Z,
        # Gate 6 — lowercase closed family
        "a": draw_a,
        "o": draw_o,
        "g": draw_g,
        "ö": _lower_diaeresis(draw_o),
        "ğ": _lower_breve(draw_g),
    }
)

MIGRATED_GLYPHS = frozenset(
    {
        "O", "0", "Ö",
        "C", "G", "c", "e", "Ç", "Ğ", "ç",
        "S", "s", "Ş", "ş",
        "2", "3", "5", "6", "9",
        "V", "W", "Z",
        "a", "o", "g", "ö", "ğ",
    }
)


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
