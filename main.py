from __future__ import annotations

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import AnalyzeRequest
from app.services.analysis import analyze_resume_job
from app.services.extractors import extract_resume_text

app = FastAPI(
    title="Resume–Job Match & Skill Gap Analyzer API",
    version="0.1.0",
    description="Explainable resume-to-job matching for an academic research project.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> dict[str, str]:
    return {"name": "Resume–Job Match & Skill Gap Analyzer", "docs": "/docs"}


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": "0.1.0"}


@app.post("/api/resume/parse")
async def parse_resume(file: UploadFile = File(...)) -> dict[str, str]:
    filename = file.filename or "resume"
    content = await file.read()
    if len(content) > 8 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File too large. Maximum upload size is 8 MB.")
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
