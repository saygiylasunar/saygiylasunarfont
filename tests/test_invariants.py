from __future__ import annotations

import math
from pathlib import Path
from tempfile import TemporaryDirectory

from fontTools.ttLib import TTFont

from saygiylasunarfont.build import build
from saygiylasunarfont.config import L, M
from saygiylasunarfont.geometry import IsoBasis
from saygiylasunarfont.glyphs import DRAWERS, build_glyphs


def test_glyph_names_are_unique() -> None:
    order, glyphs, cmap = build_glyphs()
    assert len(order) == len(set(order))
    assert set(order) == set(glyphs)
    assert len(cmap) == len(DRAWERS)


def test_trihex_cell_is_exact() -> None:
    assert M.advance == 648
    assert M.advance % 3 == 0
    assert M.advance % 6 == 0
    assert M.advance % 9 == 0
    assert (L.third, L.sixth, L.ninth) == (216, 108, 72)


def test_isometric_basis_is_symmetric() -> None:
    ux, uy = IsoBasis().project(1, 0, 0)
    vx, vy = IsoBasis().project(0, 1, 0)
    assert math.isclose(ux, -vx, abs_tol=1e-9)
    assert math.isclose(uy, vy, abs_tol=1e-9)


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
