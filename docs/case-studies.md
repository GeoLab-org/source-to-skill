# Case Studies

These cases show how the readiness gate behaves across source types. They are
not claims that the generated artifacts are publication-ready without review.

## Bundled Demo Article

```bash
source-to-skill analyze examples/article.md
```

The bundled article is a compact, structured source. It is useful for checking
the basic flow, but it is intentionally small; it should not be treated as proof
that every short source deserves a standalone skill.

## Bundled Meeting Transcript

```bash
source-to-skill clean-transcript examples/meeting-transcript.vtt --out out/clean-meeting.md
source-to-skill split-source out/clean-meeting.md --out out/topics
```

The transcript example demonstrates the conservative path: clean noisy speech,
split it into topic candidates, then build or fold only the useful segment.
Ordinary meetings often make better notes or seeds than full skills.

## Private Long-Form EPUB Validation

A privately supplied Chinese EPUB edition of *The Psychology of Money* was used
as a local validation case. The book text is not included in this repository.
Use your own legally obtained files for local analysis.

Observed readiness report:

| Metric | Result |
|---|---:|
| Score | 88/100 |
| Recommended output | Full Skill |
| Effective words | 99,321 |
| Headings | 46 |
| Source depth | 25/25 |
| Structure | 20/20 |
| Actionability | 20/20 |
| Transferability | 8/15 |
| Evidence | 6/10 |
| Signal cleanliness | 9/10 |

This case supports the product principle: a substantial, structured book can
clear the Full Skill threshold, while short meetings and noisy transcripts
should usually stop at Note or Skill Seed.

## Boundary

`source-to-skill` is currently strongest as a readiness gate and artifact
scaffold. It can identify when a source looks skill-worthy, normalize supported
input formats, and create reviewable files. It does not replace human review,
copyright judgment, or source-specific editorial work.
