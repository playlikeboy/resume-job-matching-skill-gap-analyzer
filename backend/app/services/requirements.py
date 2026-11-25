from __future__ import annotations

import re
from dataclasses import dataclass

from app.services.skill_extraction import extract_skills

PREFERRED_MARKERS = (
    "preferred", "nice to have", "nice-to-have", "bonus", "good to have",
    "desirable", "desired", "ideally", "plus", "preferred qualifications",
    "optional",
)

REQUIRED_MARKERS = (
    "required", "must have", "must-have", "minimum qualifications",
    "basic qualifications", "core requirements", "essential",
)

SECTION_HEADING_PATTERN = re.compile(r"^\s*([A-Za-z][A-Za-z\s/&\-]{2,50}):?\s*$")


@dataclass
class JobRequirement:
    skill: str
    category: str
    importance: str
    weight: float
    evidence: str
    rationale: str = ""


def _build_line_sections(job_description: str) -> list[tuple[int, str]]:
    """Map character offsets to active section importance ('required' or 'preferred')."""
    sections: list[tuple[int, str]] = [(0, "required")]
    offset = 0
    for line in job_description.splitlines(keepends=True):
        stripped = line.strip().lower()
        # Treat short standalone lines or colon-terminated headers as section markers.
        if stripped and (stripped.endswith(":") or SECTION_HEADING_PATTERN.match(stripped)):
            if any(marker in stripped for marker in PREFERRED_MARKERS):
                sections.append((offset, "preferred"))
            elif any(marker in stripped for marker in REQUIRED_MARKERS):
                sections.append((offset, "required"))
            elif any(h in stripped for h in ("qualifications", "requirements", "responsibilities")):
                sections.append((offset, "required"))
        offset += len(line)
    return sections


def _section_at(sections: list[tuple[int, str]], position: int) -> str:
    current = "required"
    for offset, label in sections:
        if offset <= position:
            current = label
        else:
            break
    return current


def extract_job_requirements(job_description: str) -> list[JobRequirement]:
    extracted = extract_skills(job_description, ignore_negated=False)
    requirements: list[JobRequirement] = []
    lowered = job_description.lower()
    sections = _build_line_sections(job_description)

    for skill, item in extracted.items():
        position = item.match_start
        before = lowered[max(0, position - 250):position]
        preferred_positions = [before.rfind(marker) for marker in PREFERRED_MARKERS]
        required_positions = [before.rfind(marker) for marker in REQUIRED_MARKERS]
        last_preferred = max(preferred_positions, default=-1)
        last_required = max(required_positions, default=-1)
        preferred_from_local = last_preferred > last_required and last_preferred >= 0

        section_label = _section_at(sections, position)
        preferred_from_section = section_label == "preferred" and last_required < 0

        # Also support inline wording such as "React is nice to have" or "React (preferred)".
        after_start = item.match_end
        sentence_end_candidates = [
            idx for idx in (
                lowered.find("\n", after_start),
                lowered.find(".", after_start),
                lowered.find(";", after_start),
                lowered.find("!", after_start),
                lowered.find("?", after_start),
            ) if idx >= 0
        ]
        sentence_end = min(sentence_end_candidates) if sentence_end_candidates else min(len(lowered), after_start + 60)
        inline_after = lowered[after_start:sentence_end]
        inline_preferred = len(inline_after) <= 60 and any(marker in inline_after for marker in PREFERRED_MARKERS)

        if inline_preferred:
            preferred = True
            rationale = "Classified as preferred from inline wording."
        elif preferred_from_local:
            preferred = True
            rationale = "Classified as preferred from nearby qualification context."
        elif preferred_from_section:
            preferred = True
            rationale = "Classified as preferred from section heading."
        else:
            preferred = False
            rationale = "Classified as required requirement (default weight 2.0)."

        importance = "preferred" if preferred else "required"
        requirements.append(JobRequirement(
            skill=skill,
            category=item.category,
            importance=importance,
            weight=1.0 if preferred else 2.0,
            evidence=item.evidence,
            rationale=rationale,
        ))
    return requirements
