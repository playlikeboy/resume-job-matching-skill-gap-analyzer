from __future__ import annotations

from app.schemas import LearningStep


RESOURCE_MAP = {
    "Python": ("Complete a focused Python fundamentals track, then practise functions, data structures and testing.", "Build a CLI expense tracker with CSV import, validation and unit tests."),
    "JavaScript": ("Practise ES modules, asynchronous code, browser APIs and debugging.", "Build a searchable job-board interface that consumes a public API."),
    "TypeScript": ("Learn types, unions, generics and typing React components.", "Convert a small JavaScript app to strict TypeScript."),
    "SQL": ("Practise joins, grouping, subqueries, indexes and query plans.", "Design a relational schema and write analytics queries for a placement portal."),
    "React": ("Practise component composition, state, effects, forms and accessibility.", "Build a role-comparison dashboard with filters and reusable components."),
    "REST APIs": ("Study HTTP methods, status codes, validation, pagination and API testing.", "Create a documented REST API with authentication and automated tests."),
    "Docker": ("Learn images, containers, volumes, networking and multi-stage builds.", "Containerize a full-stack app with a repeatable local development setup."),
    "Machine Learning": ("Review supervised learning, data leakage, validation and metric selection.", "Train and compare a baseline classifier with a documented evaluation split."),
    "NLP": ("Study tokenization, text normalization, embeddings and evaluation of extraction systems.", "Build a skill/entity extraction benchmark with manually annotated examples."),
    "PostgreSQL": ("Practise schema design, constraints, joins, indexes and migrations.", "Persist analysis history using a normalized schema and migrations."),
}


def build_roadmap(missing_skills: list[str], partial_skills: list[str]) -> list[LearningStep]:
    steps: list[LearningStep] = []
    ordered = [(skill, "High", "Required skill not detected") for skill in missing_skills]
    ordered += [(skill, "Medium", "Related evidence detected, but direct evidence is limited") for skill in partial_skills]
    for skill, priority, reason in ordered:
        task, project = RESOURCE_MAP.get(
            skill,
            (f"Review the core concepts and practise {skill} with small, measurable exercises.",
             f"Build a small end-to-end project that demonstrates {skill} with tests and a README."),
        )
        steps.append(LearningStep(skill=skill, priority=priority, reason=reason, task=task, project_idea=project))
    return steps[:12]
