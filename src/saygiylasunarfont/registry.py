from __future__ import annotations

from .glyphs import (
    DRAWERS as LEGACY_DRAWERS,
    _glyph,
    _notdef,
    _upper_diaeresis,
    glyph_name,
)
from .masters import draw_O, draw_zero


# Staged migration registry. Legacy glyph definitions remain intact until their
# family gate is promoted. This keeps each geometric migration isolated and easy
# to audit or revert.
DRAWERS = dict(LEGACY_DRAWERS)
DRAWERS.update(
    {
        "O": draw_O,
        "0": draw_zero,
        "Ö": _upper_diaeresis(draw_O),
    }
)

MIGRATED_GLYPHS = frozenset({"O", "0", "Ö"})


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
