from __future__ import annotations

import logging
import time

from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.schemas import AnalyzeRequest, CompareRequest
from app.services.analysis import analyze_resume_job, compare_resume_to_jobs
from app.services.extractors import extract_resume_text
from app.services.taxonomy import SKILLS

logger = logging.getLogger("matchwise")
settings = get_settings()

app = FastAPI(
    title=settings.app_title,
    version=settings.app_version,
    description="Explainable resume-to-job matching for an academic research project.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    started = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = (time.perf_counter() - started) * 1000.0
    response.headers["X-Process-Time-Ms"] = f"{elapsed_ms:.2f}"
    return response


@app.get("/")
def root() -> dict[str, str]:
    return {
        "name": "Resume–Job Match & Skill Gap Analyzer",
        "version": settings.app_version,
        "docs": "/docs",
    }


@app.get("/api/health")
def health() -> dict[str, str]:
    active_settings = get_settings()
    return {
        "status": "ok",
        "version": active_settings.app_version,
        "semantic_mode": "sentence-transformers" if active_settings.use_sentence_transformers else "rule-based-fallback",
    }


@app.get("/api/taxonomy")
def get_taxonomy() -> dict:
    categories: dict[str, list[dict[str, object]]] = {}
    for canonical, metadata in SKILLS.items():
        category = metadata["category"]
        categories.setdefault(category, []).append({
            "skill": canonical,
            "aliases": metadata.get("aliases", []),
        })
    return {
        "total_skills": len(SKILLS),
        "categories": categories,
    }


@app.post("/api/resume/parse")
async def parse_resume(file: UploadFile = File(...)) -> dict[str, str]:
    filename = file.filename or "resume"
    content = await file.read()
    if len(content) > settings.max_upload_bytes:
        max_mb = settings.max_upload_bytes // (1024 * 1024)
        raise HTTPException(status_code=413, detail=f"File too large. Maximum upload size is {max_mb} MB.")
    try:
        text = extract_resume_text(filename, content)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if not text.strip():
        raise HTTPException(status_code=422, detail="No readable text was found in this file.")
    return {"filename": filename, "text": text}


@app.post("/api/analyze")
def analyze(request: AnalyzeRequest) -> dict:
    if not request.resume_text.strip():
        raise HTTPException(status_code=422, detail="Resume text cannot be empty.")
    if not request.job_description.strip():
        raise HTTPException(status_code=422, detail="Job description cannot be empty.")
    try:
        result = analyze_resume_job(
            resume_text=request.resume_text,
            job_description=request.job_description,
            semantic_weight=request.semantic_weight,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return result.model_dump()


@app.post("/api/compare")
def compare(request: CompareRequest) -> dict:
    if not request.resume_text.strip():
        raise HTTPException(status_code=422, detail="Resume text cannot be empty.")
    try:
        result = compare_resume_to_jobs(
            resume_text=request.resume_text,
            jobs=request.jobs,
            semantic_weight=request.semantic_weight,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return result.model_dump()
