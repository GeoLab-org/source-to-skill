# Audio

Audio support is intentionally a thin bridge. `source-to-skill` does not bundle
a speech model. It can call an installed Whisper-compatible CLI, write a
transcript file, and then use the existing transcript cleanup and readiness gate.

## Command

```bash
source-to-skill transcribe-audio recording.m4a \
  --out out/recording.vtt \
  --model base \
  --language en
```

Then clean and score the transcript:

```bash
source-to-skill clean-transcript out/recording.vtt \
  --out out/recording-clean.md \
  --title "Recording Transcript"

source-to-skill analyze out/recording-clean.md
```

For long recordings, split the cleaned transcript before building:

```bash
source-to-skill split-source out/recording-clean.md --out out/recording-topics
source-to-skill build-segment out/recording-topics 2 --level seed --out out
```

If the source is strong enough:

```bash
source-to-skill build out/recording-clean.md --level auto --out out
```

## Product Boundary

The default posture for recordings should be conservative. A voice note or
meeting often contains useful local context, but not enough reusable judgment for
a standalone skill.

Prefer:

- `Note` for ordinary meeting context
- `Skill Seed` for one or two reusable rules
- `Mini Skill` only when the recording has a clear method, examples, and
  repeatable decision rules

For long recordings, make that decision per topic segment rather than for the
whole transcript.

## Requirements

Install a Whisper-compatible command line tool separately. The default command
name is `whisper`, but another executable can be passed:

```bash
source-to-skill transcribe-audio recording.m4a \
  --engine whisper \
  --out out/recording.vtt
```

The command writes `vtt`, `srt`, or `txt` transcripts.
