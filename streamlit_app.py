"""Streamlit interface for matchwise. — Resume–Job Matching & Explainable Skill Gap Analyzer."""

from __future__ import annotations

import html
import json
import sys
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

REPO_ROOT = Path(__file__).resolve().parent
BACKEND_ROOT = REPO_ROOT / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.config import get_settings  # noqa: E402
from app.schemas import AnalysisResult, CompareResult, JobItem, SkillMatch  # noqa: E402
from app.services.analysis import analyze_resume_job, compare_resume_to_jobs  # noqa: E402
from app.services.extractors import extract_resume_text  # noqa: E402
from app.services.taxonomy import SKILLS  # noqa: E402
from scripts.evaluate import evaluate  # noqa: E402

RESUMES_DIR = REPO_ROOT / "examples" / "resumes"
SAMPLE_PDF_PATH = REPO_ROOT / "examples" / "playlikeboy_resume.pdf"
PPT_PATH = REPO_ROOT / "docs" / "Matchwise_5th_Sem_Presentation.pptx"
REPORT_PDF_PATH = REPO_ROOT / "docs" / "Minor_Project_Report_2.pdf"

PORTFOLIO_URL = "https://playlikeboy.github.io/"
RESUME_PAGE_URL = "https://playlikeboy.github.io/resume"
LIVE_APP_URL = "https://resume-job-matching-skill-gap-analyzer.streamlit.app/"
REPO_URL = "https://github.com/playlikeboy/resume-job-matching-skill-gap-analyzer"
CANVA_PPT_URL = "https://canva.link/wy8akal2lz3jieq"
REPORT_GITHUB_URL = f"{REPO_URL}/blob/main/docs/Minor_Project_Report_2.pdf"
PPT_GITHUB_URL = f"{REPO_URL}/blob/main/docs/Matchwise_5th_Sem_Presentation.pptx"
PPT_VIEWER_URL = (
    "https://view.officeapps.live.com/op/view.aspx?src="
    "https%3A%2F%2Fraw.githubusercontent.com%2Fplaylikeboy%2Fresume-job-matching-skill-gap-analyzer"
    "%2Fmain%2Fdocs%2FMatchwise_5th_Sem_Presentation.pptx"
)
GUIDE_URL = f"{REPO_URL}/blob/main/docs/PROJECT_GUIDE.md"
SCRIPT_URL = f"{REPO_URL}/blob/main/docs/PRESENTATION_SCRIPT.md"

SAMPLE_RESUME = """Alex Example
Computer Science student

Projects
- Built REST APIs using Python and FastAPI with pytest unit tests.
- Developed responsive interfaces with React, JavaScript and TypeScript.
- Used PostgreSQL and SQL for structured data storage.
- Worked with Git, Docker and Linux during team projects.
- Explored NLP, Machine Learning and sentence embeddings in an academic prototype."""

SAMPLE_RESUMES: dict[str, dict[str, str]] = {
    "General Resume — Shaswat Raj (PDF)": {
        "kind": "pdf",
        "file": str(RESUMES_DIR / "resume.pdf"),
        "fallback_file": str(SAMPLE_PDF_PATH),
        "url": "https://playlikeboy.github.io/resume",
        "preset": "swe",
    },
    "Software Development Engineer (SDE) — Shaswat Raj (PDF)": {
        "kind": "pdf",
        "file": str(RESUMES_DIR / "resume-sde.pdf"),
        "url": "https://playlikeboy.github.io/resume/sde",
        "preset": "swe",
    },
    "Full-Stack Engineer — Shaswat Raj (PDF)": {
        "kind": "pdf",
        "file": str(RESUMES_DIR / "resume-fullstack.pdf"),
        "url": "https://playlikeboy.github.io/resume/fullstack",
        "preset": "fullstack",
    },
    "DevOps & Cloud Engineer — Shaswat Raj (PDF)": {
        "kind": "pdf",
        "file": str(RESUMES_DIR / "resume-devops.pdf"),
        "url": "https://playlikeboy.github.io/resume/devops",
        "preset": "devops",
    },
    "AI / ML Engineer — Shaswat Raj (PDF)": {
        "kind": "pdf",
        "file": str(RESUMES_DIR / "resume-ai.pdf"),
        "url": "https://playlikeboy.github.io/resume/ai",
        "preset": "ml",
    },
    "Forward Deployed Engineer (FDE) — Shaswat Raj (PDF)": {
        "kind": "pdf",
        "file": str(RESUMES_DIR / "resume-fde.pdf"),
        "url": "https://playlikeboy.github.io/resume/fde",
        "preset": "fde",
    },
    "Founding Engineer — Shaswat Raj (PDF)": {
        "kind": "pdf",
        "file": str(RESUMES_DIR / "resume-founding.pdf"),
        "url": "https://playlikeboy.github.io/resume/founding",
        "preset": "fullstack",
    },
    "Alex Example — Academic Prototype (Text)": {
        "kind": "text",
        "url": REPO_URL,
        "preset": "swe",
    },
}

