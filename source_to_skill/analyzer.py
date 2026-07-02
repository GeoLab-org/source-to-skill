from __future__ import annotations

import re
from pathlib import Path

from source_to_skill.models import ReadinessReport
from source_to_skill.scoring import (
    count_headings,
    count_words,
    recommend_level,
    score_actionability,
    score_examples,
    score_length,
    score_noise,
    score_structure,
    score_transferability,
)


def read_source(path: str | Path) -> str:
    source_path = Path(path)
    try:
        return source_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return source_path.read_text(encoding="utf-8", errors="replace")


def analyze_source(path: str | Path) -> ReadinessReport:
    source_path = Path(path)
    return analyze_text(read_source(source_path), source_path=source_path)


def analyze_text(text: str, *, source_path: Path | None = None) -> ReadinessReport:
    normalized = normalize_text(text)
    word_count = count_words(normalized)
    heading_count = count_headings(normalized)
    signals = (
        score_length(word_count),
        score_structure(normalized, heading_count),
        score_actionability(normalized, word_count),
        score_transferability(normalized, word_count),
        score_examples(normalized, word_count),
        score_noise(normalized, word_count),
    )
    score = sum(signal.score for signal in signals)
    level = recommend_level(score, word_count)
    evidence = extract_evidence(normalized)
    return ReadinessReport(
        source_path=source_path,
        title=extract_title(normalized, source_path),
        score=score,
        level=level,
        signals=signals,
        reasons=build_reasons(signals),
        cautions=build_cautions(score, normalized, word_count),
        evidence=evidence,
        word_count=word_count,
        heading_count=heading_count,
    )


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return text.strip()


def extract_title(text: str, source_path: Path | None) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
        if stripped and len(stripped) <= 90:
            return stripped.strip("# ")
    if source_path is not None:
        return source_path.stem.replace("-", " ").replace("_", " ").title()
    return "Untitled Source"


def extract_evidence(text: str, limit: int = 5) -> tuple[str, ...]:
    candidates = []
    for paragraph in re.split(r"\n\s*\n", text):
        compact = " ".join(paragraph.split())
        if len(compact) < 60 or len(compact) > 360:
            continue
        lower = compact.lower()
        if any(term in lower for term in ("should", "must", "when", "if", "because", "avoid", "prefer")):
            candidates.append(compact)
        if len(candidates) >= limit:
            break
    return tuple(candidates)


def build_reasons(signals) -> tuple[str, ...]:
    strongest = sorted(signals, key=lambda signal: signal.score / signal.max_score, reverse=True)[:3]
    return tuple(f"{signal.name}: {signal.summary}" for signal in strongest)


def build_cautions(score: int, text: str, word_count: int) -> tuple[str, ...]:
    cautions = []
    if word_count < 600:
        cautions.append("Short sources usually make better seeds than standalone full skills.")
    if score < 60:
        cautions.append("Do not publish this as a full skill without more material or stronger examples.")
    if re.search(r"\b(confidential|private|salary|password|secret|api key|token)\b", text, re.IGNORECASE):
        cautions.append("Potentially sensitive material detected; review before publishing.")
    if not cautions:
        cautions.append("Review the generated skill before relying on it in real work.")
    return tuple(cautions)
