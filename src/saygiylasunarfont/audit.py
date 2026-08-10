from __future__ import annotations

from pathlib import Path

from fontTools.ttLib import TTFont

from .build import build
from .config import M

CORE_TURKISH = "ÇĞİÖŞÜçğıöşü"
DIAGNOSTIC_STRING = "HIO0 1Ilı aoe cg CGSŞş TVWZ ÇĞİÖŞÜ çğıöşü ² ₺"


def audit(path: Path | str = "build/SaygiylaSunarMono-Regular.ttf") -> list[str]:
    path = Path(path)
    if not path.exists():
        build(path)

    font = TTFont(path)
    failures: list[str] = []

    metrics = font["hmtx"].metrics
    bad_widths = {name: width for name, (width, _lsb) in metrics.items() if width != M.advance}
    if bad_widths:
        failures.append(f"non-monospaced advance widths: {bad_widths}")

    if font["post"].isFixedPitch != 1:
        failures.append("post.isFixedPitch is not set")

    cmap = font.getBestCmap() or {}
    missing_turkish = [ch for ch in CORE_TURKISH if ord(ch) not in cmap]
    if missing_turkish:
        failures.append(f"missing Turkish core: {''.join(missing_turkish)}")

    for cp, name in cmap.items():
        if name not in metrics:
            failures.append(f"U+{cp:04X} maps to glyph without metrics: {name}")

    return failures


def main() -> None:
    path = build()
    failures = audit(path)
    print(f"font: {path}")
    print(f"advance: {M.advance} units")
    print(f"diagnostic: {DIAGNOSTIC_STRING}")
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        raise SystemExit(1)
    print("OK: monospaced and Turkish core invariants hold")


if __name__ == "__main__":
    main()
