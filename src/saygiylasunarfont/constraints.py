from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum


class PointRole(str, Enum):
    METRIC = "metric"
    STEM = "stem"
    SYMMETRY = "symmetry"
    BOWL_EXTREMUM = "bowl_extremum"
    APERTURE = "aperture"
    TERMINAL = "terminal"
    CURVE_HANDLE = "curve_handle"
    OPTICAL = "optical"


@dataclass(frozen=True)
class ConstraintProfile:
    """Relative authority of geometry rules for one point role.

    Values are deliberately dimensionless. `optical_freedom` is not another
    force; it reduces how much construction rules are allowed to move the point.
    """

    grid_weight: float
    angle_weight: float
    symmetry_weight: float
    family_weight: float
    curvature_weight: float
    optical_freedom: float

    @property
    def snap_strength(self) -> float:
        structural = (self.grid_weight + self.family_weight) / 2.0
        return max(0.0, min(1.0, structural * (1.0 - self.optical_freedom)))


ROLE_PROFILES: dict[PointRole, ConstraintProfile] = {
    PointRole.METRIC: ConstraintProfile(1.00, 0.20, 1.00, 0.90, 0.20, 0.00),
    PointRole.STEM: ConstraintProfile(0.82, 0.85, 0.78, 0.90, 0.25, 0.08),
    PointRole.SYMMETRY: ConstraintProfile(0.62, 0.25, 1.00, 0.82, 0.45, 0.10),
    PointRole.BOWL_EXTREMUM: ConstraintProfile(0.48, 0.15, 0.78, 0.88, 1.00, 0.18),
    PointRole.APERTURE: ConstraintProfile(0.32, 0.38, 0.28, 0.92, 0.86, 0.30),
    PointRole.TERMINAL: ConstraintProfile(0.38, 0.76, 0.25, 0.90, 0.55, 0.26),
    PointRole.CURVE_HANDLE: ConstraintProfile(0.12, 0.28, 0.18, 0.72, 1.00, 0.55),
    PointRole.OPTICAL: ConstraintProfile(0.02, 0.04, 0.04, 0.20, 0.45, 0.92),
}


@dataclass(frozen=True)
class AngleFamily:
    name: str
    angles: tuple[float, ...]


DOCUMENT_AXES = AngleFamily("document", (0.0, 90.0))
TRIHEX_AXES = AngleFamily("trihex", (30.0, 60.0, 120.0, 150.0))
DYADIC_AXES = AngleFamily("dyadic", (45.0, 135.0))


def _periodic_angle_distance(a: float, b: float) -> float:
    """Smallest unoriented line-angle distance, in degrees."""
    delta = abs((a - b) % 180.0)
    return min(delta, 180.0 - delta)


def nearest_angle(angle: float, *families: AngleFamily) -> float:
    if not families:
        raise ValueError("at least one angle family is required")
    candidates = [candidate for family in families for candidate in family.angles]
    return min(candidates, key=lambda candidate: _periodic_angle_distance(angle, candidate))


def attract_angle(angle: float, *, target: float, strength: float) -> float:
    """Softly rotate an unoriented line angle toward a canonical axis."""
    if not 0.0 <= strength <= 1.0:
        raise ValueError("strength must be between 0 and 1")
    # Work in doubled-angle vector space so 0° and 180° describe one line.
    a = math.radians(angle * 2.0)
    b = math.radians(target * 2.0)
    x = (1.0 - strength) * math.cos(a) + strength * math.cos(b)
    y = (1.0 - strength) * math.sin(a) + strength * math.sin(b)
    if math.isclose(x, 0.0, abs_tol=1e-12) and math.isclose(y, 0.0, abs_tol=1e-12):
        return target % 180.0
    return (math.degrees(math.atan2(y, x)) / 2.0) % 180.0


@dataclass(frozen=True)
class GeometricEnergy:
    """Energy terms used by the future constraint solver.

    Keeping terms explicit lets us inspect why a point moved instead of hiding
    design decisions inside a generic optimizer.
    """

    grid: float = 0.0
    angle: float = 0.0
    symmetry: float = 0.0
    family: float = 0.0
    curvature: float = 0.0
    optical: float = 0.0

    def total(self, profile: ConstraintProfile) -> float:
        return (
            self.grid * profile.grid_weight
            + self.angle * profile.angle_weight
            + self.symmetry * profile.symmetry_weight
            + self.family * profile.family_weight
            + self.curvature * profile.curvature_weight
            + self.optical * profile.optical_freedom
        )
