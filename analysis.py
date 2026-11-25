from __future__ import annotations

import os

from app.schemas import AnalysisResult, SkillMatch
from app.services.requirements import extract_job_requirements
from app.services.roadmap import build_roadmap
from app.services.similarity import semantic_similarity
from app.services.skill_extraction import extract_skills


def analyze_resume_job(resume_text: str, job_description: str, semantic_weight: float = 0.25) -> AnalysisResult:
    resume_skills = extract_skills(resume_text)
    requirements = extract_job_requirements(job_description)
    if not requirements:
        raise ValueError("No supported skills were detected in the job description.")

    resume_skill_names = set(resume_skills)
    matches: list[SkillMatch] = []
    total_weight = sum(item.weight for item in requirements) or 1.0
    covered = 0.0
    semantic_total = 0.0
    semantic_mode = "rule-based-fallback"

    threshold = float(os.getenv("SEMANTIC_PARTIAL_THRESHOLD", "0.48"))
    for requirement in requirements:
        evidence_item = resume_skills.get(requirement.skill)
        similarity, mode = semantic_similarity(requirement.skill, resume_text, resume_skill_names)
        semantic_mode = mode if mode == "sentence-transformers" else semantic_mode
        semantic_total += requirement.weight * similarity

        if evidence_item:
            similarity = 1.0
            status = "strong"
            match_value = 1.0
            evidence = evidence_item.evidence
            explanation = f"Direct skill evidence found as '{evidence_item.alias_found}'."
        elif similarity >= threshold:
            status = "partial"
            match_value = 0.5
            evidence = None
            explanation = "Related wording or skills were detected; verify that this experience demonstrates the requirement."
        else:
            status = "missing"
            match_value = 0.0
            evidence = None
            explanation = "No direct or sufficiently related evidence was detected in the supplied resume text."

        covered += requirement.weight * match_value
        matches.append(SkillMatch(
            skill=requirement.skill,
            category=requirement.category,
            importance=requirement.importance,
            weight=requirement.weight,
            status=status,
            match_value=match_value,
            similarity=round(similarity, 4),
            evidence=evidence,
            explanation=explanation,
        ))

    coverage_score = 100.0 * covered / total_weight
    semantic_score = 100.0 * semantic_total / total_weight
    overall = (1.0 - semantic_weight) * coverage_score + semantic_weight * semantic_score
    # Round only presentation values; all calculations above use unrounded values.
    strong = [item for item in matches if item.status == "strong"]
    partial = [item for item in matches if item.status == "partial"]
    missing = [item for item in matches if item.status == "missing"]
    roadmap = build_roadmap([item.skill for item in missing], [item.skill for item in partial])

    return AnalysisResult(
        overall_score=round(overall, 2),
        coverage_score=round(coverage_score, 2),
        semantic_score=round(semantic_score, 2),
        semantic_mode=semantic_mode,
        semantic_weight=semantic_weight,
        requirements_found=len(matches),
        strong_matches=len(strong),
        partial_matches=len(partial),
        missing_skills=len(missing),
        matched_skills=strong,
        partial_skills=partial,
        missing_skill_matches=missing,
        learning_roadmap=roadmap,
        methodology_note=(
            "Coverage uses strong=1.0, partial=0.5 and missing=0.0, with required skills weighted 2 and preferred skills weighted 1. "
            f"The overall score combines {100 * (1 - semantic_weight):.0f}% weighted coverage and "
            f"{100 * semantic_weight:.0f}% semantic alignment. Semantic mode: {semantic_mode}. "
            "Similarity is a supporting signal, not proof of skill proficiency."
        ),
    )
