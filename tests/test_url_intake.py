from __future__ import annotations

import functools
import json
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

from source_to_skill.builder import build_artifacts
from source_to_skill.cli import main
from source_to_skill.intake import read_source


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):  # noqa: A002
        return


def serve_directory(path):
    handler = functools.partial(QuietHandler, directory=str(path))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def test_read_source_fetches_remote_html(tmp_path):
    (tmp_path / "article.html").write_text(
        """
        <html>
          <head><title>Hidden title</title></head>
          <body>
            <nav>Site menu</nav>
            <article>
              <h1>Remote Playbook</h1>
              <p>When a remote source has structure, preserve the useful rule.</p>
            </article>
          </body>
        </html>
        """,
        encoding="utf-8",
    )
    server = serve_directory(tmp_path)
    try:
        url = f"http://127.0.0.1:{server.server_port}/article.html"
        text = read_source(url)
    finally:
        server.shutdown()
        server.server_close()

    assert "Remote Playbook" in text
    assert "preserve the useful rule" in text
    assert "Site menu" not in text


def test_analyze_cli_accepts_url(tmp_path, capsys):
    (tmp_path / "post.html").write_text(
        "<article><h1>URL Skill Source</h1><p>When the article has reusable guidance, score it before building.</p></article>",
        encoding="utf-8",
    )
    server = serve_directory(tmp_path)
    try:
        url = f"http://127.0.0.1:{server.server_port}/post.html"
        result = main(["analyze", url, "--json"])
    finally:
        server.shutdown()
        server.server_close()

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["title"] == "URL Skill Source"
    assert payload["source_path"] == url


def test_build_artifacts_accepts_url(tmp_path):
    (tmp_path / "build.html").write_text(
        "<article><h1>Build URL Source</h1><p>When a URL has reusable guidance, build the smallest useful artifact.</p></article>",
        encoding="utf-8",
    )
    server = serve_directory(tmp_path)
    try:
        url = f"http://127.0.0.1:{server.server_port}/build.html"
        target = build_artifacts(url, tmp_path / "out", level="seed")
    finally:
        server.shutdown()
        server.server_close()

    assert target.name == "build-url-source"
    assert (target / "readiness-report.md").exists()
    assert (target / "skill-seed.md").exists()
