#!/usr/bin/env python3
"""Build the gallery database from the photo manifest, verifying every file on disk.

Produces two upload artifacts in db/:
  gallery.sqlite       local database, for querying and inspection
  gallery-seed.sql     idempotent D1 seed, for `wrangler d1 execute --remote --file=`

A photo is only written if all four renditions exist, are non-empty, and decode
as valid images. Anything else is reported and skipped, so a broken srcset
cannot reach production through the database.
"""
from __future__ import annotations

import csv
import sqlite3
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterator

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "scripts" / "photo-manifest.csv"
SCHEMA = ROOT / "scripts" / "gallery-db-schema.sql"
GALLERY_DIR = ROOT / "img" / "gallery"
OUT_DIR = ROOT / "db"
SQLITE_OUT = OUT_DIR / "gallery.sqlite"
SEED_OUT = OUT_DIR / "gallery-seed.sql"

# Matches CATEGORY_LABELS in scripts/update-gallery.py.
CATEGORY_LABELS: dict[str, tuple[str, str, str]] = {
    "panel": ("Panel Upgrades", "rgba(245,166,35,.2)", "#f5a623"),
    "commercial": ("Commercial", "rgba(74,144,217,.2)", "#4a90d9"),
    "new-construction": ("New Construction", "rgba(126,200,80,.2)", "#7ec850"),
    "lighting": ("Lighting", "rgba(232,123,156,.2)", "#e87b9c"),
    "team": ("Team", "rgba(155,89,182,.2)", "#9b59b6"),
    "lifestyle": ("Lifestyle", "rgba(230,126,34,.2)", "#e67e22"),
    "exterior": ("Exteriors", "rgba(26,188,156,.2)", "#1abc9c"),
    "other": ("Equipment", "rgba(149,165,166,.2)", "#95a5a6"),
}
DEFAULT_CATEGORY = "other"
EXPECTED_VARIANTS: tuple[tuple[str, str], ...] = (
    ("400w", "webp"),
    ("800w", "webp"),
    ("1200w", "webp"),
    ("1200w", "jpg"),
)


@dataclass(frozen=True)
class Variant:
    slug: str
    variant: str
    fmt: str
    path: str
    byte_size: int
    width: int
    height: int


@dataclass(frozen=True)
class Photo:
    slug: str
    source_file: str
    category: str
    caption: str
    alt_text: str
    city: str
    shoot_year: int | None
    custom_crop: str | None
    variants: tuple[Variant, ...]


class ManifestError(RuntimeError):
    pass


def sql_quote(value: str) -> str:
    return "'" + str(value).replace("'", "''") + "'"


def read_manifest() -> list[dict[str, str]]:
    if not MANIFEST.exists():
        raise ManifestError(f"manifest not found: {MANIFEST}")
    with MANIFEST.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ManifestError(f"manifest is empty: {MANIFEST}")
    return rows


def probe_variant(slug: str, variant: str, fmt: str) -> tuple[Variant | None, str | None]:
    """Return the measured variant, or (None, reason) when it is unusable."""
    path = GALLERY_DIR / f"{slug}-{variant}.{fmt}"
    rel = f"img/gallery/{path.name}"
    if not path.exists():
        return None, "missing"
    size = path.stat().st_size
    if size == 0:
        return None, "zero bytes"
    try:
        with Image.open(path) as im:
            im.verify()
        with Image.open(path) as im:
            width, height = im.size
    except (OSError, SyntaxError) as exc:
        return None, f"undecodable ({type(exc).__name__})"
    return Variant(slug, variant, fmt, rel, size, width, height), None


def build_photo(row: dict[str, str], order: int) -> tuple[Photo | None, list[str], list[str]]:
    """Return (photo, errors, warnings). A non-empty error list means the photo is rejected."""
    slug = (row.get("slug") or "").strip()
    errors: list[str] = []
    warnings: list[str] = []
    if not slug:
        return None, ["manifest row has an empty slug"], warnings

    variants: list[Variant] = []
    for variant, fmt in EXPECTED_VARIANTS:
        measured, reason = probe_variant(slug, variant, fmt)
        if measured is None:
            errors.append(f"{slug}-{variant}.{fmt}: {reason}")
        else:
            variants.append(measured)
    if errors:
        return None, errors, warnings

    category = (row.get("category") or "").strip() or DEFAULT_CATEGORY
    if category not in CATEGORY_LABELS:
        warnings.append(f"{slug}: unknown category {category!r}, stored as {DEFAULT_CATEGORY!r}")
        category = DEFAULT_CATEGORY

    caption = (row.get("caption") or "").strip() or "Electrical project by AMY Electric"
    city = (row.get("city") or "").strip() or "Los Angeles"
    raw_year = (row.get("year") or "").strip()
    try:
        year = int(raw_year) if raw_year else None
    except ValueError:
        warnings.append(f"{slug}: non-numeric year {raw_year!r}, stored as NULL")
        year = None

    crop = (row.get("custom_crop") or "").strip() or None
    return (
        Photo(
            slug=slug,
            source_file=(row.get("source_file") or "").strip(),
            category=category,
            caption=caption,
            alt_text=f"{caption} - AMY Electric {city}",
            city=city,
            shoot_year=year,
            custom_crop=crop,
            variants=tuple(variants),
        ),
        errors,
        warnings,
    )


