<p align="center">
  <img src="assets/logo.svg" alt="source-to-skill logo" width="112">
</p>

# source-to-skill

[![CI](https://github.com/GeoLab-org/source-to-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/GeoLab-org/source-to-skill/actions/workflows/ci.yml)

Turn high-value long-form content into evolving AI skills.

把书、长视频、播客、访谈、课程、长文和资料集里真正可复用的方法论，沉淀进 AI agent 可以调用、可以审查、可以持续进化的 skill system。

You have saved the videos, read the books, clipped the podcasts, and collected
the PDFs. But when real work starts, most of that knowledge is still hard to use.

`source-to-skill` is an early open-source compiler for turning high-value source
material into the smallest useful skill-system update: a note, evidence, a skill
seed, a focused skill, or a proposed update to an existing skill.

Sources do not become skills by default.

内容默认不是 skill。内容先成为证据、增量或种子。只有稳定、可迁移、经过测试的方法，才应该升级成 skill。

It is not a summarizer.

摘要告诉你内容讲了什么。Skill 让 AI 在真实任务里调用这套方法。

Summaries tell you what the content said. Skills help an agent use the content
to do work. A skill system should also learn when a new source confirms,
refines, contradicts, or supersedes what it already knows.

![Source to Skill flow](assets/hero-diagram.svg)

## Why

Most AI tools summarize content. `source-to-skill` asks a stricter question:

Can this source improve a method an agent can actually use?

大多数内容工具把长内容压缩成摘要。但很多时候，真正的问题不是“我知不知道它讲了什么”，而是“我能不能在工作里用起来”。

A good source may contain frameworks, principles, decision rules, examples,
anti-patterns, and operating steps. A good skill should preserve those methods
with evidence, scope, and a clear output contract.

RAG helps an agent retrieve knowledge. Skills help an agent act with knowledge.
That means a skill needs more than text. It needs reusable judgment, evidence,
scope, and an output contract. It also needs maintenance: new sources should be
matched against existing skills before creating more files.

`source-to-skill` starts with a readiness gate before writing files. A weak
source should not become a confident-looking fake methodology. A related source
should usually become evidence, a refinement, or a pending update before it
becomes a brand-new skill.

## Why Not Just Summarize?

A summary compresses content. A skill operationalizes it.

普通总结可能会说：

> The speaker says products need clear positioning, user understanding, and
> differentiation.

A skill should make the method usable:

- when to use the positioning framework
- what information to collect first
- how to compare competing narratives
- how to test whether the difference is visible
- what evidence from the source supports the method
- where the method should not be used

这也是项目最核心的边界：不是把所有内容都包装成知识，也不是一篇内容生成一个 skill，而是让值得蒸馏的内容持续修正、补充和进化已有的能力系统。

## What Makes A Source Skill-Worthy?

A source is a good candidate when it contains:

- reusable judgment
- repeatable steps
- decision rules
- examples or cases
- clear boundaries
- transferable situations
- enough evidence to audit the generated guidance

A source is usually not a good candidate when it is mostly:

- news
- opinion fragments
- motivational content
- shallow listicles
- one-off meeting context
- unstructured personal notes

不是所有 source 都值得变成 skill。这个保守判断本身就是产品的一部分。

## Source To Delta, Not Source To Pile

The long-term direction is not "one source, one skill."

一篇博客、一场访谈、一个长视频，不应该默认生成一个新 skill。否则 skill 会越来越多、越来越重复、越来越难路由，最后变成另一个混乱的知识库。

Instead, each source should be classified by how it relates to the existing
skill system:

| Relationship | Meaning | Preferred action |
| --- | --- | --- |
| Duplicate | The source repeats what an existing skill already covers | Ignore or record as a weak reference |
| Evidence | The source supports an existing rule with a better example or quote | Add evidence without changing core guidance |
| Refinement | The source makes an existing rule more precise | Propose a targeted update |
| Contradiction | The source conflicts with an existing rule | Ask the user before merging |
| New Skill | The source contains a stable method that does not fit existing skills | Create a new mini/full skill |

New sources should become deltas first: evidence, refinements, contradictions,
or seeds. Only stable, reusable, well-tested patterns should become standalone
skills.

中文一句话：

> 内容先进化已有 skill，只有少数内容才创建新 skill。

## Skill Evolution Workflow

The intended evolution loop:

```text
Source
  -> extract method candidates
  -> match existing skills
  -> classify as duplicate / evidence / refinement / contradiction / new skill
  -> generate an update proposal
  -> ask the user at decision points
  -> run first-principles and adversarial review
  -> merge with evidence and changelog
  -> run evaluation
```

For example, a new article may overlap with an existing `product-positioning`
skill. Instead of creating another positioning skill, the tool should propose:

```text
Matched existing skill:
- product-positioning-skill (72% overlap)

Recommended action:
- refinement

Potential conflict:
- Existing rule: early products should start with narrow positioning.
- New source: early products may need broad public attention before narrowing.

Suggested merge:
- Treat early positioning as a temporary expression layer, not a fixed strategy.
- Add the new source as evidence and a boundary case.
```

The user should decide whether to merge, keep as a contradiction, or reject.

## First-Principles And Adversarial Review

Skill evolution needs an immune system.

`source-to-skill` should not only ask whether a source sounds useful. It should
challenge every proposed skill or update from two directions:

1. **First-principles test**: does this update preserve the core problem,
   method, and use case, or is it just adding attractive noise?
2. **Adversarial review**: where could this guidance fail, overgeneralize,
   contradict existing rules, or pretend to be better-supported than it is?

第一性原理测试负责问：

- 这个 skill 到底要帮 agent 做什么？
- 这条新规则是否真的服务这个核心任务？
- 它是方法的一部分，还是只是一个好看的观点？
- 换一个 source / 作者 / 场景后，它还能成立吗？

对抗式审查负责问：

- 有什么反例会击穿这条规则？
- 它和已有 skill 有没有冲突？
- 它是不是把一个局部案例包装成通用方法？
- 证据是否足够，还是 AI 自己补全了作者没说的话？
- 适用边界、失败条件、不要使用的场景是否清楚？

Proposed updates should pass these checks before they modify core guidance.
Otherwise they should stay as evidence, pending notes, contradictions, or
rejected updates.

See [docs/review-gates.md](docs/review-gates.md) for the review checklist and
pending-update report template.

## Example

Input:

A 90-minute interview about product positioning.

A summarizer might output:

> The speaker says products need clear positioning, user understanding, and
> differentiation.

`source-to-skill` first asks whether the reusable method already belongs in an
existing skill. If it is truly new, it may compile a new artifact:

```text
product-positioning-skill/
  SKILL.md
  cheatsheet.md
  references/evidence.md
  evals/smoke-questions.md
  eval-report.md
```

The generated or updated skill should help an agent:

- evaluate a product idea
- identify weak positioning
- compare competing narratives
- ask better customer interview questions
- pressure-test a go-to-market story

## Output Levels

![Output levels](assets/output-levels.svg)

| Level | Output | Use when |
|---|---|---|
| 0 | Discard | The source is too thin, local, or noisy |
| 1 | Note | The source has information, but little reusable judgment |
| 2 | Skill Seed | There are useful candidates, but not enough for a standalone skill |
| 3 | Mini Skill | The topic is focused and has enough rules/evidence for a small skill |
| 4 | Full Skill | The source is substantial, structured, and reusable |

`source-to-skill` does not promote every source into a full skill. A normal
meeting may only deserve a note. A short clip may only contain one useful seed.
A blog post may only refine an existing rule. A book, course, article series, or
dense expert interview may deserve a real skill toolkit.

中文理解：

- `Note`: 有信息，但还不是方法。
- `Skill Seed`: 有一两个可复用判断，适合并入已有 skill。
- `Mini Skill`: 有一个聚焦的方法，证据和边界基本清楚。
- `Full Skill`: 内容足够系统，可以独立成为工具包。

Future evolution levels should also include:

- `Evidence`: 支持已有判断，但不改核心方法。
- `Refinement`: 修正或精确化已有 skill。
- `Contradiction`: 和已有 skill 冲突，需要用户确认。

## Install

Install directly from GitHub:

```bash
python -m pip install "source-to-skill @ git+https://github.com/GeoLab-org/source-to-skill.git@v0.2.0"
source-to-skill --version
```

Or install an editable checkout for development:

```bash
git clone https://github.com/GeoLab-org/source-to-skill.git
cd source-to-skill
python -m pip install -e .
source-to-skill --version
```

## Usage

Run the bundled demo:

```bash
source-to-skill demo --out out/demo
```

See [docs/commands.md](docs/commands.md) for the full command reference and
[examples/README.md](examples/README.md) for the bundled example workflow.
Case behavior is summarized in [docs/case-studies.md](docs/case-studies.md).

Analyze first:

```bash
source-to-skill analyze examples/article.md
```

Analyze a remote article:

```bash
source-to-skill analyze https://example.com/article
```

Analyze a local EPUB:

```bash
source-to-skill analyze path/to/book.epub
```

Build the recommended artifact:

```bash
source-to-skill build examples/article.md --level auto --out out
```

Evaluate a generated skill against its evidence file:

```bash
source-to-skill eval-skill out/review-playbook --json
```

Force a skill seed:

```bash
source-to-skill build examples/meeting-transcript.md --level seed --out out
```

Fold a weak source into an existing skill:

```bash
source-to-skill fold examples/meeting-transcript.md ~/.codex/skills/design-review
```

Clean a transcript before scoring:

```bash
source-to-skill clean-transcript examples/meeting-transcript.vtt \
  --out out/clean-meeting.md \
  --title "Meeting Transcript"

source-to-skill analyze out/clean-meeting.md
```

Transcribe an audio file with an installed Whisper-compatible CLI:

```bash
source-to-skill transcribe-audio recording.m4a \
  --out out/recording.vtt \
  --model base
```

Split a long source into separately scored topic candidates:

```bash
source-to-skill split-source out/clean-meeting.md --out out/topics
```

Build or fold one useful segment:

```bash
source-to-skill build-segment out/topics 2 --level seed --out out
source-to-skill fold-segment out/topics 2 ~/.codex/skills/design-review
```

## What It Scores

The v0 scorer is intentionally transparent. It looks for:

- source depth
- section structure
- decision or rule language
- transferability cues
- examples or evidence
- visible conversational noise

It is not a claim of objective truth. It is a quality gate that makes weak inputs
harder to over-promote.

Generated Mini Skill and Full Skill artifacts also include `eval-report.md`, a
small check that compares `Core Guidance` bullets with `references/evidence.md`.
The same check can be run manually with `source-to-skill eval-skill`.

Evidence matters because a generated skill should not quietly invent a method
the source never supported. The goal is not just to create a useful-looking
artifact; the goal is to create something a human can review and an agent can
use without losing the source boundary.

## Example Report

```text
Skill Readiness: 85/100
Recommended output: Mini Skill

Why:
- Structure: clear sectioning and list structure
- Actionability: many rule-like phrases
- Evidence: examples are visible

Caution:
- Short sources usually make better seeds than standalone full skills
```

## Project Status

This is an early project.

The goal is not to turn every file into a fake methodology. The goal is to build
a careful compiler that can say:

- this source is too weak
- this source should only become a note
- this source has a few useful seeds
- this source contains a focused method
- this source is strong enough for a full skill toolkit
- this source should update an existing skill instead of creating a new one
- this source contradicts an existing skill and needs human review

The current version supports local UTF-8 text, Markdown, simple HTML, local
EPUB, single-page remote text/HTML URLs, transcript cleanup, and optional
Whisper-compatible audio transcription through an external CLI. It can split
long sources into separately scored topic candidates before building.

PDF, crawled websites, browser-only pages, and richer video workflows are left
for later intake plugins. The first job is to get the skill-worthiness gate
right.

The current CLI can already build and fold skill artifacts. The evolution layer
described above is the next product direction: source-to-delta, skill matching,
first-principles tests, adversarial review, user-reviewed updates, and skill
regression checks.

项目还早，但问题是真实的：我们每天都在消费高价值内容，却很少把它们变成 AI 可以在真实任务里调用、并且持续进化的能力。

## Design Principles

- Do not generate a full skill from every input.
- Do not create a new skill when the source should refine an existing one.
- Keep one-off context separate from reusable rules.
- Prefer a seed over a weak skill.
- Preserve evidence.
- Treat contradictions as review items, not automatic merges.
- Test every major update against first principles: core problem, method,
  use case, and boundary.
- Run adversarial review before changing core guidance.
- Make the generated artifact small enough to be read and reviewed.

See [docs/philosophy.md](docs/philosophy.md) and
[docs/output-levels.md](docs/output-levels.md). The scoring rules are documented
in [docs/scoring.md](docs/scoring.md). Intake support is documented in
[docs/intake.md](docs/intake.md). Transcript cleanup is documented in
[docs/transcripts.md](docs/transcripts.md). Audio transcription is documented in
[docs/audio.md](docs/audio.md). Topic splitting is documented in
[docs/splitting.md](docs/splitting.md). The bundled demo is documented in
[docs/demo.md](docs/demo.md). Skill evidence checks are documented in
[docs/evaluation.md](docs/evaluation.md). First-principles and adversarial
review gates are documented in [docs/review-gates.md](docs/review-gates.md).

## Roadmap

See [ROADMAP.md](ROADMAP.md).

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). The short version: improve the gate, do
not make weak sources look stronger than they are.

## License

MIT
