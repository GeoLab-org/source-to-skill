from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from pathlib import Path

from source_to_skill.analyzer import analyze_text, normalize_text
from source_to_skill.intake import is_url, read_source
from source_to_skill.models import ReadinessReport
from source_to_skill.templates import slugify


HEADING_RE = re.compile(r"^(#{1,3})\s+(.+?)\s*$")


@dataclass(frozen=True)
class SegmentCandidate:
    index: int
    title: str
    text: str
    report: ReadinessReport

    def to_dict(self) -> dict:
        return {
            "index": self.index,
            "title": self.title,
            "word_count": self.report.word_count,
            "score": self.report.score,
            "level": self.report.level.value,
            "level_label": self.report.level_label,
            "cautions": list(self.report.cautions),
        }


@dataclass(frozen=True)
class SplitArtifactsResult:
    output_dir: Path
    segments: tuple[SegmentCandidate, ...]

    def to_dict(self) -> dict:
        return {
            "output_dir": str(self.output_dir),
            "segment_count": len(self.segments),
            "segments": [segment.to_dict() for segment in self.segments],
        }


def split_source_text(text: str, *, source_name: str | None = None) -> tuple[SegmentCandidate, ...]:
    normalized = normalize_text(text)
    blocks = extract_heading_blocks(normalized) or extract_paragraph_blocks(normalized)
    candidates: list[SegmentCandidate] = []
    for index, (title, body) in enumerate(blocks, start=1):
        segment_text = f"# {title}\n\n{body.strip()}\n"
        source_ref = f"{source_name or 'source'}#segment-{index}"
        report = analyze_text(segment_text, source_path=source_ref)
        candidates.append(SegmentCandidate(index=index, title=title, text=segment_text, report=report))
    return tuple(candidates)


def write_split_artifacts(source: str | Path, output_dir: str | Path) -> SplitArtifactsResult:
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    source_text = read_source(source)
    segments = split_source_text(source_text, source_name=source_name(source))
    segments_dir = out_path / "segments"
    if segments_dir.exists():
        shutil.rmtree(segments_dir)
    segments_dir.mkdir()
    for segment in segments:
        filename = f"{segment.index:02d}-{slugify(segment.title)}.md"
        (segments_dir / filename).write_text(segment.text, encoding="utf-8")
    result = SplitArtifactsResult(output_dir=out_path, segments=segments)
    (out_path / "topic-report.md").write_text(render_topic_report(result), encoding="utf-8")
    return result


def extract_heading_blocks(text: str) -> list[tuple[str, str]]:
    lines = text.splitlines()
    heading_indexes = [
        (index, match.group(1), match.group(2).strip())
        for index, line in enumerate(lines)
        if (match := HEADING_RE.match(line.strip()))
    ]
    section_headings = [(index, title) for index, level, title in heading_indexes if level == "##"]
    if len(section_headings) < 2:
        return []

    blocks: list[tuple[str, str]] = []
    for position, (line_index, title) in enumerate(section_headings):
        next_index = section_headings[position + 1][0] if position + 1 < len(section_headings) else len(lines)
        body = "\n".join(lines[line_index + 1 : next_index]).strip()
        if body:
            blocks.append((title, body))
    return blocks


def extract_paragraph_blocks(text: str) -> list[tuple[str, str]]:
    blocks = []
    for paragraph in re.split(r"\n\s*\n", text):
        body = paragraph.strip()
        if not body or body.startswith("#"):
            continue
        title = title_from_text(body)
        blocks.append((title, body))
    return blocks or [("Whole Source", text)]


def title_from_text(text: str) -> str:
    compact = " ".join(text.split())
    sentence = re.split(r"[.!?。！？]", compact, maxsplit=1)[0]
    if len(sentence) > 64:
        sentence = sentence[:64].rsplit(" ", 1)[0]
    return sentence.strip("# ") or "Untitled Segment"


def source_name(source: str | Path) -> str:
    if is_url(source):
        return str(source)
    return Path(source).stem


def render_topic_report(result: SplitArtifactsResult) -> str:
    lines = [
        "# Topic Split Report",
        "",
        f"Segments: {len(result.segments)}",
        "",
        "| Segment | Score | Recommended output | Words |",
        "|---|---:|---|---:|",
    ]
    for segment in result.segments:
        lines.append(
            f"| {segment.index:02d}. {segment.title} | {segment.report.score} | "
            f"{segment.report.level_label} | {segment.report.word_count} |"
        )
    lines.extend(
        [
            "",
            "Review weak segments as notes or seeds. Do not promote a topic unless its own score and evidence support it.",
            "",
        ]
    )
    return "\n".join(lines)
