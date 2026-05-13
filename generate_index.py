#!/usr/bin/env python3
"""Auto-generates index.html for StrategyFolio — collapsible, draggable, lockable."""

import os, urllib.parse

REPO_ROOT  = os.path.dirname(os.path.abspath(__file__))
PAGES_BASE = "https://promptlane25-stack.github.io/StrategyFolio/"
BLOB_BASE  = "https://github.com/promptlane25-stack/StrategyFolio/blob/main/"

SECTIONS = [
    {"icon": "&#128202;", "color": "c-indigo",  "title": "Analytics",                          "dir": "Analytics",                        "subsections": False},
    {"icon": "&#9881;",   "color": "c-purple",  "title": "Business Operations",                "dir": "Business Operations",              "subsections": False},
    {"icon": "&#129309;", "color": "c-green",   "title": "Projects",                            "dir": "Clients",                          "subsections": True},
    {"icon": "&#128196;", "color": "c-teal",    "title": "Deliverables \u2014 Guides & Handovers",  "dir": "Deliverables - Guides & Handovers","subsections": False},
    {"icon": "&#128176;", "color": "c-amber",   "title": "Deliverables \u2014 Proposals & Pricing", "dir": "Deliverables - Proposals & Pricing","subsections": False},
    {"icon": "&#127760;", "color": "c-blue",    "title": "Deliverables \u2014 Websites",            "dir": "Deliverables-Websites",            "subsections": False},
    {"icon": "&#128227;", "color": "c-coral",   "title": "Marketing & Outreach",               "dir": "Marketing & Outreach",             "subsections": False},
    {"icon": "&#127919;", "color": "c-teal",    "title": "Prospects & Sales",                  "dir": "Prospects & Sales",                "subsections": False},
{"icon": "&#128188;", "color": "c-orange", "title": "Projects", "dir": "Projects", "subsections": False},
]
# ── Icons ─────────────────────────────────────────────────────────────────────

CHEVRON = '<svg class="chevron" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><polyline points="6 9 12 15 18 9"/></svg>'
SMALL_CHEVRON = '<svg class="sub-chevron" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><polyline points="6 9 12 15 18 9"/></svg>'

HANDLE     = '<div class="drag-handle"     title="Drag to reorder section">\u22ee\u22ee</div>'
SUB_HANDLE = '<div class="sub-drag-handle" title="Drag to reorder client">\u22ee\u22ee</div>'
FILE_HANDLE= '<div class="file-drag-handle" title="Drag to reorder">\u22ee\u22ee</div>'

LOCK_OPEN  = '&#128275;'  # 🔓
LOCK_CLOSE = '&#128274;'  # 🔒

# ── CSS ───────────────────────────────────────────────────────────────────────

