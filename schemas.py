from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class AnalyzeRequest(BaseModel):
    resume_text: str = Field(min_length=1, max_length=100_000)
    job_description: str = Field(min_length=1, max_length=50_000)
    semantic_weight: float = Field(default=0.25, ge=0.0, le=0.5)

    @field_validator("resume_text", "job_description")
    @classmethod
    def strip_text(cls, value: str) -> str:
        return value.strip()


class SkillMatch(BaseModel):
    skill: str
    category: str
    importance: str
    weight: float
    status: str
    match_value: float
    similarity: float
    evidence: str | None = None
    explanation: str


class LearningStep(BaseModel):
    skill: str
    priority: str
    reason: str
    task: str
    project_idea: str


class AnalysisResult(BaseModel):
    overall_score: float
    coverage_score: float
    semantic_score: float
    semantic_mode: str
    semantic_weight: float
    requirements_found: int
    strong_matches: int
    partial_matches: int
    missing_skills: int
    matched_skills: list[SkillMatch]
    partial_skills: list[SkillMatch]
    missing_skill_matches: list[SkillMatch]
    learning_roadmap: list[LearningStep]
    methodology_note: str
