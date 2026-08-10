from __future__ import annotations

from dataclasses import dataclass

from .constraints import (
    AngleFamily,
    PointRole,
    ROLE_PROFILES,
    attract_angle,
    nearest_angle,
)
from .moldcaster import Mold, Moldcaster


@dataclass(frozen=True)
class ConstructionSolver:
    """Single entrypoint for role-aware geometric casting.

    The solver deliberately remains lightweight: it combines normalized casting,
    role-specific mold attraction and angle attraction without hiding optical
    decisions inside an opaque optimizer. More advanced energy minimization can
    be added behind this interface without changing glyph code.
    """

    caster: Moldcaster

    def solve_coordinate(
        self,
        value: float,
        *,
        target_span: float,
        mold: Mold,
        role: PointRole,
        strength_scale: float = 1.0,
    ) -> float:
        if strength_scale < 0:
            raise ValueError("strength_scale must be non-negative")
        profile = ROLE_PROFILES[role]
        strength = min(1.0, profile.snap_strength * strength_scale)
        return self.caster.cast_with_mold(
            value,
            target_span=target_span,
            mold=mold,
            strength=strength,
        )

    def solve_point(
        self,
        point: tuple[float, float],
        *,
        source_height: float,
        target_width: float,
        target_height: float,
        mold_x: Mold,
        mold_y: Mold,
        role: PointRole,
        strength_scale: float = 1.0,
    ) -> tuple[float, float]:
        if source_height <= 0:
            raise ValueError("source_height must be positive")
        x, y = point
        solved_x = self.solve_coordinate(
            x,
            target_span=target_width,
            mold=mold_x,
            role=role,
            strength_scale=strength_scale,
        )

        y_caster = Moldcaster(source_height)
        profile = ROLE_PROFILES[role]
        strength = min(1.0, profile.snap_strength * strength_scale)
        solved_y = y_caster.cast_with_mold(
            y,
            target_span=target_height,
            mold=mold_y,
            strength=strength,
        )
        return solved_x, solved_y

    def solve_angle(
        self,
        angle: float,
        *,
        role: PointRole,
        families: tuple[AngleFamily, ...],
        strength_scale: float = 1.0,
    ) -> float:
        if not families:
            raise ValueError("at least one angle family is required")
        if strength_scale < 0:
            raise ValueError("strength_scale must be non-negative")
        profile = ROLE_PROFILES[role]
        target = nearest_angle(angle, *families)
        strength = min(
            1.0,
            profile.angle_weight * (1.0 - profile.optical_freedom) * strength_scale,
        )
        return attract_angle(angle, target=target, strength=strength)