CSS = """
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f0f2f5; color: #1a1a2e; min-height: 100vh; }

/* Header */
.page-header { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 60%, #0f3460 100%); padding: 40px 24px 32px; text-align: center; color: #fff; }
.page-header h1 { font-size: 2rem; font-weight: 700; letter-spacing: -0.5px; display: inline-flex; align-items: center; gap: 12px; }
.page-header p { margin-top: 8px; font-size: 0.85rem; color: rgba(255,255,255,0.5); }
#lock-counter { color: #fbbf24; font-weight: 600; }

.container { max-width: 780px; margin: 0 auto; padding: 28px 20px 60px; }

/* ── Section cards ── */
.section-wrap { margin-bottom: 10px; border-radius: 12px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.08), 0 4px 12px rgba(0,0,0,0.04); transition: box-shadow 0.2s, opacity 0.15s; }
.section-wrap:hover { box-shadow: 0 2px 8px rgba(0,0,0,0.12), 0 6px 20px rgba(0,0,0,0.07); }
.section-wrap.dragging { opacity: 0.4; box-shadow: none; }
.section-wrap.drag-over { box-shadow: 0 0 0 2px #4f46e5, 0 6px 24px rgba(79,70,229,0.2); }

.card-inner { display: flex; align-items: stretch; }

/* Section drag handle — sits outside <details> */
.drag-handle { display: flex; align-items: center; justify-content: center; width: 30px; flex-shrink: 0; cursor: grab; color: #ccc; font-size: 1rem; letter-spacing: -1px; border-right: 1px solid rgba(0,0,0,0.06); user-select: none; transition: color 0.15s; }
.drag-handle:hover { color: #888; }
.drag-handle:active { cursor: grabbing; }

/* Section <details> */
details.section-details { flex: 1; min-width: 0; }
details.section-details > summary { display: flex; align-items: center; gap: 12px; padding: 14px 16px; cursor: pointer; list-style: none; user-select: none; transition: filter 0.15s; }
details.section-details > summary::-webkit-details-marker { display: none; }
details.section-details > summary:hover { filter: brightness(0.97); }

.section-icon { font-size: 1.2rem; width: 36px; height: 36px; display: flex; align-items: center; justify-content: center; border-radius: 8px; flex-shrink: 0; }
.section-title { font-size: 0.95rem; font-weight: 600; flex: 1; color: #1a1a2e; }
.section-count { font-size: 0.75rem; font-weight: 600; padding: 3px 10px; border-radius: 99px; flex-shrink: 0; }
.chevron { width: 16px; height: 16px; stroke: #666; stroke-width: 2.5; fill: none; flex-shrink: 0; transition: transform 0.25s; }
details[open] > summary .chevron { transform: rotate(180deg); }

/* ── File list (flat sections) ── */
.file-list { background: #fff; padding: 8px 12px 12px 12px; }

.file-row-wrap { display: flex; align-items: center; border-radius: 8px; transition: background 0.12s; }
.file-row-wrap:hover { background: #f5f7fa; }
.file-row-wrap.locked { background: #fffbeb; }
.file-row-wrap.locked:hover { background: #fef3c7; }
.file-row-wrap.dragging { opacity: 0.4; }
.file-row-wrap.drag-over { box-shadow: 0 0 0 2px #4f46e5; border-radius: 8px; }

/* File drag handle */
.file-drag-handle { display: flex; align-items: center; justify-content: center; width: 22px; flex-shrink: 0; cursor: grab; color: #ddd; font-size: 0.75rem; letter-spacing: -1px; user-select: none; opacity: 0; transition: opacity 0.15s, color 0.15s; padding: 8px 0; }
.file-row-wrap:hover .file-drag-handle { opacity: 1; }
.file-drag-handle:hover { color: #999; }
.file-drag-handle:active { cursor: grabbing; }

.file-row { display: flex; align-items: center; gap: 10px; padding: 8px 10px; flex: 1; text-decoration: none; color: #2d2d3d; font-size: 0.875rem; border-radius: 8px 0 0 8px; min-width: 0; }
.file-row:hover { color: #1a1a2e; }
.file-icon { font-size: 0.95rem; width: 24px; text-align: center; flex-shrink: 0; opacity: 0.75; }
.file-name { flex: 1; word-break: break-word; }

/* File lock button */
.lock-btn { background: none; border: none; cursor: pointer; font-size: 0.95rem; padding: 8px 10px 8px 6px; line-height: 1; opacity: 0; transition: opacity 0.15s; flex-shrink: 0; border-radius: 0 8px 8px 0; }
.file-row-wrap:hover .lock-btn { opacity: 0.5; }
.file-row-wrap.locked .lock-btn { opacity: 1; }
.lock-btn:hover { opacity: 1 !important; }

.file-row-wrap.locked .file-row { border-left: 3px solid #f59e0b; padding-left: 7px; }
.file-row-wrap.locked .file-name::after { content: ' \2014 client ready'; font-size: 0.7rem; color: #b45309; font-weight: 600; margin-left: 6px; text-transform: uppercase; letter-spacing: 0.04em; }

/* ── Subsection tiles (Clients) ── */
.sub-list { background: #fff; padding: 8px 10px 12px 10px; display: flex; flex-direction: column; gap: 6px; }

.sub-wrap { border-radius: 8px; overflow: hidden; border: 1px solid rgba(0,0,0,0.07); transition: box-shadow 0.15s, opacity 0.15s; }
.sub-wrap:hover { box-shadow: 0 1px 4px rgba(0,0,0,0.08); }
.sub-wrap.dragging { opacity: 0.4; box-shadow: none; }
.sub-wrap.drag-over { box-shadow: 0 0 0 2px #4f46e5; }

.sub-inner { display: flex; align-items: stretch; }

/* Subsection drag handle — outside <details> */
.sub-drag-handle { display: flex; align-items: center; justify-content: center; width: 22px; flex-shrink: 0; cursor: grab; color: #ccc; font-size: 0.75rem; letter-spacing: -1px; border-right: 1px solid rgba(0,0,0,0.07); user-select: none; transition: color 0.15s; }
.sub-drag-handle:hover { color: #888; }
.sub-drag-handle:active { cursor: grabbing; }

/* Subsection <details> */
details.sub-details { flex: 1; min-width: 0; background: #fafafa; }
details.sub-details > summary { display: flex; align-items: center; gap: 8px; padding: 9px 12px; cursor: pointer; list-style: none; user-select: none; font-size: 0.875rem; font-weight: 600; color: #2d2d3d; transition: background 0.12s; }
details.sub-details > summary::-webkit-details-marker { display: none; }
details.sub-details > summary:hover { background: #f0f0f5; }

.sub-title { flex: 1; }
.sub-count { font-size: 0.7rem; font-weight: 600; padding: 2px 7px; border-radius: 99px; background: rgba(0,0,0,0.06); color: #666; flex-shrink: 0; }
.sub-chevron { width: 13px; height: 13px; stroke: #888; stroke-width: 2.5; fill: none; flex-shrink: 0; transition: transform 0.25s; }
details.sub-details[open] > summary .sub-chevron { transform: rotate(180deg); }

/* Sub lock button (on summary row) */
.sub-lock-btn { background: none; border: none; cursor: pointer; font-size: 0.85rem; padding: 4px 6px; line-height: 1; opacity: 0; transition: opacity 0.15s; flex-shrink: 0; border-radius: 4px; }
details.sub-details > summary:hover .sub-lock-btn { opacity: 0.5; }
.sub-wrap.locked .sub-lock-btn { opacity: 1; }
.sub-lock-btn:hover { opacity: 1 !important; }

.sub-wrap.locked details.sub-details > summary { border-left: 3px solid #f59e0b; padding-left: 9px; background: #fffbeb; }
.sub-wrap.locked .sub-title::after { content: ' \2014 client ready'; font-size: 0.68rem; color: #b45309; font-weight: 600; margin-left: 6px; text-transform: uppercase; letter-spacing: 0.04em; }

/* Files inside a subsection */
.sub-file-list { background: #fff; padding: 6px 10px 8px 28px; border-top: 1px solid rgba(0,0,0,0.05); }
.sub-file-list .file-row-wrap { border-radius: 6px; }
.sub-file-list .file-row { font-size: 0.835rem; padding: 6px 8px; }
.sub-file-list .lock-btn { display: none; }

.empty { color: #bbb; font-size: 0.85rem; font-style: italic; padding: 8px 10px; }

/* Colour themes */
.c-indigo .card-inner { background: #eef2ff; } .c-purple .card-inner { background: #f5f3ff; }
.c-green   .card-inner { background: #f0fdf4; } .c-teal   .card-inner { background: #f0fdfa; }
.c-amber   .card-inner { background: #fffbeb; } .c-blue   .card-inner { background: #eff6ff; }
.c-coral   .card-inner { background: #fff1f2; }

.c-indigo .section-icon { background: rgba(79,70,229,0.12); }   .c-purple .section-icon { background: rgba(124,58,237,0.12); }
.c-green  .section-icon { background: rgba(22,163,74,0.12); }   .c-teal   .section-icon { background: rgba(13,148,136,0.12); }
.c-amber  .section-icon { background: rgba(217,119,6,0.12); }   .c-blue   .section-icon { background: rgba(37,99,235,0.12); }
.c-coral  .section-icon { background: rgba(225,29,72,0.12); }

.c-indigo .section-count { background: rgba(79,70,229,0.1); color: #4338ca; }  .c-purple .section-count { background: rgba(124,58,237,0.1); color: #6d28d9; }
.c-green  .section-count { background: rgba(22,163,74,0.1); color: #15803d; }  .c-teal   .section-count { background: rgba(13,148,136,0.1); color: #0f766e; }
.c-amber  .section-count { background: rgba(217,119,6,0.1); color: #b45309; }  .c-blue   .section-count { background: rgba(37,99,235,0.1); color: #1d4ed8; }
.c-coral  .section-count { background: rgba(225,29,72,0.1); color: #be123c; }

.c-indigo .file-list, .c-indigo .sub-list { border-top: 2px solid #e0e7ff; }
.c-purple .file-list, .c-purple .sub-list { border-top: 2px solid #ede9fe; }
.c-green  .file-list, .c-green  .sub-list { border-top: 2px solid #dcfce7; }
.c-teal   .file-list, .c-teal   .sub-list { border-top: 2px solid #ccfbf1; }
.c-amber  .file-list, .c-amber  .sub-list { border-top: 2px solid #fef3c7; }
.c-blue   .file-list, .c-blue   .sub-list { border-top: 2px solid #dbeafe; }
.c-coral  .file-list, .c-coral  .sub-list { border-top: 2px solid #ffe4e6; }
"""

