from __future__ import annotations

import math

from saygiylasunarfont.config import M
from saygiylasunarfont.moldcaster import DECIMAL_10, DYADIC_32
from saygiylasunarfont.openmasters import OPEN_MASTER
from saygiylasunarfont.registry import MIGRATED_GLYPHS


def _height_for(kind: str, cell: float) -> float:
    source = M.x_height if kind.islower() else M.cap_height
    return cell * source / M.advance


def test_gate_two_is_explicitly_migrated() -> None:
    assert {"C", "G", "c", "e", "Ç", "Ğ", "ç"}.issubset(MIGRATED_GLYPHS)


def test_C_and_G_share_open_family_but_G_is_more_restrained() -> None:
    c_cap = OPEN_MASTER.resolve("C")
    g_cap = OPEN_MASTER.resolve("G")
    assert math.isclose(c_cap.center, M.advance / 2, abs_tol=1e-9)
    assert math.isclose(g_cap.center, M.advance / 2, abs_tol=1e-9)
    assert math.isclose(c_cap.x0, g_cap.x0, abs_tol=1e-9)
    assert math.isclose(c_cap.x1, g_cap.x1, abs_tol=1e-9)
    assert g_cap.profile.aperture_ratio < c_cap.profile.aperture_ratio
    assert g_cap.crossbar_y is not None
    assert g_cap.spur_y0 is not None
    assert g_cap.spur_y0 < g_cap.crossbar_y < g_cap.body_height / 2


def test_e_is_a_more_open_lowercase_derivative_of_c() -> None:
    c = OPEN_MASTER.resolve("c")
    e = OPEN_MASTER.resolve("e")
    assert math.isclose(c.center, e.center, abs_tol=1e-9)
    assert math.isclose(c.x0, e.x0, abs_tol=1e-9)
    assert math.isclose(c.x1, e.x1, abs_tol=1e-9)
    assert e.profile.aperture_ratio > c.profile.aperture_ratio
    assert e.crossbar_y is not None
    assert math.isclose(e.crossbar_y, e.body_height / 2, abs_tol=1e-9)
    assert e.crossbar_x1 is not None
    assert e.crossbar_x1 < e.x1


def test_decimal_open_family_preserves_stroke_ratio() -> None:
    cell = 100.0
    c = OPEN_MASTER.resolve(
        "C",
        target_cell=cell,
        target_body_height=_height_for("C", cell),
        mold=DECIMAL_10,
    )
    assert math.isclose(c.center, cell / 2, abs_tol=1e-9)
    assert math.isclose(c.stroke / cell, M.stroke / M.advance, rel_tol=1e-9)


def test_dyadic_lowercase_quantizes_without_family_break() -> None:
    cell = 32.0
    c = OPEN_MASTER.resolve(
        "c",
        target_cell=cell,
        target_body_height=_height_for("c", cell),
        mold=DYADIC_32,
        quantize_stroke=True,
    )
    e = OPEN_MASTER.resolve(
        "e",
        target_cell=cell,
        target_body_height=_height_for("e", cell),
        mold=DYADIC_32,
        quantize_stroke=True,
    )
    assert c.stroke == e.stroke == 4.0
    assert math.isclose(c.center, cell / 2, abs_tol=1e-9)
    assert math.isclose(e.center, cell / 2, abs_tol=1e-9)
    assert e.profile.aperture_ratio > c.profile.aperture_ratio


def test_invalid_open_master_kind_is_rejected() -> None:
    try:
        OPEN_MASTER.resolve("O")
    except ValueError:
        pass
    else:
        raise AssertionError("open master accepted a closed-round glyph")
