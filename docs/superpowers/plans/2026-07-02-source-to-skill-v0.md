# Source-to-Skill v0 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a polished open-source v0.1 repository for `source-to-skill`, a CLI that analyzes source material, scores whether it deserves an agent skill, and generates Note, Skill Seed, Mini Skill, or Full Skill artifacts.

**Architecture:** Keep the first version deterministic and readable: parse local text-like files, compute transparent readiness signals, and render templates. Avoid pretending arbitrary content is high quality; the core product surface is the readiness gate.

**Tech Stack:** Python 3.10+, standard library, pytest, SVG assets, GitHub Actions.

---

### Task 1: Repository Skeleton

**Files:**
- Create: `README.md`
- Create: `pyproject.toml`
- Create: `LICENSE`
- Create: `.gitignore`
- Create: `.github/workflows/ci.yml`
- Create: `source_to_skill/__init__.py`
- Create: `source_to_skill/cli.py`

- [ ] **Step 1: Create package and metadata files**

Create a Python package named `source-to-skill` with console script `source-to-skill = source_to_skill.cli:main`.

- [ ] **Step 2: Add a minimal CLI**

Implement subcommands `analyze`, `build`, and `fold` with argparse. `analyze` reads a local source and prints a readiness report.

- [ ] **Step 3: Add CI**

Run `python -m pytest` in GitHub Actions.

### Task 2: Readiness Analyzer

**Files:**
- Create: `source_to_skill/models.py`
- Create: `source_to_skill/analyzer.py`
- Create: `source_to_skill/scoring.py`
- Test: `tests/test_scoring.py`

- [ ] **Step 1: Define output levels**

Represent output levels as `discard`, `note`, `seed`, `mini`, and `full`.

- [ ] **Step 2: Implement deterministic signals**

Score source length, heading structure, action-rule language, example density, transferability language, and noise markers.

- [ ] **Step 3: Recommend an output level**

Map readiness scores to output levels: `<20 discard`, `<40 note`, `<60 seed`, `<80 mini`, `>=80 full`.

### Task 3: Artifact Builder

**Files:**
- Create: `source_to_skill/builder.py`
- Create: `source_to_skill/templates.py`
- Test: `tests/test_builder.py`

- [ ] **Step 1: Build Note and Seed outputs**

Render simple Markdown artifacts with evidence snippets and recommended next action.

- [ ] **Step 2: Build Mini and Full Skill outputs**

Create `SKILL.md`, `references/evidence.md`, `cheatsheet.md`, and for full skills also `references/source.md` plus `evals/smoke-questions.md`.

- [ ] **Step 3: Keep copy human**

Write sober Markdown: no hype, no AI-magic language, no claims that every input is skill-worthy.

### Task 4: Documentation and Examples

**Files:**
- Create: `docs/philosophy.md`
- Create: `docs/output-levels.md`
- Create: `docs/architecture.md`
- Create: `examples/article.md`
- Create: `examples/meeting-transcript.md`
- Create: `examples/readiness-report.md`

- [ ] **Step 1: Explain the positioning**

Lead with: not every document deserves a skill.

- [ ] **Step 2: Show examples**

Include one high-signal article and one low-signal meeting transcript so users see why the gate exists.

### Task 5: Visual Identity

**Files:**
- Create: `assets/logo.svg`
- Create: `assets/hero-diagram.svg`
- Create: `assets/output-levels.svg`

- [ ] **Step 1: Create clean SVG assets**

Use a restrained open-source tool style: simple geometry, neutral colors, no glossy AI look.

- [ ] **Step 2: Reference assets in README**

Place the logo and diagrams in the README without making it feel like a landing page.

### Task 6: Verification and Publish

**Files:**
- Modify: all files as needed

- [ ] **Step 1: Run local checks**

Run `python -m pytest` and smoke-test CLI commands.

- [ ] **Step 2: Initialize git**

Commit the v0.1 repository.

- [ ] **Step 3: Publish to GitHub**

Create public repo `qiaozhi7426-gif/source-to-skill`, push main, and report the URL.
