# Architecture

The v0 architecture is intentionally small.

```text
local text / Markdown / HTML source
  -> optional transcript cleanup
  -> analyzer
  -> readiness signals
  -> output-level decision
  -> artifact builder
  -> note / seed / mini skill / full skill
```

## Components

| Path | Responsibility |
|---|---|
| `source_to_skill/intake.py` | read local text/Markdown/HTML and normalize it into plain Markdown-like text |
| `source_to_skill/transcript.py` | clean transcript-like text, SRT, and VTT into Markdown segments |
| `source_to_skill/analyzer.py` | normalize text, extract title and evidence candidates |
| `source_to_skill/scoring.py` | compute transparent readiness signals |
| `source_to_skill/models.py` | shared dataclasses and output levels |
| `source_to_skill/templates.py` | render reports and generated artifacts |
| `source_to_skill/builder.py` | write artifacts to disk |
| `source_to_skill/cli.py` | command-line interface |

## Later Intake Plugins

PDF, EPUB, RSS, remote web pages, and audio transcription should be intake
plugins. They should normalize sources into text before the readiness gate runs.

The readiness gate should remain independent from extraction.
