import zipfile

from source_to_skill.intake import html_to_text, read_source


def test_html_to_text_removes_script_and_keeps_article():
    html = """
    <html>
      <head><title>Hidden</title></head>
      <body>
        <nav>Navigation</nav>
        <article>
          <h1>Useful Method</h1>
          <p>When the source is structured, use the readiness gate.</p>
        </article>
        <script>console.log("noise")</script>
      </body>
    </html>
    """
    text = html_to_text(html)
    assert "Useful Method" in text
    assert "readiness gate" in text
    assert "Navigation" not in text
    assert "console.log" not in text


def test_read_source_supports_html(tmp_path):
    path = tmp_path / "article.html"
    path.write_text("<article><h1>Title</h1><p>Rule text.</p></article>", encoding="utf-8")
    assert "Rule text." in read_source(path)


def test_read_source_supports_epub_spine_order(tmp_path):
    path = tmp_path / "book.epub"
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr(
            "META-INF/container.xml",
            """<?xml version="1.0"?>
            <container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
              <rootfiles>
                <rootfile full-path="OPS/content.opf" media-type="application/oebps-package+xml"/>
              </rootfiles>
            </container>
            """,
        )
        archive.writestr(
            "OPS/content.opf",
            """<?xml version="1.0"?>
            <package xmlns="http://www.idpf.org/2007/opf" version="3.0">
              <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
                <dc:title>Sample Book</dc:title>
              </metadata>
              <manifest>
                <item id="second" href="chapter-2.xhtml" media-type="application/xhtml+xml"/>
                <item id="first" href="chapter-1.xhtml" media-type="application/xhtml+xml"/>
                <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
              </manifest>
              <spine>
                <itemref idref="first"/>
                <itemref idref="second"/>
              </spine>
            </package>
            """,
        )
        archive.writestr(
            "OPS/chapter-1.xhtml",
            "<html><body><h1>First Chapter</h1><p>First reusable rule.</p></body></html>",
        )
        archive.writestr(
            "OPS/chapter-2.xhtml",
            "<html><body><h1>Second Chapter</h1><p>Second reusable rule.</p></body></html>",
        )
        archive.writestr("OPS/nav.xhtml", "<html><body><nav>Table of contents noise.</nav></body></html>")

    text = read_source(path)

    assert text.splitlines()[0] == "# Sample Book"
    assert "First Chapter" in text
    assert "Second Chapter" in text
    assert text.index("First Chapter") < text.index("Second Chapter")
    assert "Table of contents noise" not in text


def test_read_source_rejects_unknown_suffix(tmp_path):
    path = tmp_path / "data.pdf"
    path.write_text("not really a pdf", encoding="utf-8")
    try:
        read_source(path)
    except ValueError as exc:
        assert "Unsupported source type" in str(exc)
    else:
        raise AssertionError("Expected unsupported suffix to raise ValueError")
