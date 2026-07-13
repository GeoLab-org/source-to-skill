from source_to_skill.cli import main
from source_to_skill.evolution import create_evolution_report, evolve_source


def write_skill(tmp_path):
    skill = tmp_path / "product-positioning-skill"
    references = skill / "references"
    references.mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        "# Product Positioning\n\n"
        "## Core Guidance\n"
        "- Use product positioning to compare customer segments, differentiation, and market narrative.\n"
        "- Start narrow when the audience is unclear.\n",
        encoding="utf-8",
    )
    (references / "evidence.md").write_text(
        "# Evidence\n\n- Positioning needs customer evidence and clear differentiation.",
        encoding="utf-8",
    )
    return skill


def write_source(tmp_path):
    source = tmp_path / "positioning-article.md"
    source.write_text(
        "# Positioning Article\n\n"
        "Product positioning should compare customer segments, differentiation, and market narrative. "
        "Use customer evidence before choosing the positioning story. "
        "However, early products may need broad public attention before narrowing the audience.\n\n"
        "## Example\n\n"
        "For example, compare two customer segments and avoid claiming differentiation without evidence.",
        encoding="utf-8",
    )
    return source


def test_create_evolution_report_classifies_existing_skill_relationship(tmp_path):
    source = write_source(tmp_path)
    skill = write_skill(tmp_path)

    report = create_evolution_report(source, skill)

    assert report.relationship in {"contradiction", "refinement"}
    assert report.match.overlap_percent > 0
    assert report.first_principles
    assert report.adversarial_review
    assert "automatic edit" in " ".join(report.adversarial_review)


def test_evolve_source_writes_pending_update(tmp_path):
    source = write_source(tmp_path)
    skill = write_skill(tmp_path)

    target = evolve_source(source, skill, tmp_path / "out")

    assert target.exists()
    assert target.parent.name == "pending-updates"
    content = target.read_text(encoding="utf-8")
    assert "# Skill Update Review" in content
    assert "Recommended relationship" in content
    assert "## User Decision Needed" in content


def test_cli_evolve_writes_pending_update(tmp_path, capsys):
    source = write_source(tmp_path)
    skill = write_skill(tmp_path)

    result = main(["evolve", str(source), str(skill), "--out", str(tmp_path / "out")])

    captured = capsys.readouterr()
    assert result == 0
    assert "Created pending update" in captured.out
    assert list((tmp_path / "out" / "pending-updates").glob("*.md"))


def test_cli_evolve_json_prints_report(tmp_path, capsys):
    source = write_source(tmp_path)
    skill = write_skill(tmp_path)

    result = main(["evolve", str(source), str(skill), "--json"])

    captured = capsys.readouterr()
    assert result == 0
    assert '"relationship"' in captured.out
    assert '"match"' in captured.out
