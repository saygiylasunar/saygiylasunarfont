from __future__ import annotations

from .glyphs import (
    DRAWERS as LEGACY_DRAWERS,
    _cedilla,
    _glyph,
    _notdef,
    _upper_breve,
    _upper_diaeresis,
    _with,
    glyph_name,
)
from .masters import draw_O, draw_zero
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
    }
)

MIGRATED_GLYPHS = frozenset({"O", "0", "Ö", "C", "G", "c", "e", "Ç", "Ğ", "ç"})


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
