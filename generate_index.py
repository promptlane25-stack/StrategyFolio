#!/usr/bin/env python3
"""Auto-generates index.html for StrategyFolio with collapsible sections."""
import os, urllib.parse

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))

SECTIONS = [
    {"icon": "&#128202;", "color": "c-indigo", "title": "Analytics",                              "dir": "Analytics",                          "subsections": False},
    {"icon": "&#9881;",   "color": "c-purple", "title": "Business Operations",                    "dir": "Business Operations",                "subsections": False},
    {"icon": "&#129309;", "color": "c-green",  "title": "Clients",                                "dir": "Clients",                            "subsections": True},
    {"icon": "&#128196;", "color": "c-teal",   "title": "Deliverables \u2014 Guides &amp; Handovers", "dir": "Deliverables - Guides & Handovers",  "subsections": False},
    {"icon": "&#128176;", "color": "c-amber",  "title": "Deliverables \u2014 Proposals &amp; Pricing","dir": "Deliverables - Proposals & Pricing", "subsections": False},
    {"icon": "&#127760;", "color": "c-blue",   "title": "Deliverables \u2014 Websites",              "dir": "Deliverables-Websites",              "subsections": False},
    {"icon": "&#128227;", "color": "c-coral",  "title": "Marketing &amp; Outreach",               "dir": "Marketing & Outreach",               "subsections": False},
    {"icon": "&#127919;", "color": "c-teal",   "title": "Prospects &amp; Sales",                  "dir": "Prospects & Sales",                  "subsections": False},
]

CSS = """
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f8f9fa; color: #333; padding: 24px; }
  h1 { font-size: 1.6rem; font-weight: 700; margin-bottom: 20px; color: #1a1a2e; }
  .sections { display: flex; flex-direction: column; gap: 10px; max-width: 900px; }

  /* colour themes */
  .c-indigo details { border-left: 4px solid #4f46e5; }
  .c-indigo summary { background: #eef2ff; }
  .c-indigo summary:hover { background: #e0e7ff; }
  .c-purple details { border-left: 4px solid #7c3aed; }
  .c-purple summary { background: #f5f3ff; }
  .c-purple summary:hover { background: #ede9fe; }
  .c-green  details { border-left: 4px solid #16a34a; }
  .c-green  summary { background: #f0fdf4; }
  .c-green  summary:hover { background: #dcfce7; }
  .c-teal   details { border-left: 4px solid #0d9488; }
  .c-teal   summary { background: #f0fdfa; }
  .c-teal   summary:hover { background: #ccfbf1; }
  .c-amber  details { border-left: 4px solid #d97706; }
  .c-amber  summary { background: #fffbeb; }
  .c-amber  summary:hover { background: #fef3c7; }
  .c-blue   details { border-left: 4px solid #2563eb; }
  .c-blue   summary { background: #eff6ff; }
  .c-blue   summary:hover { background: #dbeafe; }
  .c-coral  details { border-left: 4px solid #e11d48; }
  .c-coral  summary { background: #fff1f2; }
  .c-coral  summary:hover { background: #ffe4e6; }

  details { border-radius: 8px; overflow: hidden; box-shadow: 0 1px 4px rgba(0,0,0,.08); }
  summary {
    display: flex; align-items: center; gap: 10px;
    padding: 12px 16px; cursor: pointer; list-style: none;
    user-select: none; transition: background .15s;
  }
  summary::-webkit-details-marker { display: none; }
  .section-icon { font-size: 1.3rem; flex-shrink: 0; }
  .section-title { font-weight: 600; font-size: .95rem; flex: 1; }
  .section-count { font-size: .8rem; color: #666; background: rgba(0,0,0,.07); padding: 2px 8px; border-radius: 99px; }
  .chevron { width: 18px; height: 18px; stroke: #555; stroke-width: 2.5; fill: none; transition: transform .25s; flex-shrink: 0; }
  details[open] .chevron { transform: rotate(180deg); }
  .file-list { padding: 8px 16px 12px 16px; background: #fff; display: flex; flex-direction: column; gap: 4px; }
  .file-row { display: flex; align-items: center; gap: 8px; padding: 6px 8px; border-radius: 6px; text-decoration: none; color: #222; font-size: .88rem; transition: background .1s; }
  .file-row:hover { background: #f1f5f9; }
  .file-icon { font-size: 1rem; }
  .sub-label { font-size: .75rem; color: #888; margin-top: 8px; margin-bottom: 2px; font-weight: 600; text-transform: uppercase; letter-spacing: .05em; }
  .empty { color: #aaa; font-size: .85rem; font-style: italic; padding: 4px 0; }
"""

CHEVRON = '<svg class="chevron" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><polyline points="6 9 12 15 18 9"/></svg>'

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
    if not os.path.isdir(full):
        return []
    return sorted(
        [f for f in os.listdir(full) if not f.startswith(".") and os.path.isfile(os.path.join(full, f))],
        key=str.lower
    )

def list_subdirs(rel_dir):
    full = os.path.join(REPO_ROOT, rel_dir)
    if not os.path.isdir(full):
        return []
    return sorted(
        [d for d in os.listdir(full) if not d.startswith(".") and os.path.isdir(os.path.join(full, d))],
        key=str.lower
    )

def file_link(rel_dir, filename):
    path = BASE_URL + urllib.parse.quote(rel_dir + "/" + filename, safe="/")
    icon = file_icon(filename)
    return f'<a class="file-row" href="{path}" target="_blank"><span class="file-icon">{icon}</span>{filename}</a>'

def render_section(s):
    rel = s["dir"]
    color = s["color"]
    title = s["title"]
    icon = s["icon"]

    rows = []
    if s["subsections"]:
        # top-level files first
        for f in list_files(rel):
            rows.append(file_link(rel, f))
        # then sub-folders
        for sub in list_subdirs(rel):
            rows.append(f'<div class="sub-label">{sub}</div>')
            sub_rel = rel + "/" + sub
            sub_files = list_files(sub_rel)
            if sub_files:
                for f in sub_files:
                    rows.append(file_link(sub_rel, f))
            else:
                rows.append('<div class="empty">No files</div>')
    else:
        for f in list_files(rel):
            rows.append(file_link(rel, f))

    count = sum(1 for r in rows if 'file-row' in r)
    if not rows:
        rows.append('<div class="empty">No files found</div>')

    inner = "\n".join(rows)
    return f"""<div class="{color}">
  <details>
    <summary>
      <span class="section-icon">{icon}</span>
      <span class="section-title">{title}</span>
      <span class="section-count">{count}</span>
      {CHEVRON}
    </summary>
    <div class="file-list">
{inner}
    </div>
  </details>
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
  <h1>&#128196; StrategyFolio</h1>
  <div class="sections">
{sections_html}
  </div>
</body>
</html>"""
    out = os.path.join(REPO_ROOT, "index.html")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"Written {out}")

if __name__ == "__main__":
    generate()
