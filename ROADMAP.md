# Roadmap

`source-to-skill` is intentionally starting with a small core: local text,
readiness scoring, and multi-level artifact generation.

## v0.1: Readiness Gate

Status: shipped.

- Local UTF-8 text and Markdown input.
- Human-readable readiness reports.
- JSON readiness reports for integrations.
- Note, Skill Seed, Mini Skill, and Full Skill artifact builders.
- Basic SVG identity and documentation.

## v0.2: Intake Plugins

Goal: normalize more source types into text before scoring.

- Local HTML intake. Shipped.
- PDF and EPUB intake.
- Remote HTML / article intake.
- Transcript file cleanup.
- Keep extraction separate from scoring.

## v0.3: Skill Quality Evaluation

Goal: make generated skills easier to trust.

- Smoke-question runner.
- Evidence coverage checks.
- Claims-without-evidence warnings.
- Fold-in quality report for existing skills.

## v0.4: Audio And Long-Form Sources

Goal: support audio without making the product "recording-to-skill."

- Local transcript intake first.
- Optional Whisper-based audio transcription.
- Transcript cleanup and topic splitting.
- Default audio output should usually be Note or Skill Seed unless the score is strong.

## v1.0: Stable Skill Compiler

Goal: a small reliable tool that can be used in real agent workflows.

- Stable CLI contract.
- Stable JSON schema.
- Better documented scoring.
- Format adapters for common agent skill layouts.
- Real examples from books, articles, interviews, and meetings.
