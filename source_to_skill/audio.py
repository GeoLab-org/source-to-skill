from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Callable


SUPPORTED_TRANSCRIPT_FORMATS = {"srt", "txt", "vtt"}


@dataclass(frozen=True)
class AudioTranscriptionResult:
    audio_path: Path
    transcript_path: Path
    engine: str
    command: tuple[str, ...]


Runner = Callable[..., subprocess.CompletedProcess]
Which = Callable[[str], str | None]


def transcribe_audio_file(
    audio_path: str | Path,
    transcript_path: str | Path,
    *,
    engine: str = "whisper",
    model: str | None = None,
    language: str | None = None,
    output_format: str = "vtt",
    runner: Runner = subprocess.run,
    which: Which = shutil.which,
    temp_dir: str | Path | None = None,
) -> AudioTranscriptionResult:
    if output_format not in SUPPORTED_TRANSCRIPT_FORMATS:
        allowed = ", ".join(sorted(SUPPORTED_TRANSCRIPT_FORMATS))
        raise ValueError(f"Unsupported transcript format '{output_format}'. Expected one of: {allowed}")

    executable = which(engine)
    if executable is None:
        raise RuntimeError(
            f"Transcription engine '{engine}' was not found. Install a Whisper-compatible CLI or pass --engine."
        )

    source = Path(audio_path)
    target = Path(transcript_path)
    target.parent.mkdir(parents=True, exist_ok=True)

    if temp_dir is None:
        with TemporaryDirectory(prefix="source-to-skill-") as tmp:
            return _run_transcription(
                executable,
                source,
                target,
                model=model,
                language=language,
                output_format=output_format,
                runner=runner,
                output_dir=Path(tmp) / "transcribe-audio",
            )

    return _run_transcription(
        executable,
        source,
        target,
        model=model,
        language=language,
        output_format=output_format,
        runner=runner,
        output_dir=Path(temp_dir) / "transcribe-audio",
    )


def _run_transcription(
    executable: str,
    source: Path,
    target: Path,
    *,
    model: str | None,
    language: str | None,
    output_format: str,
    runner: Runner,
    output_dir: Path,
) -> AudioTranscriptionResult:
    output_dir.mkdir(parents=True, exist_ok=True)
    command = build_whisper_command(
        executable,
        source,
        output_dir=output_dir,
        output_format=output_format,
        model=model,
        language=language,
    )
    runner(command, check=True, capture_output=True, text=True)
    generated = find_generated_transcript(output_dir, source, output_format)
    shutil.copyfile(generated, target)
    return AudioTranscriptionResult(
        audio_path=source,
        transcript_path=target,
        engine=Path(executable).name,
        command=tuple(command),
    )


def build_whisper_command(
    executable: str,
    source: Path,
    *,
    output_dir: Path,
    output_format: str,
    model: str | None,
    language: str | None,
) -> list[str]:
    command = [
        executable,
        str(source),
        "--output_dir",
        str(output_dir),
        "--output_format",
        output_format,
    ]
    if model:
        command.extend(["--model", model])
    if language:
        command.extend(["--language", language])
    return command


def find_generated_transcript(output_dir: Path, source: Path, output_format: str) -> Path:
    expected = output_dir / f"{source.stem}.{output_format}"
    if expected.exists():
        return expected
    matches = sorted(output_dir.glob(f"*.{output_format}"))
    if matches:
        return matches[0]
    raise FileNotFoundError(f"Transcription did not produce a .{output_format} file in {output_dir}")
