from app.services.analysis import analyze_resume_job
from app.services.requirements import extract_job_requirements
from app.services.skill_extraction import extract_skills


def test_alias_normalization_js_to_javascript():
    found = extract_skills("Built interactive dashboards using JS and ReactJS.")
    assert "JavaScript" in found
    assert "React" in found
    assert found["JavaScript"].alias_found.lower() in {"js", "javascript"}


def test_required_and_preferred_weights_are_distinguished():
    requirements = extract_job_requirements(
        "Required: Python and SQL. React is nice to have."
    )
    by_skill = {item.skill: item for item in requirements}
    assert by_skill["Python"].importance == "required"
    assert by_skill["Python"].weight == 2.0
    assert by_skill["React"].importance == "preferred"
    assert by_skill["React"].weight == 1.0


def test_ts_alias_does_not_misfire_on_requirements_word():
    jd = (
        "Required qualifications:\n"
        "- Python and SQL.\n\n"
        "Preferred qualifications:\n"
        "- Experience with TS and React.\n"
    )
    requirements = extract_job_requirements(jd)
    by_skill = {item.skill: item for item in requirements}
    assert by_skill["Python"].importance == "required"
    assert by_skill["TypeScript"].importance == "preferred"


def test_long_preferred_section_preserves_heading_context():
    filler = "Experience collaborating across agile product teams and documenting design choices. " * 6
    jd = (
        "Required qualifications:\n"
        "- Python\n\n"
        "Preferred qualifications:\n"
        f"- {filler}\n"
        "- Docker\n"
    )
    requirements = extract_job_requirements(jd)
    by_skill = {item.skill: item for item in requirements}
    assert by_skill["Python"].importance == "required"
    assert by_skill["Docker"].importance == "preferred"


def test_ambiguous_english_words_do_not_trigger_false_positives():
    found = extract_skills(
        "I want to express interest in this role and go to the next round."
    )
    assert "Express.js" not in found
    assert "Go" not in found

    tech_found = extract_skills("Built microservices in Go and Express.js.")
    assert "Go" in tech_found
    assert "Express.js" in tech_found


def test_negated_resume_mention_is_ignored():
    found = extract_skills("Built APIs with Python. No prior experience with Kubernetes.")
    assert "Python" in found
    assert "Kubernetes" not in found


def test_exact_skill_evidence_is_a_strong_match_and_consistent_semantic_score():
    result = analyze_resume_job(
        "Built APIs with JS and FastAPI. Used postgres for persistence.",
        "Required: JavaScript, FastAPI and PostgreSQL.",
    )
    assert result.requirements_found == 3
    assert result.strong_matches == 3
    assert result.coverage_score == 100.0
    assert result.semantic_score == 100.0
    assert result.overall_score == 100.0
    assert all(item.evidence for item in result.matched_skills)


def test_missing_skill_generates_learning_roadmap():
    result = analyze_resume_job(
        "Built a frontend with React and JavaScript.",
        "Required: React, JavaScript and Docker.",
    )
    assert result.missing_skills >= 1
    assert any(step.skill == "Docker" for step in result.learning_roadmap)


def test_preferred_skills_have_lower_weight():
    result = analyze_resume_job(
        "Used Python in academic projects.",
        "Required: Python. Preferred: React.",
    )
    python = next(item for item in result.matched_skills if item.skill == "Python")
    react = next(item for item in result.missing_skill_matches if item.skill == "React")
    assert python.weight == 2.0
    assert react.weight == 1.0


def test_related_technology_is_only_a_partial_match():
    result = analyze_resume_job(
        "Built backend services with FastAPI and Python.",
        "Required: REST APIs and Python.",
    )
    rest = next(item for item in result.partial_skills if item.skill == "REST APIs")
    assert rest.match_value == 0.5
    assert "Related" in rest.explanation
