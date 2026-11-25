import { useMemo, useState } from "react";
import { ArrowUpRight, BadgeCheck, BriefcaseBusiness, Check, ChevronRight, CircleAlert, FileText, LoaderCircle, Sparkles, UploadCloud } from "lucide-react";

type SkillMatch = {
  skill: string; category: string; importance: string; weight: number; status: string;
  match_value: number; similarity: number; evidence?: string | null; explanation: string;
};
type Analysis = {
  overall_score: number; coverage_score: number; semantic_score: number; semantic_mode: string;
  semantic_weight: number; requirements_found: number; strong_matches: number; partial_matches: number;
  missing_skills: number; matched_skills: SkillMatch[]; partial_skills: SkillMatch[];
  missing_skill_matches: SkillMatch[];
  learning_roadmap: { skill: string; priority: string; reason: string; task: string; project_idea: string }[];
  methodology_note: string;
};

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
const sampleResume = `Alex Example\nComputer Science student\n\nProjects\n- Built REST APIs using Python and FastAPI.\n- Developed responsive interfaces with React, JavaScript and TypeScript.\n- Used PostgreSQL and SQL for structured data storage.\n- Worked with Git, Docker and Linux during team projects.\n- Explored NLP, Machine Learning and sentence embeddings in an academic prototype.`;
const sampleJob = `Software Engineering Intern\n\nRequired qualifications\n- Strong Python and JavaScript fundamentals.\n- Experience building REST APIs using FastAPI or Express.js.\n- SQL and PostgreSQL knowledge.\n- Git and Docker familiarity.\n\nPreferred qualifications\n- React and TypeScript experience.\n- Exposure to NLP or Machine Learning.`;

function ScoreRing({ score }: { score: number }) {
  const circumference = 2 * Math.PI * 48;
  const offset = circumference - (score / 100) * circumference;
  return <div className="score-ring-wrap"><svg className="score-ring" viewBox="0 0 112 112" aria-label={`Match score ${score}%`}>
    <circle cx="56" cy="56" r="48" className="ring-track" />
    <circle cx="56" cy="56" r="48" className="ring-value" style={{ strokeDasharray: circumference, strokeDashoffset: offset }} />
  </svg><div className="score-ring-label"><strong>{Math.round(score)}</strong><span>/ 100</span></div></div>;
}

function SkillGroup({ title, items, tone, empty }: { title: string; items: SkillMatch[]; tone: string; empty: string }) {
  return <section className="skill-group">
    <div className="group-heading"><h3>{title}</h3><span className={`count ${tone}`}>{items.length}</span></div>
    {items.length ? <div className="skill-list">{items.map((item) => <article className="skill-item" key={item.skill}>
      <div className="skill-item-top"><div><strong>{item.skill}</strong><small>{item.category} · {item.importance}</small></div><span className={`status-tag ${tone}`}>{item.status}</span></div>
      <p>{item.explanation}</p>{item.evidence && <blockquote>“{item.evidence}”</blockquote>}
    </article>)}</div> : <p className="empty-state">{empty}</p>}
  </section>;
}

