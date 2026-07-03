"""Source-to-Skill: compile reusable knowledge into agent skills."""

from source_to_skill.analyzer import analyze_source, analyze_text
from source_to_skill.audio import transcribe_audio_file
from source_to_skill.builder import build_artifacts
from source_to_skill.demo import run_demo
from source_to_skill.evaluator import evaluate_skill
from source_to_skill.intake import read_source
from source_to_skill.models import OutputLevel, ReadinessReport
from source_to_skill.segmenter import build_segment, fold_segment, split_source_text
from source_to_skill.transcript import clean_transcript_file, clean_transcript_text

__all__ = [
    "OutputLevel",
    "ReadinessReport",
    "analyze_source",
    "analyze_text",
    "build_segment",
    "build_artifacts",
    "clean_transcript_file",
    "clean_transcript_text",
    "evaluate_skill",
    "fold_segment",
    "read_source",
    "run_demo",
    "split_source_text",
    "transcribe_audio_file",
]

__version__ = "0.1.1"
