from pathlib import Path

from source_to_skill.builder import build_artifacts, fold_seed


def test_build_seed_creates_seed_and_report(tmp_path):
    source = tmp_path / "source.md"
    source.write_text(
        "# Design Review\n\nWhen a review repeats, use a checklist. Avoid one-off rules.",
        encoding="utf-8",
    )
    target = build_artifacts(source, tmp_path / "out", level="seed")
    assert (target / "readiness-report.md").exists()
    assert (target / "skill-seed.md").exists()


def test_build_mini_creates_skill_files(tmp_path):
    source = tmp_path / "source.md"
    source.write_text(
        "# Review Playbook\n\n## Rules\n- Use clear criteria.\n- Avoid claims without evidence.\n\n## Example\nFor example, compare source evidence before writing.",
        encoding="utf-8",
    )
    target = build_artifacts(source, tmp_path / "out", level="mini")
    assert (target / "SKILL.md").exists()
    assert (target / "references" / "evidence.md").exists()
    assert (target / "cheatsheet.md").exists()


def test_fold_seed_adds_seed_to_existing_skill(tmp_path):
    source = tmp_path / "source.md"
    source.write_text("# Fold Me\n\nWhen useful, fold this into an existing skill.", encoding="utf-8")
    skill = tmp_path / "existing-skill"
    skill.mkdir()
    target = fold_seed(source, skill)
    assert target.exists()
    assert target.parent == skill / "seeds"
