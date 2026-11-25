# System Architecture

## Request lifecycle

1. The browser accepts pasted resume text or uploads a PDF/DOCX file.
2. FastAPI extracts selectable text from the uploaded file. Scanned PDFs are not processed in this milestone.
3. A curated taxonomy extracts canonical skills and keeps a short evidence snippet for each match.
4. The job-description parser finds the same canonical skills and classifies nearby wording as required or preferred.
5. The matcher compares resume evidence with each job requirement. Exact normalized matches are strong; related/semantic evidence may be partial; otherwise the skill is missing.
6. A weighted coverage score and a separate similarity signal are combined into an explainable score.
7. Missing and partial requirements are converted into prioritized learning steps and project ideas.

## Matching formula

For requirement `i`, use `w_i = 2` for required skills and `w_i = 1` for preferred skills. Let `m_i` be `1.0` for strong, `0.5` for partial, and `0.0` for missing.

`Coverage = 100 × Σ(w_i × m_i) / Σ(w_i)`

The initial hybrid score is `0.75 × Coverage + 0.25 × SemanticAlignment`. The 75/25 split is an initial proposal from the concept document, not a validated optimum. The experiment plan must test alternative weights and report the chosen configuration.

## Semantic modes

- `sentence-transformers`: optional model-backed similarity using `all-MiniLM-L6-v2`.
- `rule-based-fallback`: transparent related-skill rules and token overlap for local demos or environments without the optional model.

The API returns `semantic_mode` so the UI and experiments can distinguish the model-backed and fallback results. Similarity is a supporting signal and must never be presented as proof of proficiency.

## API

- `GET /api/health` — health check.
- `POST /api/resume/parse` — parse one PDF or DOCX upload into text.
- `POST /api/analyze` — analyze `resume_text`, `job_description`, and optional `semantic_weight`.

## Security and privacy baseline

- Uploaded data is processed in memory and is not persisted by the starter API.
- The first version has no user accounts or history.
- Add file-size limits and reject unsupported file types.
- Use synthetic or anonymized examples in tests and commits.
- Before deployment, add rate limiting, stricter CORS, logging redaction, retention policy and malware scanning appropriate to the hosting environment.
