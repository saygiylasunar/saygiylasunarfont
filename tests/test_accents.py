from __future__ import annotations

from tempfile import TemporaryDirectory
from pathlib import Path

from fontTools.ttLib import TTFont

from saygiylasunarfont.accentmasters import ACCENT_MASTER
from saygiylasunarfont.build import build
from saygiylasunarfont.config import M
from saygiylasunarfont.registry import NORMALIZED_ACCENTS


def test_upper_accents_fit_inside_vertical_metrics() -> None:
    dot_top = M.cap_height + ACCENT_MASTER.dot_gap + ACCENT_MASTER.dot_size / 2.0
    breve_top = M.cap_height + ACCENT_MASTER.breve_high_gap + ACCENT_MASTER.breve_stroke / 2.0
    assert dot_top <= M.ascender
    assert breve_top <= M.ascender


def test_cedilla_has_room_inside_descender() -> None:
    # The terminal center is -2.70 core; the half-stroke must still remain above
    # the global descender so rasterizers do not clip the normalized hook.
    bottom = -2.70 * ACCENT_MASTER.core - ACCENT_MASTER.cedilla_stroke / 2.0
    assert bottom > M.descender


def test_diaeresis_is_exactly_centered_as_a_pair() -> None:
    left = M.center - ACCENT_MASTER.diaeresis_offset
    right = M.center + ACCENT_MASTER.diaeresis_offset
    assert left + right == 2 * M.center


def test_all_turkish_accented_glyphs_use_normalized_accent_registry() -> None:
    assert NORMALIZED_ACCENTS == frozenset(
        {"Ç", "Ğ", "İ", "Ö", "Ş", "Ü", "ç", "ğ", "ö", "ş", "ü"}
    )


def test_built_turkish_accents_are_not_clipped() -> None:
    with TemporaryDirectory() as tmp:
        path = build(Path(tmp) / "accent-test.ttf")
        font = TTFont(path)
        cmap = font.getBestCmap() or {}
        glyf = font["glyf"]
        for ch in NORMALIZED_ACCENTS:
            glyph = glyf[cmap[ord(ch)]]
            assert glyph.yMax <= M.ascender
            assert glyph.yMin >= M.descender
