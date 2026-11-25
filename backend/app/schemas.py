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
    requirement_rationale: str = ""


class LearningStep(BaseModel):
    skill: str
    priority: str
    reason: str
    task: str
    project_idea: str


class CategorySummary(BaseModel):
    category: str
    total_requirements: int
    strong: int
    partial: int
    missing: int
    coverage_score: float


class AnalysisResult(BaseModel):
    overall_score: float
    coverage_score: float
    semantic_score: float
    semantic_mode: str
    semantic_weight: float
    score_band: str = ""
    requirements_found: int
    strong_matches: int
    partial_matches: int
    missing_skills: int
    matched_skills: list[SkillMatch]
    partial_skills: list[SkillMatch]
    missing_skill_matches: list[SkillMatch]
    resume_skills_detected: list[str] = Field(default_factory=list)
    extra_resume_skills: list[str] = Field(default_factory=list)
    category_breakdown: list[CategorySummary] = Field(default_factory=list)
    learning_roadmap: list[LearningStep]
    methodology_note: str


class JobItem(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    job_description: str = Field(min_length=1, max_length=50_000)

    @field_validator("title", "job_description")
    @classmethod
    def strip_fields(cls, value: str) -> str:
        return value.strip()


class CompareRequest(BaseModel):
    resume_text: str = Field(min_length=1, max_length=100_000)
    jobs: list[JobItem] = Field(min_length=1, max_length=5)
    semantic_weight: float = Field(default=0.25, ge=0.0, le=0.5)

    @field_validator("resume_text")
    @classmethod
    def strip_resume(cls, value: str) -> str:
        return value.strip()


class JobComparisonItem(BaseModel):
    title: str
    overall_score: float
    coverage_score: float
    semantic_score: float
    score_band: str
    requirements_found: int
    strong_matches: int
    partial_matches: int
    missing_skills: int
    top_strengths: list[str]
    top_gaps: list[str]


class CompareResult(BaseModel):
    semantic_mode: str
    semantic_weight: float
    resume_skills_detected: list[str]
    rankings: list[JobComparisonItem]