ROLE_PRESETS: dict[str, dict[str, str]] = {
    "swe": {
        "label": "SWE Intern",
        "job_description": """Software Engineering Intern

Required qualifications
- Strong Python and JavaScript fundamentals.
- Experience building REST APIs using FastAPI or Express.js.
- SQL and PostgreSQL knowledge.
- Git, Unit Testing and Docker familiarity.

Preferred qualifications
- React and TypeScript experience.
- Exposure to NLP or Machine Learning.""",
    },
    "fullstack": {
        "label": "Full-Stack",
        "job_description": """Full-Stack Software Engineer

Required qualifications
- Strong TypeScript, JavaScript, and React or Next.js experience.
- Backend API development with Node.js, Express.js, or FastAPI.
- PostgreSQL, Redis, and REST APIs design.
- Git, Docker, and CI/CD (GitHub Actions) workflow experience.

Preferred qualifications
- Go or Python backend scripting.
- Tailwind CSS and Linux production debugging.""",
    },
    "devops": {
        "label": "DevOps / Cloud",
        "job_description": """DevOps & Cloud Engineering Intern

Required qualifications
- Linux administration, bash scripting, and Git workflows.
- Docker containerization and CI/CD pipelines with GitHub Actions.
- Python or Go automation tooling.

Preferred qualifications
- Kubernetes orchestration.
- AWS, Google Cloud (GCP), or Azure familiarity.""",
    },
    "ml": {
        "label": "AI / ML",
        "job_description": """Machine Learning & NLP Intern

Required qualifications
- Python programming and scikit-learn or PyTorch experience.
- Foundations in Machine Learning, Deep Learning, and NLP.
- Git and Linux workflow familiarity.

Preferred qualifications
- Sentence Transformers or spaCy experience.
- Docker and FastAPI deployment basics.""",
    },
    "fde": {
        "label": "FDE / Founding",
        "job_description": """Forward Deployed / Founding Software Engineer

Required qualifications
- Full-stack product engineering with TypeScript, React, Next.js, and Node.js.
- API and data layer ownership with Python, FastAPI, PostgreSQL, and Redis.
- Docker, Git, CI/CD, and Linux deployment ownership.

Preferred qualifications
- Go or C++ systems programming.
- NLP or AI workflow integration.""",
    },
    "data": {
        "label": "Data Analyst",
        "job_description": """Data Analyst Intern

Required qualifications
- Strong SQL and Python skills for querying and cleaning data.
- Experience with pandas, NumPy, and Data Analysis in Jupyter.
- Data Visualization using matplotlib or plotly.

Preferred qualifications
- Statistics and hypothesis testing.
- PostgreSQL or MySQL experience.""",
    },
}

DEFAULT_COMPARE_JOBS: list[dict[str, object]] = [
    {"id": 1, "title": "Software Engineering Intern", "job_description": ROLE_PRESETS["swe"]["job_description"]},
    {"id": 2, "title": "ML / NLP Intern", "job_description": ROLE_PRESETS["ml"]["job_description"]},
    {"id": 3, "title": "Data Analyst Intern", "job_description": ROLE_PRESETS["data"]["job_description"]},
]

CUSTOM_CSS = """
<style>
.mw-hero {
    background: linear-gradient(135deg, rgba(20, 34, 53, 0.92), rgba(13, 23, 36, 0.98));
    border: 1px solid #263950;
    border-radius: 16px;
    padding: 1.2rem 1.35rem;
    margin-bottom: 0.95rem;
}
.mw-brand {
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    color: #edf3fa;
    margin: 0;
    line-height: 1.15;
}
.mw-brand span {
    color: #73d9c3;
}
.mw-sub {
    color: #a9bdd1;
    font-size: 0.96rem;
    margin-top: 0.4rem;
    line-height: 1.45;
}
.mw-pill {
    display: inline-block;
    padding: 0.22rem 0.65rem;
    border-radius: 999px;
    font-size: 0.76rem;
    font-weight: 600;
    border: 1px solid #2b485b;
    background: #142235;
    color: #b1f2df;
    margin-bottom: 0.45rem;
}
.mw-card {
    background: #142235;
    border: 1px solid #263950;
    border-radius: 12px;
    padding: 0.95rem 1.05rem;
    margin-bottom: 0.75rem;
    transition: border-color 0.15s ease;
}
.mw-card:hover {
    border-color: #3b6f77;
}
.mw-card-title {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.35rem;
}
.mw-badge {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    padding: 0.15rem 0.55rem;
    border-radius: 999px;
    letter-spacing: 0.04em;
}
.mw-strong { background: rgba(115, 217, 195, 0.16); color: #73d9c3; border: 1px solid rgba(115, 217, 195, 0.4); }
.mw-partial { background: rgba(242, 199, 122, 0.16); color: #f2c77a; border: 1px solid rgba(242, 199, 122, 0.4); }
.mw-missing { background: rgba(239, 150, 150, 0.16); color: #ef9696; border: 1px solid rgba(239, 150, 150, 0.4); }
.mw-meta {
    color: #8ea0b5;
    font-size: 0.8rem;
    margin-bottom: 0.35rem;
}
.mw-quote {
    border-left: 3px solid #73d9c3;
    padding: 0.3rem 0.65rem;
    margin: 0.4rem 0 0 0;
    background: rgba(13, 23, 36, 0.6);
    color: #d6e4f0;
    font-size: 0.84rem;
    border-radius: 0 6px 6px 0;
}
.mw-chip {
    display: inline-block;
    padding: 0.25rem 0.65rem;
    margin: 0.2rem 0.25rem 0.2rem 0;
    border-radius: 999px;
    background: #182a40;
    border: 1px solid #2b4460;
    color: #d9e7f5;
    font-size: 0.82rem;
}
.mw-rank {
    font-size: 1.25rem;
    font-weight: 800;
    color: #73d9c3;
}
.mw-footer {
    margin-top: 2rem;
    padding-top: 0.85rem;
    border-top: 1px solid rgba(142, 160, 181, 0.18);
    color: #8ea0b5;
    font-size: 0.82rem;
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 0.5rem;
}
/* Prevent Streamlit from truncating button, link, download, and metric labels with '...' */
[data-testid="stButton"] button,
[data-testid="stDownloadButton"] button,
[data-testid="stLinkButton"] a {
    white-space: normal !important;
    word-break: break-word !important;
    overflow: visible !important;
    text-overflow: unset !important;
    height: auto !important;
    min-height: 2.55rem !important;
    padding: 0.45rem 0.75rem !important;
    line-height: 1.25 !important;
}
[data-testid="stButton"] button p,
[data-testid="stDownloadButton"] button p,
[data-testid="stLinkButton"] a p,
[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] p,
[data-testid="stMetricValue"],
[data-testid="stMetricDelta"] {
    white-space: normal !important;
    overflow: visible !important;
    text-overflow: unset !important;
    line-height: 1.25 !important;
}
</style>
"""


