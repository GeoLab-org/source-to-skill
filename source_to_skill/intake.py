from __future__ import annotations

import html.parser
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen


TEXT_SUFFIXES = {".txt", ".md", ".markdown"}
HTML_SUFFIXES = {".html", ".htm"}
SUPPORTED_SUFFIXES = TEXT_SUFFIXES | HTML_SUFFIXES
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
