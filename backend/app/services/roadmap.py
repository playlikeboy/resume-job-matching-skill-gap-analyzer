from __future__ import annotations

from app.schemas import LearningStep

RESOURCE_MAP: dict[str, tuple[str, str]] = {
    "Python": (
        "Complete a focused Python fundamentals track, then practise functions, data structures and testing.",
        "Build a CLI expense tracker with CSV import, validation and unit tests.",
    ),
    "JavaScript": (
        "Practise ES modules, asynchronous code, browser APIs and debugging.",
        "Build a searchable job-board interface that consumes a public API.",
    ),
    "TypeScript": (
        "Learn types, unions, generics and typing React components.",
        "Convert a small JavaScript app to strict TypeScript.",
    ),
    "Go": (
        "Learn Go structs, interfaces, error handling, goroutines and net/http.",
        "Build a concurrent URL health-checker CLI and JSON API in Go.",
    ),
    "SQL": (
        "Practise joins, grouping, subqueries, indexes and query plans.",
        "Design a relational schema and write analytics queries for a placement portal.",
    ),
    "React": (
        "Practise component composition, state, effects, forms and accessibility.",
        "Build a role-comparison dashboard with filters and reusable components.",
    ),
    "Next.js": (
        "Learn file-based routing, server/client boundaries and API integration.",
        "Build a portfolio and project showcase with dynamic routes.",
    ),
    "REST APIs": (
        "Study HTTP methods, status codes, validation, pagination and API testing.",
        "Create a documented REST API with authentication and automated tests.",
    ),
    "FastAPI": (
        "Practise Pydantic schemas, dependency injection, status codes and TestClient tests.",
        "Build a validated FastAPI microservice with OpenAPI docs and pytest coverage.",
    ),
    "Docker": (
        "Learn images, containers, volumes, networking and multi-stage builds.",
        "Containerize a full-stack app with a repeatable local development setup.",
    ),
    "Kubernetes": (
        "Learn pods, deployments, services, ConfigMaps and health probes.",
        "Deploy a containerized API locally using kind or minikube with liveness probes.",
    ),
    "CI/CD": (
        "Learn automated test workflows, build caching and status checks.",
        "Set up a GitHub Actions workflow that runs tests and builds on every pull request.",
    ),
    "GitHub Actions": (
        "Practise YAML workflow triggers, matrix jobs and dependency caching.",
        "Automate pytest and Vite production builds with GitHub Actions.",
    ),
    "Unit Testing": (
        "Study fixtures, mocking, boundary cases and regression test design.",
        "Add unit and integration tests reaching 85%+ coverage on an API module.",
    ),
    "AWS": (
        "Learn IAM basics, S3, EC2/ECS, RDS and least-privilege security groups.",
        "Deploy a static frontend and containerized backend with environment configs.",
    ),
    "Machine Learning": (
        "Review supervised learning, data leakage, validation and metric selection.",
        "Train and compare a baseline classifier with a documented evaluation split.",
    ),
    "NLP": (
        "Study tokenization, text normalization, embeddings and evaluation of extraction systems.",
        "Build a skill/entity extraction benchmark with manually annotated examples.",
    ),
    "PyTorch": (
        "Practise tensors, Dataset/DataLoader, training loops and evaluation metrics.",
        "Train and evaluate a text classifier in PyTorch on a small labeled dataset.",
    ),
    "scikit-learn": (
        "Learn Pipelines, cross-validation, TF-IDF vectorizers and classification metrics.",
        "Build a scikit-learn TF-IDF + logistic regression baseline with F1 reporting.",
    ),
    "pandas": (
        "Practise DataFrame filtering, groupby aggregations, joins and missing-data handling.",
        "Clean and summarize a public job-market CSV dataset into reproducible charts.",
    ),
    "Data Visualization": (
        "Learn chart selection, clear axis labeling and visual hierarchy.",
        "Create an interactive dashboard visualizing skill demand across job roles.",
    ),
    "PostgreSQL": (
        "Practise schema design, constraints, joins, indexes and migrations.",
        "Persist analysis history using a normalized schema and migrations.",
    ),
}


def build_roadmap(missing_skills: list[str], partial_skills: list[str]) -> list[LearningStep]:
    steps: list[LearningStep] = []
    ordered = [(skill, "High", "Required or unverified skill not detected") for skill in missing_skills]
    ordered += [(skill, "Medium", "Related evidence detected, but direct evidence is limited") for skill in partial_skills]
    for skill, priority, reason in ordered:
        task, project = RESOURCE_MAP.get(
            skill,
            (
                f"Review the core concepts and practise {skill} with small, measurable exercises.",
                f"Build a small end-to-end project that demonstrates {skill} with tests and a README.",
            ),
        )
        steps.append(LearningStep(skill=skill, priority=priority, reason=reason, task=task, project_idea=project))
    return steps[:12]
