from __future__ import annotations

import os
from dataclasses import dataclass


def _parse_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _parse_origins(value: str | None) -> list[str]:
    if not value or not value.strip():
        return ["http://localhost:5173", "http://127.0.0.1:5173"]
    return [origin.strip() for origin in value.split(",") if origin.strip()]


@dataclass(frozen=True)
class Settings:
    app_title: str
    app_version: str
    cors_origins: list[str]
    max_upload_bytes: int
    use_sentence_transformers: bool
    sentence_transformer_model: str
    semantic_partial_threshold: float


def get_settings() -> Settings:
    max_mb = int(os.getenv("MAX_UPLOAD_MB", "8"))
    threshold = float(os.getenv("SEMANTIC_PARTIAL_THRESHOLD", "0.48"))
    threshold = max(0.0, min(1.0, threshold))
    return Settings(
        app_title="Resume–Job Match & Skill Gap Analyzer API",
        app_version="0.2.0",
        cors_origins=_parse_origins(os.getenv("CORS_ORIGINS")),
        max_upload_bytes=max(1, max_mb) * 1024 * 1024,
        use_sentence_transformers=_parse_bool(os.getenv("USE_SENTENCE_TRANSFORMERS"), default=False),
        sentence_transformer_model=os.getenv(
            "SENTENCE_TRANSFORMER_MODEL",
            "sentence-transformers/all-MiniLM-L6-v2",
        ),
        semantic_partial_threshold=threshold,
    )
