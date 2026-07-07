# Evaluation

Generated skills should be reviewed before they are used as persistent agent
behavior. The evaluator adds a small evidence check to that review.

## What It Checks

`source-to-skill eval-skill` reads a generated skill folder, extracts bullets
from `## Core Guidance`, and compares them against
`references/evidence.md`.

Each guidance bullet is marked:

| Status | Meaning |
|---|---|
| `supported` | Enough meaningful terms appear in the evidence file |
| `weak` | Some terms overlap, but the claim needs manual review |
| `unsupported` | No meaningful support was found, or evidence is missing |

This is a lexical check. It is useful for catching obvious drift, but it is not
a proof that a claim is true.

For updates that change agent behavior, use
[review-gates.md](review-gates.md) after this evidence check. The evaluator can
flag weak support, but first-principles and adversarial review decide whether a
claim belongs in the skill at all.

## Command

```bash
source-to-skill eval-skill out/example-skill
```

For integrations:

```bash
source-to-skill eval-skill out/example-skill --json
```

To write a report:

```bash
source-to-skill eval-skill out/example-skill --out out/example-skill/eval-report.md
```

Mini Skill and Full Skill builds write `eval-report.md` automatically.

## Review Rule

Treat `weak` and `unsupported` rows as a prompt to revise or delete the guidance,
not as a prompt to add decorative evidence. If the source does not support a
claim, the claim should not be promoted into the skill.

If a claim is supported but changes core behavior, keep it pending until it also
passes the review gates:

- first-principles fit
- counterexamples
- contradiction review
- overgeneralization check
- boundary and failure-case review
