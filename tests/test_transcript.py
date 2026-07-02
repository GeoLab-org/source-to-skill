from source_to_skill.transcript import clean_transcript_text


def test_clean_transcript_removes_srt_timestamps_and_preserves_speakers():
    raw = """
    WEBVTT

    1
    00:00:01,000 --> 00:00:03,000
    Alex: Um, when the review repeats, use a checklist.

    2
    00:00:04,000 --> 00:00:06,000
    Mina: You know, avoid turning one meeting into a full skill.
    """
    result = clean_transcript_text(raw, title="Review Transcript")
    assert "00:00" not in result.cleaned_text
    assert "## Segment 1 - Alex" in result.cleaned_text
    assert "When the review repeats" in result.cleaned_text
    assert "use a checklist" in result.cleaned_text
    assert "You know" not in result.cleaned_text
    assert result.removed_lines == 5
    assert result.segment_count == 2


def test_clean_transcript_handles_chinese_fillers():
    raw = "张三：嗯这个方案就是要先判断场景。\n李四：然后然后不要直接生成 full skill。"
    result = clean_transcript_text(raw, title="中文转写")
    assert "嗯" not in result.cleaned_text
    assert "就是" not in result.cleaned_text
    assert "然后然后" not in result.cleaned_text
    assert "先判断场景" in result.cleaned_text
