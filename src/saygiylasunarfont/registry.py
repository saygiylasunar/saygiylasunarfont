from __future__ import annotations

from .accentmasters import (
    lower_breve,
    lower_diaeresis,
    upper_breve,
    upper_diaeresis,
    upper_dot,
    with_cedilla,
)
from .diagonalmasters import draw_V, draw_W, draw_Z
from .flowmasters import draw_S, draw_s
from .glyphs import DRAWERS as LEGACY_DRAWERS, _glyph, _notdef, glyph_name
from .lowermasters import draw_a, draw_g, draw_o
from .masters import draw_O, draw_zero
from .numericmasters import draw_2, draw_3, draw_5, draw_6, draw_9
from .openmasters import draw_C, draw_G, draw_c, draw_e


# Staged migration registry. Legacy glyph definitions remain intact until their
# family gate is promoted. Accent composition is already normalized separately,
# including characters whose base body still comes from the legacy diagnostic set.
DRAWERS = dict(LEGACY_DRAWERS)
DRAWERS.update(
    {
        # Gate 1 — closed round / ambiguity
        "O": draw_O,
        "0": draw_zero,
        "Ö": upper_diaeresis(draw_O),
        # Gate 2 — open round / aperture
        "C": draw_C,
        "G": draw_G,
        "c": draw_c,
        "e": draw_e,
        "Ç": with_cedilla(draw_C),
        "Ğ": upper_breve(draw_G),
        "ç": with_cedilla(draw_c),
        # Gate 3 — continuous harmonic flow
        "S": draw_S,
        "s": draw_s,
        "Ş": with_cedilla(draw_S),
        "ş": with_cedilla(draw_s),
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
        "ö": lower_diaeresis(draw_o),
        "ğ": lower_breve(draw_g),
        # Accent normalization on not-yet-migrated base bodies
        "İ": upper_dot(LEGACY_DRAWERS["I"]),
        "Ü": upper_diaeresis(LEGACY_DRAWERS["U"]),
        "ü": lower_diaeresis(LEGACY_DRAWERS["u"]),
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

NORMALIZED_ACCENTS = frozenset({"Ç", "Ğ", "İ", "Ö", "Ş", "Ü", "ç", "ğ", "ö", "ş", "ü"})


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
