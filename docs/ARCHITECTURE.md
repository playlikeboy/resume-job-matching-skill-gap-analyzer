# System Architecture

## Request lifecycle

1. The browser accepts pasted resume text or uploads a PDF, DOCX, or TXT file.
2. FastAPI extracts selectable text from the uploaded file in memory. Scanned PDFs are detected and rejected with an OCR guidance error.
3. A curated taxonomy ([`taxonomy.py`](../backend/app/services/taxonomy.py)) extracts canonical skills with exact character spans, occurrence counts, negation filtering, and supporting evidence snippets.
4. The job-description parser ([`requirements.py`](../backend/app/services/requirements.py)) tracks line-level section headings as well as local/inline markers to classify requirements as `required` (`2.0`) or `preferred` (`1.0`).
5. The matcher ([`analysis.py`](../backend/app/services/analysis.py)) compares resume evidence with each job requirement. Direct normalized matches are `strong` (`1.0`); related/semantic evidence above `SEMANTIC_PARTIAL_THRESHOLD` (`0.48`) is `partial` (`0.5`); otherwise `missing` (`0.0`).
6. Weighted coverage, domain category breakdown, and semantic similarity are combined into an explainable score (`overall_score`), with extra detected resume skills surfaced separately.
7. Missing and partial requirements are prioritized (required gaps before preferred gaps) into learning tasks and project ideas.

## Matching formula

For requirement `i`, use `w_i = 2` for required skills and `w_i = 1` for preferred skills. Let `m_i` be `1.0` for strong, `0.5` for partial, and `0.0` for missing.

`Coverage = 100 × Σ(w_i × m_i) / Σ(w_i)`

The default hybrid score is `0.75 × Coverage + 0.25 × SemanticAlignment` (configurable per request via `semantic_weight` in `[0.0, 0.5]`). The 75/25 split is an initial baseline configuration; [`backend/scripts/evaluate.py`](../backend/scripts/evaluate.py) and `docs/EXPERIMENTAL_PROTOCOL.md` provide the framework for comparative evaluation and ablation testing.

## Semantic modes

- `sentence-transformers`: optional model-backed similarity using `all-MiniLM-L6-v2` (enabled via `USE_SENTENCE_TRANSFORMERS=true`).
- `rule-based-fallback`: transparent canonical skill relation rules (`RELATED_SKILLS`) and token overlap for local demos or environments without the optional model.

The API returns `semantic_mode` so the UI and experiments can distinguish model-backed and fallback results. Similarity is a supporting signal and must never be presented as proof of proficiency.

## API

- `GET /api/health` — service health, version, and active semantic mode.
- `GET /api/taxonomy` — curated skill taxonomy grouped by category.
- `POST /api/resume/parse` — parse one PDF, DOCX, or TXT upload into text (up to `MAX_UPLOAD_MB`, default 8 MB).
- `POST /api/analyze` — analyze `resume_text`, `job_description`, and optional `semantic_weight`.
- `POST /api/compare` — rank up to 5 job descriptions against one resume.

## Security and privacy baseline

- Uploaded data is processed in memory and is not persisted by the API.
- File-size limits (`MAX_UPLOAD_MB`), file-type checks, and configurable `CORS_ORIGINS` are enforced via [`config.py`](../backend/app/config.py).
- Synthetic or anonymized examples are used in tests, benchmarks, and commits.
- Before public deployment, add rate limiting, stricter CORS, logging redaction, retention policy, and malware scanning appropriate to the hosting environment.
