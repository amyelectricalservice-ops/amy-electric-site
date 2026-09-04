import json
import sys
import os

def parse_lighthouse(json_path):
    if not os.path.exists(json_path):
        print(f"File {json_path} does not exist yet.")
        return

    with open(json_path, 'r', encoding='utf-8') as fh:
        data = json.load(fh)

    categories = data.get('categories', {})
    perf = (categories.get('performance', {}).get('score') or 0) * 100
    a11y = (categories.get('accessibility', {}).get('score') or 0) * 100
    bp = (categories.get('best-practices', {}).get('score') or 0) * 100
    seo = (categories.get('seo', {}).get('score') or 0) * 100

    print("=" * 50)
    print("      LIGHTHOUSE AUDIT SCORES REPORT")
    print("=" * 50)
    print(f"  Performance:    {perf:5.1f} / 100  ({'🟢 PASS' if perf>=90 else '🟡 NEEDS IMP' if perf>=50 else '🔴 POOR'})")
    print(f"  Accessibility:  {a11y:5.1f} / 100  ({'🟢 PASS' if a11y>=90 else '🟡 NEEDS IMP' if a11y>=50 else '🔴 POOR'})")
    print(f"  Best Practices: {bp:5.1f} / 100  ({'🟢 PASS' if bp>=90 else '🟡 NEEDS IMP' if bp>=50 else '🔴 POOR'})")
    print(f"  SEO:            {seo:5.1f} / 100  ({'🟢 PASS' if seo>=90 else '🟡 NEEDS IMP' if seo>=50 else '🔴 POOR'})")
    print("=" * 50)

    audits = data.get('audits', {})
    
    print("\n--- CORE WEB VITALS & METRICS ---")
    metrics = [
        ('first-contentful-paint', 'First Contentful Paint (FCP)'),
        ('largest-contentful-paint', 'Largest Contentful Paint (LCP)'),
        ('total-blocking-time', 'Total Blocking Time (TBT)'),
        ('cumulative-layout-shift', 'Cumulative Layout Shift (CLS)'),
        ('speed-index', 'Speed Index'),
        ('server-response-time', 'Root Document TTFB'),
    ]
    for metric_id, label in metrics:
        item = audits.get(metric_id, {})
        disp_val = item.get('displayValue', 'N/A')
        score = item.get('score', 0)
        icon = '🟢' if score and score >= 0.9 else ('🟡' if score and score >= 0.5 else '🔴')
        print(f"  {icon} {label:<35}: {disp_val}")

    print("\n--- KEY OPPORTUNITIES & DIAGNOSTICS ---")
    opp_keys = [
        'render-blocking-resources',
        'unused-css-rules',
        'unused-javascript',
        'modern-image-formats',
        'uses-optimized-images',
        'font-display',
        'is-on-https',
    ]
    for k in opp_keys:
        item = audits.get(k, {})
        if item and item.get('score') is not None and item.get('score') < 1.0:
            title = item.get('title', k)
            disp = item.get('displayValue', item.get('explanation', 'Needs attention'))
            print(f"  • [!] {title}: {disp}")

if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else 'reports/lighthouse-audit.json'
    parse_lighthouse(path)
