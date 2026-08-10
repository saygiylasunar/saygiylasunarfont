from __future__ import annotations

import math

from saygiylasunarfont.constraints import DECIMAL_AXES, DYADIC_AXES, TRIHEX_AXES, nearest_angle
from saygiylasunarfont.flowcurve import periodic_flow_unit
from saygiylasunarfont.moldcaster import DECIMAL_10, DYADIC_32, TRIHEX_36
from saygiylasunarfont.numericmasters import NUMERIC_MASTER
from saygiylasunarfont.registry import MIGRATED_GLYPHS


def test_decimal_angles_are_derived_from_integer_factor_slopes() -> None:
    one_two = math.degrees(math.atan2(1.0, 2.0))
    two_five = math.degrees(math.atan2(2.0, 5.0))
    assert any(math.isclose(a, one_two, abs_tol=1e-9) for a in DECIMAL_AXES.angles)
    assert any(math.isclose(a, two_five, abs_tol=1e-9) for a in DECIMAL_AXES.angles)


def test_two_diagonal_reinterprets_without_changing_source_geometry() -> None:
    seed = math.degrees(math.atan2(8.0, 12.0))
    native = NUMERIC_MASTER.resolve(mold=TRIHEX_36)
    decimal = NUMERIC_MASTER.resolve(mold=DECIMAL_10)
    digital = NUMERIC_MASTER.resolve(mold=DYADIC_32)

    assert nearest_angle(seed, TRIHEX_AXES) == 30.0
    assert math.isclose(nearest_angle(seed, DECIMAL_AXES), math.degrees(math.atan2(1, 2)))
    assert nearest_angle(seed, DYADIC_AXES) == 45.0

    assert 30.0 < native.two_diagonal_angle < seed
    assert decimal.two_diagonal_angle < native.two_diagonal_angle
    assert seed < digital.two_diagonal_angle < 45.0


def test_three_uses_one_continuous_two_lobe_flow() -> None:
    values = [periodic_flow_unit(t, lobes=2, polarity=-1.0, stiffness=2.1) for t in (0, 0.25, 0.5, 0.75, 1)]
    expected = (-1.0, 1.0, -1.0, 1.0, -1.0)
    for value, target in zip(values, expected):
        assert math.isclose(value, target, abs_tol=1e-9)


def test_numeric_profiles_keep_open_and_ring_forms_related_but_distinct() -> None:
    ctx = NUMERIC_MASTER.resolve()
    assert ctx.ring_profile.exponent > ctx.open_profile.exponent
    assert ctx.open_profile.aperture_ratio > ctx.ring_profile.aperture_ratio


def test_dyadic_numeric_stroke_quantizes_to_four_pixels() -> None:
    ctx = NUMERIC_MASTER.resolve(
        target_cell=32,
        target_body_height=36,
        mold=DYADIC_32,
        quantize_stroke=True,
    )
    assert ctx.stroke == 4.0


def test_gate4_registry_promotes_selected_numeric_family() -> None:
    assert {"2", "3", "5", "6", "9"}.issubset(MIGRATED_GLYPHS)
