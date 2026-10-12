#!/usr/bin/env python3
"""Build lead-wizard bundles (idempotent).

- Concatenates js/src/05-estimate-data.js + js/src/06-estimate-engine.js +
  js/wizard.js -> js/lead-estimator.js, minifies (same regex pipeline as
  scripts/build-js.py) -> js/lead-estimator.min.js
- Concatenates css/lead-form.css + css/lead-form-part2.css -> css/lead-form.min.css
- Asserts budgets (JS <= 24KB, CSS <= 14KB) and fails loudly otherwise.
- Run: python3 scripts/build-leadform.py
"""

import os
import re
import sys

ROOT = os.path.join(os.path.dirname(__file__), "..")
JS_SRC = [
    "js/src/05-estimate-data.js",
    "js/src/06-estimate-engine.js",
    "js/wizard.js",
]
CSS_SRC = ["css/lead-form.css", "css/lead-form-part2.css"]
JS_OUT = "js/lead-estimator.js"
JS_MIN = "js/lead-estimator.min.js"
CSS_OUT = "css/lead-form.min.css"
JS_BUDGET = 24 * 1024
CSS_BUDGET = 14 * 1024


def minify_js(js):
    js = re.sub(r"/\*.*?\*/", "", js, flags=re.DOTALL)
    js = re.sub(r"//.*", "", js)
    js = re.sub(r"\s+", " ", js)
    js = re.sub(r"\s*;\s*", ";", js)
    js = re.sub(r"\s*{\s*", "{", js)
    js = re.sub(r"\s*}\s*", "}", js)
    js = re.sub(r"\s*\(\s*", "(", js)
    js = re.sub(r"\s*\)\s*", ")", js)
    js = re.sub(r"\s*=\s*", "=", js)
    return js.strip()


def minify_css(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*{\s*", "{", css)
    css = re.sub(r"}\s*", "}", css)
    css = re.sub(r";\s*", ";", css)
    css = re.sub(r":\s*", ":", css)
    css = re.sub(r",\s*", ",", css)
    return css.strip()


def read_many(paths):
    parts = []
    for p in paths:
        full = os.path.join(ROOT, p)
        if not os.path.exists(full):
            sys.exit("build-leadform: missing source " + p)
        with open(full, encoding="utf-8") as fh:
            parts.append(fh.read())
    return "\n".join(parts)


def main():
    js = read_many(JS_SRC)
    with open(os.path.join(ROOT, JS_OUT), "w", encoding="utf-8") as f:
        f.write(js)
    js_min = (
        "/* AMY Electric lead wizard bundle. Sources: "
        + ", ".join(JS_SRC)
        + " */\n"
        + minify_js(js)
    )
    with open(os.path.join(ROOT, JS_MIN), "w", encoding="utf-8") as f:
        f.write(js_min)

    css = read_many(CSS_SRC)
    css_min = (
        "/* AMY Electric lead form styles. Sources: " + ", ".join(CSS_SRC) + " */\n" + minify_css(css)
    )
    with open(os.path.join(ROOT, CSS_OUT), "w", encoding="utf-8") as f:
        f.write(css_min)

    js_size = len(js_min.encode("utf-8"))
    css_size = len(css_min.encode("utf-8"))
    print("Wrote %s (%d bytes)" % (JS_MIN, js_size))
    print("Wrote %s (%d bytes)" % (CSS_OUT, css_size))
    failed = False
    if js_size > JS_BUDGET:
        print("OVER BUDGET: JS %d > %d" % (js_size, JS_BUDGET))
        failed = True
    if css_size > CSS_BUDGET:
        print("OVER BUDGET: CSS %d > %d" % (css_size, CSS_BUDGET))
        failed = True
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
