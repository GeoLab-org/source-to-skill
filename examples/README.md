# Examples

These examples are small on purpose. They show the workflow and the quality
gate; they are not meant to prove that every source should become a skill.

## Files

| File | Use |
|---|---|
| `article.md` | Structured article-style source for `analyze` and `build` |
| `article.html` | HTML intake example using the same article content |
| `meeting-transcript.md` | Human-readable transcript-like source |
| `meeting-transcript.vtt` | VTT transcript cleanup example |
| `readiness-report.md` | Example readiness report output |

## Try Them

Run the complete example workflow:

```bash
source-to-skill demo --out out/demo
```

The command above uses the examples bundled inside the installed package. To run
against this directory explicitly:

```bash
source-to-skill demo --out out/demo --examples examples
```

Analyze the article:

```bash
source-to-skill analyze examples/article.md
```

Build the recommended artifact:

```bash
source-to-skill build examples/article.md --level auto --out out
```

Clean the transcript before scoring it:

```bash
source-to-skill clean-transcript examples/meeting-transcript.vtt \
  --out out/clean-meeting.md \
  --title "Meeting Transcript"
```

Split the cleaned transcript into topic candidates:

```bash
source-to-skill split-source out/clean-meeting.md --out out/topics
```

The transcript example is intentionally modest. A normal meeting often contains
useful next actions or seeds, but not enough reusable judgment for a standalone
skill.
