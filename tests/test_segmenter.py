from __future__ import annotations

import json

from source_to_skill.cli import main
from source_to_skill.segmenter import split_source_text, write_split_artifacts


def test_split_source_text_scores_heading_sections_independently():
    text = """
    # Meeting Notes

    ## Chatter

    We talked about lunch and parking. No reusable decision was made.

    ## Review Rule

    When design reviews repeat, use a checklist before generating a skill.
    The checklist should compare the source evidence, identify reusable
    judgment, and avoid turning one-off meeting context into a full skill.
    For example, a repeated client redline can become a seed, but a casual
    reminder should stay as a note.
    """

    candidates = split_source_text(text, source_name="meeting-notes")

    assert [candidate.title for candidate in candidates] == ["Chatter", "Review Rule"]
    assert candidates[0].report.score < candidates[1].report.score
    assert candidates[0].report.level.value in {"discard", "note", "seed"}
    assert candidates[1].report.word_count > candidates[0].report.word_count


def test_write_split_artifacts_creates_report_and_segment_files(tmp_path):
    source = tmp_path / "meeting.md"
    source.write_text(
        """
        # Voice Note

        ## Local Update

        We discussed schedule context. It is useful for the team, but not reusable.

        ## Reusable Method

        When a recording contains a durable method, split it before building.
        The method should preserve evidence, score each topic, and prefer a
        seed over a weak standalone skill.
        """,
        encoding="utf-8",
    )

    result = write_split_artifacts(source, tmp_path / "out")

    assert (result.output_dir / "topic-report.md").exists()
    assert (result.output_dir / "segments" / "01-local-update.md").exists()
    assert (result.output_dir / "segments" / "02-reusable-method.md").exists()
    report = (result.output_dir / "topic-report.md").read_text(encoding="utf-8")
    assert "Reusable Method" in report
    assert "Recommended output" in report


def test_write_split_artifacts_preserves_sibling_files(tmp_path):
    source = tmp_path / "meeting.md"
    source.write_text(
        """
        # Voice Note

        ## Useful Rule

        When a recording contains a durable method, split it before building.

        ## Another Rule

        When a topic is thin, keep it as a note or seed.
        """,
        encoding="utf-8",
    )
    out = tmp_path / "out"
    sibling = out / "manual-notes.md"
    out.mkdir()
    sibling.write_text("keep this", encoding="utf-8")

    write_split_artifacts(source, out)

    assert sibling.read_text(encoding="utf-8") == "keep this"


def test_split_source_cli_can_print_json(tmp_path, capsys):
    source = tmp_path / "meeting.md"
    source.write_text(
        """
        # Meeting

        ## Thin Context

        No reusable decision.

        ## Useful Rule

        When a source has repeatable decisions, split it into smaller topics.
        Each topic should be scored before it is promoted into a skill.
        """,
        encoding="utf-8",
    )

    result = main(["split-source", str(source), "--out", str(tmp_path / "split"), "--json"])

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["segment_count"] == 2
    assert payload["segments"][1]["title"] == "Useful Rule"
    assert (tmp_path / "split" / "segments" / "02-useful-rule.md").exists()


def test_build_segment_cli_builds_selected_segment(tmp_path):
    source = tmp_path / "meeting.md"
    source.write_text(
        """
        # Meeting

        ## Thin Context

        No reusable decision.

        ## Useful Rule

        When a source has repeatable decisions, split it into smaller topics.
        Each topic should be scored before it is promoted into a skill.
        """,
        encoding="utf-8",
    )
    split_dir = tmp_path / "split"
    write_split_artifacts(source, split_dir)

    result = main(["build-segment", str(split_dir), "2", "--out", str(tmp_path / "built"), "--level", "seed"])

    assert result == 0
    assert (tmp_path / "built" / "useful-rule" / "skill-seed.md").exists()


def test_fold_segment_cli_folds_selected_segment_into_existing_skill(tmp_path):
    source = tmp_path / "meeting.md"
    source.write_text(
        """
        # Meeting

        ## Thin Context

        No reusable decision.

        ## Useful Rule

        When a source has repeatable decisions, split it into smaller topics.
        Each topic should be scored before it is promoted into a skill.
        """,
        encoding="utf-8",
    )
    split_dir = tmp_path / "split"
    skill_dir = tmp_path / "existing-skill"
    skill_dir.mkdir()
    write_split_artifacts(source, split_dir)

    result = main(["fold-segment", str(split_dir), "2", str(skill_dir)])

    assert result == 0
    assert (skill_dir / "seeds" / "useful-rule-seed.md").exists()
