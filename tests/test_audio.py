from __future__ import annotations

import subprocess
from pathlib import Path

from source_to_skill.audio import transcribe_audio_file
from source_to_skill.cli import main


def test_transcribe_audio_uses_whisper_cli_and_writes_requested_output(tmp_path):
    audio = tmp_path / "meeting.m4a"
    audio.write_bytes(b"fake audio")
    out = tmp_path / "meeting.vtt"
    commands = []

    def fake_runner(command, *, check, capture_output, text):  # noqa: ARG001
        commands.append(command)
        output_dir = Path(command[command.index("--output_dir") + 1])
        output_dir.mkdir(exist_ok=True)
        (output_dir / "meeting.vtt").write_text(
            "WEBVTT\n\n00:00:00.000 --> 00:00:02.000\nUse a readiness gate.",
            encoding="utf-8",
        )
        return subprocess.CompletedProcess(command, 0, "", "")

    result = transcribe_audio_file(
        audio,
        out,
        engine="whisper",
        model="base",
        language="en",
        runner=fake_runner,
        which=lambda name: name,
        temp_dir=tmp_path,
    )

    assert out.exists()
    assert "Use a readiness gate" in out.read_text(encoding="utf-8")
    assert result.transcript_path == out
    command = commands[0]
    assert command[:2] == ["whisper", str(audio)]
    assert Path(command[command.index("--output_dir") + 1]).name == "transcribe-audio"
    assert command[command.index("--output_format") + 1] == "vtt"
    assert command[command.index("--model") + 1] == "base"
    assert command[command.index("--language") + 1] == "en"


def test_transcribe_audio_reports_missing_engine(tmp_path):
    audio = tmp_path / "meeting.m4a"
    audio.write_bytes(b"fake audio")
    out = tmp_path / "meeting.vtt"

    try:
        transcribe_audio_file(audio, out, which=lambda name: None)
    except RuntimeError as exc:
        assert "Transcription engine 'whisper' was not found" in str(exc)
    else:
        raise AssertionError("Expected missing engine to raise RuntimeError")


def test_transcribe_audio_cli_invokes_transcriber(tmp_path, monkeypatch, capsys):
    audio = tmp_path / "voice-note.m4a"
    audio.write_bytes(b"fake audio")
    out = tmp_path / "voice-note.vtt"

    def fake_transcribe(source, target, **kwargs):
        target.write_text("WEBVTT\n\nVoice note transcript.", encoding="utf-8")
        return type(
            "Result",
            (),
            {
                "audio_path": source,
                "transcript_path": target,
                "engine": kwargs["engine"],
                "command": ("whisper",),
            },
        )()

    monkeypatch.setattr("source_to_skill.cli.transcribe_audio_file", fake_transcribe)

    result = main(["transcribe-audio", str(audio), "--out", str(out), "--model", "base"])

    captured = capsys.readouterr()
    assert result == 0
    assert out.exists()
    assert "Transcribed audio" in captured.out
