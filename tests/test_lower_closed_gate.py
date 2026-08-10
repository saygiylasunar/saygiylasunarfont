from __future__ import annotations

import math

from saygiylasunarfont.config import M
from saygiylasunarfont.lowermasters import LOWER_CLOSED_MASTER
from saygiylasunarfont.moldcaster import DECIMAL_10, DYADIC_32
from saygiylasunarfont.registry import MIGRATED_GLYPHS


def test_o_a_g_share_exactly_one_body_master() -> None:
    o = LOWER_CLOSED_MASTER.resolve("o")
    a = LOWER_CLOSED_MASTER.resolve("a")
    g = LOWER_CLOSED_MASTER.resolve("g")

    for other in (a, g):
        assert math.isclose(other.x0, o.x0, abs_tol=1e-9)
        assert math.isclose(other.x1, o.x1, abs_tol=1e-9)
        assert math.isclose(other.y0, o.y0, abs_tol=1e-9)
        assert math.isclose(other.y1, o.y1, abs_tol=1e-9)
        assert other.profile == o.profile
        assert other.stroke == o.stroke


def test_a_is_single_storey_body_plus_stem_and_restrained_foot() -> None:
    a = LOWER_CLOSED_MASTER.resolve("a")
    assert a.stem_x0 is not None
    assert a.foot_right is not None
    assert math.isclose(a.x1 - a.stem_x0, a.stroke, abs_tol=1e-9)
    assert a.x1 < a.foot_right < a.cell


def test_g_extends_same_stem_into_one_continuous_quadratic_hook() -> None:
    g = LOWER_CLOSED_MASTER.resolve("g")
    assert g.stem_x0 is not None
    assert g.descender_bottom is not None
    assert g.hook_start_y is not None
    assert g.terminal_left is not None
    assert g.descender_bottom < 0.0
    assert M.descender < g.descender_bottom
    assert g.terminal_left < g.stem_x0 < g.x1
    assert g.descender_bottom < g.hook_start_y < 0.0
    assert math.isclose(
        g.hook_start_y - g.descender_bottom,
        g.stroke * LOWER_CLOSED_MASTER.g_hook_start_strokes,
        abs_tol=1e-9,
    )


def test_decimal_cast_preserves_lowercase_body_ratio() -> None:
    native = LOWER_CLOSED_MASTER.resolve("o")
    decimal = LOWER_CLOSED_MASTER.resolve(
        "o",
        target_cell=100,
        target_body_height=100 * M.x_height / M.advance,
        mold=DECIMAL_10,
    )
    assert math.isclose(decimal.x0 + decimal.x1, 100.0, abs_tol=1e-9)
    assert decimal.x0 < 50.0 < decimal.x1
    assert native.x0 < native.cell / 2.0 < native.x1


def test_dyadic_lowercase_stroke_quantizes_to_four_pixels() -> None:
    digital = LOWER_CLOSED_MASTER.resolve(
        "o",
        target_cell=32,
        target_body_height=32 * M.x_height / M.advance,
        mold=DYADIC_32,
        quantize_stroke=True,
    )
    assert digital.stroke == 4.0


def test_gate6_promotes_turkish_derivatives_with_new_bodies() -> None:
    assert {"a", "o", "g", "ö", "ğ"}.issubset(MIGRATED_GLYPHS)
