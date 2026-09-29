'Compile the markdown essays in 08_relig into standalone HTML pages.\n\nEvery ``*.md`` file directly inside the source directory is rendered with the\nshared "Hokaido Night" design system (hokaido-theme.css) and written as a\nstandalone HTML file into the output directory, next to an index.html\noverview. The design targets comfortable, atmospheric reading on mobile,\ntablet and laptop screens.\n\nThe markdown content stays in its original language; this script and all\ngenerated markup/UI strings are English.\n\nUsage:\n    python3 build_html.py\n'
from __future__ import annotations
import html
import re
from dataclasses import dataclass, field
from pathlib import Path
SCRIPT_DIR = Path(__file__).resolve().parent
SOURCE_DIR = SCRIPT_DIR.parent
OUTPUT_DIR = SOURCE_DIR.parent / 'docs' / 'phil'
CSS_FILENAME = 'hokaido-theme.css'
SITE_TITLE = 'Contemplations'
SITE_TAGLINE = 'Essays and letters on suffering, compassion and enlightenment — a small collection for quiet reading.'
'# --------------------------------------------------------------------------'
'# Minimal, dependency-free markdown -> HTML conversion'
'# --------------------------------------------------------------------------'
INLINE_CODE_RE = re.compile('`([^`]+)`')
LINK_RE = re.compile('\\[([^\\]]+)\\]\\(([^)]+)\\)')
BOLD_RE = re.compile('(\\*\\*|__)(.+?)\\1')
ITALIC_RE = re.compile('(\\*|_)(.+?)\\1')
HEADING_RE = re.compile('^(#{1,6})\\s+(.*)$')
HR_RE = re.compile('^(-{3,}|\\*{3,}|_{3,})$')
UNORDERED_ITEM_RE = re.compile('^[-*]\\s+(.*)$')
ORDERED_ITEM_RE = re.compile('^\\d+\\.\\s+(.*)$')
LIST_ITEM_RE = re.compile('^(?:\\d+\\.|[-*])\\s+(.*)$')

def convert_inline(text: str) -> str:
    """Convert inline markdown spans (code, links, bold, italic) to HTML."""
    text = html.escape(text, quote=False)
    placeholders: list[str] = []

    def stash(value: str) -> str:
        placeholders.append(value)
        return f'\x00{len(placeholders) - 1}\x00'
    text = INLINE_CODE_RE.sub(lambda m: stash(f'<code>{m.group(1)}</code>'), text)
    text = LINK_RE.sub(lambda m: stash(f'<a href="{m.group(2)}">{m.group(1)}</a>'), text)
    text = BOLD_RE.sub(lambda m: stash(f'<strong>{m.group(2)}</strong>'), text)
    text = ITALIC_RE.sub(lambda m: stash(f'<em>{m.group(2)}</em>'), text)
    return re.sub('\\x00(\\d+)\\x00', lambda m: placeholders[int(m.group(1))], text)

def strip_markdown(text: str) -> str:
    """Reduce inline markdown to plain text (for <title>, excerpts, nav)."""
    text = LINK_RE.sub(lambda m: m.group(1), text)
    text = BOLD_RE.sub(lambda m: m.group(2), text)
    text = ITALIC_RE.sub(lambda m: m.group(2), text)
    text = INLINE_CODE_RE.sub(lambda m: m.group(1), text)
    return text.strip()

@dataclass
class Block:
    """# heading | paragraph | blockquote | list | hr"""
    kind: str
    level: int = 0
    text: str = ''
    items: list[str] = field(default_factory=list)
    ordered: bool = False

def parse_blocks(md_text: str) -> list[Block]:
    """Parse a markdown document into a flat list of block elements."""
    lines = md_text.splitlines()
    blocks: list[Block] = []
    paragraph_lines: list[str] = []
    i = 0

    def flush_paragraph() -> None:
        if paragraph_lines:
            blocks.append(Block(kind='paragraph', text=' '.join(paragraph_lines).strip()))
            paragraph_lines.clear()
    while i < len(lines):
        stripped = lines[i].strip()
        if not stripped:
            flush_paragraph()
            i += 1
            continue
        heading = HEADING_RE.match(stripped)
        if heading:
            flush_paragraph()
            blocks.append(Block(kind='heading', level=len(heading.group(1)), text=heading.group(2).strip()))
            i += 1
            continue
        if HR_RE.match(stripped):
            flush_paragraph()
            blocks.append(Block(kind='hr'))
            i += 1
            continue
        if stripped.startswith('>'):
            flush_paragraph()
            quote_lines: list[str] = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                quote_lines.append(re.sub('^>\\s?', '', lines[i].strip()))
                i += 1
            blocks.append(Block(kind='blockquote', text=' '.join(quote_lines)))
            continue
        if UNORDERED_ITEM_RE.match(stripped) or ORDERED_ITEM_RE.match(stripped):
            flush_paragraph()
            ordered = bool(ORDERED_ITEM_RE.match(stripped))
            items: list[str] = []
            while i < len(lines):
                item = LIST_ITEM_RE.match(lines[i].strip())
                if not item:
                    break
                items.append(item.group(1))
                i += 1
            blocks.append(Block(kind='list', items=items, ordered=ordered))
            continue
        paragraph_lines.append(stripped)
        i += 1
    flush_paragraph()
    return blocks

