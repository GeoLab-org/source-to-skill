"""Source-to-Skill: compile reusable knowledge into agent skills."""

from source_to_skill.analyzer import analyze_source, analyze_text
from source_to_skill.audio import transcribe_audio_file
from source_to_skill.builder import build_artifacts
from source_to_skill.demo import run_demo
from source_to_skill.evaluator import evaluate_skill
from source_to_skill.evolution import create_evolution_report, evolve_source
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
    "create_evolution_report",
    "evaluate_skill",
    "evolve_source",
    "fold_segment",
    "read_source",
    "run_demo",
    "split_source_text",
    "transcribe_audio_file",
]

__version__ = "0.3.0"
