# Command Reference

`source-to-skill` is a conservative CLI. Most workflows should start with
`analyze` or `demo`, not `build`.

Install from GitHub:

```bash
python -m pip install "source-to-skill @ git+https://github.com/GeoLab-org/source-to-skill.git@v0.3.0"
```

Check the installed version:

```bash
source-to-skill --version
```

## Commands

| Command | Purpose | Typical output |
|---|---|---|
| `demo` | Run the bundled article and transcript workflow | `demo-report.md` plus example artifacts |
| `analyze` | Score one source before generating files | readiness report or JSON |
| `build` | Generate the recommended artifact level, or a forced level | note, seed, mini skill, or full skill |
| `fold` | Add a weak source as a seed under an existing skill | seed file in an existing skill folder |
| `evolve` | Compare a source with an existing skill before merging | pending update report or JSON |
| `split-source` | Split a long source into topic candidates | `topic-report.md` and segment files |
| `build-segment` | Build artifacts from one split segment | segment-derived artifact |
| `fold-segment` | Fold one split segment into an existing skill | segment seed in an existing skill folder |
| `clean-transcript` | Normalize SRT, VTT, or transcript text into Markdown | cleaned Markdown transcript |
| `transcribe-audio` | Run an installed Whisper-compatible CLI on audio | transcript file |
| `eval-skill` | Compare generated guidance against evidence | evaluation report or JSON |

## Common Workflows

Start with the bundled demo:

```bash
source-to-skill demo --out out/demo
```

Score a local source:

```bash
source-to-skill analyze examples/article.md
source-to-skill analyze examples/article.md --json
```

Score a local EPUB:

```bash
source-to-skill analyze path/to/book.epub
```

Build only after reading the score:

```bash
source-to-skill build examples/article.md --level auto --out out
```

Compare a new source with an existing skill before changing the skill:

```bash
source-to-skill evolve examples/article.md \
  examples/existing-skill/review-playbook-skill \
  --out out/evolution-demo
```

This writes a pending update under `out/evolution-demo/pending-updates/`.
It does not edit the target skill automatically.

Clean and score a transcript:

```bash
source-to-skill clean-transcript examples/meeting-transcript.vtt \
  --out out/clean-meeting.md \
  --title "Meeting Transcript"

source-to-skill analyze out/clean-meeting.md
```

Split a long transcript or article into candidates:

```bash
source-to-skill split-source out/clean-meeting.md --out out/topics
source-to-skill build-segment out/topics 2 --level seed --out out
```

Evaluate a generated skill:

```bash
source-to-skill eval-skill out/review-playbook
source-to-skill eval-skill out/review-playbook --json
```

## Notes

`transcribe-audio` does not ship a speech model. It calls an installed
Whisper-compatible command and writes the transcript to the path you choose.

Remote URL intake fetches one public text or HTML page. It does not crawl, log
in, or render JavaScript pages.

Weak material is expected to stop at `Note` or `Skill Seed`. That is a feature,
not a failure.