# ── JavaScript ────────────────────────────────────────────────────────────────

JS = r"""
(function () {

/* ── Generic drag-to-reorder ───────────────────────────────────────────────
   Call initDrag(containerEl, storageKey) on any container whose direct
   children have [data-id].  A child is only draggable when the user grabs
   an element with class .drag-handle | .sub-drag-handle | .file-drag-handle.
   stopPropagation on inner containers prevents cross-level interference.
*/
function initDrag(container, storageKey) {
  var dragged = null;

  function kids() {
    return Array.from(container.querySelectorAll(':scope > [data-id]'));
  }

  function saveOrder() {
    localStorage.setItem(storageKey, JSON.stringify(kids().map(function(el){ return el.dataset.id; })));
  }

  function restoreOrder() {
    var saved = JSON.parse(localStorage.getItem(storageKey) || 'null');
    if (!saved) return;
    saved.forEach(function(id) {
      var el = container.querySelector(':scope > [data-id="' + CSS.escape(id) + '"]');
      if (el) container.appendChild(el);
    });
  }

  // All children start non-draggable; only enabled on handle grab
  kids().forEach(function(item){ item.setAttribute('draggable', 'false'); });

  container.addEventListener('mousedown', function(e) {
    var h = e.target.closest('.drag-handle, .sub-drag-handle, .file-drag-handle');
    if (!h) return;
    var item = h.closest('[data-id]');
    if (item && item.parentElement === container) {
      item.setAttribute('draggable', 'true');
    }
  });

  container.addEventListener('dragstart', function(e) {
    var item = e.target.closest(':scope > [data-id]') ||
               (e.target.dataset && e.target.dataset.id ? e.target : null);
    // Walk up to find a direct child of container
    var t = e.target;
    while (t && t.parentElement !== container) t = t.parentElement;
    if (!t) return;
    dragged = t;
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', t.dataset.id || '');
    setTimeout(function(){ t.classList.add('dragging'); }, 0);
    e.stopPropagation();
  });

  container.addEventListener('dragend', function(e) {
    if (dragged) {
      dragged.classList.remove('dragging');
      dragged.setAttribute('draggable', 'false');
      dragged = null;
    }
    kids().forEach(function(el){ el.classList.remove('drag-over'); });
    saveOrder();
    e.stopPropagation();
  });

  container.addEventListener('dragover', function(e) {
    e.preventDefault();
    e.stopPropagation();
    if (!dragged) return;
    // Find which direct child we are over
    var t = e.target;
    while (t && t.parentElement !== container) t = t.parentElement;
    if (!t || t === dragged) return;
    kids().forEach(function(el){ el.classList.remove('drag-over'); });
    t.classList.add('drag-over');
    var rect = t.getBoundingClientRect();
    container.insertBefore(dragged, e.clientY < rect.top + rect.height / 2 ? t : t.nextSibling);
  });

  container.addEventListener('dragleave', function(e) {
    e.stopPropagation();
    var t = e.target;
    while (t && t.parentElement !== container) t = t.parentElement;
    if (t) t.classList.remove('drag-over');
  });

  container.addEventListener('drop', function(e) {
    e.preventDefault();
    e.stopPropagation();
    kids().forEach(function(el){ el.classList.remove('drag-over'); });
    saveOrder();
  });

  restoreOrder();
}

/* ── Locks ─────────────────────────────────────────────────────────────── */

var LOCK_KEY = 'sf-locks';

function getLocks() { return new Set(JSON.parse(localStorage.getItem(LOCK_KEY) || '[]')); }
function saveLocks(set) { localStorage.setItem(LOCK_KEY, JSON.stringify(Array.from(set))); updateCounter(set.size); }

function updateCounter(n) {
  var el = document.getElementById('lock-counter');
  if (el) el.textContent = n > 0 ? ' \u00b7 ' + n + ' locked' : '';
}

// Called from individual file-row lock buttons
window.toggleLock = function(btn) {
  var wrap = btn.closest('.file-row-wrap');
  var id   = wrap.dataset.id;
  var locks = getLocks();
  var link  = wrap.querySelector('.file-row');
  if (locks.has(id)) {
    locks.delete(id); wrap.classList.remove('locked');
    link.href = wrap.dataset.blobUrl;
    btn.textContent = '\u{1F513}'; btn.title = 'Mark as client-ready';
  } else {
    locks.add(id); wrap.classList.add('locked');
    link.href = wrap.dataset.viewUrl;
    btn.textContent = '\u{1F512}'; btn.title = 'Locked \u2014 click to unlock';
  }
  saveLocks(locks);
};

// Called from subsection (client tile) lock buttons
window.toggleSubLock = function(btn, event) {
  event.stopPropagation(); // Don't toggle <details>
  var wrap = btn.closest('.sub-wrap');
  var id   = wrap.dataset.id;
  var locks = getLocks();
  if (locks.has(id)) {
    locks.delete(id); wrap.classList.remove('locked');
    btn.textContent = '\u{1F513}'; btn.title = 'Mark client as ready';
  } else {
    locks.add(id); wrap.classList.add('locked');
    btn.textContent = '\u{1F512}'; btn.title = 'Locked \u2014 click to unlock';
  }
  saveLocks(locks);
};

function restoreLocks() {
  var locks = getLocks();
  locks.forEach(function(id) {
    // Try file-row-wrap first
    var wrap = document.querySelector('.file-row-wrap[data-id="' + CSS.escape(id) + '"]');
    if (wrap) {
      wrap.classList.add('locked');
      var link = wrap.querySelector('.file-row');
      if (link) link.href = wrap.dataset.viewUrl;
      var btn = wrap.querySelector('.lock-btn');
      if (btn) { btn.textContent = '\u{1F512}'; btn.title = 'Locked \u2014 click to unlock'; }
      return;
    }
    // Try sub-wrap
    var subWrap = document.querySelector('.sub-wrap[data-id="' + CSS.escape(id) + '"]');
    if (subWrap) {
      subWrap.classList.add('locked');
      var sbtn = subWrap.querySelector('.sub-lock-btn');
      if (sbtn) { sbtn.textContent = '\u{1F512}'; sbtn.title = 'Locked \u2014 click to unlock'; }
    }
  });
  updateCounter(locks.size);
}

/* ── Boot drag on all containers ─────────────────────────────────────────── */

var sectionsContainer = document.getElementById('sections-container');
if (sectionsContainer) initDrag(sectionsContainer, 'sf-order-sections');

document.querySelectorAll('.sub-list[data-drag]').forEach(function(el) {
  initDrag(el, 'sf-' + el.dataset.drag);
});

document.querySelectorAll('.file-list[data-drag]').forEach(function(el) {
  initDrag(el, 'sf-' + el.dataset.drag);
});

restoreLocks();

})();
"""

