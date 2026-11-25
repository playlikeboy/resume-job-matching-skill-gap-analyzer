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


def test_exact_skill_evidence_is_a_strong_match():
    result = analyze_resume_job(
        "Built APIs with Python and FastAPI. Used PostgreSQL for persistence.",
        "Required: Python, FastAPI and PostgreSQL.",
    )
    assert result.requirements_found == 3
    assert result.strong_matches == 3
    assert result.coverage_score == 100.0
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
