# Changelog

All notable changes to `source-to-skill` are recorded here.

## 0.2.0

- Added local EPUB intake using package metadata and spine XHTML chapters.
- Improved Chinese source scoring with CJK-aware length estimates and Chinese
  rule, example, transferability, and noise cues.
- Preserved Unicode titles in generated artifact paths.
- Tightened evidence candidate extraction to skip common front matter.

## 0.1.1

- Bundled demo examples inside the installed package so `source-to-skill demo`
  works from any directory.
- Added wheel build and installed-wheel smoke checks to CI.
- Documented direct GitHub installation with a pinned release tag.

## 0.1.0

Initial public release.

- Added conservative readiness scoring for local text and Markdown sources.
- Added multi-level artifact generation: Discard, Note, Skill Seed, Mini Skill,
  and Full Skill.
- Added local HTML and single-page remote text/HTML intake.
- Added transcript cleanup for SRT, VTT, and transcript-like text.
- Added optional audio transcription through an installed Whisper-compatible
  CLI.
- Added topic splitting for long sources and segment-level build/fold commands.
- Added evidence evaluation for generated Mini Skill and Full Skill artifacts.
- Added bundled demo workflow, example sources, SVG identity assets, and public
  documentation.