def render_block(block: Block) -> str:
    if block.kind == 'heading':
        '# keep body headings within h1..h4'
        level = min(block.level, 4)
        return f'<h{level}>{convert_inline(block.text)}</h{level}>'
    if block.kind == 'paragraph':
        return f'<p>{convert_inline(block.text)}</p>'
    if block.kind == 'blockquote':
        return f'<blockquote>{convert_inline(block.text)}</blockquote>'
    if block.kind == 'hr':
        return '<hr />'
    if block.kind == 'list':
        tag = 'ol' if block.ordered else 'ul'
        items = ''.join((f'<li>{convert_inline(item)}</li>' for item in block.items))
        return f'<{tag}>{items}</{tag}>'
    raise ValueError(f'Unknown block kind: {block.kind}')

def extract_title(blocks: list[Block], fallback: str) -> tuple[str, list[Block]]:
    """Pull the first heading out as the page title; return the rest."""
    for index, block in enumerate(blocks):
        if block.kind == 'heading':
            remaining = blocks[:index] + blocks[index + 1:]
            return (block.text, remaining)
    return (fallback, blocks)

def first_excerpt(blocks: list[Block], limit: int=180) -> str:
    for block in blocks:
        if block.kind == 'paragraph':
            plain = strip_markdown(block.text)
            if len(plain) <= limit:
                return plain
            return plain[:limit].rsplit(' ', 1)[0] + '…'
    return ''
GERMAN_MARKERS = (' der ', ' die ', ' und ', ' ist ', ' nicht ', ' eine ', ' ein ', ' sich ', ' mit ', ' für ')
ENGLISH_MARKERS = (' the ', ' and ', ' is ', ' of ', ' to ', ' that ', ' with ', ' for ')

def detect_language(text: str) -> str:
    """Naive language guess (de/en) used only for the html[lang] attribute."""
    sample = f' {text.lower()} '
    de_hits = sum((sample.count(marker) for marker in GERMAN_MARKERS))
    en_hits = sum((sample.count(marker) for marker in ENGLISH_MARKERS))
    return 'en' if en_hits > de_hits else 'de'
'# --------------------------------------------------------------------------'
'# HTML page templates'
'# --------------------------------------------------------------------------'

def render_article_page(title_html: str, title_plain: str, lang: str, body_html: str) -> str:
    return f'<!doctype html>\n<html lang="{lang}">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>{
        html.escape(title_plain)} — {SITE_TITLE}</title>\n<link rel="stylesheet" href="{CSS_FILENAME}">\n</head>\n<body class="starfield">\n<header class="site-header container">\n<a class="back-link" href="index.html">← Overview</a>\n</header>\n<main class="container article">\n<article class="card">\n<h1>{title_html}</h1>\n{body_html}\n</article>\n</main>\n<footer class="site-footer container">\n<small>{SITE_TITLE}</small>\n</footer>\n</body>\n</html>\n'

def render_index_page(cards_html: str) -> str:
    return f'<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>{SITE_TITLE}</title>\n<link rel="stylesheet" href="{CSS_FILENAME}">\n</head>\n<body class="starfield">\n<header class="site-header container">\n<h1>{SITE_TITLE}</h1>\n<p class="tagline">{
        html.escape(SITE_TAGLINE)}</p>\n</header>\n<main class="container">\n<div class="index-grid">\n{cards_html}\n</div>\n</main>\n<footer class="site-footer container">\n<small>{SITE_TITLE}</small>\n</footer>\n</body>\n</html>\n'

def render_index_card(slug: str, title_plain: str, excerpt: str) -> str:
    return f'<a class="index-card card" href="{slug}.html"><h2>{
        html.escape(title_plain)}</h2><p>{
            html.escape(excerpt)}</p></a>'
'# --------------------------------------------------------------------------'
'# Build'
'# --------------------------------------------------------------------------'

def build() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if not (OUTPUT_DIR / CSS_FILENAME).exists():
        print(f'Warning: {CSS_FILENAME} not found in {OUTPUT_DIR}')
    md_files = sorted(SOURCE_DIR.glob('*.md'))
    if not md_files:
        print(f'No markdown files found in {SOURCE_DIR}')
        return
    cards: list[str] = []
    for md_path in md_files:
        raw = md_path.read_text(encoding='utf-8')
        blocks = parse_blocks(raw)
        raw_title, body_blocks = extract_title(blocks, fallback=md_path.stem)
        title_plain = strip_markdown(raw_title)
        title_html = convert_inline(raw_title)
        lang = detect_language(raw)
        body_html = '\n'.join((render_block(b) for b in body_blocks))
        excerpt = first_excerpt(body_blocks)
        slug = md_path.stem
        page_html = render_article_page(title_html, title_plain, lang, body_html)
        (OUTPUT_DIR / f'{slug}.html').write_text(page_html, encoding='utf-8')
        cards.append(render_index_card(slug, title_plain, excerpt))
        print(f'Compiled {md_path.name} -> {slug}.html')
    index_html = render_index_page('\n'.join(cards))
    (OUTPUT_DIR / 'index.html').write_text(index_html, encoding='utf-8')
    print(f'Compiled index.html ({len(md_files)} entries)')
if __name__ == '__main__':
    build()