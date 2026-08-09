from __future__ import annotations

from tempfile import TemporaryDirectory
from pathlib import Path

from fontTools.ttLib import TTFont

from saygiylasunarfont.build import build
from saygiylasunarfont.config import M
from saygiylasunarfont.glyphs import DRAWERS, build_glyphs


def test_glyph_names_are_unique() -> None:
    order, glyphs, cmap = build_glyphs()
    assert len(order) == len(set(order))
    assert set(order) == set(glyphs)
    assert len(cmap) == len(DRAWERS)


def test_turkish_core_is_source_level() -> None:
    for ch in "ÇĞİÖŞÜçğıöşü":
        assert ch in DRAWERS


def test_built_font_is_strictly_monospaced() -> None:
    with TemporaryDirectory() as tmp:
        path = build(Path(tmp) / "test.ttf")
        font = TTFont(path)
        widths = {width for width, _lsb in font["hmtx"].metrics.values()}
        assert widths == {M.advance}
        assert font["post"].isFixedPitch == 1


def test_built_font_has_turkish_cmap() -> None:
    with TemporaryDirectory() as tmp:
        path = build(Path(tmp) / "test.ttf")
        cmap = TTFont(path).getBestCmap()
        assert cmap is not None
        for ch in "ÇĞİÖŞÜçğıöşü":
            assert ord(ch) in cmap
