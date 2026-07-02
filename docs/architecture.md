# Architecture

The v0 architecture is intentionally small.

```text
local source
  -> analyzer
  -> readiness signals
  -> output-level decision
  -> artifact builder
  -> note / seed / mini skill / full skill
```

## Components

| Path | Responsibility |
|---|---|
| `source_to_skill/analyzer.py` | read text, normalize it, extract title and evidence candidates |
| `source_to_skill/scoring.py` | compute transparent readiness signals |
| `source_to_skill/models.py` | shared dataclasses and output levels |
| `source_to_skill/templates.py` | render reports and generated artifacts |
| `source_to_skill/builder.py` | write artifacts to disk |
| `source_to_skill/cli.py` | command-line interface |

## Later Intake Plugins

PDF, EPUB, HTML, RSS, and audio transcription should be intake plugins. They
should normalize sources into text before the readiness gate runs.

The readiness gate should remain independent from extraction.
