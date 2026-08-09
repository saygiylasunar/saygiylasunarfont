from __future__ import annotations

from pathlib import Path

from fontTools.fontBuilder import FontBuilder

from .config import FAMILY_NAME, M, POSTSCRIPT_NAME, STYLE_NAME, VERSION
from .glyphs import build_glyphs


def build(output: Path | str = "build/SaygiylaSunarMono-Regular.ttf") -> Path:
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)

    order, glyphs, cmap = build_glyphs()
    fb = FontBuilder(M.upm, isTTF=True)
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap(cmap)
    fb.setupGlyf(glyphs)

    # Monospace is an invariant. Ink may move inside the cell; advance never does.
    glyph_table = fb.font["glyf"]
    metrics = {
        name: (M.advance, getattr(glyph_table[name], "xMin", 0))
        for name in order
    }
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=M.ascender, descent=M.descender)

    fb.setupNameTable(
        {
            "familyName": FAMILY_NAME,
            "styleName": STYLE_NAME,
            "uniqueFontIdentifier": f"SaygiylaSunar:{VERSION}",
            "fullName": f"{FAMILY_NAME} {STYLE_NAME}",
            "psName": POSTSCRIPT_NAME,
            "version": f"Version {VERSION}",
        }
    )
    fb.setupOS2(
        sTypoAscender=M.ascender,
        sTypoDescender=M.descender,
        sTypoLineGap=0,
        usWinAscent=M.ascender,
        usWinDescent=abs(M.descender),
        sxHeight=M.x_height,
        sCapHeight=M.cap_height,
        xAvgCharWidth=M.advance,
    )
    fb.setupPost(isFixedPitch=1)

    # Keep the font deterministic enough for review diffs.
    fb.font.recalcTimestamp = False
    fb.font["head"].created = 0
    fb.font["head"].modified = 0
    fb.save(output)
    return output


def main() -> None:
    path = build()
    print(path)


if __name__ == "__main__":
    main()
