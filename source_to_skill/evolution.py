from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from source_to_skill.analyzer import analyze_source
from source_to_skill.intake import read_source
from source_to_skill.models import OutputLevel, ReadinessReport
from source_to_skill.templates import slugify


RELATIONSHIPS = ("duplicate", "evidence", "refinement", "contradiction", "new_skill", "reject")

CONTRADICTION_TERMS = (
    "however",
    "instead",
    "rather than",
    "unless",
    "except",
    "conflict",
    "contradict",
    "但是",
    "然而",
    "反而",
    "不是",
    "除非",
    "冲突",
    "矛盾",
)

STOPWORDS = {
    "about",
    "after",
    "again",
    "against",
    "also",
    "and",
    "are",
    "because",
    "before",
    "between",
    "but",
    "can",
    "could",
    "every",
    "for",
    "from",
    "have",
    "has",
    "its",
    "into",
    "may",
    "more",
    "not",
    "only",
    "own",
    "should",
    "source",
    "standalone",
    "skill",
    "that",
    "the",
    "their",
    "there",
    "this",
    "until",
    "use",
    "using",
    "when",
    "without",
    "where",
    "which",
    "with",
    "would",
}


@dataclass(frozen=True)
class SkillMatch:
    skill_path: Path
    overlap_percent: int
    matched_terms: tuple[str, ...]
    source_terms: int
    skill_terms: int

    def to_dict(self) -> dict:
        return {
            "skill_path": str(self.skill_path),
            "overlap_percent": self.overlap_percent,
            "matched_terms": list(self.matched_terms),
            "source_terms": self.source_terms,
            "skill_terms": self.skill_terms,
        }


@dataclass(frozen=True)
class EvolutionReport:
    source_report: ReadinessReport
    match: SkillMatch
    relationship: str
    confidence: int
    method_candidates: tuple[str, ...]
    first_principles: tuple[str, ...]
    adversarial_review: tuple[str, ...]
    proposed_change: tuple[str, ...]
    evidence_to_add: tuple[str, ...]
    user_decision_needed: tuple[str, ...]

    def to_dict(self) -> dict:
        return {
            "source": self.source_report.to_dict(),
            "match": self.match.to_dict(),
            "relationship": self.relationship,
            "confidence": self.confidence,
            "method_candidates": list(self.method_candidates),
            "first_principles": list(self.first_principles),
            "adversarial_review": list(self.adversarial_review),
            "proposed_change": list(self.proposed_change),
            "evidence_to_add": list(self.evidence_to_add),
            "user_decision_needed": list(self.user_decision_needed),
        }


def evolve_source(source: str | Path, existing_skill: str | Path, output_dir: str | Path) -> Path:
    report = create_evolution_report(source, existing_skill)
    out_path = Path(output_dir)
    target_dir = out_path / "pending-updates"
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / f"{slugify(report.source_report.title)}-{report.relationship}.md"
    target.write_text(render_pending_update(report), encoding="utf-8")
    return target


def create_evolution_report(source: str | Path, existing_skill: str | Path) -> EvolutionReport:
    source_text = read_source(source)
    source_report = analyze_source(source)
    skill_path = Path(existing_skill)
    skill_text = read_skill_text(skill_path)
    match = match_skill(source_text, skill_text, skill_path)
    contradiction = has_contradiction_language(source_text)
    relationship = classify_relationship(source_report, match, contradiction)
    confidence = relationship_confidence(source_report, match, contradiction)
    method_candidates = source_report.evidence or source_report.reasons
    return EvolutionReport(
        source_report=source_report,
        match=match,
        relationship=relationship,
        confidence=confidence,
        method_candidates=tuple(method_candidates),
        first_principles=build_first_principles_review(source_report, match, relationship),
        adversarial_review=build_adversarial_review(source_report, match, relationship, contradiction),
        proposed_change=build_proposed_change(source_report, match, relationship),
        evidence_to_add=tuple(source_report.evidence or ("No strong automatic evidence candidates found.",)),
        user_decision_needed=build_user_decisions(relationship),
    )


def read_skill_text(skill_path: Path) -> str:
    if skill_path.is_file():
        return skill_path.read_text(encoding="utf-8")
    if not skill_path.exists():
        raise FileNotFoundError(f"Skill path does not exist: {skill_path}")
    parts = []
    preferred = (skill_path / "SKILL.md", skill_path / "cheatsheet.md", skill_path / "references" / "evidence.md")
    for path in preferred:
        if path.exists():
            parts.append(path.read_text(encoding="utf-8"))
    if not parts:
        for path in sorted(skill_path.rglob("*.md"))[:12]:
            parts.append(path.read_text(encoding="utf-8"))
    if not parts:
        raise ValueError(f"No Markdown files found in skill path: {skill_path}")
    return "\n\n".join(parts)


def match_skill(source_text: str, skill_text: str, skill_path: Path) -> SkillMatch:
    source_terms = extract_terms(source_text)
    skill_terms = extract_terms(skill_text)
    matched = tuple(sorted(source_terms & skill_terms))
    if not source_terms:
        overlap = 0
    else:
        overlap = round(len(matched) / len(source_terms) * 100)
    return SkillMatch(
        skill_path=skill_path,
        overlap_percent=overlap,
        matched_terms=matched[:20],
        source_terms=len(source_terms),
        skill_terms=len(skill_terms),
    )


def extract_terms(text: str) -> set[str]:
    lower = text.lower()
    latin = {term for term in re.findall(r"[a-z][a-z0-9_-]{2,}", lower) if term not in STOPWORDS}
    cjk = set(re.findall(r"[\u4e00-\u9fff]{2,}", lower))
    return latin | cjk


