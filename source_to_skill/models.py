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
