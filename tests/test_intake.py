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


def test_read_source_rejects_unknown_suffix(tmp_path):
    path = tmp_path / "data.pdf"
    path.write_text("not really a pdf", encoding="utf-8")
    try:
        read_source(path)
    except ValueError as exc:
        assert "Unsupported source type" in str(exc)
    else:
        raise AssertionError("Expected unsupported suffix to raise ValueError")
