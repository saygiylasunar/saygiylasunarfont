from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Mold:
    """A target construction lattice expressed as normalized subdivisions.

    A mold does not own glyph design. It offers attractors for reinterpreting the
    same normalized geometry in a target medium (font units, decimal diagrams,
    bitmap/pixel grids, etc.). Earlier divisions are stronger structural anchors;
    later divisions provide progressively finer correction.
    """

    name: str
    divisions: tuple[int, ...]
    weights: tuple[float, ...]

    def __post_init__(self) -> None:
        if not self.divisions:
            raise ValueError("mold needs at least one division")
        if len(self.divisions) != len(self.weights):
            raise ValueError("divisions and weights must have equal length")
        if any(d <= 0 for d in self.divisions):
            raise ValueError("mold divisions must be positive")
        if any(w <= 0 for w in self.weights):
            raise ValueError("mold weights must be positive")

    @property
    def finest_division(self) -> int:
        return max(self.divisions)

    def normalized_candidates(self) -> list[tuple[float, float]]:
        """Return unique normalized attractors and their strongest weight."""
        candidates: dict[float, float] = {}
        for division, weight in zip(self.divisions, self.weights):
            for i in range(division + 1):
                u = i / division
                candidates[u] = max(weight, candidates.get(u, 0.0))
        return sorted(candidates.items())

    def nearest(self, u: float) -> float:
        """Find the lowest-energy normalized attractor for `u`.

        Structural anchors can beat a slightly closer fine-grid point because
        distance is divided by the attractor's hierarchy weight.
        """
        if not 0.0 <= u <= 1.0:
            raise ValueError("normalized coordinate must be in [0, 1]")
        return min(
            self.normalized_candidates(),
            key=lambda item: ((u - item[0]) ** 2) / item[1],
        )[0]


# 648 = 18 × 36. Half remains useful for symmetry; 3/6/9 carry the main
# characteristic; 18 exposes the 36-unit core as the finest native quantum.
TRIHEX_36 = Mold(
    "trihex-36",
    divisions=(2, 3, 6, 9, 18),
    weights=(1.00, 1.00, 0.90, 0.78, 0.52),
)

# Base-10 geometry is fundamentally friendly to factors 2 and 5. Tenths are a
# fine representation layer, while halves and fifths remain stronger anchors.
DECIMAL_10 = Mold(
    "decimal-10",
    divisions=(2, 5, 10),
    weights=(1.00, 0.92, 0.58),
)

# Digital/bitmap work benefits from dyadic subdivision. 32 is intentionally the
# default fine grid: it is detailed enough for icon/terminal experiments while
# preserving the power-of-two hierarchy all the way down.
DYADIC_32 = Mold(
    "dyadic-32",
    divisions=(2, 4, 8, 16, 32),
    weights=(1.00, 0.94, 0.82, 0.66, 0.48),
)


@dataclass(frozen=True)
class Moldcaster:
    """Translate one normalized design into different construction media."""

    source_span: float = 648.0

    def __post_init__(self) -> None:
        if self.source_span <= 0:
            raise ValueError("source_span must be positive")

    def normalize(self, value: float) -> float:
        return value / self.source_span

    def cast(self, value: float, *, target_span: float) -> float:
        """Affine cast preserving normalized geometry exactly."""
        if target_span <= 0:
            raise ValueError("target_span must be positive")
        return self.normalize(value) * target_span

    def attract_normalized(self, u: float, *, mold: Mold, strength: float) -> float:
        """Attract normalized geometry toward a mold without making it a law."""
        if not 0.0 <= strength <= 1.0:
            raise ValueError("strength must be between 0 and 1")
        target = mold.nearest(u)
        return u + (target - u) * strength

    def cast_with_mold(
        self,
        value: float,
        *,
        target_span: float,
        mold: Mold,
        strength: float,
    ) -> float:
        u = self.normalize(value)
        if not 0.0 <= u <= 1.0:
            raise ValueError("source coordinate must be inside source span")
        return self.attract_normalized(u, mold=mold, strength=strength) * target_span

    def cast_stroke(
        self,
        stroke: float,
        *,
        target_span: float,
        mold: Mold | None = None,
        quantize: bool = False,
        minimum: float = 1.0,
    ) -> float:
        """Scale stroke by ratio, optionally quantizing for discrete media.

        Quantization uses the finest target mold quantum. For example a 72/648
        stroke cast into a 32-pixel dyadic cell resolves from 3.555… to 4 px.
        """
        if stroke <= 0:
            raise ValueError("stroke must be positive")
        result = self.cast(stroke, target_span=target_span)
        if not quantize:
            return result
        if mold is None:
            raise ValueError("quantized stroke requires a mold")
        quantum = target_span / mold.finest_division
        snapped = round(result / quantum) * quantum
        return max(minimum, snapped)

    def cast_pair_symmetric(
        self,
        left: float,
        right: float,
        *,
        target_span: float,
    ) -> tuple[float, float]:
        """Affine casting helper used to preserve mirrored construction pairs."""
        return (
            self.cast(left, target_span=target_span),
            self.cast(right, target_span=target_span),
        )
