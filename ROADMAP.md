# Roadmap

`source-to-skill` is intentionally starting with a small core: local text,
readiness scoring, and multi-level artifact generation.

The long-term direction is not "one source, one skill." The long-term direction
is source-to-delta: new sources should become evidence, refinements,
contradictions, seeds, or new skills depending on how they relate to the
existing skill system.

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
- Remote HTML / article intake. Shipped.
- Transcript cleanup command. Shipped.
- EPUB intake. Shipped.
- PDF intake.
- Keep extraction separate from scoring.

## v0.3: Skill Quality Evaluation

Goal: make generated skills easier to trust.

- Smoke-question runner.
- Evidence coverage checks. Shipped.
- Claims-without-evidence warnings.
- Fold-in quality report for existing skills.

## v0.4: Audio And Long-Form Sources

Goal: support audio without making the product "recording-to-skill."

- Local transcript intake first.
- Optional Whisper CLI transcription wrapper. Shipped.
- Transcript cleanup and topic splitting. Shipped.
- Default audio output should usually be Note or Skill Seed unless the score is strong.

## v1.0: Stable Skill Compiler

Goal: a small reliable tool that can be used in real agent workflows.

- Stable CLI contract.
- Stable JSON schema.
- Better documented scoring.
- Bundled end-to-end demo. Shipped.
- Format adapters for common agent skill layouts.
- Real examples from books, articles, interviews, and meetings.

## v1.1: Skill Evolution Layer

Goal: prevent skill sprawl by updating existing skills before creating new ones.
See `docs/review-gates.md` for the first-principles and adversarial review
model this layer should use.

- Skill metadata scanner for existing skill folders.
- Source-to-skill matching by domain, title, use case, and evidence overlap.
- Relationship classifier:
  - duplicate
  - evidence
  - refinement
  - contradiction
  - new skill
- Pending update artifacts under `evolution/pending-updates/`.
- Human review flow for contradictions and major rewrites.
- First-principles review:
  - core problem
  - core method
  - use case
  - boundary
- Adversarial review:
  - counterexamples
  - contradictions
  - overgeneralization
  - missing evidence
  - unsafe merge risk
- Changelog entries for accepted updates.
- Re-run evidence and regression checks after a skill evolves.

## v1.2: Skill Router Inputs

Goal: make large skill libraries easier for agents to use.

- Generate or update skill metadata:
  - `use_when`
  - `do_not_use_when`
  - domains
  - trigger signals
  - maturity
  - confidence
- Create a lightweight skill index for routing.
- Recommend the smallest relevant skill set for a user task.
- Avoid loading every skill into the agent context.
