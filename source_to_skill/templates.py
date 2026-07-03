from __future__ import annotations

import re

from source_to_skill.models import OutputLevel, ReadinessReport


def slugify(value: str) -> str:
    slug = re.sub(r"[^\w]+", "-", value.lower(), flags=re.UNICODE).strip("-_")
    return slug or "source-skill"


def render_report(report: ReadinessReport) -> str:
    lines = [
        f"# Skill Readiness Report: {report.title}",
        "",
        f"**Score:** {report.score}/100",
        f"**Recommended output:** {report.level_label}",
        f"**Words:** {report.word_count}",
        f"**Headings:** {report.heading_count}",
        "",
        "## Signals",
    ]
    for signal in report.signals:
        lines.append(f"- **{signal.name}:** {signal.score}/{signal.max_score} — {signal.summary}")
    lines.extend(["", "## Why"])
    lines.extend(f"- {reason}" for reason in report.reasons)
    lines.extend(["", "## Cautions"])
    lines.extend(f"- {caution}" for caution in report.cautions)
    if report.evidence:
        lines.extend(["", "## Evidence Candidates"])
        lines.extend(f"- {item}" for item in report.evidence)
    lines.extend(["", "## Next Action", next_action(report.level), ""])
    return "\n".join(lines)


def next_action(level: OutputLevel) -> str:
    return {
        OutputLevel.DISCARD: "Do not generate a skill. Keep nothing or save a short note only if the source has archival value.",
        OutputLevel.NOTE: "Create a note. The source has information, but not enough reusable judgment for a skill.",
        OutputLevel.SEED: "Create a skill seed and collect more related sources before publishing a standalone skill.",
        OutputLevel.MINI: "Create a mini skill with a tight scope, evidence file, and smoke questions.",
        OutputLevel.FULL: "Create a full skill with references, indexes, and evaluation questions.",
    }[level]


def render_note(report: ReadinessReport, source_text: str) -> str:
    return "\n".join(
        [
            f"# Note: {report.title}",
            "",
            "This source was not strong enough for a standalone skill, but it may be useful as a reference note.",
            "",
            f"- Readiness score: {report.score}/100",
            f"- Recommended output: {report.level_label}",
            "",
            "## Useful Signals",
            *(f"- {reason}" for reason in report.reasons),
            "",
            "## Source Excerpt",
            excerpt(source_text),
            "",
        ]
    )


def render_seed(report: ReadinessReport) -> str:
    evidence = report.evidence or ("No strong evidence snippets were detected; review the source manually.",)
    return "\n".join(
        [
            f"# Skill Seed: {report.title}",
            "",
            "This seed captures reusable knowledge candidates. It is not yet a standalone skill.",
            "",
            f"- Readiness score: {report.score}/100",
            "- Recommended next step: merge with related sources or fold into an existing skill.",
            "",
            "## Reusable Judgment Candidates",
            *(f"- {item}" for item in evidence),
            "",
            "## What Not To Promote Yet",
            "- Do not treat one-off context as a permanent rule.",
            "- Do not publish as a full skill until the use case and examples are stronger.",
            "",
        ]
    )


def render_skill_md(report: ReadinessReport, *, full: bool) -> str:
    skill_name = slugify(report.title)
    scope = "full reference skill" if full else "focused mini skill"
    return "\n".join(
        [
            "---",
            f"name: {skill_name}",
            f'description: "A {scope} compiled from {report.title}. Use when working with the source topic, its decision rules, and its reusable patterns. Read references before making claims beyond the evidence."',
            "---",
            "",
            f"# {report.title}",
            "",
            "## Use This Skill When",
            "- The task matches the source topic.",
            "- You need reusable judgment, not a generic summary.",
            "- You can ground the answer in the included evidence.",
            "",
            "## Core Guidance",
            *(f"- {item}" for item in (report.evidence or report.reasons)),
            "",
            "## Operating Rules",
            "- Read `references/evidence.md` before citing the source.",
            "- State uncertainty when the source does not support a claim.",
            "- Keep one-off context separate from reusable rules.",
            "- Prefer a compact answer with the decision, evidence, and next action.",
            "",
            "## Supporting Files",
            "- `references/evidence.md` — source-backed snippets and reasoning candidates.",
            "- `cheatsheet.md` — quick decision rules extracted from the source.",
            *(["- `references/source.md` — the original source text for verification."] if full else []),
            *(["- `evals/smoke-questions.md` — basic questions to test whether the skill works."] if full else []),
            "",
        ]
    )


def render_evidence(report: ReadinessReport) -> str:
    return "\n".join(
        [
            f"# Evidence: {report.title}",
            "",
            f"Readiness score: {report.score}/100",
            "",
            "## Evidence Candidates",
            *(f"- {item}" for item in (report.evidence or ("No automatic evidence candidates found.",))),
            "",
            "## Cautions",
            *(f"- {item}" for item in report.cautions),
            "",
        ]
    )


def render_cheatsheet(report: ReadinessReport) -> str:
    return "\n".join(
        [
            f"# Cheatsheet: {report.title}",
            "",
            "| Situation | Use | Check |",
            "|---|---|---|",
            "| The source has clear evidence | Apply the extracted rule | Can you point to `references/evidence.md`? |",
            "| The source is thin or local | Treat it as a seed | Is this reusable beyond one context? |",
            "| The source contradicts the task | Do not force-fit it | What does the source actually say? |",
            "",
        ]
    )


def render_smoke_questions(report: ReadinessReport) -> str:
    return "\n".join(
        [
            f"# Smoke Questions: {report.title}",
            "",
            "Use these after generation to check whether the skill is useful.",
            "",
            "1. What reusable rules does this source actually support?",
            "2. What should the agent avoid claiming from this source?",
            "3. Which evidence snippets support the main guidance?",
            "4. What is a realistic task where this skill should be used?",
            "5. What task is outside this skill's scope?",
            "",
        ]
    )


def excerpt(text: str, limit: int = 1200) -> str:
    compact = text.strip()
    if len(compact) <= limit:
        return compact
    return compact[:limit].rstrip() + "\n\n..."
