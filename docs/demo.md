# Demo Workflow

Run the bundled demo after installing the package:

```bash
source-to-skill demo --out out/demo
```

The demo runs the public workflow against the examples included in the repo:

- analyzes `examples/article.md`
- builds an article seed
- cleans `examples/meeting-transcript.vtt`
- splits the cleaned transcript into topic candidates
- builds one selected segment as a seed

The output directory contains:

- `demo-report.md`
- `article-readiness-report.md`
- `article-build/`
- `clean-meeting.md`
- `topics/topic-report.md`
- `segment-build/`

The demo is intentionally small. It is meant to show the gate, not to imply that
every source deserves a skill.
