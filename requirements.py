from __future__ import annotations

from dataclasses import dataclass

from app.services.skill_extraction import extract_skills


PREFERRED_MARKERS = (
    "preferred", "nice to have", "nice-to-have", "bonus", "good to have",
    "desirable", "desired", "ideally", "plus", "preferred qualifications",
)


@dataclass
class JobRequirement:
    skill: str
    category: str
    importance: str
    weight: float
    evidence: str


def extract_job_requirements(job_description: str) -> list[JobRequirement]:
    extracted = extract_skills(job_description)
    requirements: list[JobRequirement] = []
    lowered = job_description.lower()
    for skill, item in extracted.items():
        # Look around the first supporting line to see whether the skill is preferred.
        position = lowered.find(item.alias_found.lower())
        before = lowered[max(0, position - 250):position]
        preferred_positions = [before.rfind(marker) for marker in PREFERRED_MARKERS]
        required_markers = ("required", "must have", "minimum qualifications", "basic qualifications")
        required_positions = [before.rfind(marker) for marker in required_markers]
        last_preferred = max(preferred_positions, default=-1)
        last_required = max(required_positions, default=-1)
        preferred_from_heading = last_preferred > last_required and last_preferred >= 0

        # Also support inline wording such as "React is nice to have" or "React (preferred)".
        after_start = position + len(item.alias_found)
        sentence_end_candidates = [idx for idx in (
            lowered.find("\n", after_start), lowered.find(".", after_start),
            lowered.find(";", after_start), lowered.find("!", after_start),
            lowered.find("?", after_start),
        ) if idx >= 0]
        sentence_end = min(sentence_end_candidates) if sentence_end_candidates else min(len(lowered), after_start + 60)
        inline_after = lowered[after_start:sentence_end]
        inline_preferred = len(inline_after) <= 60 and any(marker in inline_after for marker in PREFERRED_MARKERS)
        preferred = preferred_from_heading or inline_preferred
        importance = "preferred" if preferred else "required"
        requirements.append(JobRequirement(
            skill=skill,
            category=item.category,
            importance=importance,
            weight=1.0 if preferred else 2.0,
            evidence=item.evidence,
        ))
    return requirements
