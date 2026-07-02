from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from source_to_skill.intake import read_text


TIMESTAMP_RE = re.compile(
    r"^\s*(?:\d+\s*)?(?:\[?\d{1,2}:\d{2}(?::\d{2})?(?:[,.]\d{1,3})?\]?)"
    r"(?:\s*-->\s*\d{1,2}:\d{2}(?::\d{2})?(?:[,.]\d{1,3})?)?\s*$"
)
WEBVTT_RE = re.compile(r"^\s*(WEBVTT|Kind:|Language:|NOTE\b)", re.IGNORECASE)
SPEAKER_RE = re.compile(r"^\s*([A-Za-z][A-Za-z0-9 _.-]{0,40}|[\u4e00-\u9fff]{1,8})\s*[:：]\s*(.+)$")
FILLER_RE = re.compile(
    r"\b(um+|uh+|erm+|ah+|like|you know|sort of|kind of|basically|actually)\b[, ]*",
    re.IGNORECASE,
)
CHINESE_FILLERS = ("嗯", "呃", "额", "就是", "然后然后")


@dataclass(frozen=True)
class TranscriptCleanupResult:
    title: str
    cleaned_text: str
    removed_lines: int
    segment_count: int


def clean_transcript_file(path: str | Path, *, title: str | None = None) -> TranscriptCleanupResult:
    source_path = Path(path)
    return clean_transcript_text(read_text(source_path), title=title or source_path.stem.replace("-", " ").title())


def clean_transcript_text(text: str, *, title: str = "Clean Transcript") -> TranscriptCleanupResult:
    removed_lines = 0
    segments: list[tuple[str | None, str]] = []
    current_speaker: str | None = None
    current_parts: list[str] = []

    def flush() -> None:
        nonlocal current_parts, current_speaker
        joined = " ".join(part.strip() for part in current_parts if part.strip())
        joined = normalize_sentence(joined)
        if joined:
            segments.append((current_speaker, joined))
        current_parts = []

    for raw_line in text.replace("\r\n", "\n").replace("\r", "\n").splitlines():
        line = raw_line.strip()
        if not line:
            flush()
            current_speaker = None
            continue
        if should_drop_line(line):
            removed_lines += 1
            continue
        speaker_match = SPEAKER_RE.match(line)
        if speaker_match:
            flush()
            current_speaker = speaker_match.group(1).strip()
            current_parts.append(speaker_match.group(2).strip())
            continue
        current_parts.append(line)
    flush()

    rendered = render_clean_transcript(title, segments, removed_lines)
    return TranscriptCleanupResult(
        title=title,
        cleaned_text=rendered,
        removed_lines=removed_lines,
        segment_count=len(segments),
    )


def should_drop_line(line: str) -> bool:
    if line.isdigit():
        return True
    if TIMESTAMP_RE.match(line):
        return True
    if WEBVTT_RE.match(line):
        return True
    return False


def normalize_sentence(text: str) -> str:
    text = FILLER_RE.sub("", text)
    for filler in CHINESE_FILLERS:
        text = text.replace(filler, "")
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+([,.!?;:，。！？；：])", r"\1", text)
    return capitalize_first_alpha(text)


def capitalize_first_alpha(text: str) -> str:
    for index, char in enumerate(text):
        if char.isalpha() and char.isascii():
            return text[:index] + char.upper() + text[index + 1 :]
    return text


def render_clean_transcript(title: str, segments: list[tuple[str | None, str]], removed_lines: int) -> str:
    lines = [
        f"# {title}",
        "",
        "Source type: cleaned transcript",
        f"Segments: {len(segments)}",
        f"Removed timing/noise lines: {removed_lines}",
        "",
    ]
    for index, (speaker, body) in enumerate(segments, start=1):
        heading = f"## Segment {index}"
        if speaker:
            heading += f" - {speaker}"
        lines.extend([heading, "", body, ""])
    return "\n".join(lines).rstrip() + "\n"
