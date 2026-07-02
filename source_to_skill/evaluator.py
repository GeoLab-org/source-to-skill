from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


STOPWORDS = {
    "about",
    "after",
    "again",
    "against",
    "all",
    "also",
    "always",
    "and",
    "any",
    "are",
    "before",
    "can",
    "claim",
    "claims",
    "does",
    "each",
    "every",
    "for",
    "from",
    "has",
    "have",
    "into",
    "its",
    "keep",
    "not",
    "only",
    "should",
    "skill",
    "that",
    "the",
    "this",
    "use",
    "when",
    "with",
    "without",
    "you",
    "your",
}


@dataclass(frozen=True)
class ClaimCheck:
    claim: str
    status: str
    overlap_terms: tuple[str, ...]
    support_ratio: float
    note: str

    def to_dict(self) -> dict:
        return {
            "claim": self.claim,
            "status": self.status,
            "overlap_terms": list(self.overlap_terms),
            "support_ratio": self.support_ratio,
            "note": self.note,
        }


@dataclass(frozen=True)
class SkillEvaluationReport:
    skill_path: Path
    total_claims: int
    supported_count: int
    weak_count: int
    unsupported_count: int
    warnings: tuple[str, ...]
    checks: tuple[ClaimCheck, ...]

    def to_dict(self) -> dict:
        return {
            "skill_path": str(self.skill_path),
            "total_claims": self.total_claims,
            "supported_count": self.supported_count,
            "weak_count": self.weak_count,
            "unsupported_count": self.unsupported_count,
            "warnings": list(self.warnings),
            "checks": [check.to_dict() for check in self.checks],
        }


def evaluate_skill(skill_path: str | Path) -> SkillEvaluationReport:
    root = Path(skill_path)
    skill_md = root / "SKILL.md"
    if not skill_md.exists():
        raise FileNotFoundError(f"Missing SKILL.md in {root}")

    claims = extract_core_guidance(skill_md.read_text(encoding="utf-8"))
    evidence_path = root / "references" / "evidence.md"
    warnings: list[str] = []
    evidence_text = ""
    if evidence_path.exists():
        evidence_text = evidence_path.read_text(encoding="utf-8")
    else:
        warnings.append("Missing references/evidence.md.")

    checks = tuple(check_claim(claim, evidence_text) for claim in claims)
    if not claims:
        warnings.append("No Core Guidance bullets found in SKILL.md.")

    return SkillEvaluationReport(
        skill_path=root,
        total_claims=len(checks),
        supported_count=sum(1 for check in checks if check.status == "supported"),
        weak_count=sum(1 for check in checks if check.status == "weak"),
        unsupported_count=sum(1 for check in checks if check.status == "unsupported"),
        warnings=tuple(warnings),
        checks=checks,
    )


def extract_core_guidance(markdown: str) -> tuple[str, ...]:
    section = extract_section(markdown, "Core Guidance")
    claims: list[str] = []
    for line in section.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            claims.append(stripped[2:].strip())
    return tuple(claims)


def extract_section(markdown: str, heading: str) -> str:
    pattern = re.compile(rf"^##\s+{re.escape(heading)}\s*$", re.IGNORECASE | re.MULTILINE)
    match = pattern.search(markdown)
    if not match:
        return ""
    start = match.end()
    next_heading = re.search(r"^##\s+", markdown[start:], re.MULTILINE)
    end = start + next_heading.start() if next_heading else len(markdown)
    return markdown[start:end]


def check_claim(claim: str, evidence_text: str) -> ClaimCheck:
    claim_terms = meaningful_terms(claim)
    evidence_terms = meaningful_terms(evidence_text)
    overlap = tuple(sorted(set(claim_terms) & set(evidence_terms)))
    ratio = round(len(overlap) / len(set(claim_terms)), 3) if claim_terms else 0.0
    threshold = max(3, round(len(set(claim_terms)) * 0.35))

    if not evidence_text.strip():
        status = "unsupported"
        note = "No evidence file was available for this claim."
    elif len(overlap) >= threshold:
        status = "supported"
        note = "The claim has clear lexical support in the evidence file."
    elif overlap:
        status = "weak"
        note = "The claim has partial lexical support; review it manually."
    else:
        status = "unsupported"
        note = "The claim has no meaningful lexical support in the evidence file."

    return ClaimCheck(
        claim=claim,
        status=status,
        overlap_terms=overlap,
        support_ratio=ratio,
        note=note,
    )


def meaningful_terms(text: str) -> tuple[str, ...]:
    tokens = re.findall(r"[a-zA-Z][a-zA-Z0-9'-]{2,}", text.lower())
    return tuple(token for token in tokens if token not in STOPWORDS)


def render_eval_report(report: SkillEvaluationReport) -> str:
    lines = [
        "# Skill Evaluation Report",
        "",
        "This report checks whether generated Core Guidance bullets have lexical support in `references/evidence.md`.",
        "",
        "## Summary",
        f"- Claims checked: {report.total_claims}",
        f"- Supported: {report.supported_count}",
        f"- Weak: {report.weak_count}",
        f"- Unsupported: {report.unsupported_count}",
    ]
    if report.warnings:
        lines.extend(["", "## Warnings"])
        lines.extend(f"- {warning}" for warning in report.warnings)
    lines.extend(
        [
            "",
            "## Claim Checks",
            "",
            "| Status | Claim | Evidence overlap |",
            "|---|---|---|",
        ]
    )
    for check in report.checks:
        overlap = ", ".join(check.overlap_terms) if check.overlap_terms else "None"
        lines.append(f"| {check.status} | {escape_table(check.claim)} | {escape_table(overlap)} |")
    lines.append("")
    return "\n".join(lines)


def escape_table(value: str) -> str:
    return value.replace("|", "\\|")
