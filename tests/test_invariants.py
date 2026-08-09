from __future__ import annotations

import math
from pathlib import Path
from tempfile import TemporaryDirectory

from fontTools.ttLib import TTFont

from saygiylasunarfont.build import build
from saygiylasunarfont.config import L, M
from saygiylasunarfont.curvature import (
    BOWL_DNA,
    CORE_DNA,
    FLOW_DNA,
    OPEN_DNA,
    CurveBox,
    resolve_curve,
    sample_superellipse,
)
from saygiylasunarfont.geometry import IsoBasis
from saygiylasunarfont.glyphs import DRAWERS, build_glyphs


def test_glyph_names_are_unique() -> None:
    order, glyphs, cmap = build_glyphs()
    assert len(order) == len(set(order))
    assert set(order) == set(glyphs)
    assert len(cmap) == len(DRAWERS)


def test_trihex_cell_is_available_as_a_guide() -> None:
    assert M.advance == 648
    assert M.advance % 3 == 0
    assert M.advance % 6 == 0
    assert M.advance % 9 == 0
    assert (L.third, L.sixth, L.ninth) == (216, 108, 72)

    # The lattice can attract geometry without forcing exact coordinates.
    value = 101.0
    snapped = L.soft_snap(value, division=9, strength=0.5)
    assert 72.0 < snapped < value
    assert L.soft_snap(value, division=9, strength=0.0) == value
    assert L.soft_snap(value, division=9, strength=1.0) == 72.0


def test_curve_dna_is_scale_invariant() -> None:
    regular = resolve_curve(CORE_DNA, cell=648, stroke=72)
    doubled = resolve_curve(CORE_DNA, cell=1296, stroke=144)
    assert regular == doubled


def test_weight_compensation_preserves_open_counters() -> None:
    regular = resolve_curve(CORE_DNA, cell=648, stroke=72)
    bold = resolve_curve(CORE_DNA, cell=648, stroke=96)
    assert bold.aperture_ratio > regular.aperture_ratio
    assert bold.exponent < regular.exponent


def test_family_curves_are_derivatives_not_unrelated_presets() -> None:
    assert FLOW_DNA.exponent < CORE_DNA.exponent < BOWL_DNA.exponent
    assert OPEN_DNA.aperture_ratio > CORE_DNA.aperture_ratio
    assert abs(BOWL_DNA.exponent - CORE_DNA.exponent) < 0.5
    assert abs(FLOW_DNA.exponent - CORE_DNA.exponent) < 0.5


def test_superellipse_geometry_scales_affinely() -> None:
    p1 = sample_superellipse(
        CurveBox(0, 0, 100, 200),
        exponent=CORE_DNA.exponent,
        start=0.1,
        end=1.2,
        steps=8,
    )
    p2 = sample_superellipse(
        CurveBox(0, 0, 200, 400),
        exponent=CORE_DNA.exponent,
        start=0.1,
        end=1.2,
        steps=8,
    )
    for (x1, y1), (x2, y2) in zip(p1, p2):
        assert math.isclose(x2, x1 * 2, abs_tol=1e-9)
        assert math.isclose(y2, y1 * 2, abs_tol=1e-9)


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
