import { useMemo, useState } from "react";
import {
  ArrowUpRight,
  BadgeCheck,
  BriefcaseBusiness,
  Check,
  ChevronRight,
  CircleAlert,
  Download,
  FileText,
  Layers,
  LoaderCircle,
  Plus,
  SlidersHorizontal,
  Sparkles,
  Trash2,
  UploadCloud,
} from "lucide-react";

import { analyzeLocal, compareLocal } from "./localEngine";
import { DEFAULT_COMPARE_JOBS, ROLE_PRESETS, SAMPLE_RESUME } from "./presets";
import type { Analysis, CompareResult, JobComparisonInput, SkillMatch } from "./types";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

function ScoreRing({ score }: { score: number }) {
  const circumference = 2 * Math.PI * 48;
  const clamped = Math.max(0, Math.min(100, score));
  const offset = circumference - (clamped / 100) * circumference;
  return (
    <div className="score-ring-wrap">
      <svg className="score-ring" viewBox="0 0 112 112" aria-label={`Match score ${score}%`}>
        <circle cx="56" cy="56" r="48" className="ring-track" />
        <circle
          cx="56"
          cy="56"
          r="48"
          className="ring-value"
          style={{ strokeDasharray: circumference, strokeDashoffset: offset }}
        />
      </svg>
      <div className="score-ring-label">
        <strong>{Math.round(score)}</strong>
        <span>/ 100</span>
      </div>
    </div>
  );
}

function SkillGroup({
  title,
  items,
  tone,
  empty,
}: {
  title: string;
  items: SkillMatch[];
  tone: string;
  empty: string;
}) {
  return (
    <section className="skill-group">
      <div className="group-heading">
        <h3>{title}</h3>
        <span className={`count ${tone}`}>{items.length}</span>
      </div>
      {items.length ? (
        <div className="skill-list">
          {items.map((item) => (
            <article className="skill-item" key={item.skill}>
              <div className="skill-item-top">
                <div>
                  <strong>{item.skill}</strong>
                  <small>
                    {item.category} · {item.importance} (w={item.weight}) · sim {Math.round(item.similarity * 100)}%
                  </small>
                </div>
                <span className={`status-tag ${tone}`}>{item.status}</span>
              </div>
              <p>{item.explanation}</p>
              {item.evidence && <blockquote>“{item.evidence}”</blockquote>}
            </article>
          ))}
        </div>
      ) : (
        <p className="empty-state">{empty}</p>
      )}
    </section>
  );
}

function formatMarkdownReport(analysis: Analysis): string {
  const lines: string[] = [
    "# Matchwise — Resume & Skill Gap Report",
    "",
    `- **Overall Score:** ${analysis.overall_score}% (${analysis.score_band})`,
    `- **Weighted Coverage:** ${analysis.coverage_score}%`,
    `- **Semantic Alignment:** ${analysis.semantic_score}% (${analysis.semantic_mode}, weight=${analysis.semantic_weight})`,
    `- **Breakdown:** ${analysis.strong_matches} strong, ${analysis.partial_matches} partial, ${analysis.missing_skills} missing (out of ${analysis.requirements_found} requirements)`,
    "",
    "## Strong Matches",
    ...(analysis.matched_skills.length
      ? analysis.matched_skills.map((s) => `- **${s.skill}** (${s.importance}): ${s.explanation}${s.evidence ? ` — Evidence: "${s.evidence}"` : ""}`)
      : ["- None detected"]),
    "",
    "## Partial Matches",
    ...(analysis.partial_skills.length
      ? analysis.partial_skills.map((s) => `- **${s.skill}** (${s.importance}, sim=${s.similarity}): ${s.explanation}`)
      : ["- None"]),
    "",
    "## Missing Skills",
    ...(analysis.missing_skill_matches.length
      ? analysis.missing_skill_matches.map((s) => `- **${s.skill}** (${s.importance}): ${s.explanation}`)
      : ["- None"]),
    "",
    "## Prioritized Learning Roadmap",
    ...(analysis.learning_roadmap.length
      ? analysis.learning_roadmap.map(
          (step, idx) => `${idx + 1}. **${step.skill}** [${step.priority} priority]\n   - Task: ${step.task}\n   - Project: ${step.project_idea}`,
        )
      : ["- No skill gaps detected."]),
    "",
    `> ${analysis.methodology_note}`,
  ];
  return lines.join("\n");
}

