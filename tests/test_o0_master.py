from __future__ import annotations

import math

from saygiylasunarfont.config import M
from saygiylasunarfont.masters import O0_MASTER
from saygiylasunarfont.moldcaster import DECIMAL_10, DYADIC_32
from saygiylasunarfont.registry import MIGRATED_GLYPHS


def _proportional_cap(cell: float) -> float:
    return cell * M.cap_height / M.advance


def test_gate_one_is_explicitly_migrated() -> None:
    assert {"O", "0", "Ö"}.issubset(MIGRATED_GLYPHS)


def test_zero_is_a_controlled_derivative_of_O() -> None:
    letter = O0_MASTER.resolve("O")
    zero = O0_MASTER.resolve("0")

    assert math.isclose(letter.center, M.advance / 2)
    assert math.isclose(zero.center, M.advance / 2)
    assert zero.width < letter.width
    assert zero.profile.exponent > letter.profile.exponent
    assert zero.profile.axis_bias > letter.profile.axis_bias
    assert zero.stroke == letter.stroke == M.stroke


def test_native_zero_slash_is_attracted_toward_trihex_axis() -> None:
    zero = O0_MASTER.resolve("0")
    assert zero.slash_angle is not None
    assert abs(zero.slash_angle - 60.0) < abs(O0_MASTER.slash_seed_angle - 60.0)


def test_decimal_cast_preserves_normalized_center_and_round_family() -> None:
    cell = 100.0
    letter = O0_MASTER.resolve(
        "O",
        target_cell=cell,
        target_cap_height=_proportional_cap(cell),
        mold=DECIMAL_10,
    )
    zero = O0_MASTER.resolve(
        "0",
        target_cell=cell,
        target_cap_height=_proportional_cap(cell),
        mold=DECIMAL_10,
    )
    assert math.isclose(letter.center, cell / 2, abs_tol=1e-9)
    assert math.isclose(zero.center, cell / 2, abs_tol=1e-9)
    assert zero.width < letter.width
    assert math.isclose(letter.stroke / cell, M.stroke / M.advance, rel_tol=1e-9)


def test_dyadic_cast_quantizes_stroke_and_reinterprets_slash() -> None:
    cell = 32.0
    zero = O0_MASTER.resolve(
        "0",
        target_cell=cell,
        target_cap_height=_proportional_cap(cell),
        mold=DYADIC_32,
        quantize_stroke=True,
    )
    assert math.isclose(zero.center, cell / 2, abs_tol=1e-9)
    assert zero.stroke == 4.0
    assert zero.slash_width is not None
    assert zero.slash_width == round(zero.slash_width)
    assert zero.slash_angle is not None
    assert abs(zero.slash_angle - 45.0) < abs(O0_MASTER.slash_seed_angle - 45.0)


def test_invalid_master_kind_is_rejected() -> None:
    try:
        O0_MASTER.resolve("Q")
    except ValueError:
        pass
    else:
        raise AssertionError("O0 master accepted an unrelated glyph")
