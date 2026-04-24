#!/usr/bin/env python3
"""Auto-generates index.html for StrategyFolio with collapsible, draggable sections."""
import os, urllib.parse

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))

SECTIONS = [
    {"icon": "&#128202;", "color": "c-indigo", "title": "Analytics",                                    "dir": "Analytics",                          "subsections": False},
    {"icon": "&#9881;",   "color": "c-purple", "title": "Business Operations",                          "dir": "Business Operations",                "subsections": False},
    {"icon": "&#129309;", "color": "c-green",  "title": "Clients",                                      "dir": "Clients",                            "subsections": True},
    {"icon": "&#128196;", "color": "c-teal",   "title": "Deliverables \u2014 Guides &amp; Handovers",  "dir": "Deliverables - Guides & Handovers",  "subsections": False},
    {"icon": "&#128176;", "color": "c-amber",  "title": "Deliverables \u2014 Proposals &amp; Pricing", "dir": "Deliverables - Proposals & Pricing", "subsections": False},
    {"icon": "&#127760;", "color": "c-blue",   "title": "Deliverables \u2014 Websites",                "dir": "Deliverables-Websites",              "subsections": False},
    {"icon": "&#128227;", "color": "c-coral",  "title": "Marketing &amp; Outreach",                     "dir": "Marketing & Outreach",               "subsections": False},
    {"icon": "&#127919;", "color": "c-teal",   "title": "Prospects &amp; Sales",                        "dir": "Prospects & Sales",                  "subsections": False},
]

CSS = """
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #f0f2f5;
    color: #1a1a2e;
    min-height: 100vh;
  }
  .page-header {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 60%, #0f3460 100%);
    padding: 40px 24px 36px;
    text-align: center;
    color: #fff;
  }
  .page-header h1 { font-size: 2rem; font-weight: 700; letter-spacing: -0.5px; display: inline-flex; align-items: center; gap: 12px; }
  .page-header p { margin-top: 8px; font-size: 0.9rem; color: rgba(255,255,255,0.5); }
  .container { max-width: 780px; margin: 0 auto; padding: 32px 20px 60px; }

  /* Card */
  .section-wrap {
    margin-bottom: 10px;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08), 0 4px 12px rgba(0,0,0,0.04);
    transition: box-shadow 0.2s, transform 0.15s, opacity 0.15s;
  }
  .section-wrap:hover { box-shadow: 0 2px 8px rgba(0,0,0,0.12), 0 6px 20px rgba(0,0,0,0.07); }
  .section-wrap.dragging { opacity: 0.4; transform: scale(0.98); box-shadow: none; }
  .section-wrap.drag-over { box-shadow: 0 0 0 2px #4f46e5, 0 6px 24px rgba(79,70,229,0.2); }

  /* card-inner: handle + details side by side */
  .card-inner { display: flex; align-items: stretch; border-radius: 12px; overflow: hidden; }

  /* Drag handle sits OUTSIDE <details> so summary doesn't swallow it */
  .drag-handle {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    flex-shrink: 0;
    cursor: grab;
    color: #bbb;
    font-size: 1rem;
    letter-spacing: -1px;
    transition: color 0.15s, background 0.15s;
    border-right: 1px solid rgba(0,0,0,0.06);
    user-select: none;
  }
  .drag-handle:hover { color: #777; }
  .drag-handle:active { cursor: grabbing; }

  details { flex: 1; min-width: 0; }

  summary {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 14px 16px;
    cursor: pointer;
    list-style: none;
    user-select: none;
    transition: filter 0.15s;
  }
  summary::-webkit-details-marker { display: none; }
  summary:hover { filter: brightness(0.97); }

  .section-icon {
    font-size: 1.2rem; width: 36px; height: 36px;
    display: flex; align-items: center; justify-content: center;
    border-radius: 8px; flex-shrink: 0;
  }
  .section-title { font-size: 0.95rem; font-weight: 600; flex: 1; color: #1a1a2e; }
  .section-count { font-size: 0.75rem; font-weight: 600; padding: 3px 10px; border-radius: 99px; flex-shrink: 0; }
  .chevron { width: 16px; height: 16px; stroke: #666; stroke-width: 2.5; fill: none; flex-shrink: 0; transition: transform 0.25s; }
  details[open] .chevron { transform: rotate(180deg); }

  .file-list { background: #fff; padding: 8px 12px 12px 40px; }
  .file-row {
    display: flex; align-items: center; gap: 10px;
    padding: 8px 10px; border-radius: 8px;
    text-decoration: none; color: #2d2d3d; font-size: 0.875rem;
    transition: background 0.12s;
  }
  .file-row:hover { background: #f5f7fa; color: #1a1a2e; }
  .file-icon { font-size: 0.95rem; width: 24px; text-align: center; flex-shrink: 0; opacity: 0.75; }
  .file-name { flex: 1; word-break: break-word; }
  .sub-label { font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.07em; color: #999; padding: 10px 10px 4px 10px; }
  .empty { color: #bbb; font-size: 0.85rem; font-style: italic; padding: 8px 10px; }

  /* Colour themes — applied to .card-inner so handle inherits bg */
  .c-indigo .card-inner { background: #eef2ff; }
  .c-purple .card-inner { background: #f5f3ff; }
  .c-green  .card-inner { background: #f0fdf4; }
  .c-teal   .card-inner { background: #f0fdfa; }
  .c-amber  .card-inner { background: #fffbeb; }
  .c-blue   .card-inner { background: #eff6ff; }
  .c-coral  .card-inner { background: #fff1f2; }

  .c-indigo .section-icon { background: rgba(79,70,229,0.12); }
  .c-purple .section-icon { background: rgba(124,58,237,0.12); }
  .c-green  .section-icon { background: rgba(22,163,74,0.12); }
  .c-teal   .section-icon { background: rgba(13,148,136,0.12); }
  .c-amber  .section-icon { background: rgba(217,119,6,0.12); }
  .c-blue   .section-icon { background: rgba(37,99,235,0.12); }
  .c-coral  .section-icon { background: rgba(225,29,72,0.12); }

  .c-indigo .section-count { background: rgba(79,70,229,0.1); color: #4338ca; }
  .c-purple .section-count { background: rgba(124,58,237,0.1); color: #6d28d9; }
  .c-green  .section-count { background: rgba(22,163,74,0.1); color: #15803d; }
  .c-teal   .section-count { background: rgba(13,148,136,0.1); color: #0f766e; }
  .c-amber  .section-count { background: rgba(217,119,6,0.1); color: #b45309; }
  .c-blue   .section-count { background: rgba(37,99,235,0.1); color: #1d4ed8; }
  .c-coral  .section-count { background: rgba(225,29,72,0.1); color: #be123c; }

  .c-indigo .file-list { border-top: 2px solid #e0e7ff; }
  .c-purple .file-list { border-top: 2px solid #ede9fe; }
  .c-green  .file-list { border-top: 2px solid #dcfce7; }
  .c-teal   .file-list { border-top: 2px solid #ccfbf1; }
  .c-amber  .file-list { border-top: 2px solid #fef3c7; }
  .c-blue   .file-list { border-top: 2px solid #dbeafe; }
  .c-coral  .file-list { border-top: 2px solid #ffe4e6; }
"""

