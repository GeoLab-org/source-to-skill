# Scoring

The v0 scorer is deterministic and intentionally plain. It is a gate, not an
oracle.

## Signals

| Signal | Max | Meaning |
|---|---:|---|
| Source depth | 25 | More words usually provide more room for structure and evidence |
| Structure | 20 | Headings, bullets, and numbered lists make extraction safer |
| Actionability | 20 | Rule-like language suggests reusable behavior |
| Transferability | 15 | Reuse, workflow, checklist, and decision cues suggest future use |
| Evidence | 10 | Examples and cases reduce unsupported claims |
| Signal cleanliness | 10 | Conversational noise lowers confidence |

## Output-Level Mapping

Default score mapping:

| Score | Level |
|---:|---|
| 0-19 | Discard |
| 20-39 | Note |
| 40-59 | Skill Seed |
| 60-79 | Mini Skill |
| 80-100 | Full Skill |

Length caps prevent short sources from being promoted too far:

- under 120 words: at most Skill Seed
- under 600 words: at most Mini Skill
- under 2,500 words: at most Mini Skill

This is conservative on purpose. Dense short sources are often useful, but they
rarely deserve a full standalone skill.

## Why No LLM Scoring In v0

LLMs can be useful later, especially for evidence classification and claim
checking. The first version keeps scoring transparent so users can understand why
a source was promoted or held back.