function downloadTextFile(filename: string, content: string, mimeType: string) {
  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
}

export default function App() {
  const [mode, setMode] = useState<"single" | "compare">("single");
  const [resumeText, setResumeText] = useState(SAMPLE_RESUME);
  const [jobDescription, setJobDescription] = useState(ROLE_PRESETS.swe.jobDescription);
  const [compareJobs, setCompareJobs] = useState<JobComparisonInput[]>(DEFAULT_COMPARE_JOBS);
  const [semanticWeight, setSemanticWeight] = useState(0.25);
  const [fileName, setFileName] = useState("");
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [compareResult, setCompareResult] = useState<CompareResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const readySingle = useMemo(
    () => resumeText.trim().length > 0 && jobDescription.trim().length > 0,
    [resumeText, jobDescription],
  );
  const readyCompare = useMemo(
    () =>
      resumeText.trim().length > 0 &&
      compareJobs.length > 0 &&
      compareJobs.every((j) => j.title.trim().length > 0 && j.job_description.trim().length > 0),
    [resumeText, compareJobs],
  );

  async function uploadResume(file?: File) {
    if (!file) return;
    setError("");
    setFileName(file.name);
    if (file.name.toLowerCase().endsWith(".txt")) {
      const text = await file.text();
      if (!text.trim()) {
        setError("No readable text was found in this file.");
        return;
      }
      setResumeText(text);
      return;
    }
    const body = new FormData();
    body.append("file", file);
    try {
      const response = await fetch(`${API_BASE}/api/resume/parse`, { method: "POST", body });
      const payload = await response.json();
      if (!response.ok) {
        setError(payload.detail || "Could not parse this file.");
        return;
      }
      setResumeText(payload.text);
    } catch {
      setError("PDF/DOCX parsing requires a running FastAPI backend. Upload a .txt resume or paste text directly.");
    }
  }

  async function runAnalysis() {
    setLoading(true);
    setError("");
    try {
      let response: Response | null = null;
      try {
        response = await fetch(`${API_BASE}/api/analyze`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            resume_text: resumeText,
            job_description: jobDescription,
            semantic_weight: semanticWeight,
          }),
        });
      } catch {
        // Backend unreachable (e.g., static GitHub Pages demo); run browser-side fallback engine.
        setAnalysis(analyzeLocal(resumeText, jobDescription, semanticWeight));
        return;
      }
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.detail || "Analysis failed.");
      setAnalysis(payload);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Analysis failed.");
    } finally {
      setLoading(false);
    }
  }

  async function runComparison() {
    setLoading(true);
    setError("");
    try {
      let response: Response | null = null;
      try {
        response = await fetch(`${API_BASE}/api/compare`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            resume_text: resumeText,
            jobs: compareJobs,
            semantic_weight: semanticWeight,
          }),
        });
      } catch {
        setCompareResult(compareLocal(resumeText, compareJobs, semanticWeight));
        return;
      }
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.detail || "Comparison failed.");
      setCompareResult(payload);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Comparison failed.");
    } finally {
      setLoading(false);
    }
  }

  function updateCompareJob(index: number, patch: Partial<JobComparisonInput>) {
    setCompareJobs((prev) => prev.map((item, idx) => (idx === index ? { ...item, ...patch } : item)));
  }

  return (
    <main className="app-shell">
      <header className="topbar">
        <a className="brand" href="#top">
          <span className="brand-mark">
            <Sparkles size={18} />
          </span>
          <span>
            matchwise<span className="brand-dot">.</span>
          </span>
        </a>
        <div className="topbar-right">
          <span className="top-pill">
            <span className="live-dot" /> Explainable career readiness
          </span>
          <a
            className="github-link"
            href="https://github.com/playlikeboy/resume-job-matching-skill-gap-analyzer"
            target="_blank"
            rel="noreferrer"
          >
            GitHub repo <ArrowUpRight size={14} />
          </a>
        </div>
      </header>

      <section className="hero" id="top">
        <div className="eyebrow">
          <span className="eyebrow-line" /> CAREER READINESS, WITH EVIDENCE
        </div>
        <h1>
          Know where you stand.
          <br />
          <em>See what to build next.</em>
        </h1>
        <p>
          Compare your resume against one or more job descriptions with normalized skill matching, evidence snippets,
          weighted coverage, and a prioritized learning roadmap.
        </p>

        <div className="mode-switch" role="tablist" aria-label="Analysis mode">
          <button
            type="button"
            role="tab"
            aria-selected={mode === "single"}
            className={`mode-tab ${mode === "single" ? "active" : ""}`}
            onClick={() => setMode("single")}
          >
            <BriefcaseBusiness size={15} /> Single role analysis
          </button>
          <button
            type="button"
            role="tab"
            aria-selected={mode === "compare"}
            className={`mode-tab ${mode === "compare" ? "active" : ""}`}
            onClick={() => setMode("compare")}
          >
            <Layers size={15} /> Compare multiple roles
          </button>
        </div>
      </section>

      <section className="workspace-grid">
        <div className="input-panel panel">
          <div className="panel-heading">
            <div>
              <span className="step-label">01 / YOUR PROFILE</span>
              <h2>Resume</h2>
            </div>
            <FileText size={19} />
          </div>
          <label className="upload-box">
            <input type="file" accept=".pdf,.docx,.txt" onChange={(event) => uploadResume(event.target.files?.[0])} />
            <UploadCloud size={19} />
            <span>
              <strong>{fileName || "Upload your resume"}</strong>
              <small>PDF, DOCX, or TXT · up to 8 MB</small>
            </span>
            <span className="browse-link">Browse</span>
          </label>
          <div className="or-divider">
            <span>OR PASTE YOUR RESUME</span>
          </div>
          <textarea
            value={resumeText}
            onChange={(event) => setResumeText(event.target.value)}
            placeholder="Paste resume text here…"
            aria-label="Resume text"
          />
          <div className="field-foot">
            <span>{resumeText.trim().split(/\s+/).filter(Boolean).length} words</span>
            <div className="foot-actions">
              <button
                type="button"
                className="text-button"
                onClick={() => {
                  setResumeText(SAMPLE_RESUME);
                  setFileName("");
                }}
              >
                Load sample
              </button>
              <button
                type="button"
                className="text-button"
                onClick={() => {
                  setResumeText("");
                  setFileName("");
                  setAnalysis(null);
                  setCompareResult(null);
                }}
              >
                Clear text
              </button>
            </div>
          </div>
        </div>

        {mode === "single" ? (
          <div className="input-panel panel">
            <div className="panel-heading">
              <div>
                <span className="step-label">02 / TARGET ROLE</span>
                <h2>Job description</h2>
              </div>
              <BriefcaseBusiness size={19} />
            </div>
            <div className="preset-row">
              {Object.entries(ROLE_PRESETS).map(([key, preset]) => (
                <button
                  key={key}
                  type="button"
                  className="preset-chip"
                  onClick={() => setJobDescription(preset.jobDescription)}
                >
                  {preset.label}
                </button>
              ))}
            </div>
            <div className="jd-tip">
              <Sparkles size={15} />
              <span>
                Paste the full role description. Required and preferred skills are weighted 2:1 when headings or inline
                markers appear.
              </span>
            </div>
            <textarea
              className="job-textarea"
              value={jobDescription}
              onChange={(event) => setJobDescription(event.target.value)}
              placeholder="Paste the job description here…"
              aria-label="Job description"
            />
            <div className="field-foot">
              <span>{jobDescription.trim().split(/\s+/).filter(Boolean).length} words</span>
              <button
                type="button"
                className="text-button"
                onClick={() => {
                  setJobDescription("");
                  setAnalysis(null);
                }}
              >
                Clear text
              </button>
            </div>
          </div>
        ) : (
          <div className="input-panel panel">
            <div className="panel-heading">
              <div>
                <span className="step-label">02 / TARGET ROLES (UP TO 5)</span>
                <h2>Roles to compare</h2>
              </div>
              {compareJobs.length < 5 && (
                <button
                  type="button"
                  className="preset-chip"
                  onClick={() => setCompareJobs((prev) => [...prev, { title: "New Role", job_description: "" }])}
                >
                  <Plus size={13} /> Add role
                </button>
              )}
            </div>
            <div className="compare-inputs">
              {compareJobs.map((job, index) => (
                <div className="compare-job-box" key={index}>
                  <div className="compare-job-head">
                    <input
                      type="text"
                      value={job.title}
                      onChange={(e) => updateCompareJob(index, { title: e.target.value })}
                      placeholder="Role title (e.g., Backend Intern)"
                      aria-label={`Role ${index + 1} title`}
                    />
                    {compareJobs.length > 1 && (
                      <button
                        type="button"
                        className="icon-button"
                        onClick={() => setCompareJobs((prev) => prev.filter((_, i) => i !== index))}
                        aria-label={`Remove role ${index + 1}`}
                      >
                        <Trash2 size={14} />
                      </button>
                    )}
                  </div>
                  <textarea
                    rows={3}
                    value={job.job_description}
                    onChange={(e) => updateCompareJob(index, { job_description: e.target.value })}
                    placeholder="Paste job description…"
                    aria-label={`Role ${index + 1} description`}
                  />
                </div>
              ))}
            </div>
          </div>
        )}
      </section>

      <section className="weight-bar panel">
        <div className="weight-label">
          <SlidersHorizontal size={15} />
          <span>
            Semantic signal weight: <strong>{Math.round(semanticWeight * 100)}%</strong>{" "}
            <small>(Coverage {Math.round((1 - semanticWeight) * 100)}%)</small>
          </span>
        </div>
        <div className="weight-controls">
          <input
            type="range"
            min={0}
            max={0.5}
            step={0.05}
            value={semanticWeight}
            onChange={(e) => setSemanticWeight(parseFloat(e.target.value))}
            aria-label="Semantic weight"
          />
          <div className="weight-presets">
            {[0, 0.25, 0.4].map((w) => (
              <button
                key={w}
                type="button"
                className={`preset-chip ${Math.abs(semanticWeight - w) < 0.01 ? "selected" : ""}`}
                onClick={() => setSemanticWeight(w)}
              >
                {w === 0 ? "0% (Baseline)" : `${Math.round(w * 100)}%`}
              </button>
            ))}
          </div>
        </div>
      </section>

      {error && (
        <div className="error-banner" role="alert">
          <CircleAlert size={17} />
          {error}
        </div>
      )}

      <div className="analyze-row">
        <div className="privacy-note">
          <BadgeCheck size={16} />
          <span>In-memory only: text is analyzed on demand and never persisted by the server.</span>
        </div>
        {mode === "single" ? (
          <button
            type="button"
            className="analyze-button"
            disabled={!readySingle || loading}
            onClick={runAnalysis}
          >
            {loading ? (
              <>
                <LoaderCircle className="spin" size={17} /> Analysing…
              </>
            ) : (
              <>
                Analyse match <ChevronRight size={17} />
              </>
            )}
          </button>
        ) : (
          <button
            type="button"
            className="analyze-button"
            disabled={!readyCompare || loading}
            onClick={runComparison}
          >
            {loading ? (
              <>
                <LoaderCircle className="spin" size={17} /> Comparing…
              </>
            ) : (
              <>
                Compare roles <ChevronRight size={17} />
              </>
            )}
          </button>
        )}
      </div>

      {mode === "single" && analysis && (
        <section className="results-section" aria-live="polite">
          <div className="results-header">
            <div>
              <span className="step-label">03 / YOUR MATCH REPORT</span>
              <h2>The signal behind your score.</h2>
              <p>Every match is tied to detected skills and evidence, so you can verify the result.</p>
            </div>
            <div className="results-actions">
              <button
                type="button"
                className="export-button"
                onClick={() => downloadTextFile("match-report.md", formatMarkdownReport(analysis), "text/markdown")}
              >
                <Download size={14} /> Export Markdown
              </button>
              <button
                type="button"
                className="export-button"
                onClick={() =>
                  downloadTextFile("match-report.json", JSON.stringify(analysis, null, 2), "application/json")
                }
              >
                <Download size={14} /> JSON
              </button>
              <span className="report-badge">
                <Check size={14} /> {analysis.score_band || "Analysis complete"}
              </span>
            </div>
          </div>

          <div className="overview-grid">
            <article className="score-card panel">
              <div>
                <span className="card-kicker">OVERALL ALIGNMENT</span>
                <h3>Role match score</h3>
                <p>Use this as a decision-support guide, not a hiring verdict.</p>
              </div>
              <ScoreRing score={analysis.overall_score} />
              <div className="score-breakdown">
                <div>
                  <span>Weighted coverage</span>
                  <strong>{analysis.coverage_score}%</strong>
                </div>
                <div className="mini-track">
                  <span style={{ width: `${analysis.coverage_score}%` }} />
                </div>
                <div>
                  <span>Semantic signal</span>
                  <strong>{analysis.semantic_score}%</strong>
                </div>
                <div className="mini-track semantic">
                  <span style={{ width: `${analysis.semantic_score}%` }} />
                </div>
                <small>
                  Mode: {analysis.semantic_mode.replaceAll("-", " ")} · Semantic weight:{" "}
                  {Math.round(analysis.semantic_weight * 100)}%
                </small>
              </div>
            </article>

            <article className="stats-card panel">
              <span className="card-kicker">SKILL BREAKDOWN</span>
              <div className="stat-row">
                <div className="stat-icon strong">
                  <Check size={17} />
                </div>
                <div>
                  <strong>{analysis.strong_matches}</strong>
                  <span>Strong matches</span>
                </div>
              </div>
              <div className="stat-row">
                <div className="stat-icon partial">
                  <Sparkles size={17} />
                </div>
                <div>
                  <strong>{analysis.partial_matches}</strong>
                  <span>Partial matches</span>
                </div>
              </div>
              <div className="stat-row">
                <div className="stat-icon missing">
                  <CircleAlert size={17} />
                </div>
                <div>
                  <strong>{analysis.missing_skills}</strong>
                  <span>Missing requirements</span>
                </div>
              </div>
              <div className="stats-foot">{analysis.requirements_found} requirements detected in the job description</div>
            </article>
          </div>

          {analysis.category_breakdown.length > 0 && (
            <section className="category-panel panel">
              <div className="panel-heading compact">
                <div>
                  <span className="step-label">CATEGORY COVERAGE</span>
                  <h3>Alignment by skill domain</h3>
                </div>
              </div>
              <div className="category-grid">
                {analysis.category_breakdown.map((cat) => (
                  <div className="category-card" key={cat.category}>
                    <div className="category-top">
                      <strong>{cat.category}</strong>
                      <span>{cat.coverage_score}%</span>
                    </div>
                    <div className="mini-track">
                      <span style={{ width: `${cat.coverage_score}%` }} />
                    </div>
                    <small>
                      {cat.strong} strong · {cat.partial} partial · {cat.missing} missing
                    </small>
                  </div>
                ))}
              </div>
            </section>
          )}

          <div className="match-columns">
            <SkillGroup
              title="Strong matches"
              items={analysis.matched_skills}
              tone="green"
              empty="No direct skill evidence detected yet."
            />
            <SkillGroup
              title="Partial matches"
              items={analysis.partial_skills}
              tone="amber"
              empty="No partial matches found."
            />
            <SkillGroup
              title="Missing skills"
              items={analysis.missing_skill_matches}
              tone="red"
              empty="No missing skills detected."
            />
          </div>

          {analysis.extra_resume_skills.length > 0 && (
            <section className="extra-skills panel">
              <span className="card-kicker">ADDITIONAL DETECTED RESUME SKILLS</span>
              <p>Skills detected in your resume that were not listed in this job description:</p>
              <div className="chip-list">
                {analysis.extra_resume_skills.map((skill) => (
                  <span className="skill-chip" key={skill}>
                    {skill}
                  </span>
                ))}
              </div>
            </section>
          )}

          <section className="roadmap panel">
            <div className="panel-heading">
              <div>
                <span className="step-label">04 / NEXT STEPS</span>
                <h2>Your skill-gap roadmap</h2>
              </div>
              <Sparkles size={19} />
            </div>
            <p className="roadmap-intro">
              Turn the gaps into proof of work. Start with required missing skills before polishing preferred ones.
            </p>
            {analysis.learning_roadmap.length ? (
              <div className="roadmap-list">
                {analysis.learning_roadmap.map((step, index) => (
                  <article className="roadmap-item" key={step.skill}>
                    <div className="roadmap-index">{String(index + 1).padStart(2, "0")}</div>
                    <div className="roadmap-content">
                      <div className="roadmap-title">
                        <strong>{step.skill}</strong>
                        <span className={`priority ${step.priority.toLowerCase()}`}>{step.priority} priority</span>
                      </div>
                      <p>{step.reason}</p>
                      <div className="roadmap-detail">
                        <span>LEARNING TASK</span>
                        {step.task}
                      </div>
                      <div className="roadmap-detail">
                        <span>PROJECT IDEA</span>
                        {step.project_idea}
                      </div>
                    </div>
                  </article>
                ))}
              </div>
            ) : (
              <p className="empty-state">No skill gaps were found in this comparison.</p>
            )}
          </section>

          <details className="methodology panel">
            <summary>
              How this score is calculated <ChevronRight size={16} />
            </summary>
            <p>{analysis.methodology_note}</p>
            <p>
              Exact normalized skills receive a strong match (1.0). Related evidence may receive a partial match (0.5);
              absent evidence receives 0. Required skills carry weight 2 and preferred skills carry weight 1.
            </p>
          </details>
        </section>
      )}

      {mode === "compare" && compareResult && (
        <section className="results-section" aria-live="polite">
          <div className="results-header">
            <div>
              <span className="step-label">03 / MULTI-ROLE RANKING</span>
              <h2>Best-fit role comparison.</h2>
              <p>
                Evaluated across {compareResult.rankings.length} roles · Mode:{" "}
                {compareResult.semantic_mode.replaceAll("-", " ")}
              </p>
            </div>
            <span className="report-badge">
              <Check size={14} /> {compareResult.resume_skills_detected.length} resume skills detected
            </span>
          </div>

          <div className="compare-rankings">
            {compareResult.rankings.map((item, idx) => (
              <article className="compare-rank-card panel" key={`${item.title}-${idx}`}>
                <div className="compare-rank-left">
                  <span className="rank-number">#{idx + 1}</span>
                  <div>
                    <h3>{item.title}</h3>
                    <small>
                      {item.score_band} · {item.strong_matches} strong · {item.partial_matches} partial ·{" "}
                      {item.missing_skills} missing
                    </small>
                    <div className="compare-tags">
                      {item.top_strengths.map((s) => (
                        <span key={s} className="status-tag green">
                          {s}
                        </span>
                      ))}
                      {item.top_gaps.map((g) => (
                        <span key={g} className="status-tag red">
                          Gap: {g}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
                <div className="compare-rank-score">
                  <strong>{item.overall_score}%</strong>
                  <span>Cov {item.coverage_score}% · Sem {item.semantic_score}%</span>
                </div>
              </article>
            ))}
          </div>
        </section>
      )}

      <footer className="footer">
        <span>
          matchwise<span className="brand-dot">.</span> <small>Academic project prototype · v0.2</small>
        </span>
        <span>Evidence over guesswork.</span>
      </footer>
    </main>
  );
}
