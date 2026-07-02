# Topic Splitting

Long sources should usually be split before they are built into artifacts.

Meetings, recordings, interviews, and long articles often contain mixed signal:
some local context, some noise, and a few reusable rules. `split-source` divides
the source into topic candidates and scores each candidate with the same
readiness gate used by `analyze`.

## Command

```bash
source-to-skill split-source out/recording-clean.md --out out/topics
```

This writes:

- `topic-report.md` with score and recommended output per segment
- `segments/01-*.md`, `segments/02-*.md`, and so on

For integrations:

```bash
source-to-skill split-source out/recording-clean.md --out out/topics --json
```

## Build Or Fold A Segment

After reviewing `topic-report.md`, build only the segment that has enough signal:

```bash
source-to-skill build-segment out/topics 2 --level seed --out out
```

Or fold it into an existing skill:

```bash
source-to-skill fold-segment out/topics 2 ~/.codex/skills/design-review
```

The index is the 1-based segment number shown in `topic-report.md` and encoded
in the segment filename, for example `segments/02-useful-rule.md`.

## When To Use

Use splitting before building when the source is:

- a meeting transcript
- a voice note
- an interview
- a long article with multiple sections
- a document that mixes project context and reusable method

## Review Rule

Treat each segment independently. A strong source can contain weak segments, and
a weak meeting can still contain one useful seed.

Do not build from the whole source just because one segment is valuable. Build
from the segment whose own score, evidence, and scope support the artifact.
