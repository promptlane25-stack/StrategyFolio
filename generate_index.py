#!/usr/bin/env python3
"""Auto-generates index.html for StrategyFolio with collapsible sections."""
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
    padding: 0;
  }

  /* ── Page header ── */
  .page-header {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 60%, #0f3460 100%);
    padding: 40px 24px 36px;
    text-align: center;
    color: #fff;
  }
  .page-header h1 {
    font-size: 2rem;
    font-weight: 700;
    letter-spacing: -0.5px;
    display: inline-flex;
    align-items: center;
    gap: 12px;
  }
  .page-header p {
    margin-top: 8px;
    font-size: 0.9rem;
    color: rgba(255,255,255,0.55);
    letter-spacing: 0.4px;
  }

  /* ── Container ── */
  .container {
    max-width: 780px;
    margin: 0 auto;
    padding: 32px 20px 60px;
  }

  /* ── Section cards ── */
  .section-wrap {
    margin-bottom: 10px;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08), 0 4px 12px rgba(0,0,0,0.04);
    transition: box-shadow 0.2s;
  }
  .section-wrap:hover { box-shadow: 0 2px 8px rgba(0,0,0,0.12), 0 6px 20px rgba(0,0,0,0.07); }

  details { display: block; }

  /* ── Summary row ── */
  summary {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 15px 18px;
    cursor: pointer;
    list-style: none;
    user-select: none;
    border-radius: 12px;
    transition: filter 0.15s;
  }
  summary::-webkit-details-marker { display: none; }
  details[open] summary { border-radius: 12px 12px 0 0; }
  summary:hover { filter: brightness(0.97); }

  .section-icon {
    font-size: 1.25rem;
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 8px;
    background: rgba(255,255,255,0.55);
    flex-shrink: 0;
  }
  .section-title {
    font-size: 0.95rem;
    font-weight: 600;
    flex: 1;
    color: #1a1a2e;
  }
  .section-count {
    font-size: 0.75rem;
    font-weight: 600;
    color: #555;
    background: rgba(0,0,0,0.08);
    padding: 3px 10px;
    border-radius: 99px;
    flex-shrink: 0;
  }
  .chevron {
    width: 16px;
    height: 16px;
    stroke: #666;
    stroke-width: 2.5;
    fill: none;
    flex-shrink: 0;
    transition: transform 0.25s ease;
  }
  details[open] .chevron { transform: rotate(180deg); }

  /* ── File list ── */
  .file-list {
    background: #fff;
    padding: 8px 12px 12px 12px;
    border-radius: 0 0 12px 12px;
  }
  .file-row {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 10px;
    border-radius: 8px;
    text-decoration: none;
    color: #2d2d3d;
    font-size: 0.875rem;
    transition: background 0.12s;
    line-height: 1.3;
  }
  .file-row:hover { background: #f5f7fa; color: #1a1a2e; }
  .file-icon {
    font-size: 0.95rem;
    width: 24px;
    text-align: center;
    flex-shrink: 0;
    opacity: 0.75;
  }
  .file-name { flex: 1; word-break: break-word; }

  .sub-label {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: #999;
    padding: 10px 10px 4px 10px;
  }
  .empty { color: #bbb; font-size: 0.85rem; font-style: italic; padding: 8px 10px; }

  /* ── Colour themes ── */
  .c-indigo summary { background: #eef2ff; }
  .c-purple summary { background: #f5f3ff; }
  .c-green  summary { background: #f0fdf4; }
  .c-teal   summary { background: #f0fdfa; }
  .c-amber  summary { background: #fffbeb; }
  .c-blue   summary { background: #eff6ff; }
  .c-coral  summary { background: #fff1f2; }

  .c-indigo .section-icon { background: rgba(79, 70, 229, 0.12); }
  .c-purple .section-icon { background: rgba(124, 58, 237, 0.12); }
  .c-green  .section-icon { background: rgba(22, 163, 74, 0.12); }
  .c-teal   .section-icon { background: rgba(13, 148, 136, 0.12); }
  .c-amber  .section-icon { background: rgba(217, 119, 6, 0.12); }
  .c-blue   .section-icon { background: rgba(37, 99, 235, 0.12); }
  .c-coral  .section-icon { background: rgba(225, 29, 72, 0.12); }

  .c-indigo .section-count { background: rgba(79, 70, 229, 0.1); color: #4338ca; }
  .c-purple .section-count { background: rgba(124, 58, 237, 0.1); color: #6d28d9; }
  .c-green  .section-count { background: rgba(22, 163, 74, 0.1); color: #15803d; }
  .c-teal   .section-count { background: rgba(13, 148, 136, 0.1); color: #0f766e; }
  .c-amber  .section-count { background: rgba(217, 119, 6, 0.1); color: #b45309; }
  .c-blue   .section-count { background: rgba(37, 99, 235, 0.1); color: #1d4ed8; }
  .c-coral  .section-count { background: rgba(225, 29, 72, 0.1); color: #be123c; }

  .c-indigo .file-list { border-top: 2px solid #e0e7ff; }
  .c-purple .file-list { border-top: 2px solid #ede9fe; }
  .c-green  .file-list { border-top: 2px solid #dcfce7; }
  .c-teal   .file-list { border-top: 2px solid #ccfbf1; }
  .c-amber  .file-list { border-top: 2px solid #fef3c7; }
  .c-blue   .file-list { border-top: 2px solid #dbeafe; }
  .c-coral  .file-list { border-top: 2px solid #ffe4e6; }
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
    return (
        f'<a class="file-row" href="{path}" target="_blank">'
        f'<span class="file-icon">{icon}</span>'
        f'<span class="file-name">{filename}</span>'
        f'</a>'
    )

def render_section(s):
    rel   = s["dir"]
    color = s["color"]
    title = s["title"]
    icon  = s["icon"]

    rows = []
    if s["subsections"]:
        for f in list_files(rel):
            rows.append(file_link(rel, f))
        for sub in list_subdirs(rel):
            rows.append(f'<div class="sub-label">{sub}</div>')
            sub_files = list_files(rel + "/" + sub)
            if sub_files:
                for f in sub_files:
                    rows.append(file_link(rel + "/" + sub, f))
            else:
                rows.append('<div class="empty">No files</div>')
    else:
        for f in list_files(rel):
            rows.append(file_link(rel, f))

    count = sum(1 for r in rows if "file-row" in r)
    if not rows:
        rows.append('<div class="empty">No files found</div>')

    inner = "\n".join(rows)
    return f"""<div class="section-wrap {color}">
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
    <p>Click any section to expand &mdash; multiple sections can be open at once</p>
  </header>
  <div class="container">
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
