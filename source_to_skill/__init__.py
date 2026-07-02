"""Source-to-Skill: compile reusable knowledge into agent skills."""

from source_to_skill.analyzer import analyze_source, analyze_text
from source_to_skill.builder import build_artifacts
from source_to_skill.intake import read_source
from source_to_skill.models import OutputLevel, ReadinessReport
from source_to_skill.transcript import clean_transcript_file, clean_transcript_text

__all__ = [
    "OutputLevel",
    "ReadinessReport",
    "analyze_source",
    "analyze_text",
    "build_artifacts",
    "clean_transcript_file",
    "clean_transcript_text",
    "read_source",
]

__version__ = "0.1.0"