def _init_state() -> None:
    defaults: dict[str, object] = {
        "mode": "Single Role Analysis",
        "sample_resume_choice": "General Resume — Shaswat Raj (PDF)",
        "resume_text": SAMPLE_RESUME,
        "resume_filename": "Alex Example (Default Text)",
        "resume_load_error": "",
        "last_uploaded_key": "",
        "job_description": ROLE_PRESETS["swe"]["job_description"],
        "semantic_weight": 0.25,
        "compare_jobs": [dict(item) for item in DEFAULT_COMPARE_JOBS],
        "next_job_id": 4,
        "analysis_result": None,
        "compare_result": None,
        "benchmark_results": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _set_semantic_weight(weight: float) -> None:
    st.session_state["semantic_weight"] = weight


def _selected_sample_path(choice: str) -> Path | None:
    meta = SAMPLE_RESUMES.get(choice)
    if not meta or meta.get("kind") != "pdf":
        return None
    primary = Path(meta["file"])
    if primary.exists():
        return primary
    fallback = meta.get("fallback_file")
    if fallback and Path(fallback).exists():
        return Path(fallback)
    return None


def _load_selected_sample(sync_preset: bool = False) -> None:
    choice = str(st.session_state["sample_resume_choice"])
    meta = SAMPLE_RESUMES[choice]
    st.session_state["resume_load_error"] = ""
    if meta["kind"] == "text":
        st.session_state["resume_text"] = SAMPLE_RESUME
        st.session_state["resume_filename"] = "Alex Example (Synthetic Sample)"
    else:
        pdf_path = _selected_sample_path(choice)
        if pdf_path is None:
            st.session_state["resume_load_error"] = f"Sample PDF not found for {choice}."
            return
        try:
            extracted = extract_resume_text(pdf_path.name, pdf_path.read_bytes())
        except ValueError as exc:
            st.session_state["resume_load_error"] = str(exc)
            return
        st.session_state["resume_text"] = extracted
        st.session_state["resume_filename"] = f"{pdf_path.name} ({meta['url']})"

    if sync_preset and meta.get("preset") in ROLE_PRESETS:
        st.session_state["job_description"] = ROLE_PRESETS[meta["preset"]]["job_description"]


def _clear_resume() -> None:
    st.session_state["resume_text"] = ""
    st.session_state["resume_filename"] = ""
    st.session_state["resume_load_error"] = ""
    st.session_state["analysis_result"] = None
    st.session_state["compare_result"] = None


def _apply_preset(preset_key: str) -> None:
    st.session_state["job_description"] = ROLE_PRESETS[preset_key]["job_description"]


def _clear_jd() -> None:
    st.session_state["job_description"] = ""
    st.session_state["analysis_result"] = None


def _add_compare_job() -> None:
    jobs = st.session_state["compare_jobs"]
    if len(jobs) < 5:
        job_id = int(st.session_state["next_job_id"])
        st.session_state["next_job_id"] = job_id + 1
        jobs.append({"id": job_id, "title": f"Role {len(jobs) + 1}", "job_description": ""})


def _remove_compare_job(job_id: int) -> None:
    jobs = st.session_state["compare_jobs"]
    if len(jobs) > 1:
        st.session_state["compare_jobs"] = [j for j in jobs if j["id"] != job_id]
        st.session_state.pop(f"cmp_title_{job_id}", None)
        st.session_state.pop(f"cmp_jd_{job_id}", None)


def _format_markdown_report(analysis: AnalysisResult) -> str:
    lines: list[str] = [
        "# Matchwise — Resume & Skill Gap Report",
        "",
        f"- **Overall Score:** {analysis.overall_score}% ({analysis.score_band})",
        f"- **Weighted Coverage:** {analysis.coverage_score}%",
        f"- **Semantic Alignment:** {analysis.semantic_score}% ({analysis.semantic_mode}, weight={analysis.semantic_weight})",
        f"- **Breakdown:** {analysis.strong_matches} strong, {analysis.partial_matches} partial, "
        f"{analysis.missing_skills} missing (out of {analysis.requirements_found} requirements)",
        "",
        "## Strong Matches",
        *(
            [
                f"- **{s.skill}** ({s.importance}): {s.explanation}"
                + (f' — Evidence: "{s.evidence}"' if s.evidence else "")
                for s in analysis.matched_skills
            ]
            or ["- None detected"]
        ),
        "",
        "## Partial Matches",
        *(
            [
                f"- **{s.skill}** ({s.importance}, sim={s.similarity}): {s.explanation}"
                for s in analysis.partial_skills
            ]
            or ["- None"]
        ),
        "",
        "## Missing Skills",
        *(
            [
                f"- **{s.skill}** ({s.importance}): {s.explanation}"
                for s in analysis.missing_skill_matches
            ]
            or ["- None"]
        ),
        "",
        "## Prioritized Learning Roadmap",
        *(
            [
                f"{idx}. **{step.skill}** [{step.priority} priority]\n"
                f"   - Task: {step.task}\n"
                f"   - Project: {step.project_idea}"
                for idx, step in enumerate(analysis.learning_roadmap, start=1)
            ]
            or ["- No skill gaps detected."]
        ),
        "",
        f"> {analysis.methodology_note}",
    ]
    return "\n".join(lines)


def _build_score_gauge(score: float) -> go.Figure:
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={"suffix": "%", "font": {"size": 36, "color": "#edf3fa"}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#8ea0b5", "tickwidth": 1},
                "bar": {"color": "#73d9c3", "thickness": 0.35},
                "bgcolor": "#182a40",
                "borderwidth": 1,
                "bordercolor": "#263950",
                "steps": [
                    {"range": [0, 40], "color": "rgba(239, 150, 150, 0.14)"},
                    {"range": [40, 60], "color": "rgba(242, 199, 122, 0.14)"},
                    {"range": [60, 80], "color": "rgba(115, 217, 195, 0.14)"},
                    {"range": [80, 100], "color": "rgba(115, 217, 195, 0.25)"},
                ],
            },
        )
    )
    fig.update_layout(
        height=220,
        margin=dict(l=20, r=20, t=20, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": "#edf3fa"},
    )
    return fig


def _build_category_chart(analysis: AnalysisResult) -> go.Figure:
    ordered = sorted(analysis.category_breakdown, key=lambda c: c.coverage_score)
    categories = [c.category for c in ordered]
    scores = [c.coverage_score for c in ordered]
    hover = [
        f"{c.category}: {c.coverage_score}% ({c.strong} strong, {c.partial} partial, {c.missing} missing)"
        for c in ordered
    ]
    fig = go.Figure(
        go.Bar(
            x=scores,
            y=categories,
            orientation="h",
            marker={"color": "#73d9c3", "line": {"color": "#b1f2df", "width": 1}},
            text=[f"{s:.0f}%" for s in scores],
            textposition="outside",
            hovertext=hover,
            hoverinfo="text",
        )
    )
    fig.update_layout(
        height=max(220, 42 * len(ordered) + 60),
        margin=dict(l=16, r=56, t=12, b=24),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis={"range": [0, 114], "title": "Coverage (%)", "gridcolor": "rgba(142,160,181,0.15)", "automargin": True},
        yaxis={"title": "", "automargin": True},
        font={"color": "#edf3fa"},
    )
    return fig


def _build_compare_chart(compare_result: CompareResult) -> go.Figure:
    rankings = list(reversed(compare_result.rankings))
    titles = [item.title for item in rankings]
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            name="Overall Score",
            y=titles,
            x=[item.overall_score for item in rankings],
            orientation="h",
            marker_color="#73d9c3",
        )
    )
    fig.add_trace(
        go.Bar(
            name="Weighted Coverage",
            y=titles,
            x=[item.coverage_score for item in rankings],
            orientation="h",
            marker_color="#4fa3d1",
        )
    )
    fig.add_trace(
        go.Bar(
            name="Semantic Signal",
            y=titles,
            x=[item.semantic_score for item in rankings],
            orientation="h",
            marker_color="#f2c77a",
        )
    )
    fig.update_layout(
        barmode="group",
        height=max(260, 80 * len(rankings) + 70),
        margin=dict(l=16, r=24, t=24, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis={"range": [0, 106], "title": "Score (%)", "gridcolor": "rgba(142,160,181,0.15)", "automargin": True},
        yaxis={"automargin": True},
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "left", "x": 0},
        font={"color": "#edf3fa"},
    )
    return fig


