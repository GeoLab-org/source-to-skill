from __future__ import annotations

from source_to_skill.cli import main
from source_to_skill.demo import run_demo


def write_demo_examples(examples_dir):
    examples_dir.mkdir()
    (examples_dir / "article.md").write_text(
        """
        # Review Playbook

        ## Rule

        When a source contains repeatable decisions, score it before building.
        The artifact should preserve evidence, avoid unsupported claims, and
        prefer a seed over a weak full skill.

        ## Example

        For example, one reusable review rule can become a seed while local
        project chatter remains a note.
        """,
        encoding="utf-8",
    )
    (examples_dir / "meeting-transcript.vtt").write_text(
        """
        WEBVTT

        1
        00:00:01.000 --> 00:00:04.000
        Alex: When a meeting has one reusable rule, split the transcript first.

        2
        00:00:04.500 --> 00:00:08.000
        Mina: The useful rule should become a seed, not a full skill.
        """,
        encoding="utf-8",
    )


def test_run_demo_creates_end_to_end_outputs(tmp_path):
    examples_dir = tmp_path / "examples"
    write_demo_examples(examples_dir)

    result = run_demo(tmp_path / "demo", examples_dir=examples_dir)

    assert (result.output_dir / "demo-report.md").exists()
    assert result.article_build.exists()
    assert result.cleaned_transcript.exists()
    assert (result.topics_dir / "topic-report.md").exists()
    assert (result.segment_build / "skill-seed.md").exists()
    assert result.selected_segment_index >= 1


def test_demo_cli_runs_workflow(tmp_path):
    examples_dir = tmp_path / "examples"
    write_demo_examples(examples_dir)

    result = main(["demo", "--out", str(tmp_path / "demo"), "--examples", str(examples_dir)])

    assert result == 0
    assert (tmp_path / "demo" / "demo-report.md").exists()
    assert (tmp_path / "demo" / "topics" / "topic-report.md").exists()
