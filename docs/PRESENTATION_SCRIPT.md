# How to Present the 5th-Semester PPT (All 14 Slides) + Viva Q&A + Complete Run Guide

This guide prepares **Shaswat Raj (`BTECH/10574/24`)** and **Satyam Hansda (`BTECH/10616/24`)** to present **`matchwise.` — Intelligent Resume–Job Matching & Explainable Skill Gap Analyzer** (guided by **Dr. Sumit Srivastava**, Assistant Professor, Dept. of CSE, BIT Mesra) smoothly, confidently, and within a typical **8–10 minute** evaluation slot.

---

## 1. Quick Presentation Strategy & Split Between Teammates

- **Total Slides:** 14 slides (strictly within BIT Mesra's 12–15 slide guideline).
- **Recommended Time:** ~9 minutes speaking + 3 minutes live demo / Q&A.
- **Suggested Two-Presenter Split:**
  - **Presenter 1 (Satyam / Shaswat — Problem, Architecture & Methodology):** Slides **1 to 8** (~4.5 min).
  - **Presenter 2 (Shaswat / Satyam — Tech Stack, Live Demo, Results & Conclusion):** Slides **9 to 14** (~4.5 min).
- **Resources to keep open before your turn:**
  1. **Live Streamlit App:** `https://resume-job-matching-skill-gap-analyzer.streamlit.app/`
  2. **Canva Presentation:** `https://canva.link/b49q19khynjv1j9` (or local [`docs/Matchwise_5th_Sem_Presentation.pptx`](Matchwise_5th_Sem_Presentation.pptx))
  3. **Canva Project Report:** `https://canva.link/5n32fpxtsql4sbn` (and PDF [`docs/Minor_Project_Report_2.pdf`](Minor_Project_Report_2.pdf))

---

## 2. Slide-by-Slide Speaking Script (All 14 Slides)

### Slide 1 — Title Slide *(~20 sec)*
- **What is on screen:** Project title, BIT Mesra Dept. of CSE header, Shaswat Raj (`BTECH/10574/24`), Satyam Hansda (`BTECH/10616/24`), Dr. Sumit Srivastava (Assistant Professor), live Streamlit URL.
- **What to say:**
  > *"Good morning/afternoon respected panel members and Dr. Sumit Srivastava. I am [Your Name], and along with my teammate [Partner Name], we present our 5th-semester B.Tech. CSE Minor Project: **matchwise. — Intelligent Resume–Job Matching and Explainable Skill Gap Analyzer**."*

### Slide 2 — Motivation & Background *(~35 sec)*
- **Key message:** Students waste time manually comparing resumes to job descriptions, while keyword-based ATS checkers fail silently.
- **What to say:**
  > *"When applying for internships, students rarely know which job requirements their resume already proves and which skills they actually lack. Simple keyword tools fail for three reasons: they miss aliases like `JS` for `JavaScript` or `k8s` for `Kubernetes`, they trigger false matches on English prose like `'express interest'`, and they give a bare percentage with zero explanation or next steps."*

### Slide 3 — Problem Statement *(~35 sec)*
- **Key message:** Four concrete sub-problems + privacy constraint (in-memory only).
- **What to say:**
  > *"Our problem statement is to take a candidate's resume—PDF, DOCX, TXT, or pasted text—and one or more job descriptions, then: extract skills accurately, distinguish mandatory from preferred skills, grade each requirement with verifiable resume evidence, and turn gaps into a prioritized learning plan—all processed purely in memory without storing candidate data."*

### Slide 4 — Objectives & Scope *(~35 sec)*
- **Key message:** All 6 core objectives implemented in `v0.2.0`; honest scope boundaries.
- **What to say:**
  > *"All seven project objectives in our report are implemented in version 0.2.0, spanning entry-level SWE, Full-Stack, Data, ML/NLP, and Cloud/DevOps roles. To keep the system verifiable and honest, scanned-PDF OCR, user accounts, and job-board scraping are intentionally deferred to future scope."*

### Slide 5 — Related Work & Literature Context *(~40 sec)*
- **Key message:** Why neural recruitment models (`PJFNN`, `APJFNN`) aren't practical for students, and why our hybrid rule+embedding approach bridges the gap.
- **What to say:**
  > *"Prior person–job fit models like PJFNN and APJFNN require massive private recruitment histories. Domain-trained extractors like SkillSpan need labeled datasets, while pure TF-IDF misses synonyms. We combine a transparent 54-skill taxonomy (inspired by ESCO) with optional Sentence-BERT / MiniLM embeddings and explicit evidence quotes—requiring zero training data."*

### Slide 6 — Research Gap & Contributions *(~40 sec)*
- **Key message:** State the Research Question clearly, then highlight C1–C4.
- **What to say:**
  > *"Our central research question asks whether combining normalized skill extraction, weighted coverage, and semantic similarity yields better, more explainable feedback than exact keyword matching alone. Our four contributions are: boundary-aware extraction with negation filtering (C1), 2:1 required/preferred weighting (C2), a reproducible B0/B1/H1 evaluation script (C3), and our live Streamlit dashboard (C4)."*

### Slide 7 — Dataset, Taxonomy & Experimental Hygiene *(~40 sec)*
- **Key message:** Explain the 54 skills, 87 aliases, 12 domains, and the synthetic benchmark (`evaluation_dataset.jsonl`).
- **What to say:**
  > *"As shown in the chart, our curated taxonomy covers 54 canonical skills and 87 aliases across 12 technical domains, paired with a conservative `RELATED_SKILLS` map for partial credit. For reproducible testing without leaking personal data, we built a 6-pair synthetic benchmark (`41` labeled requirements) across six internship role families."*

### Slide 8 — System Architecture (Graphical Flow) *(~45 sec)*
- **Key message:** Walk left-to-right across the architecture diagram.
- **What to say:**
  > *"Here is our system pipeline. On the top branch, `extractors.py` reads PDF, DOCX, or TXT bytes in memory and `skill_extraction.py` extracts normalized skills with exact evidence snippets. On the bottom branch, `requirements.py` parses job descriptions into required (`2.0`) and preferred (`1.0`) weights. Both merge in `analysis.py`, which computes coverage and semantic scores and feeds the Streamlit + Plotly UI and 12-step roadmap."*

### Slide 9 — Methodology & Mathematical Formulation *(~50 sec)*
- **Key message:** Walk through the two equations, weights, and `Strong / Partial / Missing` rules.
- **What to say:**
  > *"Mathematically, each requirement `i` gets weight `2.0` if required or `1.0` if preferred, and match score `1.0` for Strong, `0.5` for Partial, or `0.0` for Missing. Weighted Coverage is `100 × Σ(wᵢ·mᵢ) / Σ(wᵢ)`. The Overall Score blends `(1 - α)·Coverage + α·Semantic`, defaulting to 75% coverage and 25% semantic similarity—with a slider letting the user test pure baseline (`α = 0`) up to `α = 0.5`. Partial matches require similarity `≥ 0.48`, and fallback vs embedding mode is always displayed explicitly."*

### Slide 10 — Tools & Techniques Used *(~30 sec)*
- **Key message:** Highlight unified Python + Streamlit + Plotly + PyMuPDF + pytest/AppTest.
- **What to say:**
  > *"Our stack is unified in Python: Streamlit and Plotly power the interactive UI and charts; PyMuPDF and python-docx handle in-memory parsing; boundary-aware regex and optional `all-MiniLM-L6-v2` embeddings drive matching; FastAPI remains available as an optional REST layer; and 22 automated pytest + AppTest tests verify every layer."*

### Slide 11 — Application Demo & Features *(~45 sec — Switch to Live App if permitted!)*
- **Key message:** Show the 7 live sample PDFs, 5 role presets, evidence cards, multi-role ranking, and Markdown/JSON export.
- **What to say:**
  > *"In our live Streamlit app, we can either upload a PDF/DOCX/TXT resume or pick from 7 real domain-tailored resume PDFs (`General`, `SDE`, `FDE`, `DevOps`, `AI/ML`, `Full-Stack`, `Founding Engineer`) plus Alex Example. Running a match produces an interactive gauge, domain coverage bars, Strong/Partial/Missing cards with exact resume quotes, a prioritized roadmap, and one-click Markdown/JSON export—and Compare Mode ranks up to 5 roles simultaneously."*

### Slide 12 — Results & Discussion *(~50 sec)*
- **Key message:** Quote the exact numbers and explain *why* Macro-F1 jumped (`0.325 → 0.467 → 0.918`).
- **What to say:**
  > *"On the synthetic benchmark, all three systems achieve `1.000` skill-detection F1, while match Macro-F1 rises sharply from `0.325` in exact keyword baseline (`B0`) to `0.467` in weighted taxonomy (`B1`)—recovering 9 strong matches hidden behind aliases like `JS` and `postgres`—and reaches `0.918` in our hybrid pipeline (`H1`) by detecting 11 of 12 partial matches at ~1.5 ms per pair. All 22 automated tests pass, and we candidly note this is a 6-pair synthetic benchmark pending larger human annotation."*

### Slide 13 — Conclusion, Limitations & Future Work *(~35 sec)*
- **Key message:** Summarize achievement honestly and present concrete next milestones.
- **What to say:**
  > *"To conclude, we delivered a transparent, deployed career-readiness web app that replaces black-box scores with evidence and actionable roadmaps. Its main limitations are the 54-skill scope, selectable-text-only PDFs, and synthetic-only evaluation so far. Next steps include evaluating 30–50 human-annotated pairs with `all-MiniLM-L6-v2`, adding OCR for scanned PDFs, handling `'X or Y'` alternatives, and aligning with ESCO."*

### Slide 14 — References & Q&A *(~15 sec)*
- **What to say:**
  > *"These are our primary academic and software references; all architecture diagrams and charts were generated directly from our project code and benchmark runs. Thank you—we are happy to take your questions or show a live demo."*

---

## 3. Questions That Can Be Asked During Presentation (Viva Q&A Bank)

### Technical & Algorithmic Questions
1. **Q: Why did you choose a curated taxonomy instead of training a NER model or calling an LLM API?**
   - **A:** A curated 54-skill taxonomy requires zero labeled training data, runs in ~1.5 ms, is 100% deterministic and auditable, and never hallucinates skills. Every match points directly to a rule and an exact resume quote. We also designed an optional `sentence-transformers` mode so learned semantic representations can be ablated cleanly against the baseline.
2. **Q: Why do you use `(?<![A-Za-z0-9])` instead of Python's `\b` word boundary?**
   - **A:** `\b` only works between `\w` and `\W` characters. Skills containing punctuation like `C++` or `CI/CD` end with non-word characters, so `\b` fails to match them. Negative lookarounds around `[A-Za-z0-9]` handle `C++`, `Node.js`, and `CI/CD` while still blocking `TS` from matching inside `"requirements"`.
3. **Q: Wait—didn't your error analysis find a boundary edge case with `Node.js` and `js`?**
   - **A:** Yes! In `syn-005`, `"js"` matched inside `"Node.js"` because `.` is not in `[A-Za-z0-9]`. Documenting this in Section 4.8 shows real error analysis; fixing it requires also excluding a preceding `.` (or matching multi-token boundaries first) in `_pattern_for()`.
4. **Q: How do you avoid false positives on words like `"Go"` or `"express"`?**
   - **A:** `"Go"` is marked in `case_sensitive_terms`, so lowercase `"go"` in prose is ignored. `"express"` uses a negative lookahead (`excluded_following_words`) to ignore `"express interest"`, `"express concern"`, `"express delivery"`, etc. On resumes, `NEGATION_PATTERN` also rejects matches preceded within 55 characters by phrases like `"no prior experience with"` or `"never used"`.
5. **Q: Why weight Required as `2.0` and Preferred as `1.0`, and why default `α = 0.25`?**
   - **A:** Required qualifications carry twice the impact of nice-to-have skills so missing a core requirement lowers readiness appropriately. Setting `α = 0.25` keeps verified skill coverage dominant (`75%`) while letting semantic similarity (`25%`) reward adjacent technologies without overriding missing core skills—and the sidebar slider lets any user inspect `α = 0%` (pure coverage) to `50%`.
6. **Q: What is the difference between `B0`, `B1`, and `H1`?**
   - **A:** `B0` checks exact canonical names only (Macro-F1 `0.325`). `B1` adds alias normalization, negation filtering, and 2:1 weighting (Macro-F1 `0.467`). `H1` adds partial-match detection (`σᵢ ≥ 0.48`) via related skills or embeddings (Macro-F1 `0.918`).
7. **Q: Why did you switch from React + Vite to Streamlit?**
   - **A:** Unifying the UI and NLP engine in Python removes CORS/dual-server deployment overhead, allows full in-memory PyMuPDF/python-docx PDF/DOCX parsing directly on Streamlit Community Cloud (where static GitHub Pages couldn't parse PDFs), and simplifies interactive Plotly visualizations while keeping FastAPI available as an optional REST API.

### Evaluation, Security & Practical Questions
8. **Q: Is `0.918` Macro-F1 proof that your system works on real resumes?**
   - **A:** No—and we explicitly state that in Section 4.11! That score is on a 6-pair synthetic starter benchmark (`41` requirements) designed to sanity-check the pipeline. Real-world claims require 30–50 independently annotated resumes under `docs/EXPERIMENTAL_PROTOCOL.md`.
9. **Q: What happens if someone uploads a scanned image PDF or a huge file?**
   - **A:** Files larger than `MAX_UPLOAD_MB` (8 MB) are rejected immediately. If PyMuPDF opens a PDF (`page_count > 0`) and finds zero selectable text, `extractors.py` rejects it with a clear message explaining that scanned PDFs require OCR.
10. **Q: Do you store uploaded resumes anywhere?**
    - **A:** No. All uploaded PDF/DOCX/TXT bytes are processed strictly in memory (`BytesIO` / PyMuPDF memory stream) and discarded after analysis. All custom HTML cards also escape user text with `html.escape()` to prevent injection.
11. **Q: How does the app handle `"FastAPI or Express.js"` in a job description?**
    - **A:** Currently `requirements.py` extracts both as separate requirements; handling disjunctive `"X or Y"` skill groups is documented as an error-analysis finding and future improvement.

---

## 4. How to Run the App Everything in Detail

### Option A — Use the Live Deployed Website (Fastest for Demo)
1. Open **[https://resume-job-matching-skill-gap-analyzer.streamlit.app/](https://resume-job-matching-skill-gap-analyzer.streamlit.app/)**.
2. Use the top bar to open the **Canva PPT**, **PowerPoint**, **Canva Report**, **Report PDF**, or **Project Guide**.
3. Pick any of the **8 sample resumes** (Alex Example + 7 `playlikeboy.github.io` PDFs) or upload your own `.pdf`, `.docx`, or `.txt` resume.
4. Pick a target role preset (or paste any job description) and click **Analyse match**, or switch to **Compare Multiple Roles** / **Skill Taxonomy & Benchmark**.

### Option B — Run Locally on Linux / macOS / Windows
1. **Clone the repository:**
   ```bash
   git clone https://github.com/playlikeboy/resume-job-matching-skill-gap-analyzer.git
   cd resume-job-matching-skill-gap-analyzer
   ```
2. **Create and activate a Python 3.11+ virtual environment:**
   ```bash
   python3 -m venv .venv
   # macOS / Linux:
   source .venv/bin/activate
   # Windows PowerShell:
   .venv\Scripts\Activate.ps1
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *(If you also want to run the optional FastAPI server and full pytest suite: `pip install -r backend/requirements.txt`.)*
4. **Launch the Streamlit application:**
   ```bash
   streamlit run streamlit_app.py
   ```
   Open **`http://localhost:8501`** in your browser.

### Option C — Enable Real Sentence-Transformer Embeddings (Optional ML Mode)
```bash
pip install -r backend/requirements-ml.txt
export USE_SENTENCE_TRANSFORMERS=true   # Windows PowerShell: $env:USE_SENTENCE_TRANSFORMERS="true"
streamlit run streamlit_app.py
```
The first analysis downloads `sentence-transformers/all-MiniLM-L6-v2` (~90 MB), and the sidebar badge switches from `rule-based-fallback` to `sentence-transformers`.

### Option D — Run Automated Tests & Benchmark Script
```bash
cd backend
pytest -v
python scripts/evaluate.py
```
Expected: **22 passed** across `test_api.py` (6), `test_evaluation.py` (2), `test_matching.py` (10), and `test_streamlit_app.py` (4), plus the `B0` vs `B1` vs `H1` benchmark table.

### Option E — Run Optional FastAPI Server or Docker Compose
- **FastAPI only:**
  ```bash
  cd backend
  uvicorn app.main:app --reload --port 8000
  ```
  Interactive OpenAPI docs: `http://localhost:8000/docs`.
- **Docker Compose (Streamlit on `8501` + FastAPI on `8000`):**
  ```bash
  docker compose up --build
  ```
