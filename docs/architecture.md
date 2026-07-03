# Architecture

The v0 architecture is intentionally small.

```text
local text / Markdown / HTML source or single remote text / HTML URL
  -> optional transcript cleanup
  -> optional topic splitting
  -> analyzer
  -> readiness signals
  -> output-level decision
  -> artifact builder
  -> skill evaluator
  -> note / seed / mini skill / full skill
```

## Components

| Path | Responsibility |
|---|---|
| `source_to_skill/intake.py` | read local text/Markdown/HTML or single remote text/HTML URLs and normalize them into plain Markdown-like text |
| `source_to_skill/transcript.py` | clean transcript-like text, SRT, and VTT into Markdown segments |
| `source_to_skill/segmenter.py` | split long sources into separately scored topic candidates |
| `source_to_skill/analyzer.py` | normalize text, extract title and evidence candidates |
| `source_to_skill/scoring.py` | compute transparent readiness signals |
| `source_to_skill/models.py` | shared dataclasses and output levels |
| `source_to_skill/templates.py` | render reports and generated artifacts |
| `source_to_skill/evaluator.py` | compare generated guidance against evidence and render evaluation reports |
| `source_to_skill/builder.py` | write artifacts to disk |
| `source_to_skill/demo.py` | run the bundled end-to-end example workflow |
| `source_to_skill/cli.py` | command-line interface |

## Later Intake Plugins

PDF, EPUB, RSS, crawling, and JavaScript-rendered web pages should be intake
plugins. They should normalize sources into text before the readiness gate runs.

The readiness gate should remain independent from extraction.

The evaluator should also remain independent from extraction. It reviews the
generated skill folder and can be run after build output has been edited by a
human.
