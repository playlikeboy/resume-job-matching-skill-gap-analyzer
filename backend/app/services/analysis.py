from __future__ import annotations

from collections import defaultdict

from app.config import get_settings
from app.schemas import (
    AnalysisResult,
    CategorySummary,
    CompareResult,
    JobComparisonItem,
    JobItem,
    SkillMatch,
)
from app.services.requirements import extract_job_requirements
from app.services.roadmap import build_roadmap
from app.services.similarity import semantic_similarity
from app.services.skill_extraction import extract_skills


def _score_band(overall_score: float) -> str:
    if overall_score >= 80.0:
        return "Strong alignment"
    if overall_score >= 60.0:
        return "Moderate alignment"
    if overall_score >= 40.0:
        return "Developing alignment"
    return "Early-stage gap"


def analyze_resume_job(resume_text: str, job_description: str, semantic_weight: float = 0.25) -> AnalysisResult:
    settings = get_settings()
    resume_skills = extract_skills(resume_text, ignore_negated=True)
    requirements = extract_job_requirements(job_description)
    if not requirements:
        raise ValueError("No supported skills were detected in the job description.")

    resume_skill_names = set(resume_skills)
    matches: list[SkillMatch] = []
    total_weight = sum(item.weight for item in requirements) or 1.0
    covered = 0.0
    semantic_total = 0.0
    semantic_mode = "rule-based-fallback"

    threshold = settings.semantic_partial_threshold
    cat_stats: dict[str, dict[str, float | int]] = defaultdict(
        lambda: {"total": 0, "strong": 0, "partial": 0, "missing": 0, "weight": 0.0, "covered": 0.0}
    )

    for requirement in requirements:
        evidence_item = resume_skills.get(requirement.skill)
        raw_similarity, mode = semantic_similarity(requirement.skill, resume_text, resume_skill_names)
        if mode == "sentence-transformers":
            semantic_mode = mode

        if evidence_item:
            similarity = 1.0
            status = "strong"
            match_value = 1.0
            evidence = evidence_item.evidence
            mention_note = f" ({evidence_item.occurrences} mentions)" if evidence_item.occurrences > 1 else ""
            explanation = f"Direct skill evidence found as '{evidence_item.alias_found}'{mention_note}."
        elif raw_similarity >= threshold:
            similarity = raw_similarity
            status = "partial"
            match_value = 0.5
            evidence = None
            explanation = (
                "Related wording or skills were detected; verify that this experience demonstrates the requirement."
            )
        else:
            similarity = raw_similarity
            status = "missing"
            match_value = 0.0
            evidence = None
            explanation = "No direct or sufficiently related evidence was detected in the supplied resume text."

        semantic_total += requirement.weight * similarity
        covered += requirement.weight * match_value

        stats = cat_stats[requirement.category]
        stats["total"] += 1
        stats[status] += 1
        stats["weight"] += requirement.weight
        stats["covered"] += requirement.weight * match_value

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
            requirement_rationale=requirement.rationale,
        ))

    coverage_score = 100.0 * covered / total_weight
    semantic_score = 100.0 * semantic_total / total_weight
    overall = (1.0 - semantic_weight) * coverage_score + semantic_weight * semantic_score

    # Round only presentation values; all calculations above use unrounded values.
    strong = [item for item in matches if item.status == "strong"]
    partial = [item for item in matches if item.status == "partial"]
    missing = [item for item in matches if item.status == "missing"]

    # Sort roadmap gaps so required missing skills precede preferred missing skills, then partials.
    missing_ordered = [
        item.skill for item in sorted(missing, key=lambda x: -x.weight)
    ]
    partial_ordered = [
        item.skill for item in sorted(partial, key=lambda x: -x.weight)
    ]
    roadmap = build_roadmap(missing_ordered, partial_ordered)

    required_skills = {item.skill for item in requirements}
    resume_detected = sorted(resume_skill_names)
    extra_resume = sorted(resume_skill_names - required_skills)

    category_breakdown = [
        CategorySummary(
            category=category,
            total_requirements=int(stats["total"]),
            strong=int(stats["strong"]),
            partial=int(stats["partial"]),
            missing=int(stats["missing"]),
            coverage_score=round(100.0 * float(stats["covered"]) / (float(stats["weight"]) or 1.0), 2),
        )
        for category, stats in sorted(cat_stats.items())
    ]

    overall_rounded = round(overall, 2)
    return AnalysisResult(
        overall_score=overall_rounded,
        coverage_score=round(coverage_score, 2),
        semantic_score=round(semantic_score, 2),
        semantic_mode=semantic_mode,
        semantic_weight=semantic_weight,
        score_band=_score_band(overall_rounded),
        requirements_found=len(matches),
        strong_matches=len(strong),
        partial_matches=len(partial),
        missing_skills=len(missing),
        matched_skills=strong,
        partial_skills=partial,
        missing_skill_matches=missing,
        resume_skills_detected=resume_detected,
        extra_resume_skills=extra_resume,
        category_breakdown=category_breakdown,
        learning_roadmap=roadmap,
        methodology_note=(
            "Coverage uses strong=1.0, partial=0.5 and missing=0.0, with required skills weighted 2 and preferred skills weighted 1. "
            f"The overall score combines {100 * (1 - semantic_weight):.0f}% weighted coverage and "
            f"{100 * semantic_weight:.0f}% semantic alignment. Semantic mode: {semantic_mode}. "
            "Similarity is a supporting signal, not proof of skill proficiency."
        ),
    )


def compare_resume_to_jobs(
    resume_text: str,
    jobs: list[JobItem],
    semantic_weight: float = 0.25,
) -> CompareResult:
    resume_skills = sorted(extract_skills(resume_text, ignore_negated=True))
    semantic_mode = "rule-based-fallback"
    rankings: list[JobComparisonItem] = []

    for job in jobs:
        analysis = analyze_resume_job(
            resume_text=resume_text,
            job_description=job.job_description,
            semantic_weight=semantic_weight,
        )
        if analysis.semantic_mode == "sentence-transformers":
            semantic_mode = analysis.semantic_mode
        rankings.append(JobComparisonItem(
            title=job.title,
            overall_score=analysis.overall_score,
            coverage_score=analysis.coverage_score,
            semantic_score=analysis.semantic_score,
            score_band=analysis.score_band,
            requirements_found=analysis.requirements_found,
            strong_matches=analysis.strong_matches,
            partial_matches=analysis.partial_matches,
            missing_skills=analysis.missing_skills,
            top_strengths=[item.skill for item in analysis.matched_skills[:5]],
            top_gaps=[item.skill for item in analysis.missing_skill_matches[:5]],
        ))

    rankings.sort(key=lambda item: (-item.overall_score, -item.strong_matches, item.missing_skills))
    return CompareResult(
        semantic_mode=semantic_mode,
        semantic_weight=semantic_weight,
        resume_skills_detected=resume_skills,
        rankings=rankings,
    )