def write_sqlite(photos: list[Photo], stamp: str) -> None:
    if SQLITE_OUT.exists():
        SQLITE_OUT.unlink()
    con = sqlite3.connect(SQLITE_OUT)
    try:
        con.executescript(SCHEMA.read_text(encoding="utf-8"))
        with con:
            con.executemany(
                "INSERT INTO gallery_images (slug, source_file, category, caption, alt_text,"
                " city, shoot_year, width, height, custom_crop, display_order, verified_at)"
                " VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                [
                    (
                        p.slug, p.source_file, p.category, p.caption, p.alt_text,
                        p.city, p.shoot_year, 1200, 900, p.custom_crop, i, stamp,
                    )
                    for i, p in enumerate(photos, 1)
                ],
            )
            con.executemany(
                "INSERT INTO gallery_image_variants (slug, variant, format, path, byte_size, width, height)"
                " VALUES (?,?,?,?,?,?,?)",
                [
                    (v.slug, v.variant, v.fmt, v.path, v.byte_size, v.width, v.height)
                    for p in photos
                    for v in p.variants
                ],
            )
    finally:
        con.close()


def iter_seed_statements(photos: list[Photo], stamp: str) -> Iterator[str]:
    for order, (slug, (label, bg, color)) in enumerate(
        sorted(CATEGORY_LABELS.items(), key=lambda kv: kv[1][0]), 1
    ):
        yield (
            "INSERT OR IGNORE INTO gallery_categories (slug,label,bg,color,display_order)"
            f" VALUES ({sql_quote(slug)},{sql_quote(label)},{sql_quote(bg)},{sql_quote(color)},{order});"
        )
    for p in photos:
        yield (
            "INSERT OR REPLACE INTO gallery_images (slug,source_file,category,caption,alt_text,"
            " city,shoot_year,width,height,custom_crop,display_order,verified_at) VALUES ("
            + ",".join(
                sql_quote(v) if isinstance(v, str) else ("NULL" if v is None else str(v))
                for v in (p.slug, p.source_file, p.category, p.caption, p.alt_text,
                          p.city, p.shoot_year, 1200, 900, p.custom_crop, 0, stamp)
            )
            + ");"
        )
        for v in p.variants:
            yield (
                "INSERT OR REPLACE INTO gallery_image_variants (slug,variant,format,path,byte_size,width,height)"
                f" VALUES ({sql_quote(v.slug)},{sql_quote(v.variant)},{sql_quote(v.fmt)},"
                f"{sql_quote(v.path)},{v.byte_size},{v.width},{v.height});"
            )


def main() -> int:
    rows = read_manifest()
    stamp = date.today().isoformat()
    photos: list[Photo] = []
    errors: list[str] = []
    warnings: list[str] = []

    for order, row in enumerate(rows, 1):
        photo, row_errors, row_warnings = build_photo(row, order)
        errors.extend(row_errors)
        warnings.extend(row_warnings)
        if photo is not None:
            photos.append(photo)

    print(f"manifest rows      : {len(rows)}")
    print(f"photos written     : {len(photos)}")
    print(f"photos rejected    : {len(rows) - len(photos)}")
    if errors:
        print(f"\nrejected ({len(errors)}):")
        for problem in errors:
            print(f"  {problem}")
    if warnings:
        by_kind: dict[str, int] = {}
        for problem in warnings:
            key = problem.split(":", 1)[1].strip() if ":" in problem else problem
            kind = key.split(",")[0]
            by_kind[kind] = by_kind.get(kind, 0) + 1
        print(f"\nwarnings ({len(warnings)}), grouped:")
        for kind, count in sorted(by_kind.items(), key=lambda kv: -kv[1]):
            print(f"  {count:>4}  {kind}")

    OUT_DIR.mkdir(exist_ok=True)
    write_sqlite(photos, stamp)
    header = (
        f"-- Generated by scripts/build-gallery-db.py on {stamp}. Do not edit by hand.\n"
        f"-- {len(photos)} photos, {len(photos) * len(EXPECTED_VARIANTS)} verified renditions.\n"
        f"-- Idempotent: safe to re-apply.\n\n"
        f"PRAGMA foreign_keys = ON;\n"
    )
    SEED_OUT.write_text(
        header + "\n".join(iter_seed_statements(photos, stamp)) + "\n", encoding="utf-8"
    )
    (OUT_DIR / "gallery-schema.sql").write_text(SCHEMA.read_text(encoding="utf-8"), encoding="utf-8")

    print(f"\nwrote {SQLITE_OUT.relative_to(ROOT)}")
    print(f"wrote {SEED_OUT.relative_to(ROOT)}")
    print(f"wrote {(OUT_DIR / 'gallery-schema.sql').relative_to(ROOT)}")
    return 1 if len(photos) != len(rows) else 0


if __name__ == "__main__":
    sys.exit(main())
