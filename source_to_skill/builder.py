from __future__ import annotations

import shutil
from pathlib import Path

from source_to_skill.analyzer import analyze_source, read_source
from source_to_skill.models import OutputLevel, ReadinessReport
from source_to_skill.templates import (
    render_cheatsheet,
    render_evidence,
    render_note,
    render_report,
    render_seed,
    render_skill_md,
    render_smoke_questions,
    slugify,
)


def parse_level(value: str, report: ReadinessReport) -> OutputLevel:
    if value == "auto":
        return report.level
    try:
        return OutputLevel(value)
    except ValueError as exc:
        allowed = ", ".join(["auto", *[level.value for level in OutputLevel]])
        raise ValueError(f"Unknown level '{value}'. Expected one of: {allowed}") from exc


def build_artifacts(source: str | Path, output_dir: str | Path, *, level: str = "auto") -> Path:
    source_path = Path(source)
    out_path = Path(output_dir)
    source_text = read_source(source_path)
    report = analyze_source(source_path)
    selected = parse_level(level, report)
    target = out_path / slugify(report.title)
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    (target / "readiness-report.md").write_text(render_report(report), encoding="utf-8")

    if selected == OutputLevel.DISCARD:
        (target / "decision.md").write_text(
            "This source was not strong enough to generate a skill.\n",
            encoding="utf-8",
        )
    elif selected == OutputLevel.NOTE:
        (target / "note.md").write_text(render_note(report, source_text), encoding="utf-8")
    elif selected == OutputLevel.SEED:
        (target / "skill-seed.md").write_text(render_seed(report), encoding="utf-8")
    elif selected in {OutputLevel.MINI, OutputLevel.FULL}:
        full = selected == OutputLevel.FULL
        references = target / "references"
        references.mkdir()
        (target / "SKILL.md").write_text(render_skill_md(report, full=full), encoding="utf-8")
        (target / "cheatsheet.md").write_text(render_cheatsheet(report), encoding="utf-8")
        (references / "evidence.md").write_text(render_evidence(report), encoding="utf-8")
        if full:
            (references / "source.md").write_text(source_text, encoding="utf-8")
            evals = target / "evals"
            evals.mkdir()
            (evals / "smoke-questions.md").write_text(render_smoke_questions(report), encoding="utf-8")
    return target


def fold_seed(source: str | Path, existing_skill: str | Path) -> Path:
    source_path = Path(source)
    skill_path = Path(existing_skill)
    report = analyze_source(source_path)
    seeds = skill_path / "seeds"
    seeds.mkdir(parents=True, exist_ok=True)
    target = seeds / f"{slugify(report.title)}-seed.md"
    target.write_text(render_seed(report), encoding="utf-8")
    return target
