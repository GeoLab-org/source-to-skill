import json

from source_to_skill.builder import build_artifacts
from source_to_skill.cli import main
from source_to_skill.evaluator import evaluate_skill


def write_skill(skill_dir, guidance, evidence=None):
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text(
        "\n".join(
            [
                "# Evidence Skill",
                "",
                "## Core Guidance",
                *[f"- {item}" for item in guidance],
                "",
                "## Operating Rules",
                "- Keep claims grounded.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    if evidence is not None:
        references = skill_dir / "references"
        references.mkdir()
        (references / "evidence.md").write_text(evidence, encoding="utf-8")


def test_evaluate_skill_marks_supported_and_unsupported_guidance(tmp_path):
    skill = tmp_path / "skill"
    write_skill(
        skill,
        [
            "Compare source evidence before writing reusable guidance.",
            "Always schedule a launch party after every review.",
        ],
        "Evidence candidates show that teams should compare source evidence before writing guidance.",
    )

    report = evaluate_skill(skill)

    assert report.total_claims == 2
    assert report.supported_count == 1
    assert report.unsupported_count == 1
    assert report.checks[0].status == "supported"
    assert report.checks[1].status == "unsupported"
    assert "source" in report.checks[0].overlap_terms


def test_evaluate_skill_reports_missing_evidence_file(tmp_path):
    skill = tmp_path / "skill"
    write_skill(skill, ["Use evidence before publishing guidance."])

    report = evaluate_skill(skill)

    assert report.total_claims == 1
    assert report.unsupported_count == 1
    assert report.warnings == ("Missing references/evidence.md.",)
    assert report.checks[0].status == "unsupported"


def test_build_mini_writes_eval_report(tmp_path):
    source = tmp_path / "source.md"
    source.write_text(
        "# Review Playbook\n\n## Rules\n- Compare source evidence before publishing.\n- Avoid reusable claims without support.\n\n## Example\nFor example, keep guidance tied to source evidence.",
        encoding="utf-8",
    )

    target = build_artifacts(source, tmp_path / "out", level="mini")

    eval_report = target / "eval-report.md"
    assert eval_report.exists()
    assert "Skill Evaluation Report" in eval_report.read_text(encoding="utf-8")


def test_eval_skill_cli_outputs_json(tmp_path, capsys):
    skill = tmp_path / "skill"
    write_skill(
        skill,
        ["Compare source evidence before writing reusable guidance."],
        "Compare source evidence before writing reusable guidance.",
    )

    result = main(["eval-skill", str(skill), "--json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["total_claims"] == 1
    assert payload["supported_count"] == 1