# ── Helpers ───────────────────────────────────────────────────────────────────

def file_icon(name):
    ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
    icons = {
        "pdf": "&#128196;", "xlsx": "&#128202;", "xls": "&#128202;",
        "docx": "&#128196;", "doc": "&#128196;", "pptx": "&#127916;",
        "png": "&#128444;", "jpg": "&#128444;", "jpeg": "&#128444;",
        "html": "&#127760;", "md": "&#128196;", "csv": "&#128202;",
    }
    return icons.get(ext, "&#128196;")


def list_files(rel_dir):
    full = os.path.join(REPO_ROOT, rel_dir)
    if not os.path.isdir(full):
        return []
    return sorted(
        [f for f in os.listdir(full) if not f.startswith(".") and os.path.isfile(os.path.join(full, f))],
        key=str.lower,
    )


def list_subdirs(rel_dir):
    full = os.path.join(REPO_ROOT, rel_dir)
    if not os.path.isdir(full):
        return []
    return sorted(
        [d for d in os.listdir(full) if not d.startswith(".") and os.path.isdir(os.path.join(full, d))],
        key=str.lower,
    )


def safe_drag_id(path):
    """URL-encode a path then turn % signs into - so it's a valid data-drag value."""
    return urllib.parse.quote(path, safe="").replace("%", "-")


