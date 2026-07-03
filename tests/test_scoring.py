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


def test_long_structured_source_can_become_full():
    sections = []
    for i in range(40):
        sections.append(
            f"""
            ## Pattern {i}

            When the source repeats across projects, use a clear decision rule
            because future agents need stable criteria. Prefer evidence before
            generation. Avoid promoting one-off context into a permanent skill.
            For example, a source bundle can include a rule, a scenario, a
            failure mode, and a checklist. The next time this task appears, the
            agent should check the evidence and apply the rule only when the
            scenario matches.

            - Use the rule when the user task matches the source topic.
            - Prefer a seed when examples are thin.
            - Avoid claims that the evidence does not support.
            - Check the workflow, decision, criteria, and future reuse case.
            """
        )
    report = analyze_text("# Long Playbook\n\n" + "\n".join(sections))
    assert report.word_count > 2500
    assert report.level == OutputLevel.FULL


def test_long_structured_chinese_source_can_become_full():
    sections = []
    for i in range(40):
        sections.append(
            f"""
            ## 模型 {i}

            当资料在多个场景反复出现时，应该先提炼判断原则，因为未来的
            agent 需要稳定标准。优先保留证据，避免把一次性的上下文变成
            永久规则。比如，一个案例可以包含原则、场景、失败模式和检查清单。
            下次遇到相似任务时，agent 应该检查证据，只在场景匹配时使用规则。

            - 使用规则前先确认任务是否匹配。
            - 案例不足时优先作为 seed。
            - 避免提出证据不支持的结论。
            - 检查流程、判断、标准和未来复用场景。
            """
        )
    report = analyze_text("# 中文方法论\n\n" + "\n".join(sections))
    assert report.word_count > 2500
    assert report.level == OutputLevel.FULL


def test_sensitive_content_adds_caution():
    report = analyze_text("# Notes\n\nThis private client note includes a secret.")
    assert any("sensitive" in caution.lower() for caution in report.cautions)


def test_report_serializes_to_dict():
    report = analyze_text("# Method\n\nWhen this repeats, use a checklist.")
    data = report.to_dict()
    assert data["title"] == "Method"
    assert data["level"] == report.level.value
    assert data["signals"][0]["name"] == "Source depth"