export default function App() {
  const [resumeText, setResumeText] = useState(sampleResume);
  const [jobDescription, setJobDescription] = useState(sampleJob);
  const [fileName, setFileName] = useState("");
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const ready = useMemo(() => resumeText.trim().length > 0 && jobDescription.trim().length > 0, [resumeText, jobDescription]);

  async function uploadResume(file?: File) {
    if (!file) return;
    setError(""); setFileName(file.name);
    const body = new FormData(); body.append("file", file);
    try {
      const response = await fetch(`${API_BASE}/api/resume/parse`, { method: "POST", body });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.detail || "Could not parse this file.");
      setResumeText(payload.text);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Resume upload failed.");
    }
  }

  async function runAnalysis() {
    setLoading(true); setError("");
    try {
      const response = await fetch(`${API_BASE}/api/analyze`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ resume_text: resumeText, job_description: jobDescription, semantic_weight: 0.25 }),
      });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.detail || "Analysis failed.");
      setAnalysis(payload);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not reach the analysis API. Is the backend running?");
    } finally { setLoading(false); }
  }

  return <main className="app-shell">
    <header className="topbar"><a className="brand" href="#top"><span className="brand-mark"><Sparkles size={18} /></span><span>matchwise<span className="brand-dot">.</span></span></a><div className="topbar-right"><span className="top-pill"><span className="live-dot" /> Explainable career readiness</span><a className="github-link" href="https://github.com/" target="_blank" rel="noreferrer">Project workspace <ArrowUpRight size={14} /></a></div></header>
    <section className="hero" id="top"><div className="eyebrow"><span className="eyebrow-line" /> CAREER READINESS, WITH EVIDENCE</div><h1>Know where you stand.<br /><em>See what to build next.</em></h1><p>Compare your resume with a job description and get a clear view of your strengths, skill gaps and next learning steps.</p></section>
    <section className="workspace-grid">
      <div className="input-panel panel"><div className="panel-heading"><div><span className="step-label">01 / YOUR PROFILE</span><h2>Resume</h2></div><FileText size={19} /></div>
        <label className="upload-box"><input type="file" accept=".pdf,.docx" onChange={(event) => uploadResume(event.target.files?.[0])} /><UploadCloud size={19} /><span><strong>{fileName || "Upload your resume"}</strong><small>PDF or DOCX · up to 8 MB</small></span><span className="browse-link">Browse</span></label>
        <div className="or-divider"><span>OR PASTE YOUR RESUME</span></div>
        <textarea value={resumeText} onChange={(event) => setResumeText(event.target.value)} placeholder="Paste resume text here…" aria-label="Resume text" />
        <div className="field-foot"><span>{resumeText.trim().split(/\s+/).filter(Boolean).length} words</span><button className="text-button" onClick={() => { setResumeText(""); setFileName(""); setAnalysis(null); }}>Clear text</button></div>
      </div>
      <div className="input-panel panel"><div className="panel-heading"><div><span className="step-label">02 / TARGET ROLE</span><h2>Job description</h2></div><BriefcaseBusiness size={19} /></div>
        <div className="jd-tip"><Sparkles size={15} /><span>Paste the full role description. We’ll separate required and preferred skills where the wording makes that clear.</span></div>
        <textarea className="job-textarea" value={jobDescription} onChange={(event) => setJobDescription(event.target.value)} placeholder="Paste the job description here…" aria-label="Job description" />
        <div className="field-foot"><span>{jobDescription.trim().split(/\s+/).filter(Boolean).length} words</span><button className="text-button" onClick={() => { setJobDescription(""); setAnalysis(null); }}>Clear text</button></div>
      </div>
    </section>
    {error && <div className="error-banner"><CircleAlert size={17} />{error}</div>}
    <div className="analyze-row"><div className="privacy-note"><BadgeCheck size={16} /><span>Demo only: text is analyzed in memory and is not stored by this starter app.</span></div><button className="analyze-button" disabled={!ready || loading} onClick={runAnalysis}>{loading ? <><LoaderCircle className="spin" size={17} /> Analysing…</> : <>Analyse match <ChevronRight size={17} /></>}</button></div>

    {analysis && <section className="results-section" aria-live="polite"><div className="results-header"><div><span className="step-label">03 / YOUR MATCH REPORT</span><h2>The signal behind your score.</h2><p>Every match is tied to detected skills and evidence, so you can verify the result.</p></div><span className="report-badge"><Check size={14} /> Analysis complete</span></div>
      <div className="overview-grid"><article className="score-card panel"><div><span className="card-kicker">OVERALL ALIGNMENT</span><h3>Role match score</h3><p>Use this as a guide, not a hiring verdict.</p></div><ScoreRing score={analysis.overall_score} /><div className="score-breakdown"><div><span>Weighted coverage</span><strong>{analysis.coverage_score}%</strong></div><div className="mini-track"><span style={{ width: `${analysis.coverage_score}%` }} /></div><div><span>Semantic signal</span><strong>{analysis.semantic_score}%</strong></div><div className="mini-track semantic"><span style={{ width: `${analysis.semantic_score}%` }} /></div><small>Mode: {analysis.semantic_mode.replaceAll("-", " ")}</small></div></article>
        <article className="stats-card panel"><span className="card-kicker">SKILL BREAKDOWN</span><div className="stat-row"><div className="stat-icon strong"><Check size={17} /></div><div><strong>{analysis.strong_matches}</strong><span>Strong matches</span></div></div><div className="stat-row"><div className="stat-icon partial"><Sparkles size={17} /></div><div><strong>{analysis.partial_matches}</strong><span>Partial matches</span></div></div><div className="stat-row"><div className="stat-icon missing"><CircleAlert size={17} /></div><div><strong>{analysis.missing_skills}</strong><span>Missing requirements</span></div></div><div className="stats-foot">{analysis.requirements_found} requirements detected in the job description</div></article></div>
      <div className="match-columns"><SkillGroup title="Strong matches" items={analysis.matched_skills} tone="green" empty="No direct skill evidence detected yet." /><SkillGroup title="Partial matches" items={analysis.partial_skills} tone="amber" empty="No partial matches found." /><SkillGroup title="Missing skills" items={analysis.missing_skill_matches} tone="red" empty="No missing skills detected." /></div>
      <section className="roadmap panel"><div className="panel-heading"><div><span className="step-label">04 / NEXT STEPS</span><h2>Your skill-gap roadmap</h2></div><Sparkles size={19} /></div><p className="roadmap-intro">Turn the gaps into proof of work. Start with required skills before polishing preferred ones.</p>
        {analysis.learning_roadmap.length ? <div className="roadmap-list">{analysis.learning_roadmap.map((step, index) => <article className="roadmap-item" key={step.skill}><div className="roadmap-index">{String(index + 1).padStart(2, "0")}</div><div className="roadmap-content"><div className="roadmap-title"><strong>{step.skill}</strong><span className={`priority ${step.priority.toLowerCase()}`}>{step.priority} priority</span></div><p>{step.reason}</p><div className="roadmap-detail"><span>LEARNING TASK</span>{step.task}</div><div className="roadmap-detail"><span>PROJECT IDEA</span>{step.project_idea}</div></div></article>)}</div> : <p className="empty-state">No skill gaps were found in this comparison.</p>}
      </section>
      <details className="methodology panel"><summary>How this score is calculated <ChevronRight size={16} /></summary><p>{analysis.methodology_note}</p><p>Exact normalized skills receive a strong match (1.0). Related evidence may receive a partial match (0.5); absent evidence receives 0. Required skills carry weight 2 and preferred skills carry weight 1. The initial hybrid configuration combines 75% coverage and 25% semantic signal. The experiment plan will test and tune this weighting.</p></details>
    </section>}
    <footer className="footer"><span>matchwise<span className="brand-dot">.</span> <small>Academic project prototype · v0.1</small></span><span>Evidence over guesswork.</span></footer>
  </main>;
}
