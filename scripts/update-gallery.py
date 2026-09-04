#!/usr/bin/env python3
"""Regenerate gallery.html — first 36 items as HTML, rest loaded from JSON via 'Show more'."""
import csv
import json
import re
from pathlib import Path

WEBSITE = Path(__file__).parent.parent
MANIFEST = WEBSITE / "scripts/photo-manifest.csv"
GALLERY_FILE = WEBSITE / "gallery.html"
SITEMAP_FILE = WEBSITE / "sitemap.xml"

ITEMS_PER_PAGE = 36

CATEGORY_LABELS = {
    "panel": ("Panel Upgrades", "rgba(245,166,35,.2)", "#f5a623"),
    "commercial": ("Commercial", "rgba(74,144,217,.2)", "#4a90d9"),
    "new-construction": ("New Construction", "rgba(126,200,80,.2)", "#7ec850"),
    "lighting": ("Lighting", "rgba(232,123,156,.2)", "#e87b9c"),
    "team": ("Team", "rgba(155,89,182,.2)", "#9b59b6"),
    "lifestyle": ("Lifestyle", "rgba(230,126,34,.2)", "#e67e22"),
    "exterior": ("Exteriors", "rgba(26,188,156,.2)", "#1abc9c"),
    "other": ("Equipment", "rgba(149,165,166,.2)", "#95a5a6"),
}

GALLERY_ITEM_TPL = '''    <div class="gallery-item" data-category="{cat}" data-city="{city}" data-year="{year}">
      <picture>
        <source srcset="img/gallery/{slug}-400w.webp 400w, img/gallery/{slug}-800w.webp 800w, img/gallery/{slug}-1200w.webp 1200w" type="image/webp" sizes="(max-width: 480px) calc(100vw - 48px), (max-width: 768px) calc(50vw - 36px), (max-width: 1400px) calc(33vw - 32px), 300px">
        <source srcset="img/gallery/{slug}-1200w.jpg" type="image/jpeg">
        <img src="img/gallery/{slug}-1200w.jpg" alt="{alt}" width="1200" height="900" loading="lazy" decoding="async">
      </picture>
      <div class="gallery-overlay">
        <h3>{caption}</h3>
        <p class="gallery-location">{city}, CA &middot; {year}</p>
        <span class="gallery-tag" style="background:{bg};color:{color}">{label}</span>
      </div>
    </div>'''


def read_manifest():
    with open(MANIFEST, newline="") as f:
        return list(csv.DictReader(f))


def make_item_data(row):
    cat = row.get("category", "other").strip() or "other"
    label, bg, color = CATEGORY_LABELS.get(cat, CATEGORY_LABELS["other"])
    city = row.get("city", "").strip() or "Los Angeles"
    year = row.get("year", "").strip() or "2025"
    caption = row.get("caption", "").strip() or "Electrical project by AMY Electric"
    slug = row["slug"].strip()
    return {
        "slug": slug,
        "cat": cat,
        "caption": caption,
        "city": city,
        "year": year,
        "label": label,
        "bg": bg,
        "color": color,
        "alt": f"{caption} - AMY Electric {city}",
    }


def gallery_item_html(d):
    return GALLERY_ITEM_TPL.format(**d)


def gallery_item_js_template():
    """Return JS to render a gallery item from the JSON data array."""
    return r'''
function renderGalleryItem(d) {
  var h = '<div class="gallery-item" data-category="' + d.c + '" data-city="' + d.city + '" data-year="' + d.y + '">';
  h += '<picture><source srcset="img/gallery/' + d.s + '-400w.webp 400w, img/gallery/' + d.s + '-800w.webp 800w, img/gallery/' + d.s + '-1200w.webp 1200w" type="image/webp" sizes="(max-width: 480px) calc(100vw - 48px), (max-width: 768px) calc(50vw - 36px), (max-width: 1400px) calc(33vw - 32px), 300px">';
  h += '<source srcset="img/gallery/' + d.s + '-1200w.jpg" type="image/jpeg">';
  h += '<img src="img/gallery/' + d.s + '-1200w.jpg" alt="' + d.cap + ' - AMY Electric ' + d.city + '" width="1200" height="900" loading="lazy" decoding="async"></picture>';
  h += '<div class="gallery-overlay"><h3>' + d.cap + '</h3>';
  h += '<p class="gallery-location">' + d.city + ', CA &middot; ' + d.y + '</p>';
  h += '<span class="gallery-tag" style="background:' + d.bg + ';color:' + d.cl + '">' + d.lbl + '</span></div></div>';
  return h;
}
'''


def itemlist_json(rows):
    items = []
    for i, r in enumerate(rows, 1):
        slug = r["slug"]
        caption = r.get("caption", "").strip() or "Electrical project by AMY Electric"
        city = r.get("city", "").strip() or "Los Angeles"
        year = r.get("year", "").strip() or "2025"
        items.append(
            '{"@type":"ListItem","position":%d,"item":{"@type":"ImageObject",'
            '"contentUrl":"https://amyelectric.com/img/gallery/%s-1200w.webp",'
            '"caption":"%s in %s, CA","name":"%s",'
            '"uploadDate":"%s-01-01"}}' % (i, slug, caption, city, caption, year)
        )
    return '{"@context":"https://schema.org","@type":"ItemList","itemListElement":[\n' + ",\n".join(items) + "]}"


