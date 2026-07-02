import textwrap

from source_to_skill.analyzer import analyze_text
from source_to_skill.models import OutputLevel


def test_short_meeting_becomes_note_or_seed():
    text = textwrap.dedent("""
    # Weekly Sync

    Okay, quick update. We talked about moving the meeting and checking the file.
    There is not much method here, mostly status and next steps.
    """)
    report = analyze_text(text)
    assert report.level in {OutputLevel.DISCARD, OutputLevel.NOTE, OutputLevel.SEED}
    assert report.score < 60


def test_structured_short_method_becomes_seed_or_mini():
    text = textwrap.dedent("""
    # Review Playbook

    ## Principle
    When a source contains reusable judgment, prefer a skill seed before a full skill.

    ## Rules
    - Use a full skill when the source has chapters, examples, and repeatable decisions.
    - Avoid publishing a full skill from one meeting because one-off context becomes noise.
    - Prefer folding weak sources into an existing skill.

    ## Example
    For example, a design review transcript can produce a decision rule, evidence, and a caution.
    The next time a similar review appears, the agent should check whether the rule still applies.

    ## Checklist
    1. Check the user.
    2. Check the recurring scenario.
    3. Check evidence.
    4. Check whether the output can guide a future task.
    """)
    report = analyze_text(text)
    assert report.level in {OutputLevel.SEED, OutputLevel.MINI}
    assert report.score >= 60


def test_short_structured_source_does_not_become_full():
    text = textwrap.dedent("""
    # Tiny Method

    ## Rule
    When a source is short, use a seed before a full skill.

    ## Example
    For example, one meeting can produce one rule.
    """)
    report = analyze_text(text)
    assert report.level != OutputLevel.FULL


def test_sensitive_content_adds_caution():
    report = analyze_text("# Notes\n\nThis private client note includes a secret.")
    assert any("sensitive" in caution.lower() for caution in report.cautions)