JS = """
(function () {
  var STORE_KEY = 'sf-order';
  var container = document.getElementById('sections-container');
  var dragged = null;

  function saveOrder() {
    var ids = Array.from(container.querySelectorAll('.section-wrap')).map(function(el){ return el.dataset.id; });
    localStorage.setItem(STORE_KEY, JSON.stringify(ids));
  }

  function restoreOrder() {
    var saved = JSON.parse(localStorage.getItem(STORE_KEY) || 'null');
    if (!saved || !Array.isArray(saved)) return;
    saved.forEach(function(id) {
      var el = container.querySelector('[data-id="' + id + '"]');
      if (el) container.appendChild(el);
    });
  }

  // Attach drag events directly to each handle
  container.querySelectorAll('.drag-handle').forEach(function(handle) {
    handle.addEventListener('mousedown', function(e) {
      // Enable draggable only when handle is pressed
      var wrap = handle.closest('.section-wrap');
      if (wrap) wrap.setAttribute('draggable', 'true');
    });
  });

  container.addEventListener('dragstart', function(e) {
    var wrap = e.target.closest('.section-wrap');
    if (!wrap) return;
    dragged = wrap;
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', wrap.dataset.id);
    setTimeout(function() { wrap.classList.add('dragging'); }, 0);
  });

  container.addEventListener('dragend', function(e) {
    if (dragged) {
      dragged.classList.remove('dragging');
      dragged.setAttribute('draggable', 'false');
      dragged = null;
    }
    container.querySelectorAll('.drag-over').forEach(function(el){ el.classList.remove('drag-over'); });
    saveOrder();
  });

  container.addEventListener('dragover', function(e) {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    var target = e.target.closest('.section-wrap');
    if (!target || target === dragged) return;
    container.querySelectorAll('.drag-over').forEach(function(el){ el.classList.remove('drag-over'); });
    target.classList.add('drag-over');
    var rect = target.getBoundingClientRect();
    if (e.clientY < rect.top + rect.height / 2) {
      container.insertBefore(dragged, target);
    } else {
      container.insertBefore(dragged, target.nextSibling);
    }
  });

  container.addEventListener('dragleave', function(e) {
    var target = e.target.closest('.section-wrap');
    if (target) target.classList.remove('drag-over');
  });

  container.addEventListener('drop', function(e) {
    e.preventDefault();
    container.querySelectorAll('.drag-over').forEach(function(el){ el.classList.remove('drag-over'); });
    saveOrder();
  });

  // Initially not draggable — only becomes draggable on handle mousedown
  container.querySelectorAll('.section-wrap').forEach(function(wrap) {
    wrap.setAttribute('draggable', 'false');
  });

  restoreOrder();
})();
"""

