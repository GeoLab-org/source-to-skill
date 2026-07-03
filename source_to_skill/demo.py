from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

from source_to_skill.analyzer import analyze_source
from source_to_skill.builder import build_artifacts
from source_to_skill.segmenter import build_segment, write_split_artifacts
from source_to_skill.templates import render_report
from source_to_skill.transcript import clean_transcript_file


@dataclass(frozen=True)
class DemoResult:
    output_dir: Path
    article_report: Path
    article_build: Path
    cleaned_transcript: Path
    topics_dir: Path
    segment_build: Path
    selected_segment_index: int


def run_demo(output_dir: str | Path, *, examples_dir: str | Path = "examples") -> DemoResult:
    out_path = Path(output_dir)
    examples_path = Path(examples_dir)
    article = examples_path / "article.md"
    transcript = examples_path / "meeting-transcript.vtt"
    if not article.exists():
        raise FileNotFoundError(f"Missing demo article: {article}")
    if not transcript.exists():
        raise FileNotFoundError(f"Missing demo transcript: {transcript}")

    if out_path.exists():
        shutil.rmtree(out_path)
    out_path.mkdir(parents=True)

    article_report = out_path / "article-readiness-report.md"
    article_analysis = analyze_source(article)
    article_report.write_text(render_report(article_analysis), encoding="utf-8")
    article_build = build_artifacts(article, out_path / "article-build", level="seed")

    cleaned_transcript = out_path / "clean-meeting.md"
    clean_result = clean_transcript_file(transcript, title="Demo Meeting Transcript")
    cleaned_transcript.write_text(clean_result.cleaned_text, encoding="utf-8")

    topics_dir = out_path / "topics"
    split_result = write_split_artifacts(cleaned_transcript, topics_dir)
    selected_segment_index = select_demo_segment(split_result)
    segment_build_root = out_path / "segment-build"
    segment_build = build_segment(topics_dir, selected_segment_index, segment_build_root, level="seed")

    result = DemoResult(
        output_dir=out_path,
        article_report=article_report,
        article_build=article_build,
        cleaned_transcript=cleaned_transcript,
        topics_dir=topics_dir,
        segment_build=segment_build,
        selected_segment_index=selected_segment_index,
    )
    (out_path / "demo-report.md").write_text(render_demo_report(result), encoding="utf-8")
    return result


def select_demo_segment(split_result) -> int:
    if not split_result.segments:
        raise ValueError("Demo split did not produce any segments.")
    strongest = max(split_result.segments, key=lambda segment: (segment.report.score, segment.report.word_count))
    return strongest.index


def render_demo_report(result: DemoResult) -> str:
    return "\n".join(
        [
            "# Source-to-Skill Demo Report",
            "",
            "This demo runs the core public workflow on the bundled examples.",
            "",
            "## Outputs",
            f"- Article readiness report: `{result.article_report.relative_to(result.output_dir)}`",
            f"- Article seed build: `{result.article_build.relative_to(result.output_dir)}`",
            f"- Cleaned transcript: `{result.cleaned_transcript.relative_to(result.output_dir)}`",
            f"- Topic split report: `{(result.topics_dir / 'topic-report.md').relative_to(result.output_dir)}`",
            f"- Selected segment: `{result.selected_segment_index}`",
            f"- Segment seed build: `{result.segment_build.relative_to(result.output_dir)}`",
            "",
            "## Next Step",
            "Open the reports and compare what was built with what was only split or scored.",
            "",
        ]
    )
