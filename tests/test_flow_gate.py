from __future__ import annotations

import math

from saygiylasunarfont.config import M
from saygiylasunarfont.flowcurve import (
    harmonic_flow_derivative,
    harmonic_flow_unit,
)
from saygiylasunarfont.flowmasters import FLOW_MASTER
from saygiylasunarfont.moldcaster import DYADIC_32
from saygiylasunarfont.registry import MIGRATED_GLYPHS


def test_harmonic_flow_has_odd_mirror_symmetry() -> None:
    for t in (0.0, 0.07, 0.19, 0.33, 0.5, 0.71, 0.93, 1.0):
        a = harmonic_flow_unit(t, harmonic_mix=0.72, stiffness=1.9)
        b = harmonic_flow_unit(1.0 - t, harmonic_mix=0.72, stiffness=1.9)
        assert math.isclose(a, -b, abs_tol=1e-9)

    assert math.isclose(harmonic_flow_unit(0.0), 1.0, abs_tol=1e-9)
    assert math.isclose(harmonic_flow_unit(0.5), 0.0, abs_tol=1e-9)
    assert math.isclose(harmonic_flow_unit(1.0), -1.0, abs_tol=1e-9)


def test_third_harmonic_creates_two_shoulders_near_thirds() -> None:
    assert harmonic_flow_derivative(0.34) < 0.0
    assert harmonic_flow_derivative(0.36) > 0.0
    assert harmonic_flow_derivative(0.64) > 0.0
    assert harmonic_flow_derivative(0.66) < 0.0


def test_optical_S_holds_terminal_longer_before_quieter_turn() -> None:
    upper = FLOW_MASTER.resolve("S")
    one_eighth = harmonic_flow_unit(
        1.0 / 8.0,
        harmonic_mix=upper.harmonic_mix,
        stiffness=upper.stiffness,
    )
    one_quarter = harmonic_flow_unit(
        1.0 / 4.0,
        harmonic_mix=upper.harmonic_mix,
        stiffness=upper.stiffness,
    )
    # This is a specimen-derived band, not a hard geometric law. Compared with
    # the previous accepted S, the terminal holds longer while the quarter-turn
    # is materially quieter; the test protects that direction without forcing a
    # cosmetic threshold that could damage recognition.
    assert one_eighth > 0.88
    assert -0.60 < one_quarter < 0.0


def test_S_and_s_are_one_family_with_optical_lowercase_relaxation() -> None:
    upper = FLOW_MASTER.resolve("S")
    lower = FLOW_MASTER.resolve("s")

    assert math.isclose(upper.center_x, M.advance / 2.0)
    assert math.isclose(lower.center_x, M.advance / 2.0)
    assert upper.amplitude > lower.amplitude
    assert upper.profile.exponent > lower.profile.exponent
    assert upper.stiffness > lower.stiffness
    assert upper.harmonic_mix > lower.harmonic_mix


def test_flow_outline_is_finite_and_stays_in_the_mono_cell() -> None:
    for kind in ("S", "s"):
        points = FLOW_MASTER.outline(kind)
        assert len(points) >= 100
        assert all(math.isfinite(x) and math.isfinite(y) for x, y in points)
        xs = [x for x, _y in points]
        assert min(xs) > 0.0
        assert max(xs) < M.advance


def test_dyadic_flow_cast_quantizes_stroke_without_changing_family() -> None:
    digital = FLOW_MASTER.resolve(
        "S",
        target_cell=32,
        target_body_height=36,
        mold=DYADIC_32,
        quantize_stroke=True,
    )
    assert digital.stroke == 4.0
    assert digital.left_terminal_x < digital.center_x < digital.right_terminal_x
    assert digital.stiffness > 1.0


def test_gate3_registry_promotes_turkish_S_family_together() -> None:
    assert {"S", "s", "Ş", "ş"}.issubset(MIGRATED_GLYPHS)
