#!/usr/bin/env python3
"""Compute metric-matched fallback values for the self-hosted webfonts.

Barlow Condensed is roughly 26% narrower than Arial, so the swap reflows any
element sized in `--cond`. `size-adjust` / `ascent-override` / `descent-override`
on a local() fallback face make the fallback occupy the same space.

Run this after replacing a font file, then paste the numbers into the
'Barlow Condensed Fallback' @font-face in css/src/01-base.css.

Usage: python3 scripts/font-fallback-metrics.py [--ref /path/to/reference.ttf]
"""
import argparse
import os

from fontTools.ttLib import TTFont

ROOT = os.path.join(os.path.dirname(__file__), '..')

# Metric-compatible with Arial; Arial itself is usually not installed on Linux.
DEFAULT_REF = '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'

WEBFONTS = [
    ('Barlow Condensed', 'fonts/BarlowCondensed-700.woff2'),
    ('Source Serif 4', 'fonts/SourceSerif4-400.woff2'),
]


def read(path):
    f = TTFont(path)
    return {
        'upem': f['head'].unitsPerEm,
        'ascent': f['hhea'].ascent,
        'descent': f['hhea'].descent,
        'linegap': f['hhea'].lineGap,
        'avg': f['OS/2'].xAvgCharWidth,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ref', default=DEFAULT_REF)
    args = ap.parse_args()

    if not os.path.exists(args.ref):
        raise SystemExit(f'reference font not found: {args.ref}\n'
                         'Pass --ref with a font whose widths match your CSS fallback.')

    ref = read(args.ref)
    ref_avg = ref['avg'] / ref['upem']
    print(f'reference: {os.path.basename(args.ref)}  avg advance {ref_avg:.4f} em\n')

    for name, rel in WEBFONTS:
        web = read(os.path.join(ROOT, rel))
        avg = web['avg'] / web['upem']
        size_adjust = avg / ref_avg
        ascent = (web['ascent'] / web['upem']) / size_adjust
        descent = abs(web['descent'] / web['upem']) / size_adjust
        linegap = (web['linegap'] / web['upem']) / size_adjust
        print(f'{name}  ({rel})')
        print(f'  avg advance          {avg:.4f} em')
        print(f'  size-adjust:         {size_adjust * 100:.2f}%')
        print(f'  ascent-override:     {ascent * 100:.2f}%')
        print(f'  descent-override:    {descent * 100:.2f}%')
        print(f'  line-gap-override:   {linegap * 100:.2f}%')
        print()


if __name__ == '__main__':
    main()
