from __future__ import annotations

import os
import re
from functools import lru_cache

from app.services.taxonomy import RELATED_SKILLS


def _tokens(value: str) -> set[str]:
    return {token for token in re.findall(r"[a-z0-9+#.]+", value.lower()) if len(token) > 1}


@lru_cache(maxsize=1)
def _load_model():
    from sentence_transformers import SentenceTransformer
    model_name = os.getenv("SENTENCE_TRANSFORMER_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    return SentenceTransformer(model_name)


def semantic_similarity(skill: str, resume_text: str, resume_skills: set[str]) -> tuple[float, str]:
    """Return best similarity signal and its mode; it is not a proficiency estimate."""
    if os.getenv("USE_SENTENCE_TRANSFORMERS", "false").lower() in {"1", "true", "yes"}:
        try:
            import numpy as np
            model = _load_model()
            # Compare the target skill to resume-sized sentence fragments, not to the full document only.
            fragments = [part.strip() for part in re.split(r"[\n.!?;]+", resume_text) if part.strip()]
            if not fragments:
                return 0.0, "sentence-transformers"
            embeddings = model.encode([skill, *fragments], normalize_embeddings=True)
            similarities = np.dot(embeddings[1:], embeddings[0])
            return float(max(0.0, min(1.0, float(np.max(similarities))))), "sentence-transformers"
        except Exception:
            # Do not silently pretend an unavailable model ran; expose the fallback mode.
            pass

    related = RELATED_SKILLS.get(skill, set())
    if related.intersection(resume_skills):
        return 0.55, "rule-based-fallback"

    skill_tokens = _tokens(skill)
    resume_tokens = _tokens(resume_text)
    if not skill_tokens or not resume_tokens:
        return 0.0, "rule-based-fallback"
    overlap = len(skill_tokens & resume_tokens) / len(skill_tokens)
    return float(min(1.0, overlap * 0.7)), "rule-based-fallback"
