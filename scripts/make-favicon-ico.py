#!/usr/bin/env python3
"""Render favicon.svg's design into a multi-size favicon.ico.

/favicon.ico was never generated, so it 404'd (~50 requests/week from browsers
and SEO tooling that still probe the conventional path). This reproduces the
SVG (navy rounded square, gold "AE" wordmark, gold bolt) as a real
image/x-icon.

Each size is drawn on its own rather than downscaled from the 256px master:
below 32px the bolt crosses the wordmark and merges everything into a blob, so
small entries drop the bolt and set the letters larger. That needs a
hand-written ICO container (PNG-compressed entries), since Pillow's ICO encoder
derives every size from a single source image.

    python3 scripts/make-favicon-ico.py
"""
import io
import os
import struct

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "favicon.ico")

NAVY = (11, 22, 40, 255)      # #0b1628
GOLD = (245, 166, 35, 255)    # #f5a623
S = 4                         # supersample factor
BASE = 100                    # the SVG viewBox is 100x100
FONT = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SIZES = [16, 32, 48, 64, 128, 256]
MIN_DETAIL_PX = 32            # below this, the bolt is dropped for legibility


def render(size_px: int) -> Image.Image:
    """Draw one icon at `size_px`, rendered oversized then downscaled."""
    work = size_px * S
    k = work / BASE

    img = Image.new("RGBA", (work, work), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # <rect width="100" height="100" rx="12" fill="#0b1628"/>
    d.rounded_rectangle([0, 0, work - 1, work - 1], radius=12 * k, fill=NAVY)

    detail = size_px >= MIN_DETAIL_PX
    if detail:
        # <path d="M30 78 L50 20 L60 50 L70 30" stroke="#f5a623" stroke-width="3"/>
        bolt = [(30 * k, 78 * k), (50 * k, 20 * k), (60 * k, 50 * k), (70 * k, 30 * k)]
        d.line(bolt, fill=GOLD, width=max(1, int(round(3 * k))), joint="curve")

    # <text x="50" y="62" font-size="40" ... text-anchor="middle" letter-spacing="2">
    font = ImageFont.truetype(FONT, int(round((40 if detail else 58) * k)))
    tracking = (2 if detail else 1.5) * k
    chars = ["A", "E"]
    widths = [d.textlength(c, font=font) for c in chars]
    total = sum(widths) + tracking * (len(chars) - 1)
    x = 50 * k - total / 2
    baseline = 62 * k if detail else 50 * k + font.size * 0.36
    for c, w in zip(chars, widths):
        d.text((x, baseline), c, font=font, fill=GOLD, anchor="ls")
        x += w + tracking

    return img.resize((size_px, size_px), Image.LANCZOS)


def encode_ico(pngs: list[tuple[int, bytes]]) -> bytes:
    """Assemble an ICO from (size, PNG bytes) entries."""
    count = len(pngs)
    header = struct.pack("<HHH", 0, 1, count)
    # 16-byte directory entry per icon; data follows the table.
    offset = 6 + 16 * count
    directory, payloads = b"", b""
    for size, blob in pngs:
        width = 0 if size >= 256 else size
        height = 0 if size >= 256 else size
        directory += struct.pack(
            "<BBBBHHII", width, height, 0, 0, 1, 32, len(blob), offset
        )
        payloads += blob
        offset += len(blob)
    return header + directory + payloads


def main() -> int:
    pngs = []
    for size in SIZES:
        buf = io.BytesIO()
        render(size).save(buf, format="PNG", optimize=True)
        pngs.append((size, buf.getvalue()))

    blob = encode_ico(pngs)
    with open(OUT, "wb") as fh:
        fh.write(blob)

    print(f"wrote {os.path.relpath(OUT, ROOT)}  ({len(blob):,} bytes, sizes={SIZES})")

    # Sanity checks: it must parse as an ICO, and the icon must not be blank.
    with Image.open(OUT) as check:
        assert check.format == "ICO", check.format
        assert sorted(check.info.get("sizes")) == [(s, s) for s in SIZES]
    alpha = render(32).getchannel("A")
    opaque = sum(1 for p in alpha.tobytes() if p > 0)
    assert opaque > 900, f"icon looks blank: {opaque} opaque px"
    print(f"verified: parses as ICO, 32px has {opaque}/{32 * 32} opaque px")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
