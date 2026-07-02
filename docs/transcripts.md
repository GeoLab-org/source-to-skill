# Transcript Cleanup

Meeting transcripts and voice notes often contain timing lines, filler words,
speaker noise, and one-off context. Sending that raw text straight into a skill
generator makes weak sources look stronger than they are.

`source-to-skill clean-transcript` performs a conservative cleanup before the
readiness gate runs.

If the source is audio, transcribe it first with `source-to-skill
transcribe-audio` or another transcription tool, then clean the transcript.

## What It Does

- removes SRT / VTT timing lines
- removes common English filler words
- removes a small set of common Chinese filler fragments
- preserves speaker labels when they are written as `Name: text`
- renders a Markdown file with numbered segments

## What It Does Not Do

- it does not summarize
- it does not invent structure
- it does not decide that a transcript deserves a full skill
- it does not replace human review for sensitive recordings

## Example

```bash
source-to-skill clean-transcript examples/meeting-transcript.vtt \
  --out out/clean-meeting.md \
  --title "Meeting Transcript"

source-to-skill analyze out/clean-meeting.md
```

The cleanup step should make the source easier to score, not more impressive
than it really is.