def file_link(rel_dir, filename, draggable=False):
    rel_path = rel_dir + "/" + filename
    blob_url = BLOB_BASE + urllib.parse.quote(rel_path, safe="/")
    ext      = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    view_url = PAGES_BASE + urllib.parse.quote(rel_path, safe="/") if ext == "html" else blob_url
    icon     = file_icon(filename)
    safe_id  = rel_path.replace('"', '&quot;')
    handle   = FILE_HANDLE if draggable else ""
    return (
        f'<div class="file-row-wrap" data-id="{safe_id}" '
        f'data-view-url="{view_url}" data-blob-url="{blob_url}">'
        f'{handle}'
        f'<a class="file-row" href="{view_url}" target="_blank">'
        f'<span class="file-icon">{icon}</span>'
        f'<span class="file-name">{filename}</span></a>'
        f'<button class="lock-btn" onclick="toggleLock(this)" title="Mark as client-ready">{LOCK_OPEN}</button>'
        f'</div>'
    )


def render_subsection(parent_rel, sub_name):
    """Render one client folder as a collapsible, draggable tile."""
    rel      = parent_rel + "/" + sub_name
    files    = list_files(rel)
    count    = len(files)
    sub_id   = safe_drag_id(rel)

    if files:
        rows = "\n".join(
            f'<div class="file-row-wrap" data-id="{(rel+"/"+f).replace(chr(34), "&quot;")}"'
            f' data-view-url="{PAGES_BASE + urllib.parse.quote(rel+"/"+f, safe="/") if f.lower().endswith(".html") else BLOB_BASE + urllib.parse.quote(rel+"/"+f, safe="/")}"'
            f' data-blob-url="{BLOB_BASE + urllib.parse.quote(rel+"/"+f, safe="/")}">'
            f'<a class="file-row" href="'
            f'{ PAGES_BASE + urllib.parse.quote(rel+"/"+f, safe="/") if f.lower().endswith(".html") else BLOB_BASE + urllib.parse.quote(rel+"/"+f, safe="/") }'
            f'" target="_blank">'
            f'<span class="file-icon">{file_icon(f)}</span>'
            f'<span class="file-name">{f}</span></a>'
            f'</div>'
            for f in files
        )
    else:
        rows = '<div class="empty">No files</div>'

    return f"""<div class="sub-wrap" data-id="{sub_id}">
  <div class="sub-inner">
    {SUB_HANDLE}
    <details class="sub-details">
      <summary>
        <span class="sub-title">{sub_name}</span>
        <span class="sub-count">{count} file{'s' if count != 1 else ''}</span>
        <button class="sub-lock-btn" onclick="toggleSubLock(this, event)" title="Mark client as ready">{LOCK_OPEN}</button>
        {SMALL_CHEVRON}
      </summary>
      <div class="sub-file-list">
{rows}
      </div>
    </details>
  </div>
</div>"""


