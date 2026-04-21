#!/usr/bin/env python3
"""
generate_index.py — Auto-generates index.html for StrategyFolio.
Runs automatically via GitHub Actions on every push, or manually anytime.
"""

import os
from pathlib import Path
from urllib.parse import quote
import html

REPO_ROOT = Path(__file__).parent
ALLOWED_EXTENSIONS = {'.html', '.md'}

# Section config — defines order, colour, icon, and display title.
# Add new top-level folders here if you create them.
SECTIONS = [
    {
        "folder": "Business Operations",
        "title": "Business Operations",
        "color": "c-purple",
        "icon": "&#9881;",
    },
    {
        "folder": "Clients",
        "title": "Clients",
        "color": "c-green",
        "icon": "&#129309;",
        "subfolders": True,   # Each subfolder = one client subsection
    },
    {
        "folder": "Deliverables - Guides & Handovers",
        "title": "Deliverables — Guides &amp; Handovers",
        "color": "c-teal",
        "icon": "&#128196;",
    },
    {
        "folder": "Deliverables - Proposals & Pricing",
        "title": "Deliverables — Proposals &amp; Pricing",
        "color": "c-amber",
        "icon": "&#128176;",
    },
    {
        "folder": "Deliverables-Websites",
        "title": "Deliverables — Websites",
        "color": "c-blue",
        "icon": "&#127760;",
    },
    {
        "folder": "Marketing & Outreach",
        "title": "Marketing &amp; Outreach",
        "color": "c-coral",
        "icon": "&#128227;",
    },
    {
        "folder": "Prospects & Sales",
        "title": "Prospects &amp; Sales",
        "color": "c-teal",
        "icon": "&#127919;",
    },
]

# Words to keep uppercase in display names
UPPERCASE_WORDS = {"ai", "sc", "html", "md", "seo", "crm", "uk", "v2", "v3", "v4", "v5", "v9"}

CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: system-ui, -apple-system, sans-serif; background: #f5f4f0; color: #1a1a1a; padding: 2rem 1rem; }
.header { max-width: 860px; margin: 0 auto 2.5rem; }
.header h1 { font-size: 28px; font-weight: 600; color: #1a1a1a; margin-bottom: 4px; }
.header p { font-size: 14px; color: #666; }
.grid { max-width: 860px; margin: 0 auto; display: grid; gap: 1.5rem; }
.section { background: #fff; border-radius: 12px; border: 0.5px solid #ddd; overflow: hidden; }
.section-header { padding: 1rem 1.25rem; border-bottom: 0.5px solid #eee; display: flex; align-items: center; gap: 10px; }
.section-icon { width: 32px; height: 32px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 15px; flex-shrink: 0; }
.section-title { font-size: 15px; font-weight: 500; color: #1a1a1a; }
.section-count { font-size: 12px; color: #999; margin-left: auto; }
.file-list { padding: 0.5rem 0; }
.file-item { display: flex; align-items: center; gap: 10px; padding: 0.65rem 1.25rem; text-decoration: none; color: #1a1a1a; transition: background 0.15s; border-bottom: 0.5px solid #f0f0f0; }
.file-item:last-child { border-bottom: none; }
.file-item:hover { background: #f8f7f4; }
.file-dot { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }
.file-name { font-size: 14px; flex: 1; }
.file-tag { font-size: 11px; padding: 2px 8px; border-radius: 4px; font-weight: 500; }
.tag-live { background: #eaf3de; color: #3b6d11; }
.tag-md { background: #f1efe8; color: #5f5e5a; }
.arrow { font-size: 12px; color: #bbb; }
.c-purple .section-icon { background: #EEEDFE; color: #534AB7; }
.c-purple .file-dot { background: #7F77DD; }
.c-teal .section-icon { background: #E1F5EE; color: #0F6E56; }
.c-teal .file-dot { background: #1D9E75; }
.c-blue .section-icon { background: #E6F1FB; color: #185FA5; }
.c-blue .file-dot { background: #378ADD; }
.c-coral .section-icon { background: #FAECE7; color: #993C1D; }
.c-coral .file-dot { background: #D85A30; }
.c-amber .section-icon { background: #FAEEDA; color: #854F0B; }
.c-amber .file-dot { background: #BA7517; }
.c-green .section-icon { background: #E2F5E1; color: #1A6B18; }
.c-green .file-dot { background: #2E9E2A; }
.subsection-label { font-size: 11px; font-weight: 600; color: #aaa; text-transform: uppercase; letter-spacing: 0.06em; padding: 0.75rem 1.25rem 0.3rem; }
.footer { max-width: 860px; margin: 2rem auto 0; font-size: 12px; color: #aaa; text-align: center; }
"""


def make_display_name(filename: str) -> str:
    """Convert a filename into a readable display name."""
    stem = Path(filename).stem
    # " - " becomes " — "
    stem = stem.replace(" - ", " — ")
    # Underscores and remaining hyphens become spaces
    stem = stem.replace("_", " ").replace("-", " ")
    # Title-case each word, then fix known uppercase words
    words = []
    for word in stem.split():
        if word.lower() in UPPERCASE_WORDS:
            words.append(word.upper())
        else:
            words.append(word.capitalize())
    return " ".join(words)


def encode_path(path: str) -> str:
    """URL-encode a relative file path, preserving forward slashes."""
    return "/".join(quote(part) for part in path.split("/"))


def get_tag(filename: str) -> str:
    ext = Path(filename).suffix.lower()
    if ext == ".md":
        return '<span class="file-tag tag-md">MD</span>'
    return '<span class="file-tag tag-live">HTML</span>'


def list_files(folder: Path) -> list[str]:
    """Return sorted list of allowed files directly inside a folder."""
    if not folder.exists():
        return []
    return sorted(
        f.name for f in folder.iterdir()
        if f.is_file() and f.suffix.lower() in ALLOWED_EXTENSIONS
    )


def render_file_item(rel_path: str, display_name: str, filename: str) -> str:
    encoded = encode_path(rel_path)
    tag = get_tag(filename)
    return (
        f'      <a class="file-item" href="{encoded}" target="_blank">'
        f'<div class="file-dot"></div>'
        f'<span class="file-name">{html.escape(display_name)}</span>'
        f'{tag}'
        f'<span class="arrow">&#8599;</span></a>\n'
    )


def render_section(section: dict) -> str:
    folder_name = section["folder"]
    folder_path = REPO_ROOT / folder_name
    color = section["color"]
    icon = section["icon"]
    title = section["title"]
    use_subfolders = section.get("subfolders", False)

    lines = []
    file_count = 0

    if use_subfolders:
        # Each direct subfolder is a client — list its files under a subsection label
        if not folder_path.exists():
            return ""
        subfolders = sorted(
            d for d in folder_path.iterdir() if d.is_dir()
        )
        client_blocks = []
        for sub in subfolders:
            files = list_files(sub)
            if not files:
                continue
            block = f'      <div class="subsection-label">{html.escape(sub.name)}</div>\n'
            for fname in files:
                rel = f"{folder_name}/{sub.name}/{fname}"
                block += render_file_item(rel, make_display_name(fname), fname)
                file_count += 1
            client_blocks.append(block)
        file_items = "".join(client_blocks)
    else:
        files = list_files(folder_path)
        file_count = len(files)
        file_items = ""
        for fname in files:
            rel = f"{folder_name}/{fname}"
            file_items += render_file_item(rel, make_display_name(fname), fname)

    if file_count == 0:
        return ""

    count_label = f"{file_count} file{'s' if file_count != 1 else ''}"

    lines.append(f'  <!-- {folder_name} -->\n')
    lines.append(f'  <div class="section {color}">\n')
    lines.append(f'    <div class="section-header">\n')
    lines.append(f'      <div class="section-icon">{icon}</div>\n')
    lines.append(f'      <span class="section-title">{title}</span>\n')
    lines.append(f'      <span class="section-count">{count_label}</span>\n')
    lines.append(f'    </div>\n')
    lines.append(f'    <div class="file-list">\n')
    lines.append(file_items)
    lines.append(f'    </div>\n')
    lines.append(f'  </div>\n')

    return "".join(lines)


def generate():
    sections_html = "\n".join(
        s for section in SECTIONS if (s := render_section(section))
    )

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>StrategyFolio — Salman's AI Consultancy Hub</title>
<style>
{CSS.strip()}
</style>
</head>
<body>
<div class="header">
  <h1>StrategyFolio</h1>
  <p>Salman's AI Consultancy — all live pages in one place</p>
</div>
<div class="grid">

{sections_html}
</div>
<div class="footer">
  StrategyFolio — promptlane25-stack — auto-generated
</div>
</body>
</html>
"""

    output = REPO_ROOT / "index.html"
    output.write_text(page, encoding="utf-8")
    print(f"✅ index.html updated — {sum(1 for s in SECTIONS if (REPO_ROOT / s['folder']).exists())} sections written.")


if __name__ == "__main__":
    generate()