def has_contradiction_language(text: str) -> bool:
    lower = text.lower()
    return any(term in lower for term in CONTRADICTION_TERMS)


def classify_relationship(report: ReadinessReport, match: SkillMatch, contradiction: bool) -> str:
    if report.score < 35:
        return "reject"
    if match.overlap_percent >= 55 and report.level in {OutputLevel.NOTE, OutputLevel.SEED}:
        return "duplicate"
    if match.overlap_percent >= 25 and contradiction:
        return "contradiction"
    if match.overlap_percent >= 35:
        return "refinement"
    if match.overlap_percent >= 18:
        return "evidence"
    if report.level in {OutputLevel.MINI, OutputLevel.FULL}:
        return "new_skill"
    return "reject"


def relationship_confidence(report: ReadinessReport, match: SkillMatch, contradiction: bool) -> int:
    score_component = min(report.score, 100) * 0.45
    overlap_component = min(match.overlap_percent, 100) * 0.45
    contradiction_component = 10 if contradiction else 0
    return round(min(95, score_component + overlap_component + contradiction_component))


def build_first_principles_review(
    report: ReadinessReport, match: SkillMatch, relationship: str
) -> tuple[str, ...]:
    return (
        f"Core job: improve a callable method related to `{match.skill_path.name}` without creating a duplicate skill.",
        f"Core method signal: readiness score {report.score}/100 with recommended output `{report.level.value}`.",
        f"Transferability: {report.word_count} words, {report.heading_count} headings, and {len(report.evidence)} evidence candidates.",
        f"Boundary: classify as `{relationship}` before changing core guidance.",
        "Pass/fail: keep this as pending until a human confirms the relationship and scope.",
    )


def build_adversarial_review(
    report: ReadinessReport, match: SkillMatch, relationship: str, contradiction: bool
) -> tuple[str, ...]:
    return (
        "Counterexample: this may be a local example rather than a reusable rule.",
        f"Contradiction: {'conflict language detected; ask before merging' if contradiction else 'no obvious conflict language detected by heuristic scan'}.",
        f"Overgeneralization risk: `{relationship}` should not automatically rewrite the target skill.",
        f"Evidence gap: {len(report.evidence)} automatic evidence candidates found; each proposed rule still needs source review.",
        f"Use-case drift: matched {match.overlap_percent}% of source terms against the existing skill.",
        "Unsafe merge risk: keep output as a pending update, not an automatic edit.",
    )


def build_proposed_change(
    report: ReadinessReport, match: SkillMatch, relationship: str
) -> tuple[str, ...]:
    if relationship == "duplicate":
        return ("Do not change core guidance; optionally record the source as a weak reference.",)
    if relationship == "evidence":
        return ("Add source-backed evidence without changing the target skill's core method.",)
    if relationship == "refinement":
        return (
            "Propose a targeted edit to the target skill's core guidance.",
            "Keep the existing skill job intact and add only source-backed boundaries or sharper wording.",
        )
    if relationship == "contradiction":
        return (
            "Do not merge automatically.",
            "Ask the user whether to keep the source as a contradiction, merge a boundary case, or reject it.",
        )
    if relationship == "new_skill":
        return (
            f"Create a separate seed or mini skill because overlap with `{match.skill_path.name}` is low.",
            "Do not force-fit unrelated methodology into the target skill.",
        )
    return ("Reject this source for skill evolution unless a human supplies stronger context.",)


def build_user_decisions(relationship: str) -> tuple[str, ...]:
    if relationship == "contradiction":
        return ("merge as boundary case", "keep as contradiction", "add as evidence only", "reject")
    if relationship == "refinement":
        return ("merge targeted refinement", "add as evidence only", "keep pending", "reject")
    if relationship == "new_skill":
        return ("create separate skill seed", "search for a better target skill", "keep as note", "reject")
    if relationship == "evidence":
        return ("add evidence", "keep as weak reference", "reject")
    return ("accept recommendation", "override manually")


def render_pending_update(report: EvolutionReport) -> str:
    lines = [
        "# Skill Update Review",
        "",
        f"Source: {report.source_report.title}",
        f"Target skill: {report.match.skill_path}",
        f"Recommended relationship: `{report.relationship}`",
        f"Confidence: {report.confidence}/100",
        "",
        "## Match Summary",
        "",
        f"- Overlap: {report.match.overlap_percent}%",
        f"- Source terms: {report.match.source_terms}",
        f"- Skill terms: {report.match.skill_terms}",
        "- Matched terms: " + (", ".join(report.match.matched_terms) if report.match.matched_terms else "none"),
        "",
        "## Extracted Method Candidates",
        "",
        *(f"- {item}" for item in report.method_candidates),
        "",
        "## First-Principles Review",
        "",
        *(f"- {item}" for item in report.first_principles),
        "",
        "## Adversarial Review",
        "",
        *(f"- {item}" for item in report.adversarial_review),
        "",
        "## Proposed Change",
        "",
        *(f"- {item}" for item in report.proposed_change),
        "",
        "## Evidence To Add",
        "",
        *(f"- {item}" for item in report.evidence_to_add),
        "",
        "## User Decision Needed",
        "",
        *(f"- [ ] {item}" for item in report.user_decision_needed),
        "",
        "## Final Decision",
        "",
        "- [ ] accepted",
        "- [ ] rejected",
        "- [ ] needs more source material",
        "",
    ]
    return "\n".join(lines)
