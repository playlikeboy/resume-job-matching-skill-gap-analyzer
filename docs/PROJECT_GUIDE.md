# Complete Learning Guide: `matchwise.` (Easy → Advanced)

Welcome! This guide explains the entire **Intelligent Resume–Job Matching & Explainable Skill Gap Analyzer (`matchwise.`)** project step by step—starting from plain-English intuition and moving all the way down to the exact regex patterns, scoring math, Streamlit UI state management, evaluation harness, and deployment.

- **Portfolio & Sample Resume Source:** [https://playlikeboy.github.io/](https://playlikeboy.github.io/) · [https://playlikeboy.github.io/resume](https://playlikeboy.github.io/resume)
- **Repository:** [https://github.com/playlikeboy/resume-job-matching-skill-gap-analyzer](https://github.com/playlikeboy/resume-job-matching-skill-gap-analyzer)

---

## Level 1 — Beginner: What Problem Are We Solving?

Imagine you are a 5th-semester CS student applying for internships. You have a PDF resume and 5 job descriptions (JDs). You want to know:

1. **Which skills do I already prove in my resume?** (with the exact line from my resume so I can verify it!)
2. **Which skills are mandatory vs "nice to have"?**
3. **Which skills am I missing, and what should I build next to close those gaps?**

### Why simple keyword matching fails
If a tool only checks exact words:
- It misses **synonyms/aliases**: your resume says `JS`, `k8s`, or `postgres`, while the JD asks for `JavaScript`, `Kubernetes`, or `PostgreSQL`.
- It triggers **false positives** on English words: `"I want to express interest and go to the next round"` accidentally matches `Express.js` and `Go`!
- It falls for **negations**: `"No prior experience with Kubernetes"` gets counted as knowing Kubernetes!
- It gives **no explanation**: a random number like `"72%"` doesn't tell you *why* or *what to learn next*.

`matchwise.` solves all four problems transparently.

---

## Level 2 — Intermediate: How Data Flows Through the System

```text
  Resume (PDF / DOCX / TXT / Pasted Text)       Job Description(s) (1 to 5 Roles)
                  │                                             │
                  ▼                                             ▼
    [1. Text Extraction]                         [2. Requirement Parser]
    extractors.py (in-memory)                    requirements.py (headings + inline)
                  │                                             │
                  ▼                                             ▼
    [3. Skill Extractor]                         [4. Importance Weighting]
    skill_extraction.py                          required (2.0) vs preferred (1.0)
                  │                                             │
                  └──────────────────┬──────────────────────────┘
                                     ▼
                       [5. Evidence-Aware Matcher]
                       analysis.py + similarity.py
                       Strong (1.0) / Partial (0.5) / Missing (0.0)
                                     │
                    ┌────────────────┴────────────────┐
                    ▼                                 ▼
      [6. Streamlit + Plotly UI]         [7. Prioritized Learning Roadmap]
      streamlit_app.py                   roadmap.py (tasks + project ideas)
```

### Project File Map
- [`streamlit_app.py`](../streamlit_app.py) — Interactive web UI (Single Role Analysis, Compare Multiple Roles, Skill Taxonomy & Benchmark).
- [`backend/app/services/extractors.py`](../backend/app/services/extractors.py) — Reads PDF (`PyMuPDF`), DOCX (`python-docx`), and TXT bytes in memory.
- [`backend/app/services/taxonomy.py`](../backend/app/services/taxonomy.py) — Curated dictionary of `54` canonical skills (`SKILLS`) across `12` domains plus conservative `RELATED_SKILLS`.
- [`backend/app/services/skill_extraction.py`](../backend/app/services/skill_extraction.py) — Boundary-aware regex matching, alias normalization, negation filtering, and evidence snippet extraction.
- [`backend/app/services/requirements.py`](../backend/app/services/requirements.py) — Classifies each JD skill as `required` (`2.0`) or `preferred` (`1.0`).
- [`backend/app/services/similarity.py`](../backend/app/services/similarity.py) — Computes semantic similarity using either `rule-based-fallback` or optional `sentence-transformers`.
- [`backend/app/services/analysis.py`](../backend/app/services/analysis.py) — Orchestrates scoring, category breakdown, and multi-role comparison.
- [`backend/app/services/roadmap.py`](../backend/app/services/roadmap.py) — Converts missing and partial skills into prioritized learning tasks & project ideas.
- [`backend/app/schemas.py`](../backend/app/schemas.py) & [`backend/app/config.py`](../backend/app/config.py) — Pydantic data contracts and environment configuration.
- [`backend/app/main.py`](../backend/app/main.py) — Optional FastAPI REST API exposing the same engine over HTTP.
- [`backend/scripts/evaluate.py`](../backend/scripts/evaluate.py) — Benchmark script comparing `B0` vs `B1` vs `H1` on [`examples/evaluation_dataset.jsonl`](../examples/evaluation_dataset.jsonl).

---

## Level 3 — Code Walkthrough: Module by Module

### 3.1 In-Memory Resume Parsing (`extractors.py`)
`extract_resume_text(filename, content)` inspects the file suffix:
- **`.pdf`**: Opens `fitz.open(stream=content, filetype="pdf")` directly from bytes (never saved to disk). If `page_count > 0` and extracted text is empty, it raises a clear `ValueError` explaining that scanned/image PDFs require OCR.
- **`.docx`**: Opens `Document(BytesIO(content))` and extracts both paragraphs and table cells (many resumes use two-column Word tables!).
- **`.txt`**: Decodes UTF-8, falling back to Latin-1 if needed.

Try it with the included real PDF resume at [`examples/playlikeboy_resume.pdf`](../examples/playlikeboy_resume.pdf) (fetched from [playlikeboy.github.io/resume](https://playlikeboy.github.io/resume)):
- It extracts ~3,524 characters and detects 21 canonical skills (`Python`, `TypeScript`, `Go`, `FastAPI`, `React`, `Next.js`, `PostgreSQL`, `Redis`, `Docker`, `CI/CD`, etc.).

### 3.2 Curated Taxonomy & Regex Guards (`taxonomy.py` & `skill_extraction.py`)
Every entry in `SKILLS` has a `category` and `aliases`, plus optional safety guards:
- **Boundary-aware matching (`_pattern_for`)**:
  ```python
  rf"(?<![A-Za-z0-9]){escaped}(?![A-Za-z0-9]){negative_after}"
  ```
  Why not Python's `\b`? Because skills like `C++` end with `+`, which is not a word character (`\w`), so `\b` fails on `C++`! Negative lookarounds `(?<![A-Za-z0-9])` and `(?![A-Za-z0-9])` work cleanly for both `TS` (won't match inside `"requirements"`) and `C++`.
- **Case sensitivity**: `"Go"` has `"case_sensitive_terms": ["Go"]` so `"go to the next round"` is ignored while `"microservices in Go"` matches.
- **Negative lookahead**: `"express"` in `Express.js` excludes following words like `interest`, `concern`, `thoughts`, `gratitude`, `lane`, `delivery`.
- **Negation filtering (`_is_negated`)**: Checks the 55 characters before a match against `NEGATION_PATTERN` (`"no experience with"`, `"never used"`, `"not familiar with"`, etc.). Enabled (`ignore_negated=True`) for resumes, disabled (`ignore_negated=False`) for job descriptions.
- **Evidence snippet (`_evidence_for`)**: Extracts the containing line/sentence (up to ~220 chars) and counts total `occurrences` across aliases.

### 3.3 Required vs Preferred Parsing (`requirements.py`)
`extract_job_requirements(job_description)` combines three signals in priority order:
1. **Inline after-text** (within 60 chars to sentence end): e.g., `"React is nice to have"` or `"Docker (preferred)"` → `preferred`.
2. **Local before-context** (last 250 chars): checks nearest `PREFERRED_MARKERS` vs `REQUIRED_MARKERS`.
3. **Line-level section headings** (`_build_line_sections`): tracks headings like `Required qualifications:` (`required`, weight `2.0`) vs `Preferred qualifications:` (`preferred`, weight `1.0`). Tracking line offsets ensures long multi-bullet preferred sections don't accidentally revert to required!

### 3.4 Semantic Similarity & Hybrid Matching (`similarity.py` & `analysis.py`)
For each job requirement `r`:
- If found directly in `resume_skills`:
  - `status = "strong"`, `match_value = 1.0`, `similarity = 1.0`, `evidence = snippet`
- Otherwise, `semantic_similarity(skill, resume_text, resume_skill_names)` runs:
  - **Optional ML mode (`USE_SENTENCE_TRANSFORMERS=true`):** Encodes `[skill, *resume_sentences]` with `all-MiniLM-L6-v2` and takes max cosine similarity across resume fragments (clamped to `[0, 1]`).
  - **Default fallback mode (`rule-based-fallback`):** Checks `RELATED_SKILLS.get(skill)` against detected `resume_skills` (returns `0.55` if a related skill is present, e.g., `FastAPI` detected when JD asks for `REST APIs`), otherwise computes token overlap `min(1.0, overlap * 0.7)`.
- If `raw_similarity >= SEMANTIC_PARTIAL_THRESHOLD` (default `0.48`):
  - `status = "partial"`, `match_value = 0.5`
- Else:
  - `status = "missing"`, `match_value = 0.0`

---

## Level 4 — Advanced: Scoring Math, Roadmaps & Evaluation

### 4.1 Scoring Equations
Given requirements $i \in \{1, \dots, n\}$ with weight $w_i \in \{2.0, 1.0\}$, match value $m_i \in \{1.0, 0.5, 0.0\}$, similarity $s_i \in [0, 1]$, and user-selected semantic weight $\alpha \in [0.0, 0.5]$ (default $\alpha = 0.25$):

$$\text{Coverage} = 100 \times \frac{\sum_{i=1}^n w_i \cdot m_i}{\sum_{i=1}^n w_i}$$

$$\text{Semantic} = 100 \times \frac{\sum_{i=1}^n w_i \cdot s_i}{\sum_{i=1}^n w_i}$$

$$\text{Overall} = (1 - \alpha) \cdot \text{Coverage} + \alpha \cdot \text{Semantic}$$

All intermediate calculations use unrounded floats; rounding to 2 decimal places happens only at output time (`AnalysisResult`).

### 4.2 Score Bands & Category Breakdown
- `>= 80`: **Strong alignment**
- `>= 60`: **Moderate alignment**
- `>= 40`: **Developing alignment**
- `< 40`: **Early-stage gap**

`category_breakdown` groups requirements by domain (`Backend`, `Frontend`, `AI/ML`, etc.) and computes per-domain weighted coverage. `extra_resume_skills` lists skills demonstrated in the resume that weren't requested in the JD.

### 4.3 Prioritized Learning Roadmap (`roadmap.py`)
Gaps are sorted by **missing required (`w=2.0`) → missing preferred (`w=1.0`) → partial required → partial preferred**, capped at 12 steps, and paired with concrete learning tasks and portfolio project ideas from `RESOURCE_MAP` (with structured fallback templates for any skill).

### 4.4 Experimental Evaluation: `B0` vs `B1` vs `H1`
Run `cd backend && python scripts/evaluate.py` to compare all three systems on [`examples/evaluation_dataset.jsonl`](../examples/evaluation_dataset.jsonl):
- **B0 (`exact-canonical`):** Matches canonical names only; cannot assign `partial` or resolve aliases.
- **B1 (`taxonomy-aliases`):** Adds alias normalization and required/preferred importance classification, without partial semantic matching.
- **H1 (`rule-based-fallback` / `sentence-transformers`):** Full hybrid pipeline with partial-match detection.

Observed results on the 6-pair synthetic starter benchmark:

| System | Mode | Skill F1 | Match Macro-F1 | Median Latency |
|---|---|---:|---:|---:|
| B0 | `exact-canonical` | `1.000` | `0.325` | `~0.4 ms` |
| B1 | `taxonomy-aliases` | `1.000` | `0.467` | `~1.5 ms` |
| H1 | `rule-based-fallback` | `1.000` | `0.918` | `~1.6 ms` |

> **Research honesty note:** This 6-pair dataset is a synthetic starter benchmark. Real-world validation requires 30–50 human-annotated resume–JD pairs following [`docs/EXPERIMENTAL_PROTOCOL.md`](EXPERIMENTAL_PROTOCOL.md).

---

## Level 5 — Engineering & Viva Prep

### 5.1 Streamlit Architecture & State Pitfalls Solved
In [`streamlit_app.py`](../streamlit_app.py):
- **In-process execution:** Imports `backend/app/services/` directly so it deploys on **Streamlit Community Cloud** as a single Python process without needing a separate FastAPI server.
- **Dynamic compare-role keys:** Each target role in `Compare Multiple Roles` has a monotonic `id` (`cmp_title_{job_id}`, `cmp_jd_{job_id}`) so deleting role #2 never causes Streamlit widget-state collisions.
- **HTML escaping:** All user-supplied resume quotes and job titles pass through `html.escape(...)` before rendering inside styled HTML cards.
- **Automated UI tests:** [`backend/tests/test_streamlit_app.py`](../backend/tests/test_streamlit_app.py) uses `streamlit.testing.v1.AppTest` to click buttons, switch modes, load the sample PDF, and assert zero exceptions.

### 5.2 Common Viva / Presentation Questions & Answers
1. **Why not use an LLM for everything?**
   - LLMs are non-deterministic, slow/costly, and can hallucinate proficiency. Here, every strong match is deterministic and backed by an exact quote from the resume, while semantic similarity is bounded (`α ≤ 0.5`) and clearly labeled.
2. **Why `0.75 * Coverage + 0.25 * Semantic` as default?**
   - Coverage of verified skills should dominate the score (`75%`), while semantic alignment (`25%`) rewards adjacent tooling (e.g., `Flask` vs `REST APIs`) without overriding missing core skills. Users can also inspect `α = 0%` (pure baseline) via the sidebar slider.
3. **Why did you choose Streamlit instead of React?**
   - Unifying the UI and NLP engine in Python eliminates cross-origin (CORS) setup, enables full in-memory PDF/DOCX parsing directly on Streamlit Community Cloud, and simplifies maintenance for a data/NLP project.
4. **How do you prevent false positives on short skill names like `Go`, `TS`, or `Express`?**
   - Boundary lookarounds (`(?<![A-Za-z0-9])`), case sensitivity (`Go`), excluded following words (`express interest`), and a 55-character negation window before matches.

### 5.3 Commands Cheat Sheet
```bash
# Run the Streamlit app locally
.venv/bin/python -m streamlit run streamlit_app.py

# Run all 22 automated tests (matching, evaluation, FastAPI, Streamlit AppTest)
cd backend && ../.venv/bin/python -m pytest -v

# Run the B0 vs B1 vs H1 benchmark
cd backend && ../.venv/bin/python scripts/evaluate.py

# Optional: run the FastAPI REST server separately
cd backend && ../.venv/bin/python -m uvicorn app.main:app --reload --port 8000
```
