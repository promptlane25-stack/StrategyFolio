#!/usr/bin/env python3
"""Auto-generates index.html for StrategyFolio — collapsible, draggable, lockable."""
import os, urllib.parse

REPO_ROOT  = os.path.dirname(os.path.abspath(__file__))
PAGES_BASE = "https://promptlane25-stack.github.io/StrategyFolio/"
BLOB_BASE  = "https://github.com/promptlane25-stack/StrategyFolio/blob/main/"

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
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f0f2f5; color: #1a1a2e; min-height: 100vh; }

  .page-header { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 60%, #0f3460 100%); padding: 40px 24px 32px; text-align: center; color: #fff; }
  .page-header h1 { font-size: 2rem; font-weight: 700; letter-spacing: -0.5px; display: inline-flex; align-items: center; gap: 12px; }
  .page-header p { margin-top: 8px; font-size: 0.85rem; color: rgba(255,255,255,0.5); }
  #lock-counter { color: #fbbf24; font-weight: 600; }

  .container { max-width: 780px; margin: 0 auto; padding: 28px 20px 60px; }

  /* ── Section cards ── */
  .section-wrap { margin-bottom: 10px; border-radius: 12px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.08), 0 4px 12px rgba(0,0,0,0.04); transition: box-shadow 0.2s, transform 0.15s, opacity 0.15s; }
  .section-wrap:hover { box-shadow: 0 2px 8px rgba(0,0,0,0.12), 0 6px 20px rgba(0,0,0,0.07); }
  .section-wrap.dragging { opacity: 0.4; transform: scale(0.98); box-shadow: none; }
  .section-wrap.drag-over { box-shadow: 0 0 0 2px #4f46e5, 0 6px 24px rgba(79,70,229,0.2); }
  .card-inner { display: flex; align-items: stretch; border-radius: 12px; overflow: hidden; }

  /* Drag handle — outside <details> so summary doesn't block dragstart */
  .drag-handle { display: flex; align-items: center; justify-content: center; width: 30px; flex-shrink: 0; cursor: grab; color: #ccc; font-size: 1rem; letter-spacing: -1px; border-right: 1px solid rgba(0,0,0,0.06); user-select: none; transition: color 0.15s; }
  .drag-handle:hover { color: #888; }
  .drag-handle:active { cursor: grabbing; }

  details { flex: 1; min-width: 0; }
  summary { display: flex; align-items: center; gap: 12px; padding: 14px 16px; cursor: pointer; list-style: none; user-select: none; transition: filter 0.15s; }
  summary::-webkit-details-marker { display: none; }
  summary:hover { filter: brightness(0.97); }
  .section-icon { font-size: 1.2rem; width: 36px; height: 36px; display: flex; align-items: center; justify-content: center; border-radius: 8px; flex-shrink: 0; }
  .section-title { font-size: 0.95rem; font-weight: 600; flex: 1; color: #1a1a2e; }
  .section-count { font-size: 0.75rem; font-weight: 600; padding: 3px 10px; border-radius: 99px; flex-shrink: 0; }
  .chevron { width: 16px; height: 16px; stroke: #666; stroke-width: 2.5; fill: none; flex-shrink: 0; transition: transform 0.25s; }
  details[open] .chevron { transform: rotate(180deg); }

  /* ── File list ── */
  .file-list { background: #fff; padding: 8px 12px 12px 12px; }

  /* file-row-wrap: link + lock button side by side */
  .file-row-wrap { display: flex; align-items: center; border-radius: 8px; transition: background 0.12s; }
  .file-row-wrap:hover { background: #f5f7fa; }
  .file-row-wrap.locked { background: #fffbeb; }
  .file-row-wrap.locked:hover { background: #fef3c7; }

  .file-row { display: flex; align-items: center; gap: 10px; padding: 8px 10px; flex: 1; text-decoration: none; color: #2d2d3d; font-size: 0.875rem; border-radius: 8px 0 0 8px; min-width: 0; }
  .file-row:hover { color: #1a1a2e; }
  .file-icon { font-size: 0.95rem; width: 24px; text-align: center; flex-shrink: 0; opacity: 0.75; }
  .file-name { flex: 1; word-break: break-word; }

  /* Lock button */
  .lock-btn { background: none; border: none; cursor: pointer; font-size: 0.95rem; padding: 8px 10px 8px 6px; line-height: 1; opacity: 0; transition: opacity 0.15s; flex-shrink: 0; border-radius: 0 8px 8px 0; }
  .file-row-wrap:hover .lock-btn { opacity: 0.5; }
  .file-row-wrap.locked .lock-btn { opacity: 1; }
  .lock-btn:hover { opacity: 1 !important; }

  /* Locked file: amber left accent + badge */
  .file-row-wrap.locked .file-row { border-left: 3px solid #f59e0b; padding-left: 7px; }
  .file-row-wrap.locked .file-name::after { content: ' \2014 client ready'; font-size: 0.7rem; color: #b45309; font-weight: 600; margin-left: 6px; text-transform: uppercase; letter-spacing: 0.04em; }

  .sub-label { font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.07em; color: #999; padding: 10px 10px 4px 10px; }
  .empty { color: #bbb; font-size: 0.85rem; font-style: italic; padding: 8px 10px; }

  /* Colour themes */
  .c-indigo .card-inner { background: #eef2ff; } .c-purple .card-inner { background: #f5f3ff; }
  .c-green  .card-inner { background: #f0fdf4; } .c-teal   .card-inner { background: #f0fdfa; }
  .c-amber  .card-inner { background: #fffbeb; } .c-blue   .card-inner { background: #eff6ff; }
  .c-coral  .card-inner { background: #fff1f2; }

  .c-indigo .section-icon { background: rgba(79,70,229,0.12); }   .c-purple .section-icon { background: rgba(124,58,237,0.12); }
  .c-green  .section-icon { background: rgba(22,163,74,0.12); }   .c-teal   .section-icon { background: rgba(13,148,136,0.12); }
  .c-amber  .section-icon { background: rgba(217,119,6,0.12); }   .c-blue   .section-icon { background: rgba(37,99,235,0.12); }
  .c-coral  .section-icon { background: rgba(225,29,72,0.12); }

  .c-indigo .section-count { background: rgba(79,70,229,0.1); color: #4338ca; }   .c-purple .section-count { background: rgba(124,58,237,0.1); color: #6d28d9; }
  .c-green  .section-count { background: rgba(22,163,74,0.1); color: #15803d; }   .c-teal   .section-count { background: rgba(13,148,136,0.1); color: #0f766e; }
  .c-amber  .section-count { background: rgba(217,119,6,0.1); color: #b45309; }   .c-blue   .section-count { background: rgba(37,99,235,0.1); color: #1d4ed8; }
  .c-coral  .section-count { background: rgba(225,29,72,0.1); color: #be123c; }

  .c-indigo .file-list { border-top: 2px solid #e0e7ff; } .c-purple .file-list { border-top: 2px solid #ede9fe; }
  .c-green  .file-list { border-top: 2px solid #dcfce7; } .c-teal   .file-list { border-top: 2px solid #ccfbf1; }
  .c-amber  .file-list { border-top: 2px solid #fef3c7; } .c-blue   .file-list { border-top: 2px solid #dbeafe; }
  .c-coral  .file-list { border-top: 2px solid #ffe4e6; }
"""

JS = """
(function () {
  var ORDER_KEY = 'sf-order';
  var LOCK_KEY  = 'sf-locks';
  var container = document.getElementById('sections-container');
  var dragged   = null;

  /* ── Locks ── */
  function getLocks()      { return new Set(JSON.parse(localStorage.getItem(LOCK_KEY) || '[]')); }
  function saveLocks(set)  { localStorage.setItem(LOCK_KEY, JSON.stringify(Array.from(set))); updateCounter(set.size); }
  function updateCounter(n) {
    var el = document.getElementById('lock-counter');
    if (el) el.textContent = n > 0 ? ' \u00b7 ' + n + ' locked' : '';
  }

  window.toggleLock = function(btn) {
    var wrap   = btn.closest('.file-row-wrap');
    var id     = wrap.dataset.id;
    var locks  = getLocks();
    var link   = wrap.querySelector('.file-row');
    if (locks.has(id)) {
      locks.delete(id);
      wrap.classList.remove('locked');
      link.href = wrap.dataset.blobUrl;
      btn.textContent = '\ud83d\udd13';
      btn.title = 'Mark as client-ready';
    } else {
      locks.add(id);
      wrap.classList.add('locked');
      link.href = wrap.dataset.viewUrl;
      btn.textContent = '\ud83d\udd12';
      btn.title = 'Locked — click to unlock';
    }
    saveLocks(locks);
  };

  function restoreLocks() {
    var locks = getLocks();
    locks.forEach(function (id) {
      var wrap = container.querySelector('.file-row-wrap[data-id="' + CSS.escape(id) + '"]');
      if (!wrap) return;
      wrap.classList.add('locked');
      wrap.querySelector('.file-row').href = wrap.dataset.viewUrl;
      var btn = wrap.querySelector('.lock-btn');
      if (btn) { btn.textContent = '\ud83d\udd12'; btn.title = 'Locked — click to unlock'; }
    });
    updateCounter(locks.size);
  }

  /* ── Drag to reorder ── */
  container.querySelectorAll('.drag-handle').forEach(function (h) {
    h.addEventListener('mousedown', function () {
      h.closest('.section-wrap').setAttribute('draggable', 'true');
    });
  });

  container.addEventListener('dragstart', function (e) {
    var wrap = e.target.closest('.section-wrap');
    if (!wrap) return;
    dragged = wrap;
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', wrap.dataset.id);
    setTimeout(function () { wrap.classList.add('dragging'); }, 0);
  });

  container.addEventListener('dragend', function () {
    if (dragged) { dragged.classList.remove('dragging'); dragged.setAttribute('draggable', 'false'); dragged = null; }
    container.querySelectorAll('.drag-over').forEach(function (el) { el.classList.remove('drag-over'); });
    saveOrder();
  });

  container.addEventListener('dragover', function (e) {
    e.preventDefault();
    var target = e.target.closest('.section-wrap');
    if (!target || target === dragged) return;
    container.querySelectorAll('.drag-over').forEach(function (el) { el.classList.remove('drag-over'); });
    target.classList.add('drag-over');
    var rect = target.getBoundingClientRect();
    container.insertBefore(dragged, e.clientY < rect.top + rect.height / 2 ? target : target.nextSibling);
  });

  container.addEventListener('dragleave', function (e) {
    var t = e.target.closest('.section-wrap');
    if (t) t.classList.remove('drag-over');
  });

  container.addEventListener('drop', function (e) {
    e.preventDefault();
    container.querySelectorAll('.drag-over').forEach(function (el) { el.classList.remove('drag-over'); });
    saveOrder();
  });

  container.querySelectorAll('.section-wrap').forEach(function (w) { w.setAttribute('draggable', 'false'); });

  function saveOrder() {
    var ids = Array.from(container.querySelectorAll('.section-wrap')).map(function (el) { return el.dataset.id; });
    localStorage.setItem(ORDER_KEY, JSON.stringify(ids));
  }

  function restoreOrder() {
    var saved = JSON.parse(localStorage.getItem(ORDER_KEY) || 'null');
    if (!saved) return;
    saved.forEach(function (id) {
      var el = container.querySelector('.section-wrap[data-id="' + id + '"]');
      if (el) container.appendChild(el);
    });
  }

  restoreOrder();
  restoreLocks();
})();
"""

CHEVRON  = '<svg class="chevron" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><polyline points="6 9 12 15 18 9"/></svg>'
HANDLE   = '<div class="drag-handle" title="Drag to reorder">&#8942;&#8942;</div>'
LOCK_OPEN = '&#128275;'  # unlocked padlock

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
    rel_path  = rel_dir + "/" + filename
    blob_url  = BLOB_BASE  + urllib.parse.quote(rel_path, safe="/")
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    # HTML files open as rendered pages; everything else opens the GitHub blob viewer
    view_url  = PAGES_BASE + urllib.parse.quote(rel_path, safe="/") if ext == "html" else blob_url
    icon      = file_icon(filename)
    safe_id   = rel_path.replace('"', '&quot;')
    return (
        f'<div class="file-row-wrap" data-id="{safe_id}" data-view-url="{view_url}" data-blob-url="{blob_url}">'
        f'<a class="file-row" href="{view_url}" target="_blank">'
        f'<span class="file-icon">{icon}</span><span class="file-name">{filename}</span></a>'
        f'<button class="lock-btn" onclick="toggleLock(this)" title="Mark as client-ready">{LOCK_OPEN}</button>'
        f'</div>'
    )

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
    count  = sum(1 for r in rows if "file-row" in r)
    if not rows: rows.append('<div class="empty">No files found</div>')
    inner  = "\n".join(rows)
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
    <p>Drag &#8942;&#8942; to reorder &nbsp;&middot;&nbsp; Click to expand &nbsp;&middot;&nbsp; &#128275; to lock client files<span id="lock-counter"></span></p>
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