def gallery_data_js(data):
    """Generate compact JSON array of gallery data for JS."""
    compact = []
    for d in data:
        compact.append({
            "s": d["slug"],
            "c": d["cat"],
            "cap": d["caption"],
            "city": d["city"],
            "y": d["year"],
            "lbl": d["label"],
            "bg": d["bg"],
            "cl": d["color"],
        })
    return json.dumps(compact, ensure_ascii=False, separators=(',', ':'))


GALLERY_JS = r'''
(function(){
  var grid = document.getElementById('gallery-grid');
  var chips = document.querySelectorAll('.filter-chip');
  var modal = document.getElementById('gallery-modal');
  var modalImg = document.getElementById('modal-image');
  var modalCap = modal.querySelector('.modal-caption');
  var modalClose = modal.querySelector('.modal-close');
  var modalPrev = modal.querySelector('.modal-prev');
  var modalNext = modal.querySelector('.modal-next');
  var modalBackdrop = modal.querySelector('.modal-backdrop');
  var currentIndex = -1;
  var showMoreBtn = document.getElementById('show-more-btn');

  function getItems() {
    return Array.from(grid.querySelectorAll('.gallery-item'));
  }

  function filterGallery(category) {
    chips.forEach(function(c) { c.classList.toggle('active', c.dataset.filter === category); });
    var items = getItems();
    items.forEach(function(item) {
      var match = category === 'all' || item.dataset.category === category;
      item.classList.toggle('hidden', !match);
    });
  }

  chips.forEach(function(chip) {
    chip.addEventListener('click', function() { filterGallery(chip.dataset.filter); });
  });

  function openModal(index) {
    var items = getItems().filter(function(i) { return !i.classList.contains('hidden'); });
    if (index < 0 || index >= items.length) return;
    currentIndex = index;
    var item = items[index];
    var img = item.querySelector('img');
    var h3 = item.querySelector('h3');
    var loc = item.querySelector('.gallery-location');
    var tag = item.querySelector('.gallery-tag');
    var largeSrc = img.src.replace('-1200w.jpg', '-1200w.webp');
    modalImg.src = largeSrc;
    modalImg.alt = img.alt;
    modalCap.innerHTML = (h3 ? h3.textContent : '') + '<br><span style="font-size:13px;opacity:.7;">' + (loc ? loc.textContent : '') + ' &middot; ' + (tag ? tag.textContent : '') + '</span>';
    modal.removeAttribute('hidden');
    document.body.style.overflow = 'hidden';
  }

  function closeModal() {
    modal.setAttribute('hidden', '');
    document.body.style.overflow = '';
    currentIndex = -1;
  }

  function navigate(direction) {
    var items = getItems().filter(function(i) { return !i.classList.contains('hidden'); });
    var idx = currentIndex + direction;
    if (idx < 0) idx = items.length - 1;
    if (idx >= items.length) idx = 0;
    openModal(idx);
  }

  function attachClick(items) {
    items.forEach(function(item) {
      item.addEventListener('click', function() {
        var visible = getItems().filter(function(i) { return !i.classList.contains('hidden'); });
        openModal(visible.indexOf(item));
      });
    });
  }

  attachClick(getItems());

  modalClose.addEventListener('click', closeModal);
  modalBackdrop.addEventListener('click', closeModal);
  modalPrev.addEventListener('click', function() { navigate(-1); });
  modalNext.addEventListener('click', function() { navigate(1); });

  document.addEventListener('keydown', function(e) {
    if (modal.hasAttribute('hidden')) return;
    if (e.key === 'Escape') closeModal();
    if (e.key === 'ArrowLeft') navigate(-1);
    if (e.key === 'ArrowRight') navigate(1);
  });

  if (showMoreBtn) {
    showMoreBtn.addEventListener('click', function() {
      var idx = parseInt(showMoreBtn.dataset.next, 10);
      var batch = galleryData.slice(idx, idx + 36);
      var frag = document.createDocumentFragment();
      batch.forEach(function(d) {
        var div = document.createElement('div');
        div.innerHTML = renderGalleryItem(d);
        frag.appendChild(div.firstElementChild);
      });
      grid.appendChild(frag);
      attachClick(Array.from(frag.children));
      var newIdx = idx + batch.length;
      if (newIdx >= galleryData.length) {
        showMoreBtn.style.display = 'none';
      } else {
        showMoreBtn.dataset.next = newIdx;
      }
    });
  }
})();
'''


