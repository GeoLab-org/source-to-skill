# Contributing

Thanks for taking the project seriously.

The main rule is: do not make weak sources look stronger than they are.

## Development Setup

```bash
git clone https://github.com/qiaozhi7426-gif/source-to-skill.git
cd source-to-skill
python -m venv .venv
. .venv/bin/activate
python -m pip install -e . pytest
python -m pytest -q
```

## What Makes A Good Contribution

Good changes usually improve one of these:

- readiness scoring accuracy
- clearer artifact boundaries
- evidence preservation
- source intake quality
- tests with realistic weak and strong examples
- documentation that reduces overclaiming

## What To Avoid

- Do not claim every source can become a full skill.
- Do not hide scoring logic behind an opaque model call.
- Do not add a new source type unless it normalizes into text before scoring.
- Do not add glossy marketing copy that makes the project sound magical.
- Do not mix private source examples into the public repo.

## Test Expectations

Add tests when changing scoring, output-level thresholds, or generated file
layouts.

Useful tests compare at least two cases:

- a weak source that should stay Note or Seed
- a strong source that can become Mini or Full Skill

## Copy Style

Keep prose direct and conservative. Prefer:

> This source is not strong enough for a full skill.

Over:

> Transform any knowledge into a powerful AI skill instantly.
