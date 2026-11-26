# Complete Learning Guide: `matchwise.` (Easy → Advanced)

Welcome! This guide teaches the entire **Intelligent Resume–Job Matching & Explainable Skill Gap Analyzer (`matchwise.`)** from zero to deep mastery—using concrete examples, actual code walkthroughs, solved bugs, viva Q&A, and complete step-by-step run instructions.

- **Live Streamlit App:** [https://resume-job-matching-skill-gap-analyzer.streamlit.app/](https://resume-job-matching-skill-gap-analyzer.streamlit.app/)
- **Canva Presentation (14 Slides):** [https://canva.link/wy8akal2lz3jieq](https://canva.link/wy8akal2lz3jieq)
- **Project Report (PDF):** [`docs/Minor_Project_Report_2.pdf`](Minor_Project_Report_2.pdf) | [`docs/Minor_Project_Report_2.docx`](Minor_Project_Report_2.docx)
- **Presenter Script & Viva Q&A:** [`docs/PRESENTATION_SCRIPT.md`](PRESENTATION_SCRIPT.md)
- **Minor Project Report:** [`docs/Minor_Project_Report_2.pdf`](Minor_Project_Report_2.pdf) · [`docs/Minor_Project_Report_2.docx`](Minor_Project_Report_2.docx)
- **Author Portfolio & 7 Sample Resume PDFs:** [https://playlikeboy.github.io/](https://playlikeboy.github.io/) · [https://playlikeboy.github.io/resume](https://playlikeboy.github.io/resume)
- **Team & Guide:** Shaswat Raj (`BTECH/10574/24`), Satyam Hansda (`BTECH/10616/24`) — Guided by **Dr. Sumit Srivastava**, Assistant Professor, Dept. of CSE, BIT Mesra

---

## Level 1 — Beginner: The Intuition in 60 Seconds

Think of `matchwise.` as a **transparent career coach** that sits between your resume and a job description (JD):

1. You give it a **resume** (PDF, DOCX, TXT, pasted text, or one of the **7 real PDFs** from `playlikeboy.github.io` + Alex Example).
2. You give it **1 job description** (or up to **5 roles** to compare side by side).
3. Instead of giving a mystery percentage like most ATS checkers, `matchwise.` answers four exact questions:
   - **What did the job ask for, and how important is each skill?** (`Required = 2.0`, `Preferred = 1.0`)
   - **Where does your resume prove each skill?** (exact quoted sentence from your resume!)
   - **Which skills are Strong (`1.0`), Partial (`0.5`), or Missing (`0.0`)?**
   - **What should you learn and build next?** (prioritized 12-step roadmap starting with missing required skills)

### Why simple keyword counters fail (4 classic traps)
| Trap | Example | What Naive Tools Do | What `matchwise.` Does |
|---|---|---|---|
| **Alias Blindness** | Resume says `JS`, `k8s`, `postgres` | Marks as Missing | Normalizes to `JavaScript`, `Kubernetes`, `PostgreSQL` |
| **English Word Collision** | `"express interest and go forward"` | Falsely detects `Express.js` & `Go` | Case-sensitive `"Go"` + excluded-word lookahead on `"express"` |
| **Negation Blindness** | `"No prior experience with Kubernetes"` | Counts `Kubernetes` as a match! | 55-char negation window rejects it on resumes |
| **No Next Step** | Score = `64%` | Leaves candidate confused | Shows missing required gaps + tasks & project ideas |

---

## Level 2 — Intermediate: Trace One Real Example End-to-End

Suppose we pass this **resume snippet** and **JD snippet** into `analyze_resume_job()`:

- **Resume:** `"Built REST services with FastAPI and Python. Used postgres. No prior experience with Kubernetes."`
- **JD:** `"Required: Python, REST APIs, PostgreSQL. Preferred: Kubernetes."`

Watch what each module does step-by-step:

1. **`extractors.py` (if uploaded as PDF/DOCX):**
   Reads uploaded bytes in memory using `PyMuPDF` (`fitz`) or `python-docx`—never writing files to disk.
2. **`skill_extraction.py` on Resume (`ignore_negated=True`):**
   - `"Python"` → **Found** (alias `"Python"`, evidence = `"Built REST services with FastAPI and Python."`)
   - `"FastAPI"` → **Found** (alias `"FastAPI"`)
   - `"PostgreSQL"` → **Found** via alias `"postgres"`!
   - `"Kubernetes"` → Matched by regex, **rejected by `_is_negated()`** because `"No prior experience with "` precedes it!
3. **`requirements.py` on JD (`ignore_negated=False`):**
   - `Python` → `required` (`w = 2.0`)
   - `REST APIs` → `required` (`w = 2.0`)
   - `PostgreSQL` → `required` (`w = 2.0`)
   - `Kubernetes` → `preferred` (`w = 1.0`, because `"Preferred:"` precedes it)
4. **`similarity.py` + `analysis.py` Matching:**
   - `Python` (`w=2`): direct hit → **Strong** (`m = 1.0`, `σ = 1.0`)
   - `PostgreSQL` (`w=2`): direct alias hit (`postgres`) → **Strong** (`m = 1.0`, `σ = 1.0`)
   - `REST APIs` (`w=2`): not directly in resume, but `RELATED_SKILLS["REST APIs"]` contains `FastAPI` (which IS in resume!) → fallback similarity `σ = 0.55 ≥ 0.48` → **Partial** (`m = 0.5`)
   - `Kubernetes` (`w=1`): negated on resume, and only `Python`/`FastAPI`/`PostgreSQL` present (not in `RELATED_SKILLS["Kubernetes"]`) → `σ = 0.0 < 0.48` → **Missing** (`m = 0.0`)
5. **Final Score Calculation (`α = 0.25`):**
   - Total weight = `2 + 2 + 2 + 1 = 7.0`
   - Coverage = `100 × (2×1.0 + 2×1.0 + 2×0.5 + 1×0.0) / 7.0 = 500 / 7.0 = 71.43%`
   - Semantic = `100 × (2×1.0 + 2×1.0 + 2×0.55 + 1×0.0) / 7.0 = 510 / 7.0 = 72.86%`
   - Overall = `0.75 × 71.43 + 0.25 × 72.86 = 71.79%` (**Moderate alignment**)
6. **`roadmap.py` Output:**
   - Step 1 (**High priority**): `Kubernetes` (Missing)
   - Step 2 (**Medium priority**): `REST APIs` (Partial)

---

## Level 3 — Code Architecture & File-by-File Map

```text
streamlit_app.py                  ← Interactive UI, 7+1 sample resumes, 5 presets, Plotly charts
backend/app/
  ├── config.py                   ← Settings via env vars (MAX_UPLOAD_MB, SEMANTIC_PARTIAL_THRESHOLD, etc.)
  ├── schemas.py                  ← Typed Pydantic contracts (AnalysisResult, CompareResult, SkillMatch, LearningStep)
  ├── main.py                     ← Optional FastAPI HTTP server (/api/analyze, /api/compare, /api/resume/parse)
  └── services/
      ├── extractors.py           ← In-memory PDF (PyMuPDF), DOCX (python-docx), TXT extraction
      ├── taxonomy.py             ← 54 canonical skills, 87 aliases across 12 domains + RELATED_SKILLS
      ├── skill_extraction.py     ← Boundary-aware regex, negation filter, evidence snippet builder
      ├── requirements.py         ← Section headings + local window + inline preferred/required parser
      ├── similarity.py           ← Rule-based fallback OR Sentence Transformers (all-MiniLM-L6-v2)
      ├── analysis.py             ← Coverage, semantic, hybrid score, domain breakdown, multi-role ranking
      └── roadmap.py              ← Prioritized 12-step task & project-idea generator
backend/scripts/evaluate.py       ← Reproducible B0 vs B1 vs H1 benchmark script
backend/tests/                    ← 22 automated pytest tests (matching, evaluation, FastAPI, Streamlit AppTest)
examples/resumes/                 ← 7 real PDF resumes from playlikeboy.github.io/resume*
```

### Real Bugs & Subtle Edge Cases Solved in This Codebase
1. **Why `\b` fails on `C++` and `CI/CD`:** Python's `\b` checks transitions between `\w` and `\W`. Since `+` in `C++` is `\W`, `C++\b` fails! Solution in `skill_extraction.py`: `(?<![A-Za-z0-9]){escaped}(?![A-Za-z0-9])`.
2. **Why `TS` won't match `"requirements"`:** `(?<![A-Za-z0-9])ts(?![A-Za-z0-9])` fails inside `"requirements"` because `n` precedes `ts`.
3. **Why long Preferred sections used to lose context:** Early regex windows only looked back 250 characters. `_build_line_sections()` in `requirements.py` parses colon-ended or standalone headings across the whole JD so even 10-line Preferred sections keep `weight = 1.0`.
4. **Why Streamlit `st.tabs` + dynamic lists broke state:** Two tabs rendering `st.text_area(..., key="resume_text")` trigger `DuplicateWidgetID`, and deleting an item from a list shifts indices. Solution in `streamlit_app.py`: horizontal workspace switcher (`st.radio`) + monotonic unique `id` per compare job (`cmp_title_{job_id}`).
5. **Why Streamlit buttons/metrics showed `...`:** Narrow `st.columns(...)` caused CSS `text-overflow: ellipsis`. Solution: custom CSS wrapping overrides + spacious 2-row preset layout + `automargin=True` on Plotly axes.

---

## Level 4 — Advanced: Formulas, Benchmarks & Trade-offs

### 4.1 Mathematical Formulas
For requirements $i = 1 \dots n$ with importance weights $w_i \in \{2.0, 1.0\}$, match values $m_i \in \{1.0, 0.5, 0.0\}$, similarity signals $\sigma_i \in [0, 1]$, threshold $\tau = 0.48$, and semantic weight $\alpha \in [0.0, 0.5]$ (default $0.25$):

$$\text{Coverage} = 100 \times \frac{\sum_{i=1}^n w_i \cdot m_i}{\sum_{i=1}^n w_i}, \qquad \text{Semantic} = 100 \times \frac{\sum_{i=1}^n w_i \cdot \sigma_i}{\sum_{i=1}^n w_i}$$

$$\text{Overall} = (1 - \alpha)\cdot\text{Coverage} + \alpha\cdot\text{Semantic}$$

### 4.2 Synthetic Benchmark (`B0` vs `B1` vs `H1`)
Evaluated on [`examples/evaluation_dataset.jsonl`](../examples/evaluation_dataset.jsonl) (6 internship role families, 41 labeled requirements):

| System | Description | Skill F1 | Match Macro-F1 | Accuracy | Median Latency |
|---|---|---:|---:|---:|---:|
| **B0** | Exact canonical names only | `1.000` | `0.325` | `46.3%` | `~0.4 ms` |
| **B1** | Taxonomy + aliases + 2:1 weights (no partial) | `1.000` | `0.467` | `70.7%` | `~1.4 ms` |
| **H1** | Full hybrid (`rule-based-fallback`, $\tau=0.48$) | `1.000` | `0.918` | `95.1%` | `~1.5 ms` |

- **Why did B1 beat B0?** Alias normalization recovered all 9 strong matches written as `"JS"`, `"TS"`, `"ReactJS"`, or `"postgres"`.
- **Why did H1 beat B1?** `RELATED_SKILLS` detected 11 of 12 partial matches (`σᵢ = 0.55 ≥ 0.48`).
- **Known Error Analysis (Section 4.8 of Report):**
  1. `syn-002` (`SQLite` → partial for `PostgreSQL`): reflects a taxonomy policy choice.
  2. `syn-005` (`"js"` matching inside `"Node.js"`): `.` is not in `[A-Za-z0-9]`, documented for future boundary tightening.

---

## Level 5 — How to Run Everything in Detail + Viva Prep

### 5.1 Step-by-Step Local Setup & Run
```bash
# 1. Clone and enter repo
git clone https://github.com/playlikeboy/resume-job-matching-skill-gap-analyzer.git
cd resume-job-matching-skill-gap-analyzer

# 2. Create Python 3.11+ virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate              # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 3. Launch the Streamlit app
streamlit run streamlit_app.py
```
Open **`http://localhost:8501`** (or use the hosted app at **[https://resume-job-matching-skill-gap-analyzer.streamlit.app/](https://resume-job-matching-skill-gap-analyzer.streamlit.app/)**).

### 5.2 Run Tests, Benchmark & Optional Modes
```bash
# Install backend + FastAPI test dependencies (if running API tests too)
pip install -r backend/requirements.txt

# Run all 22 automated tests (matching, evaluation, FastAPI, Streamlit AppTest)
cd backend && pytest -v

# Run B0 vs B1 vs H1 evaluation table
python scripts/evaluate.py

# Optional: run FastAPI REST server separately on port 8000
uvicorn app.main:app --reload --port 8000

# Optional: enable Sentence Transformers (all-MiniLM-L6-v2)
pip install -r backend/requirements-ml.txt
USE_SENTENCE_TRANSFORMERS=true streamlit run ../streamlit_app.py
```

### 5.3 Top Questions Examiners Ask (See [`docs/PRESENTATION_SCRIPT.md`](PRESENTATION_SCRIPT.md) for full script!)
1. **Why not just use GPT/LLMs?** → Non-deterministic, costly, opaque, and prone to inventing proficiency. `matchwise.` is deterministic, ~1.5 ms, and quotes exact resume evidence.
2. **How do you prevent false positives on `"Go"`, `"TS"`, or `"No experience with Kubernetes"`?** → Case sensitivity on `"Go"`, excluded following words on `"express"`, boundary lookarounds `(?<![A-Za-z0-9])`, and a 55-char `NEGATION_PATTERN` window.
3. **Why replace React with Streamlit?** → Unified Python stack eliminates CORS/dual-hosting, enables native PDF/DOCX parsing on Streamlit Community Cloud, and supports interactive Plotly visualizations.
4. **What are the honest limitations?** → 54-skill entry-level scope, selectable-text-only PDFs (no OCR yet), and synthetic starter evaluation awaiting 30–50 human-annotated pairs.
