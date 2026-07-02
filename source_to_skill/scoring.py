from __future__ import annotations

import re

from source_to_skill.models import OutputLevel, Signal


HEADING_RE = re.compile(r"^\s{0,3}(#{1,6}\s+.+|[A-Z][^\n]{3,80}\n[-=]{3,})", re.MULTILINE)
ACTION_RE = re.compile(
    r"\b(should|must|avoid|prefer|use|when|if|because|therefore|rule|principle|pattern|framework)\b",
    re.IGNORECASE,
)
EXAMPLE_RE = re.compile(
    r"\b(example|case|for instance|before|after|scenario|sample|evidence|story)\b",
    re.IGNORECASE,
)
TRANSFER_RE = re.compile(
    r"\b(reuse|repeat|whenever|in future|next time|workflow|playbook|checklist|decision|criteria)\b",
    re.IGNORECASE,
)
NOISE_RE = re.compile(
    r"\b(um|uh|haha|lol|okay okay|you know|sort of|kind of|anyway|meeting adjourned)\b",
    re.IGNORECASE,
)


def clamp(value: int, floor: int = 0, ceiling: int = 100) -> int:
    return max(floor, min(ceiling, value))


def count_words(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def count_headings(text: str) -> int:
    return len(HEADING_RE.findall(text))


def score_length(word_count: int) -> Signal:
    if word_count < 120:
        score = 4
        summary = "Very short source; unlikely to contain stable reusable knowledge."
    elif word_count < 600:
        score = 10
        summary = "Short source; can produce a note or seed when the signal is dense."
    elif word_count < 2500:
        score = 17
        summary = "Enough material for a seed or mini skill if the topic is focused."
    elif word_count < 12000:
        score = 22
        summary = "Substantial source; enough material for structured extraction."
    else:
        score = 25
        summary = "Large source; likely enough material for a full skill if coherent."
    return Signal("Source depth", score, 25, summary)


def score_structure(text: str, heading_count: int) -> Signal:
    bullets = len(re.findall(r"^\s*[-*]\s+", text, re.MULTILINE))
    numbered = len(re.findall(r"^\s*\d+[.)]\s+", text, re.MULTILINE))
    raw = heading_count * 3 + min(bullets + numbered, 25)
    score = clamp(raw, ceiling=20)
    if score >= 16:
        summary = "Clear sectioning and list structure."
    elif score >= 8:
        summary = "Some structure is present, but the hierarchy is thin."
    else:
        summary = "Little explicit structure; extraction will rely on prose cues."
    return Signal("Structure", score, 20, summary)


def score_actionability(text: str, word_count: int) -> Signal:
    hits = len(ACTION_RE.findall(text))
    density = hits / max(word_count, 1) * 1000
    score = clamp(round(density * 4), ceiling=20)
    if score >= 15:
        summary = "Many rule-like or decision-oriented phrases."
    elif score >= 8:
        summary = "Some actionable language appears."
    else:
        summary = "Few clear rules or decision cues."
    return Signal("Actionability", score, 20, summary)


def score_transferability(text: str, word_count: int) -> Signal:
    hits = len(TRANSFER_RE.findall(text))
    density = hits / max(word_count, 1) * 1000
    score = clamp(round(density * 5), ceiling=15)
    if score >= 11:
        summary = "The source points toward repeatable use."
    elif score >= 5:
        summary = "Some phrases suggest reusable workflow or criteria."
    else:
        summary = "Mostly local information; reuse case is not yet obvious."
    return Signal("Transferability", score, 15, summary)


def score_examples(text: str, word_count: int) -> Signal:
    hits = len(EXAMPLE_RE.findall(text))
    density = hits / max(word_count, 1) * 1000
    score = clamp(round(density * 5), ceiling=10)
    if score >= 7:
        summary = "Examples or evidence are visible."
    elif score >= 3:
        summary = "A few examples are present."
    else:
        summary = "Little example or evidence support."
    return Signal("Evidence", score, 10, summary)


def score_noise(text: str, word_count: int) -> Signal:
    hits = len(NOISE_RE.findall(text))
    density = hits / max(word_count, 1) * 1000
    penalty = clamp(round(density * 8), ceiling=10)
    score = 10 - penalty
    if score >= 8:
        summary = "Low visible noise."
    elif score >= 5:
        summary = "Some conversational noise; cleanup may be needed."
    else:
        summary = "High noise; do not generate a full skill without cleanup."
    return Signal("Signal cleanliness", score, 10, summary)


def recommend_level(score: int, word_count: int | None = None) -> OutputLevel:
    if word_count is not None:
        if word_count < 120 and score >= 60:
            return OutputLevel.SEED
        if word_count < 120 and score >= 20:
            return OutputLevel.NOTE
        if word_count < 600 and score >= 60:
            return OutputLevel.MINI
        if word_count < 2500 and score >= 80:
            return OutputLevel.MINI
    if score < 20:
        return OutputLevel.DISCARD
    if score < 40:
        return OutputLevel.NOTE
    if score < 60:
        return OutputLevel.SEED
    if score < 80:
        return OutputLevel.MINI
    return OutputLevel.FULL
