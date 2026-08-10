from __future__ import annotations

import math

from saygiylasunarfont.config import CORE_UNIT, M
from saygiylasunarfont.diagonalmasters import DIAGONAL_MASTER
from saygiylasunarfont.moldcaster import DECIMAL_10, DYADIC_32, TRIHEX_36
from saygiylasunarfont.registry import MIGRATED_GLYPHS


def test_diagonal_fit_overrules_impossible_mold_angles() -> None:
    native = DIAGONAL_MASTER.resolve(mold=TRIHEX_36)
    decimal = DIAGONAL_MASTER.resolve(mold=DECIMAL_10)
    digital = DIAGONAL_MASTER.resolve(mold=DYADIC_32)

    max_v_run = M.advance / 2.0 - CORE_UNIT
    minimum_v = math.degrees(math.atan2(M.cap_height, max_v_run))
    for ctx in (native, decimal, digital):
        assert ctx.v_angle >= minimum_v - 1e-9
        assert ctx.v_angle < 90.0

    # Z has enough room to respond more visibly to each mold, but dyadic 45° is
    # still too shallow for the mono cell and therefore gets fit-clamped.
    assert decimal.z_angle > native.z_angle > digital.z_angle
    assert digital.z_angle > 45.0


def test_W_skeleton_is_exactly_mirrored() -> None:
    ctx = DIAGONAL_MASTER.resolve()
    p0, p1, p2, p3, p4 = ctx.w_points
    assert math.isclose(p0[0] + p4[0], ctx.cell, abs_tol=1e-9)
    assert math.isclose(p1[0] + p3[0], ctx.cell, abs_tol=1e-9)
    assert math.isclose(p2[0], ctx.cell / 2.0, abs_tol=1e-9)
    assert math.isclose(p2[1], ctx.body_height * 0.4, abs_tol=1e-9)
    assert p0[1] == p4[1] == ctx.body_height
    assert p1[1] == p3[1] == 0.0


def test_dyadic_diagonal_stroke_quantizes_to_four_pixels() -> None:
    ctx = DIAGONAL_MASTER.resolve(
        target_cell=32,
        target_body_height=36,
        mold=DYADIC_32,
        quantize_stroke=True,
    )
    assert ctx.stroke == 4.0


def test_gate5_registry_promotes_diagonal_family() -> None:
    assert {"V", "W", "Z"}.issubset(MIGRATED_GLYPHS)