def main():
    rows = read_manifest()
    total = len(rows)
    print(f"Building gallery for {total} photos...")

    data = [make_item_data(r) for r in rows]

    # First N items as static HTML
    head = data[:ITEMS_PER_PAGE]
    tail = data[ITEMS_PER_PAGE:]
    all_items_html = "\n".join(gallery_item_html(d) for d in head)

    # Show more button + data script
    show_more_html = ""
    if tail:
        show_more_html = '\n  <div class="show-more-wrap"><button id="show-more-btn" class="btn btn-gold" data-next="%d">Show More (%d more)</button></div>' % (
            ITEMS_PER_PAGE, len(tail)
        )
        show_more_html += '\n<script>var galleryData = %s;</script>' % gallery_data_js(data)
        show_more_html += '\n<script>' + gallery_item_js_template() + '</script>'

    # Read current gallery.html and make replacements
    content = GALLERY_FILE.read_text(encoding="utf-8")

    # 1. Remove the first inline <style> block (full site CSS, redundant with style.min.css)
    content = re.sub(r'<style>.*?</style>', '', content, count=1, flags=re.DOTALL)

    # 2. Replace the gallery section content (from gallery-grid open to </section>)
    # This approach is idempotent — any existing items or show-more content are fully replaced.
    grid_start = content.find('<div class="gallery-grid" id="gallery-grid">')
    if grid_start == -1:
        raise SystemExit("ERROR: gallery-grid div not found in gallery.html")

    section_end = content.find('</section>', grid_start)
    if section_end == -1:
        raise SystemExit("ERROR: </section> not found after gallery-grid")

    new_grid = '<div class="gallery-grid" id="gallery-grid">\n' + all_items_html + '\n  </div>\n' + show_more_html + '\n</section>'
    content = content[:grid_start] + new_grid + content[section_end + len('</section>'):]

    # 3. Remove the gallery-specific inline <style> block (duplicate with 12-gallery.css)
    # content = re.sub(r'<style>\n?\.gallery-filters.*?</style>', '', content, flags=re.DOTALL)
    # More robust: remove any remaining <style> block that contains gallery- or modal-related CSS
    content = re.sub(r'<style>\s*\.gallery-filters.*?</style>', '', content, flags=re.DOTALL)

    # 4. Update descripion counts
    content = re.sub(
        r'<meta name="description" content="View our gallery of \d+\+? real electrical projects',
        f'<meta name="description" content="View our gallery of {total} real electrical projects',
        content
    )
    content = re.sub(
        r'<meta property="og:description" content="View our gallery of \d+\+? real electrical projects',
        f'<meta property="og:description" content="View our gallery of {total} real electrical projects',
        content
    )
    content = re.sub(
        r'<meta name="twitter:description" content="View our gallery of \d+\+? real electrical projects',
        f'<meta name="twitter:description" content="View our gallery of {total} real electrical projects',
        content
    )

    # 5. Replace the ItemList JSON-LD — find old ItemList object by brace matching
    new_itemlist_obj = itemlist_json(rows)
    idx = content.find('"@type":"ItemList"')
    if idx > -1:
        obj_start = content.rfind('{', 0, idx)
        depth = 1
        pos = obj_start + 1
        while depth > 0 and pos < len(content):
            if content[pos] == '{':
                depth += 1
            elif content[pos] == '}':
                depth -= 1
            pos += 1
        content = content[:obj_start] + new_itemlist_obj + content[pos:]

    GALLERY_FILE.write_text(content, encoding="utf-8")
    print(f"Updated {GALLERY_FILE}")
    print(f"  First {ITEMS_PER_PAGE} items as HTML, {len(tail)} items loaded via JS on 'Show more'")

    update_sitemap(rows)
    print(f"Done — {total} photos.")


def update_sitemap(rows):
    sitemap_content = SITEMAP_FILE.read_text(encoding="utf-8")
    prefix = "ns0:" if "<ns0:urlset" in sitemap_content else ""
    image_prefix = "ns1:" if "xmlns:ns1=" in sitemap_content else "image:"
    image_tags = "".join(
        '<%simage><%sloc>https://amyelectric.com/img/gallery/%s-1200w.webp</%sloc></%simage>\n'
        % (image_prefix, image_prefix, r["slug"], image_prefix, image_prefix)
        for r in rows
    )
    new_gallery_entry = (
        '<%surl>\n'
        '<%sloc>https://amyelectric.com/gallery</%sloc>\n'
        '<%slastmod>2026-06-19</%slastmod>\n'
        '<%spriority>0.7</%spriority>\n'
        f'{image_tags}'
        '</%surl>'
        % (prefix, prefix, prefix, prefix, prefix, prefix, prefix, prefix)
    )
    pattern = rf'<{prefix}url>\s*<{prefix}loc>https://amyelectric\.com/gallery</{prefix}loc>.*?</{prefix}url>'
    match = re.search(pattern, sitemap_content, re.DOTALL)
    if match:
        sitemap_content = sitemap_content.replace(match.group(0), new_gallery_entry)
        SITEMAP_FILE.write_text(sitemap_content, encoding="utf-8")
        print(f"Updated {SITEMAP_FILE} with {len(rows)} image entries")
    else:
        print("WARNING: gallery URL not found in sitemap.xml")


if __name__ == "__main__":
    main()