def render_section(s):
    rel, color, title, icon = s["dir"], s["color"], s["title"], s["icon"]
    safe_id = safe_drag_id(rel)

    if s["subsections"]:
        # Top-level files in the section directory (if any)
        top_files = list_files(rel)
        top_rows  = "".join(file_link(rel, f, draggable=False) for f in top_files)

        # Client subdirectory tiles
        subdirs = list_subdirs(rel)
        sub_drag_key = safe_drag_id("subs-" + rel)
        sub_tiles = "\n".join(render_subsection(rel, d) for d in subdirs)
        if not sub_tiles:
            sub_tiles = '<div class="empty">No client folders found</div>'

        # Total count = top files + all files inside subdirs
        total = len(top_files) + sum(len(list_files(rel + "/" + d)) for d in subdirs)
        count_label = f"{total} file{'s' if total != 1 else ''}"

        inner = f"""{top_rows}
<div class="sub-list" data-drag="{sub_drag_key}">
{sub_tiles}
</div>"""

    else:
        files = list_files(rel)
        file_drag_key = safe_drag_id("files-" + rel)
        total = len(files)
        count_label = f"{total} file{'s' if total != 1 else ''}"
        rows  = "\n".join(file_link(rel, f, draggable=True) for f in files)
        if not rows:
            rows = '<div class="empty">No files found</div>'
        inner = f'<div class="file-list" data-drag="{file_drag_key}">\n{rows}\n</div>'

    return f"""<div class="section-wrap {color}" data-id="{safe_id}">
  <div class="card-inner">
    {HANDLE}
    <details class="section-details">
      <summary>
        <span class="section-icon">{icon}</span>
        <span class="section-title">{title}</span>
        <span class="section-count">{count_label}</span>
        {CHEVRON}
      </summary>
      {inner}
    </details>
  </div>
</div>"""


# ── Generate ──────────────────────────────────────────────────────────────────

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
    print(f"Written {out} ({len(html):,} chars)")


if __name__ == "__main__":
    generate()
