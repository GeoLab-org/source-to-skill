from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from source_to_skill import __version__
from source_to_skill.analyzer import analyze_source
from source_to_skill.audio import SUPPORTED_TRANSCRIPT_FORMATS, transcribe_audio_file
from source_to_skill.builder import build_artifacts, fold_seed
from source_to_skill.demo import run_demo
from source_to_skill.evaluator import evaluate_skill, render_eval_report
from source_to_skill.models import OutputLevel
from source_to_skill.segmenter import build_segment, fold_segment, write_split_artifacts
from source_to_skill.templates import render_report
from source_to_skill.transcript import clean_transcript_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="source-to-skill",
        description="Analyze source material and compile only reusable knowledge into agent-skill artifacts.",
    )
    parser.add_argument("--version", action="version", version=f"source-to-skill {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze = subparsers.add_parser("analyze", help="score a source before generating anything")
    analyze.add_argument("source", help="path to a UTF-8 text or Markdown source")
    analyze.add_argument("--out", help="optional path to write readiness-report.md")
    analyze.add_argument("--json", action="store_true", help="print a machine-readable JSON report")

    build = subparsers.add_parser("build", help="generate note, seed, mini skill, or full skill artifacts")
    build.add_argument("source", help="path to a UTF-8 text or Markdown source")
    build.add_argument("--out", default="out", help="output directory (default: out)")
    build.add_argument(
        "--level",
        default="auto",
        choices=["auto", *[level.value for level in OutputLevel]],
        help="artifact level to generate (default: auto)",
    )

    fold = subparsers.add_parser("fold", help="add a source as a seed under an existing skill")
    fold.add_argument("source", help="path to a UTF-8 text or Markdown source")
    fold.add_argument("skill", help="path to an existing skill folder")

    split = subparsers.add_parser("split-source", help="split a long source into separately scored topic candidates")
    split.add_argument("source", help="path or URL to a source")
    split.add_argument("--out", required=True, help="output directory for topic-report.md and segment files")
    split.add_argument("--json", action="store_true", help="print a machine-readable split report")

    build_segment_parser = subparsers.add_parser("build-segment", help="build artifacts from a split-source segment")
    build_segment_parser.add_argument("split_dir", help="directory created by split-source")
    build_segment_parser.add_argument("index", type=int, help="1-based segment index to build")
    build_segment_parser.add_argument("--out", default="out", help="output directory (default: out)")
    build_segment_parser.add_argument(
        "--level",
        default="auto",
        choices=["auto", *[level.value for level in OutputLevel]],
        help="artifact level to generate (default: auto)",
    )

    fold_segment_parser = subparsers.add_parser("fold-segment", help="fold a split-source segment into an existing skill")
    fold_segment_parser.add_argument("split_dir", help="directory created by split-source")
    fold_segment_parser.add_argument("index", type=int, help="1-based segment index to fold")
    fold_segment_parser.add_argument("skill", help="path to an existing skill folder")

    clean = subparsers.add_parser("clean-transcript", help="clean transcript, SRT, or VTT text into Markdown")
    clean.add_argument("source", help="path to a transcript-like text file")
    clean.add_argument("--out", required=True, help="output Markdown path")
    clean.add_argument("--title", help="title to use in the cleaned transcript")

    transcribe = subparsers.add_parser("transcribe-audio", help="transcribe an audio file with an installed Whisper CLI")
    transcribe.add_argument("source", help="path to an audio file")
    transcribe.add_argument("--out", required=True, help="path to write the transcript")
    transcribe.add_argument("--engine", default="whisper", help="transcription CLI executable (default: whisper)")
    transcribe.add_argument("--model", help="optional model name passed to the engine")
    transcribe.add_argument("--language", help="optional language code passed to the engine")
    transcribe.add_argument(
        "--format",
        default="vtt",
        choices=sorted(SUPPORTED_TRANSCRIPT_FORMATS),
        help="transcript format to request (default: vtt)",
    )

    eval_skill = subparsers.add_parser("eval-skill", help="check generated skill claims against evidence")
    eval_skill.add_argument("skill", help="path to a generated skill folder")
    eval_skill.add_argument("--out", help="optional path to write eval-report.md")
    eval_skill.add_argument("--json", action="store_true", help="print a machine-readable evaluation report")

    demo = subparsers.add_parser("demo", help="run the bundled end-to-end demo workflow")
    demo.add_argument("--out", default="out/demo", help="output directory (default: out/demo)")
    demo.add_argument("--examples", help="optional examples directory override")

    return parser


def main(argv: list[str] | None = None) -> int:
    if argv == ["--version"]:
        print(f"source-to-skill {__version__}")
        return 0
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "analyze":
            report = analyze_source(args.source)
            rendered = json.dumps(report.to_dict(), ensure_ascii=False, indent=2) if args.json else render_report(report)
            if args.out:
                Path(args.out).write_text(rendered, encoding="utf-8")
            else:
                print(rendered)
            return 0
        if args.command == "build":
            target = build_artifacts(args.source, args.out, level=args.level)
            print(f"Created {target}")
            return 0
        if args.command == "fold":
            target = fold_seed(args.source, args.skill)
            print(f"Added seed {target}")
            return 0
        if args.command == "split-source":
            result = write_split_artifacts(args.source, args.out)
            if args.json:
                print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
            else:
                print(f"Split source into {len(result.segments)} segments at {result.output_dir}")
            return 0
        if args.command == "build-segment":
            target = build_segment(args.split_dir, args.index, args.out, level=args.level)
            print(f"Built segment {args.index} into {target}")
            return 0
        if args.command == "fold-segment":
            target = fold_segment(args.split_dir, args.index, args.skill)
            print(f"Folded segment {args.index} into {target}")
            return 0
        if args.command == "clean-transcript":
            result = clean_transcript_file(args.source, title=args.title)
            out_path = Path(args.out)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(result.cleaned_text, encoding="utf-8")
            print(f"Cleaned transcript {out_path} ({result.segment_count} segments, {result.removed_lines} removed lines)")
            return 0
        if args.command == "transcribe-audio":
            out_path = Path(args.out)
            result = transcribe_audio_file(
                Path(args.source),
                out_path,
                engine=args.engine,
                model=args.model,
                language=args.language,
                output_format=args.format,
            )
            print(f"Transcribed audio {result.audio_path} -> {result.transcript_path} using {result.engine}")
            return 0
        if args.command == "eval-skill":
            report = evaluate_skill(args.skill)
            rendered = json.dumps(report.to_dict(), ensure_ascii=False, indent=2) if args.json else render_eval_report(report)
            if args.out:
                Path(args.out).write_text(rendered, encoding="utf-8")
            else:
                print(rendered)
            return 0
        if args.command == "demo":
            result = run_demo(args.out, examples_dir=args.examples)
            print(f"Demo written to {result.output_dir}")
            return 0
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    parser.error("unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
