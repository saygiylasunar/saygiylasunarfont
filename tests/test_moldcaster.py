from __future__ import annotations

import math

from saygiylasunarfont.config import CORE_UNIT, L, M
from saygiylasunarfont.constraints import (
    DOCUMENT_AXES,
    DYADIC_AXES,
    ROLE_PROFILES,
    TRIHEX_AXES,
    PointRole,
    attract_angle,
    nearest_angle,
)
from saygiylasunarfont.moldcaster import DECIMAL_10, DYADIC_32, TRIHEX_36, Moldcaster


def test_36_is_the_native_core_not_an_incidental_number() -> None:
    assert CORE_UNIT == 36
    assert M.core == 36
    assert M.advance == 18 * CORE_UNIT == 648
    assert M.stroke == 2 * CORE_UNIT == 72
    assert M.cap_height == 20 * CORE_UNIT == 720
    assert M.x_height == 15 * CORE_UNIT == 540
    assert L.core == CORE_UNIT


def test_molds_express_distinct_factor_systems() -> None:
    assert TRIHEX_36.divisions == (2, 3, 6, 9, 18)
    assert DECIMAL_10.divisions == (2, 5, 10)
    assert DYADIC_32.divisions == (2, 4, 8, 16, 32)


def test_affine_cast_preserves_normalized_geometry() -> None:
    caster = Moldcaster(M.advance)
    # One 36-unit core is exactly 1/18 of the source cell.
    assert math.isclose(caster.cast(CORE_UNIT, target_span=180), 10.0)
    assert math.isclose(caster.cast(M.advance / 3, target_span=100), 100 / 3)
    assert math.isclose(caster.cast(M.advance / 3, target_span=32), 32 / 3)


def test_mold_attraction_is_optional_and_medium_specific() -> None:
    caster = Moldcaster(M.advance)
    source = M.advance * 0.487
    free = caster.cast_with_mold(source, target_span=100, mold=DECIMAL_10, strength=0.0)
    decimal = caster.cast_with_mold(source, target_span=100, mold=DECIMAL_10, strength=1.0)
    dyadic = caster.cast_with_mold(source, target_span=32, mold=DYADIC_32, strength=1.0)
    assert math.isclose(free, 48.7)
    assert math.isclose(decimal, 50.0)
    assert math.isclose(dyadic, 16.0)


def test_dyadic_pixel_stroke_quantizes_without_changing_source_ratio() -> None:
    caster = Moldcaster(M.advance)
    free = caster.cast_stroke(M.stroke, target_span=32)
    pixel = caster.cast_stroke(
        M.stroke,
        target_span=32,
        mold=DYADIC_32,
        quantize=True,
    )
    assert math.isclose(free, 32 / 9)
    assert pixel == 4.0


def test_affine_cast_preserves_mirrored_pairs() -> None:
    caster = Moldcaster(M.advance)
    left = M.advance * 0.17
    right = M.advance - left
    x0, x1 = caster.cast_pair_symmetric(left, right, target_span=100)
    assert math.isclose(x0 + x1, 100.0, abs_tol=1e-9)


def test_role_hierarchy_leaves_curve_handles_freer_than_stems() -> None:
    stem = ROLE_PROFILES[PointRole.STEM]
    handle = ROLE_PROFILES[PointRole.CURVE_HANDLE]
    optical = ROLE_PROFILES[PointRole.OPTICAL]
    assert stem.snap_strength > handle.snap_strength > optical.snap_strength
    assert handle.curvature_weight > stem.curvature_weight


def test_angle_families_cover_document_trihex_and_dyadic_axes() -> None:
    assert nearest_angle(88.0, DOCUMENT_AXES) == 90.0
    assert nearest_angle(58.0, TRIHEX_AXES) == 60.0
    assert nearest_angle(47.0, DYADIC_AXES) == 45.0
    assert math.isclose(attract_angle(58.0, target=60.0, strength=1.0), 60.0)
