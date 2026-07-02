from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class OutputLevel(str, Enum):
    DISCARD = "discard"
    NOTE = "note"
    SEED = "seed"
    MINI = "mini"
    FULL = "full"

    @property
    def label(self) -> str:
        return {
            OutputLevel.DISCARD: "Discard",
            OutputLevel.NOTE: "Note",
            OutputLevel.SEED: "Skill Seed",
            OutputLevel.MINI: "Mini Skill",
            OutputLevel.FULL: "Full Skill",
        }[self]


@dataclass(frozen=True)
class Signal:
    name: str
    score: int
    max_score: int
    summary: str

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "score": self.score,
            "max_score": self.max_score,
            "summary": self.summary,
        }


@dataclass(frozen=True)
class ReadinessReport:
    source_path: Path | None
    title: str
    score: int
    level: OutputLevel
    signals: tuple[Signal, ...]
    reasons: tuple[str, ...]
    cautions: tuple[str, ...]
    evidence: tuple[str, ...]
    word_count: int
    heading_count: int

    @property
    def level_label(self) -> str:
        return self.level.label

    def to_dict(self) -> dict:
        return {
            "source_path": str(self.source_path) if self.source_path else None,
            "title": self.title,
            "score": self.score,
            "level": self.level.value,
            "level_label": self.level_label,
            "signals": [signal.to_dict() for signal in self.signals],
            "reasons": list(self.reasons),
            "cautions": list(self.cautions),
            "evidence": list(self.evidence),
            "word_count": self.word_count,
            "heading_count": self.heading_count,
        }
