from __future__ import annotations

import html.parser
import zipfile
from posixpath import dirname, normpath
from pathlib import Path
from urllib.parse import unquote, urlparse
from urllib.request import Request, urlopen
from xml.etree import ElementTree


TEXT_SUFFIXES = {".txt", ".md", ".markdown"}
HTML_SUFFIXES = {".html", ".htm"}
EPUB_SUFFIXES = {".epub"}
SUPPORTED_SUFFIXES = TEXT_SUFFIXES | HTML_SUFFIXES | EPUB_SUFFIXES
URL_SCHEMES = {"http", "https"}


class _HTMLTextExtractor(html.parser.HTMLParser):
    skip_tags = {"script", "style", "head", "nav", "footer"}
    block_tags = {"article", "main", "section", "p", "br", "li", "h1", "h2", "h3", "h4", "h5", "h6", "div"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip_depth = 0

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag in self.skip_tags:
            self.skip_depth += 1
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            level = int(tag[1])
            self.parts.append("\n" + "#" * level + " ")
            return
        if tag in self.block_tags:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in self.skip_tags and self.skip_depth:
            self.skip_depth -= 1
        if tag in self.block_tags:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self.skip_depth:
            self.parts.append(data)

    def text(self) -> str:
        lines = [" ".join(line.split()) for line in "".join(self.parts).splitlines()]
        cleaned = [line for line in lines if line]
        return "\n".join(cleaned)


def read_source(path: str | Path) -> str:
    if is_url(path):
        return read_url(str(path))

    source_path = Path(path)
    suffix = source_path.suffix.lower()
    if suffix not in SUPPORTED_SUFFIXES:
        supported = ", ".join(sorted(SUPPORTED_SUFFIXES))
        raise ValueError(f"Unsupported source type '{suffix or '<none>'}'. Supported: {supported}")
    if suffix in EPUB_SUFFIXES:
        return epub_to_text(source_path)
    raw = read_text(source_path)
    if suffix in HTML_SUFFIXES:
        return html_to_text(raw)
    return raw


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def is_url(value: str | Path) -> bool:
    parsed = urlparse(str(value))
    return parsed.scheme in URL_SCHEMES and bool(parsed.netloc)


def read_url(url: str, *, timeout: int = 20) -> str:
    request = Request(url, headers={"User-Agent": "source-to-skill/0.1"})
    with urlopen(request, timeout=timeout) as response:
        raw = response.read()
        content_type = response.headers.get_content_type()
        charset = response.headers.get_content_charset() or "utf-8"
    text = raw.decode(charset, errors="replace")
    suffix = Path(urlparse(url).path).suffix.lower()
    if content_type == "text/html" or suffix in HTML_SUFFIXES:
        return html_to_text(text)
    if content_type.startswith("text/") or suffix in TEXT_SUFFIXES:
        return text
    raise ValueError(f"Unsupported remote source type '{content_type}'. Expected text or HTML.")


def html_to_text(raw_html: str) -> str:
    parser = _HTMLTextExtractor()
    parser.feed(raw_html)
    return parser.text()


def epub_to_text(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        opf_path = find_opf_path(archive)
        opf_bytes = archive.read(opf_path)
        title = epub_title(opf_bytes)
        chapter_paths = spine_chapter_paths(opf_bytes, opf_path)
        parts = []
        if title:
            parts.append(f"# {title}")
        for chapter_path in chapter_paths:
            try:
                raw = archive.read(chapter_path).decode("utf-8", errors="replace")
            except KeyError:
                continue
            text = html_to_text(raw)
            if text:
                parts.append(text)
    if not parts:
        raise ValueError(f"EPUB source did not contain readable spine chapters: {path}")
    return "\n\n".join(parts)


def find_opf_path(archive: zipfile.ZipFile) -> str:
    try:
        container = archive.read("META-INF/container.xml")
    except KeyError as exc:
        raise ValueError("EPUB is missing META-INF/container.xml") from exc
    root = ElementTree.fromstring(container)
    for element in root.iter():
        if local_name(element.tag) == "rootfile":
            full_path = element.attrib.get("full-path")
            if full_path:
                return full_path
    raise ValueError("EPUB container does not point to an OPF package file")


def spine_chapter_paths(opf_bytes: bytes, opf_path: str) -> list[str]:
    root = ElementTree.fromstring(opf_bytes)
    manifest: dict[str, str] = {}
    spine_ids: list[str] = []
    for element in root.iter():
        name = local_name(element.tag)
        if name == "item":
            item_id = element.attrib.get("id")
            href = element.attrib.get("href")
            media_type = element.attrib.get("media-type", "")
            if item_id and href and media_type in {"application/xhtml+xml", "text/html"}:
                manifest[item_id] = resolve_epub_path(opf_path, href)
        elif name == "itemref":
            idref = element.attrib.get("idref")
            if idref:
                spine_ids.append(idref)
    return [manifest[item_id] for item_id in spine_ids if item_id in manifest]


def epub_title(opf_bytes: bytes) -> str | None:
    root = ElementTree.fromstring(opf_bytes)
    for element in root.iter():
        if local_name(element.tag) == "title" and element.text:
            title = " ".join(element.text.split())
            if title:
                return title
    return None


def resolve_epub_path(opf_path: str, href: str) -> str:
    clean_href = unquote(href.split("#", 1)[0])
    base = dirname(opf_path)
    return normpath(f"{base}/{clean_href}" if base else clean_href)


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]