def _render_skill_cards(title: str, items: list[SkillMatch], tone_class: str, empty_msg: str) -> None:
    st.markdown(f"#### {html.escape(title)} ({len(items)})")
    if not items:
        st.info(empty_msg)
        return
    for item in items:
        evidence_html = (
            f'<div class="mw-quote">“{html.escape(item.evidence)}”</div>' if item.evidence else ""
        )
        rationale_html = (
            f'<div class="mw-meta">{html.escape(item.requirement_rationale)}</div>'
            if item.requirement_rationale
            else ""
        )
        card_html = (
            f'<div class="mw-card">'
            f'<div class="mw-card-title">'
            f'<strong>{html.escape(item.skill)}</strong>'
            f'<span class="mw-badge {tone_class}">{html.escape(item.status)}</span>'
            f'</div>'
            f'<div class="mw-meta">{html.escape(item.category)} · {html.escape(item.importance)} '
            f'(w={item.weight:g}) · sim {round(item.similarity * 100)}%</div>'
            f'<div style="font-size:0.9rem;color:#dce7f3;">{html.escape(item.explanation)}</div>'
            f'{rationale_html}'
            f'{evidence_html}'
            f'</div>'
        )
        st.markdown(card_html, unsafe_allow_html=True)


def _render_resume_input(sync_preset: bool = False) -> None:
    settings = get_settings()
    max_mb = max(1, settings.max_upload_bytes // (1024 * 1024))
    st.subheader("01 / Resume")

    st.selectbox(
        "Quick-load sample resume (7 real PDFs from playlikeboy.github.io + Alex Example)",
        list(SAMPLE_RESUMES.keys()),
        key="sample_resume_choice",
    )
    choice = str(st.session_state["sample_resume_choice"])
    pdf_path = _selected_sample_path(choice)

    s_load, s_dl, s_clr = st.columns(3)
    s_load.button(
        "Load Sample",
        on_click=_load_selected_sample,
        args=(sync_preset,),
        key="btn_load_sample",
        use_container_width=True,
        help="Loads and extracts text from the selected sample resume",
    )
    if pdf_path is not None:
        s_dl.download_button(
            "Download PDF",
            data=pdf_path.read_bytes(),
            file_name=pdf_path.name,
            mime="application/pdf",
            key="btn_download_sample_pdf",
            use_container_width=True,
        )
    else:
        s_dl.link_button("Portfolio", PORTFOLIO_URL, use_container_width=True)
    s_clr.button("Clear Text", on_click=_clear_resume, key="btn_clear_resume", use_container_width=True)

    uploaded = st.file_uploader(
        f"Or upload your own resume (PDF, DOCX, or TXT · up to {max_mb} MB)",
        type=["pdf", "docx", "txt"],
        key="resume_uploader",
    )
    if uploaded is not None:
        file_token = f"{uploaded.name}:{uploaded.size}"
        if st.session_state["last_uploaded_key"] != file_token:
            raw_bytes = uploaded.getvalue()
            if len(raw_bytes) > settings.max_upload_bytes:
                st.error(f"File too large. Maximum upload size is {max_mb} MB.")
            else:
                try:
                    extracted = extract_resume_text(uploaded.name, raw_bytes)
                    if not extracted.strip():
                        st.error("No readable text was found in this file.")
                    else:
                        st.session_state["resume_text"] = extracted
                        st.session_state["resume_filename"] = uploaded.name
                        st.session_state["resume_load_error"] = ""
                        st.session_state["last_uploaded_key"] = file_token
                except ValueError as exc:
                    st.error(str(exc))

    if st.session_state["resume_load_error"]:
        st.error(st.session_state["resume_load_error"])

    if st.session_state["resume_filename"]:
        st.caption(f"Active resume: `{st.session_state['resume_filename']}`")

    st.text_area(
        "Resume text (editable)",
        height=230,
        key="resume_text",
        placeholder="Paste resume text here…",
    )
    words = len(st.session_state["resume_text"].split())
    sample_url = SAMPLE_RESUMES[choice]["url"]
    st.caption(f"{words} words · Sample source: [{sample_url}]({sample_url})")


def _render_single_analysis_results(analysis: AnalysisResult) -> None:
    st.divider()
    header_col, md_col, json_col = st.columns([2.4, 1.3, 1.3])
    with header_col:
        st.subheader("03 / Match Report")
        st.caption(f"Score band: **{analysis.score_band}** · Semantic mode: `{analysis.semantic_mode}`")
    with md_col:
        st.download_button(
            "Export Markdown",
            data=_format_markdown_report(analysis),
            file_name="match-report.md",
            mime="text/markdown",
            use_container_width=True,
        )
    with json_col:
        st.download_button(
            "Export JSON",
            data=json.dumps(analysis.model_dump(), indent=2),
            file_name="match-report.json",
            mime="application/json",
            use_container_width=True,
        )

    gauge_col, stats_col = st.columns([1.15, 1.85])
    with gauge_col:
        st.plotly_chart(_build_score_gauge(analysis.overall_score), use_container_width=True)
    with stats_col:
        m1, m2, m3 = st.columns(3)
        m1.metric("Overall Match", f"{analysis.overall_score:.1f}%", analysis.score_band)
        m2.metric("Coverage", f"{analysis.coverage_score:.1f}%")
        m3.metric("Semantic", f"{analysis.semantic_score:.1f}%")
        st.caption("Use this score as a decision-support signal, not a hiring verdict.")

    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Requirements", analysis.requirements_found)
    s2.metric("Strong Matches", analysis.strong_matches)
    s3.metric("Partial Matches", analysis.partial_matches)
    s4.metric("Missing Skills", analysis.missing_skills)

    if analysis.category_breakdown:
        st.markdown("### Domain Category Coverage")
        st.plotly_chart(_build_category_chart(analysis), use_container_width=True)

    st.markdown("### Evidence-Aware Skill Breakdown")
    c1, c2, c3 = st.columns(3)
    with c1:
        _render_skill_cards(
            "Strong matches",
            analysis.matched_skills,
            "mw-strong",
            "No direct skill evidence detected yet.",
        )
    with c2:
        _render_skill_cards(
            "Partial matches",
            analysis.partial_skills,
            "mw-partial",
            "No partial matches found.",
        )
    with c3:
        _render_skill_cards(
            "Missing skills",
            analysis.missing_skill_matches,
            "mw-missing",
            "No missing skills detected.",
        )

    if analysis.extra_resume_skills:
        st.markdown("### Additional Detected Resume Skills")
        st.caption("Skills detected in your resume that were not listed in this job description:")
        chips = "".join(f'<span class="mw-chip">{html.escape(skill)}</span>' for skill in analysis.extra_resume_skills)
        st.markdown(f"<div>{chips}</div>", unsafe_allow_html=True)

    st.markdown("### 04 / Prioritized Learning Roadmap")
    if analysis.learning_roadmap:
        for idx, step in enumerate(analysis.learning_roadmap, start=1):
            badge_cls = "mw-missing" if step.priority.lower() == "high" else "mw-partial"
            roadmap_html = (
                f'<div class="mw-card">'
                f'<div class="mw-card-title">'
                f'<strong>{idx:02d}. {html.escape(step.skill)}</strong>'
                f'<span class="mw-badge {badge_cls}">{html.escape(step.priority)} priority</span>'
                f'</div>'
                f'<div class="mw-meta">{html.escape(step.reason)}</div>'
                f'<div style="font-size:0.9rem;"><strong>Learning task:</strong> {html.escape(step.task)}</div>'
                f'<div style="font-size:0.9rem;margin-top:0.25rem;"><strong>Project idea:</strong> '
                f'{html.escape(step.project_idea)}</div>'
                f'</div>'
            )
            st.markdown(roadmap_html, unsafe_allow_html=True)
    else:
        st.success("No skill gaps were found in this comparison.")

    with st.expander("How this score is calculated"):
        st.write(analysis.methodology_note)
        st.write(
            "Exact normalized skills receive a strong match (1.0). Related evidence may receive a partial match (0.5); "
            "absent evidence receives 0.0. Required skills carry weight 2.0 and preferred skills carry weight 1.0."
        )


def _render_compare_results(compare_result: CompareResult) -> None:
    st.divider()
    st.subheader("03 / Multi-Role Ranking")
    st.caption(
        f"Evaluated across {len(compare_result.rankings)} roles · "
        f"Mode: `{compare_result.semantic_mode}` · "
        f"{len(compare_result.resume_skills_detected)} resume skills detected"
    )
    st.plotly_chart(_build_compare_chart(compare_result), use_container_width=True)

    for idx, item in enumerate(compare_result.rankings, start=1):
        strengths_html = "".join(
            f'<span class="mw-badge mw-strong" style="margin-right:0.35rem;">{html.escape(s)}</span>'
            for s in item.top_strengths
        )
        gaps_html = "".join(
            f'<span class="mw-badge mw-missing" style="margin-right:0.35rem;">Gap: {html.escape(g)}</span>'
            for g in item.top_gaps
        )
        card_html = (
            f'<div class="mw-card">'
            f'<div class="mw-card-title">'
            f'<div><span class="mw-rank">#{idx}</span> &nbsp; <strong style="font-size:1.1rem;">'
            f'{html.escape(item.title)}</strong></div>'
            f'<strong style="font-size:1.15rem;color:#73d9c3;">{item.overall_score:.1f}%</strong>'
            f'</div>'
            f'<div class="mw-meta">{html.escape(item.score_band)} · Cov {item.coverage_score:.1f}% · '
            f'Sem {item.semantic_score:.1f}% · {item.strong_matches} strong · '
            f'{item.partial_matches} partial · {item.missing_skills} missing</div>'
            f'<div style="margin-top:0.45rem;">{strengths_html}{gaps_html}</div>'
            f'</div>'
        )
        st.markdown(card_html, unsafe_allow_html=True)


def _render_taxonomy_and_benchmark() -> None:
    st.subheader("Curated Skill Taxonomy")
    st.caption(f"{len(SKILLS)} canonical skills across domain categories with boundary-aware alias normalization.")

    categories = sorted({meta["category"] for meta in SKILLS.values()})
    col_filter, col_search = st.columns([1, 2])
    selected_cat = col_filter.selectbox("Filter category", ["All categories", *categories])
    search_query = col_search.text_input("Search skill or alias", placeholder="e.g. k8s, FastAPI, SQL").strip().lower()

    grouped: dict[str, list[tuple[str, list[str]]]] = {}
    for canonical, meta in SKILLS.items():
        cat = meta["category"]
        if selected_cat != "All categories" and cat != selected_cat:
            continue
        aliases = list(meta.get("aliases", []))
        if search_query:
            haystack = " ".join([canonical, *aliases]).lower()
            if search_query not in haystack:
                continue
        grouped.setdefault(cat, []).append((canonical, aliases))

    if not grouped:
        st.info("No matching skills in the taxonomy.")
    else:
        for cat in sorted(grouped):
            expanded = selected_cat != "All categories" or bool(search_query)
            with st.expander(f"{cat} ({len(grouped[cat])} skills)", expanded=expanded):
                for canonical, aliases in grouped[cat]:
                    alias_text = ", ".join(aliases) if aliases else "none"
                    st.markdown(f"- **{canonical}** — aliases: `{alias_text}`")

    st.divider()
    st.subheader("Synthetic Starter Benchmark (B0 vs B1 vs H1)")
    st.caption(
        "Compares exact canonical keyword matching (B0), weighted taxonomy + aliases (B1), "
        "and the hybrid matcher (H1) on `examples/evaluation_dataset.jsonl`."
    )
    dataset_path = REPO_ROOT / "examples" / "evaluation_dataset.jsonl"
    if st.button("Run synthetic benchmark", key="run_benchmark"):
        if dataset_path.exists():
            st.session_state["benchmark_results"] = evaluate(dataset_path)
        else:
            st.error("Benchmark dataset file not found.")

    if st.session_state["benchmark_results"]:
        results = st.session_state["benchmark_results"]
        cols = st.columns(3)
        for col, sys_name in zip(cols, ("B0", "B1", "H1")):
            metrics = results[sys_name]
            with col:
                st.markdown(f"#### {sys_name} (`{metrics['mode']}`)")
                st.metric("Skill F1", f"{metrics['skill_f1']:.3f}")
                st.metric("Match Macro-F1", f"{metrics['match_macro_f1']:.3f}")
                st.caption(
                    f"Precision: {metrics['skill_precision']:.3f} · "
                    f"Recall: {metrics['skill_recall']:.3f} · "
                    f"Median latency: {metrics['median_latency_ms']:.2f} ms"
                )


def main() -> None:
    st.set_page_config(
        page_title="matchwise. — Resume–Job Match & Skill Gap Analyzer",
        page_icon="✨",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    _init_state()
    settings = get_settings()
    semantic_mode = "sentence-transformers" if settings.use_sentence_transformers else "rule-based-fallback"

    with st.sidebar:
        st.markdown('<div class="mw-brand">matchwise<span>.</span></div>', unsafe_allow_html=True)
        st.caption("5th Sem B.Tech CSE Project · BIT Mesra")
        st.markdown(f'<span class="mw-pill">Mode: {html.escape(semantic_mode)}</span>', unsafe_allow_html=True)
        st.divider()

        st.markdown("### Scoring Configuration")
        st.slider(
            "Semantic signal weight",
            min_value=0.0,
            max_value=0.5,
            step=0.05,
            key="semantic_weight",
            help="Overall score = (1 - w) * Weighted Coverage + w * Semantic Alignment.",
        )
        p1, p2, p3 = st.columns(3)
        p1.button("0%", on_click=_set_semantic_weight, args=(0.0,), use_container_width=True)
        p2.button("25%", on_click=_set_semantic_weight, args=(0.25,), use_container_width=True)
        p3.button("40%", on_click=_set_semantic_weight, args=(0.40,), use_container_width=True)

        w = float(st.session_state["semantic_weight"])
        st.caption(
            f"Coverage weight: **{round((1 - w) * 100)}%** · Semantic weight: **{round(w * 100)}%**\n\n"
            f"Partial threshold: `{settings.semantic_partial_threshold:.2f}`"
        )
        st.divider()
        st.markdown("### Project Docs & Links")
        st.markdown(f"- [Canva PPT (14 Slides)]({CANVA_PPT_URL})")
        st.markdown(f"- [Project Report (PDF)]({REPORT_GITHUB_URL})")
        st.markdown(f"- [PowerPoint Web Viewer]({PPT_VIEWER_URL})")
        st.markdown(f"- [Easy → Advanced Guide]({GUIDE_URL})")
        st.markdown(f"- [PPT Presenter Script & Q&A]({SCRIPT_URL})")
        st.markdown(f"- [Portfolio (playlikeboy.github.io)]({PORTFOLIO_URL})")
        st.markdown(f"- [7 Resume PDFs Source]({RESUME_PAGE_URL}/devops)")
        st.markdown(f"- [GitHub Repository]({REPO_URL})")
        if PPT_PATH.exists():
            st.download_button(
                "Download PPT (.pptx)",
                data=PPT_PATH.read_bytes(),
                file_name="Matchwise_5th_Sem_Presentation.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                key="sidebar_download_ppt",
                use_container_width=True,
            )
        if REPORT_PDF_PATH.exists():
            st.download_button(
                "Download Report (.pdf)",
                data=REPORT_PDF_PATH.read_bytes(),
                file_name="Minor_Project_Report_2.pdf",
                mime="application/pdf",
                key="sidebar_download_report_pdf",
                use_container_width=True,
            )
        st.divider()
        st.caption("In-memory only: uploaded resumes and pasted text are analyzed on demand and never persisted.")

    st.markdown(
        '<div class="mw-hero">'
        '<div class="mw-pill">CAREER READINESS, WITH EVIDENCE · BIT MESRA MINOR PROJECT</div>'
        '<div class="mw-brand">Know where you stand. <span>See what to build next.</span></div>'
        '<div class="mw-sub">'
        'Compare your resume (or test 7 real role-specific resume PDFs) against job descriptions with '
        'normalized skill matching, quoted evidence, weighted coverage, and a prioritized learning roadmap.'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    q1, q2 = st.columns(2)
    q1.link_button("Canva PPT", CANVA_PPT_URL, use_container_width=True)
    if REPORT_PDF_PATH.exists():
        q2.download_button(
            "Project Report",
            data=REPORT_PDF_PATH.read_bytes(),
            file_name="Minor_Project_Report_2.pdf",
            mime="application/pdf",
            key="hero_download_report_pdf",
            use_container_width=True,
        )
    else:
        q2.link_button("Project Report", REPORT_GITHUB_URL, use_container_width=True)

    mode = st.radio(
        "Workspace",
        ["Single Role Analysis", "Compare Multiple Roles", "Skill Taxonomy & Benchmark"],
        horizontal=True,
        key="mode",
        label_visibility="collapsed",
    )

    if mode == "Single Role Analysis":
        col_resume, col_jd = st.columns(2, gap="large")
        with col_resume:
            _render_resume_input(sync_preset=True)

        with col_jd:
            st.subheader("02 / Target Job Description")
            preset_items = list(ROLE_PRESETS.items())
            for row_start in range(0, len(preset_items), 3):
                row_slice = preset_items[row_start:row_start + 3]
                row_cols = st.columns(len(row_slice))
                for col, (preset_key, preset) in zip(row_cols, row_slice):
                    col.button(
                        preset["label"],
                        on_click=_apply_preset,
                        args=(preset_key,),
                        key=f"preset_{preset_key}",
                        use_container_width=True,
                    )
            st.caption(
                "Required and preferred skills are weighted 2:1 when section headings or inline markers appear."
            )
            st.text_area(
                "Job description",
                height=310,
                key="job_description",
                placeholder="Paste the target job description here…",
            )
            jd_words = len(st.session_state["job_description"].split())
            jd_count_col, jd_clear_col = st.columns([3, 1])
            jd_count_col.caption(f"{jd_words} words")
            jd_clear_col.button("Clear JD", on_click=_clear_jd, key="clear_jd", use_container_width=True)

        ready_single = bool(
            st.session_state["resume_text"].strip() and st.session_state["job_description"].strip()
        )
        if st.button(
            "Analyse match",
            type="primary",
            disabled=not ready_single,
            key="btn_analyze",
            use_container_width=True,
        ):
            try:
                st.session_state["analysis_result"] = analyze_resume_job(
                    resume_text=st.session_state["resume_text"],
                    job_description=st.session_state["job_description"],
                    semantic_weight=float(st.session_state["semantic_weight"]),
                )
            except ValueError as exc:
                st.error(str(exc))

        if st.session_state["analysis_result"] is not None:
            _render_single_analysis_results(st.session_state["analysis_result"])

    elif mode == "Compare Multiple Roles":
        col_resume_cmp, col_roles_cmp = st.columns([1, 1.35], gap="large")
        with col_resume_cmp:
            _render_resume_input(sync_preset=False)

        with col_roles_cmp:
            head_col, add_col = st.columns([3, 1])
            head_col.subheader("02 / Target Roles (up to 5)")
            if len(st.session_state["compare_jobs"]) < 5:
                add_col.button("+ Add role", on_click=_add_compare_job, key="add_role", use_container_width=True)

            jobs_list = st.session_state["compare_jobs"]
            for idx, job in enumerate(jobs_list):
                job_id = int(job["id"])
                with st.container():
                    t_col, rm_col = st.columns([5, 1])
                    job["title"] = t_col.text_input(
                        f"Role {idx + 1} title",
                        value=str(job["title"]),
                        key=f"cmp_title_{job_id}",
                        placeholder="Role title (e.g., Backend Intern)",
                    )
                    if len(jobs_list) > 1:
                        rm_col.markdown("<div style='height:1.75rem;'></div>", unsafe_allow_html=True)
                        rm_col.button(
                            "Remove",
                            on_click=_remove_compare_job,
                            args=(job_id,),
                            key=f"rm_role_{job_id}",
                            use_container_width=True,
                        )
                    job["job_description"] = st.text_area(
                        f"Role {idx + 1} description",
                        value=str(job["job_description"]),
                        height=115,
                        key=f"cmp_jd_{job_id}",
                        placeholder="Paste job description…",
                    )

        ready_compare = bool(
            st.session_state["resume_text"].strip()
            and st.session_state["compare_jobs"]
            and all(
                str(j["title"]).strip() and str(j["job_description"]).strip()
                for j in st.session_state["compare_jobs"]
            )
        )
        if st.button(
            "Compare roles",
            type="primary",
            disabled=not ready_compare,
            key="btn_compare",
            use_container_width=True,
        ):
            try:
                items = [
                    JobItem(title=str(j["title"]), job_description=str(j["job_description"]))
                    for j in st.session_state["compare_jobs"]
                ]
                st.session_state["compare_result"] = compare_resume_to_jobs(
                    resume_text=st.session_state["resume_text"],
                    jobs=items,
                    semantic_weight=float(st.session_state["semantic_weight"]),
                )
            except ValueError as exc:
                st.error(str(exc))

        if st.session_state["compare_result"] is not None:
            _render_compare_results(st.session_state["compare_result"])

    else:
        _render_taxonomy_and_benchmark()

    st.markdown(
        '<div class="mw-footer">'
        '<span><strong>matchwise.</strong> v0.2.0 — Shaswat Raj (BTECH/10574/24) &amp; Satyam Hansda (BTECH/10616/24)</span>'
        '<span>Guided by Dr. Sumit Srivastava · Dept. of CSE, BIT Mesra</span>'
        '</div>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
