from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from source_to_skill.analyzer import analyze_source
from source_to_skill.builder import build_artifacts, fold_seed
from source_to_skill.models import OutputLevel
from source_to_skill.templates import render_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="source-to-skill",
        description="Analyze source material and compile only reusable knowledge into agent-skill artifacts.",
    )
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

    return parser


def main(argv: list[str] | None = None) -> int:
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
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    parser.error("unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