CHEVRON = '<svg class="chevron" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><polyline points="6 9 12 15 18 9"/></svg>'
HANDLE  = '<div class="drag-handle" title="Drag to reorder">&#8942;&#8942;</div>'
BASE_URL = "https://github.com/promptlane25-stack/StrategyFolio/blob/main/"

def file_icon(name):
    ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
    icons = {"pdf": "&#128196;", "xlsx": "&#128202;", "xls": "&#128202;",
             "docx": "&#128196;", "doc": "&#128196;", "pptx": "&#127916;",
             "png": "&#128444;", "jpg": "&#128444;", "jpeg": "&#128444;",
             "html": "&#127760;", "md": "&#128196;", "csv": "&#128202;"}
    return icons.get(ext, "&#128196;")

def list_files(rel_dir):
    full = os.path.join(REPO_ROOT, rel_dir)
    if not os.path.isdir(full): return []
    return sorted([f for f in os.listdir(full) if not f.startswith(".") and os.path.isfile(os.path.join(full, f))], key=str.lower)

def list_subdirs(rel_dir):
    full = os.path.join(REPO_ROOT, rel_dir)
    if not os.path.isdir(full): return []
    return sorted([d for d in os.listdir(full) if not d.startswith(".") and os.path.isdir(os.path.join(full, d))], key=str.lower)

def file_link(rel_dir, filename):
    path = BASE_URL + urllib.parse.quote(rel_dir + "/" + filename, safe="/")
    return (f'<a class="file-row" href="{path}" target="_blank">'
            f'<span class="file-icon">{file_icon(filename)}</span>'
            f'<span class="file-name">{filename}</span></a>')

def render_section(s):
    rel, color, title, icon = s["dir"], s["color"], s["title"], s["icon"]
    rows = []
    if s["subsections"]:
        for f in list_files(rel): rows.append(file_link(rel, f))
        for sub in list_subdirs(rel):
            rows.append(f'<div class="sub-label">{sub}</div>')
            subs = list_files(rel + "/" + sub)
            rows += [file_link(rel + "/" + sub, f) for f in subs] or ['<div class="empty">No files</div>']
    else:
        for f in list_files(rel): rows.append(file_link(rel, f))
    count = sum(1 for r in rows if "file-row" in r)
    if not rows: rows.append('<div class="empty">No files found</div>')
    inner = "\n".join(rows)
    safe_id = rel.replace(" ", "-").replace("&", "and")
    return f"""<div class="section-wrap {color}" data-id="{safe_id}">
  <div class="card-inner">
    {HANDLE}
    <details>
      <summary>
        <span class="section-icon">{icon}</span>
        <span class="section-title">{title}</span>
        <span class="section-count">{count} files</span>
        {CHEVRON}
      </summary>
      <div class="file-list">
{inner}
      </div>
    </details>
  </div>
</div>"""

def generate():
    sections_html = "\n".join(render_section(s) for s in SECTIONS)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>StrategyFolio</title>
  <style>{CSS}</style>
</head>
<body>
  <header class="page-header">
    <h1>&#128196; StrategyFolio</h1>
    <p>Drag &#8942;&#8942; to reorder &nbsp;&middot;&nbsp; Click to expand</p>
  </header>
  <div class="container">
    <div id="sections-container">
{sections_html}
    </div>
  </div>
  <script>{JS}</script>
</body>
</html>"""
    out = os.path.join(REPO_ROOT, "index.html")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"Written {out}")

if __name__ == "__main__":
    generate()
