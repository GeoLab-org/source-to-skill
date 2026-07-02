# Intake

The intake layer turns source material into plain text before the readiness gate
scores it. It should extract text, not decide whether the source deserves a
skill.

## Supported Inputs

| Input | Status | Notes |
|---|---|---|
| Local `.txt` | Supported | Read as UTF-8 text |
| Local `.md` / `.markdown` | Supported | Preserves Markdown structure |
| Local `.html` / `.htm` | Supported | Removes script, style, head, nav, and footer content |
| Remote `http` / `https` HTML | Supported | Fetches one URL and applies the HTML cleaner |
| Remote `http` / `https` text | Supported | Fetches one URL and reads text content |
| SRT / VTT transcripts | Supported through `clean-transcript` | Clean first, then analyze the Markdown output |

## URL Usage

```bash
source-to-skill analyze https://example.com/article
source-to-skill build https://example.com/article --level auto --out out
```

URL intake is intentionally modest. It fetches a single URL with a normal user
agent and uses the same conservative HTML cleaner as local HTML files.

## Not Yet Supported

- multi-page crawling
- JavaScript-rendered extraction
- login-gated pages
- PDF / EPUB parsing
- audio transcription

Those should be added as intake plugins that normalize sources into text before
the readiness gate runs.
