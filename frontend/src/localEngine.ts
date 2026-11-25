import type { Analysis, CategorySummary, CompareResult, JobComparisonInput, LearningStep, SkillMatch } from "./types";

type SkillMeta = {
  category: string;
  aliases: string[];
  caseSensitiveTerms?: string[];
  excludedFollowing?: string[];
};

const SKILLS: Record<string, SkillMeta> = {
  Python: { category: "Programming", aliases: ["python3"] },
  Java: { category: "Programming", aliases: ["java language"] },
  JavaScript: { category: "Programming", aliases: ["javascript", "js"] },
  TypeScript: { category: "Programming", aliases: ["ts"] },
  "C++": { category: "Programming", aliases: ["cpp", "cplusplus"] },
  Go: { category: "Programming", aliases: ["golang"], caseSensitiveTerms: ["Go"] },
  SQL: { category: "Data", aliases: ["structured query language"] },
  HTML: { category: "Frontend", aliases: ["html5"] },
  CSS: { category: "Frontend", aliases: ["css3"] },
  React: { category: "Frontend", aliases: ["react.js", "reactjs"] },
  "Next.js": { category: "Frontend", aliases: ["nextjs"] },
  "Vue.js": { category: "Frontend", aliases: ["vuejs", "vue"] },
  "Tailwind CSS": { category: "Frontend", aliases: ["tailwind", "tailwindcss"] },
  "Node.js": { category: "Backend", aliases: ["nodejs", "node"] },
  "Express.js": {
    category: "Backend",
    aliases: ["expressjs", "express"],
    excludedFollowing: [
      "interest", "interests", "concern", "concerns", "thoughts",
      "ideas", "gratitude", "yourself", "opinion", "opinions", "lane", "delivery",
    ],
  },
  FastAPI: { category: "Backend", aliases: ["fast api"] },
  Flask: { category: "Backend", aliases: [] },
  Django: { category: "Backend", aliases: ["django rest framework", "drf"] },
  "Spring Boot": { category: "Backend", aliases: ["springboot"] },
  "REST APIs": { category: "Backend", aliases: ["rest api", "restful api", "restful apis"] },
  GraphQL: { category: "Backend", aliases: [] },
  PostgreSQL: { category: "Databases", aliases: ["postgres"] },
  MySQL: { category: "Databases", aliases: ["mysql database"] },
  SQLite: { category: "Databases", aliases: ["sqlite3"] },
  MongoDB: { category: "Databases", aliases: ["mongo"] },
  Redis: { category: "Databases", aliases: [] },
  Docker: { category: "DevOps", aliases: ["containerization", "containers"] },
  Kubernetes: { category: "DevOps", aliases: ["k8s"] },
  "CI/CD": { category: "DevOps", aliases: ["continuous integration", "continuous delivery", "continuous deployment"] },
  "GitHub Actions": { category: "DevOps", aliases: ["gh actions"] },
  Git: { category: "Developer Tools", aliases: ["git version control", "github", "gitlab"] },
  "Unit Testing": { category: "Developer Tools", aliases: ["pytest", "jest", "unit tests", "automated testing"] },
  Linux: { category: "Systems", aliases: ["linux operating system", "bash", "shell scripting"] },
  AWS: { category: "Cloud", aliases: ["amazon web services"] },
  Azure: { category: "Cloud", aliases: ["microsoft azure"] },
  "Google Cloud": { category: "Cloud", aliases: ["gcp", "google cloud platform"] },
  "Machine Learning": { category: "AI/ML", aliases: ["ml", "machine learning algorithms"] },
  "Deep Learning": { category: "AI/ML", aliases: ["dl", "neural networks"] },
  NLP: { category: "AI/ML", aliases: ["natural language processing"] },
  PyTorch: { category: "AI/ML", aliases: ["pytorch framework"] },
  TensorFlow: { category: "AI/ML", aliases: ["tensorflow framework", "keras"] },
  "scikit-learn": { category: "AI/ML", aliases: ["sklearn", "scikit learn"] },
  pandas: { category: "Data", aliases: ["python pandas"] },
  NumPy: { category: "Data", aliases: ["numpy"] },
  Jupyter: { category: "Data", aliases: ["jupyter notebook", "jupyter notebooks"] },
  "Data Analysis": { category: "Data", aliases: ["data analytics", "exploratory data analysis", "eda"] },
  "Data Visualization": { category: "Data", aliases: ["matplotlib", "seaborn", "plotly", "recharts"] },
  Statistics: { category: "Data", aliases: ["statistical analysis", "hypothesis testing"] },
  "Sentence Transformers": { category: "AI/ML", aliases: ["sentence transformer", "sentence embeddings"] },
  spaCy: { category: "AI/ML", aliases: ["spacy"] },
  "Apache Spark": { category: "Data Engineering", aliases: ["pyspark", "spark"] },
  Kafka: { category: "Data Engineering", aliases: ["apache kafka"] },
  "Object-Oriented Programming": { category: "Engineering Practices", aliases: ["oop"] },
  "Data Structures & Algorithms": { category: "Engineering Practices", aliases: ["dsa", "data structures", "algorithms"] },
};

const RELATED_SKILLS: Record<string, string[]> = {
  "REST APIs": ["FastAPI", "Flask", "Django", "Express.js", "Node.js", "Spring Boot", "GraphQL"],
  GraphQL: ["REST APIs", "FastAPI", "Express.js", "Node.js"],
  FastAPI: ["Flask", "Django", "REST APIs", "Python"],
  Flask: ["FastAPI", "Django", "REST APIs", "Python"],
  Django: ["FastAPI", "Flask", "REST APIs", "Python"],
  "Express.js": ["Node.js", "REST APIs", "FastAPI", "JavaScript", "TypeScript"],
  "Node.js": ["Express.js", "JavaScript", "TypeScript", "REST APIs"],
  "Spring Boot": ["Java", "REST APIs"],
  PostgreSQL: ["SQL", "MySQL", "SQLite"],
  MySQL: ["SQL", "PostgreSQL", "SQLite"],
  SQLite: ["SQL", "PostgreSQL", "MySQL"],
  SQL: ["PostgreSQL", "MySQL", "SQLite", "Data Analysis"],
  React: ["Next.js", "Vue.js", "JavaScript", "TypeScript", "HTML", "CSS"],
  "Next.js": ["React", "TypeScript", "JavaScript"],
  "Vue.js": ["React", "JavaScript", "TypeScript", "HTML", "CSS"],
  TypeScript: ["JavaScript", "React", "Next.js", "Node.js"],
  JavaScript: ["TypeScript", "React", "Node.js", "HTML"],
  "Tailwind CSS": ["CSS", "HTML", "React"],
  Docker: ["Kubernetes", "CI/CD", "Linux"],
  Kubernetes: ["Docker", "AWS", "Azure", "Google Cloud"],
  "CI/CD": ["GitHub Actions", "Docker", "Git", "Unit Testing"],
  "GitHub Actions": ["CI/CD", "Git", "Docker"],
  AWS: ["Azure", "Google Cloud", "Docker", "Linux"],
  Azure: ["AWS", "Google Cloud", "Docker"],
  "Google Cloud": ["AWS", "Azure", "Docker"],
  "Machine Learning": ["scikit-learn", "PyTorch", "TensorFlow", "Deep Learning", "Statistics"],
  "Deep Learning": ["PyTorch", "TensorFlow", "Machine Learning", "NLP"],
  PyTorch: ["TensorFlow", "Deep Learning", "Machine Learning"],
  TensorFlow: ["PyTorch", "Deep Learning", "Machine Learning"],
  "scikit-learn": ["Machine Learning", "pandas", "NumPy", "Statistics"],
  NLP: ["spaCy", "Sentence Transformers", "PyTorch", "Machine Learning"],
  spaCy: ["NLP", "Sentence Transformers", "Python"],
  "Sentence Transformers": ["NLP", "PyTorch", "spaCy"],
  "Data Analysis": ["pandas", "NumPy", "SQL", "Statistics", "Data Visualization", "Jupyter"],
  "Data Visualization": ["Data Analysis", "pandas", "Jupyter"],
  pandas: ["NumPy", "Data Analysis", "Python", "scikit-learn"],
  NumPy: ["pandas", "Data Analysis", "scikit-learn", "Python"],
  Statistics: ["Data Analysis", "Machine Learning", "NumPy"],
};

const RESOURCE_MAP: Record<string, [string, string]> = {
  Python: ["Complete a focused Python fundamentals track, then practise functions, data structures and testing.", "Build a CLI expense tracker with CSV import, validation and unit tests."],
  JavaScript: ["Practise ES modules, asynchronous code, browser APIs and debugging.", "Build a searchable job-board interface that consumes a public API."],
  TypeScript: ["Learn types, unions, generics and typing React components.", "Convert a small JavaScript app to strict TypeScript."],
  SQL: ["Practise joins, grouping, subqueries, indexes and query plans.", "Design a relational schema and write analytics queries for a placement portal."],
  React: ["Practise component composition, state, effects, forms and accessibility.", "Build a role-comparison dashboard with filters and reusable components."],
  "REST APIs": ["Study HTTP methods, status codes, validation, pagination and API testing.", "Create a documented REST API with authentication and automated tests."],
  Docker: ["Learn images, containers, volumes, networking and multi-stage builds.", "Containerize a full-stack app with a repeatable local development setup."],
  "Machine Learning": ["Review supervised learning, data leakage, validation and metric selection.", "Train and compare a baseline classifier with a documented evaluation split."],
  NLP: ["Study tokenization, text normalization, embeddings and evaluation of extraction systems.", "Build a skill/entity extraction benchmark with manually annotated examples."],
  PostgreSQL: ["Practise schema design, constraints, joins, indexes and migrations.", "Persist analysis history using a normalized schema and migrations."],
};

const PREFERRED_MARKERS = [
  "preferred", "nice to have", "nice-to-have", "bonus", "good to have",
  "desirable", "desired", "ideally", "plus", "preferred qualifications", "optional",
];
const REQUIRED_MARKERS = [
  "required", "must have", "must-have", "minimum qualifications",
  "basic qualifications", "core requirements", "essential",
];
const NEGATION_RE = /\b(?:no\s+(?:prior\s+)?(?:experience|knowledge|background|familiarity)\s+(?:with|in)|not\s+familiar\s+with|never\s+used|haven't\s+used|have\s+not\s+used|do\s+not\s+know)\s*$/i;

function escapeRegex(value: string): string {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&").replace(/\s+/g, "\\s+");
}

function isNegated(text: string, start: number): boolean {
  const prefix = text.slice(Math.max(0, start - 55), start);
  return NEGATION_RE.test(prefix);
}

function snippetFor(text: string, start: number, end: number): string {
  const lineStart = Math.max(0, text.lastIndexOf("\n", start) + 1);
  const nextNl = text.indexOf("\n", end);
  const nextDot = text.indexOf(".", end);
  const candidates = [nextNl, nextDot].filter((i) => i >= 0);
  const lineEnd = candidates.length ? Math.min(...candidates) + 1 : Math.min(text.length, end + 100);
  const line = text.slice(lineStart, lineEnd).replace(/\s+/g, " ").trim();
  if (line.length > 220) {
    const left = Math.max(0, start - lineStart - 75);
    return `…${line.slice(left, left + 180).trim()}…`;
  }
  return line || text.slice(Math.max(0, start - 40), end + 60).trim();
}

type Extracted = { name: string; category: string; evidence: string; aliasFound: string; start: number; end: number; occurrences: number };

function extractSkillsLocal(text: string, ignoreNegated: boolean): Record<string, Extracted> {
  const found: Record<string, Extracted> = {};
  for (const [canonical, meta] of Object.entries(SKILLS)) {
    const aliases = [canonical, ...meta.aliases];
    let bestStart = -1;
    let bestEnd = -1;
    let bestAlias = canonical;
    let total = 0;

    for (const alias of aliases) {
      const escaped = escapeRegex(alias.trim());
      const negAfter =
        alias.toLowerCase() === "express" && meta.excludedFollowing
          ? `(?!\\s+(?:${meta.excludedFollowing.map(escapeRegex).join("|")})\\b)`
          : "";
      const flags = meta.caseSensitiveTerms?.includes(alias) ? "g" : "gi";
      const re = new RegExp(`(?<![A-Za-z0-9])${escaped}(?![A-Za-z0-9])${negAfter}`, flags);

      for (const m of text.matchAll(re)) {
        const idx = m.index ?? -1;
        if (idx < 0) continue;
        if (ignoreNegated && isNegated(text, idx)) continue;
        total += 1;
        if (bestStart === -1 || idx < bestStart) {
          bestStart = idx;
          bestEnd = idx + m[0].length;
          bestAlias = alias;
        }
      }
    }
    if (bestStart >= 0) {
      found[canonical] = {
        name: canonical,
        category: meta.category,
        evidence: snippetFor(text, bestStart, bestEnd),
        aliasFound: bestAlias,
        start: bestStart,
        end: bestEnd,
        occurrences: total,
      };
    }
  }
  return found;
}

function buildLineSections(jd: string): Array<[number, "required" | "preferred"]> {
  const sections: Array<[number, "required" | "preferred"]> = [[0, "required"]];
  let offset = 0;
  for (const line of jd.split(/(?<=\n)/)) {
    const stripped = line.trim().toLowerCase();
    if (stripped && (stripped.endsWith(":") || /^[a-z][a-z\s/&\-]{2,50}:?$/i.test(stripped))) {
      if (PREFERRED_MARKERS.some((m) => stripped.includes(m))) sections.push([offset, "preferred"]);
      else if (REQUIRED_MARKERS.some((m) => stripped.includes(m))) sections.push([offset, "required"]);
      else if (["qualifications", "requirements", "responsibilities"].some((h) => stripped.includes(h))) {
        sections.push([offset, "required"]);
      }
    }
    offset += line.length;
  }
  return sections;
}

function scoreBand(score: number): string {
  if (score >= 80) return "Strong alignment";
  if (score >= 60) return "Moderate alignment";
  if (score >= 40) return "Developing alignment";
  return "Early-stage gap";
}

function tokens(value: string): Set<string> {
  return new Set((value.toLowerCase().match(/[a-z0-9+#.]+/g) || []).filter((t) => t.length > 1));
}

function localSimilarity(skill: string, resumeText: string, resumeSkills: Set<string>): number {
  const related = RELATED_SKILLS[skill] || [];
  if (related.some((r) => resumeSkills.has(r))) return 0.55;
  const sTok = tokens(skill);
  const rTok = tokens(resumeText);
  if (!sTok.size || !rTok.size) return 0;
  let overlap = 0;
  for (const t of sTok) if (rTok.has(t)) overlap += 1;
  return Math.min(1, (overlap / sTok.size) * 0.7);
}

export function analyzeLocal(resumeText: string, jobDescription: string, semanticWeight = 0.25): Analysis {
  const resumeSkills = extractSkillsLocal(resumeText, true);
  const jdSkills = extractSkillsLocal(jobDescription, false);
  const jdList = Object.values(jdSkills);
  if (!jdList.length) {
    throw new Error("No supported skills were detected in the job description.");
  }

  const lowered = jobDescription.toLowerCase();
  const sections = buildLineSections(jobDescription);
  const resumeSet = new Set(Object.keys(resumeSkills));
  const matches: SkillMatch[] = [];
  let totalWeight = 0;
  let covered = 0;
  let semanticTotal = 0;

  const catMap = new Map<string, { total: number; strong: number; partial: number; missing: number; weight: number; covered: number }>();

  for (const item of jdList) {
    const before = lowered.slice(Math.max(0, item.start - 250), item.start);
    const lastPref = Math.max(-1, ...PREFERRED_MARKERS.map((m) => before.lastIndexOf(m)));
    const lastReq = Math.max(-1, ...REQUIRED_MARKERS.map((m) => before.lastIndexOf(m)));
    let sectionLabel: "required" | "preferred" = "required";
    for (const [off, lbl] of sections) if (off <= item.start) sectionLabel = lbl;

    const ends = ["\n", ".", ";", "!", "?"].map((ch) => lowered.indexOf(ch, item.end)).filter((i) => i >= 0);
    const sentEnd = ends.length ? Math.min(...ends) : Math.min(lowered.length, item.end + 60);
    const inlineAfter = lowered.slice(item.end, sentEnd);
    const inlinePref = inlineAfter.length <= 60 && PREFERRED_MARKERS.some((m) => inlineAfter.includes(m));
    const localPref = lastPref > lastReq && lastPref >= 0;
    const sectionPref = sectionLabel === "preferred" && lastReq < 0;
    const preferred = inlinePref || localPref || sectionPref;
    const weight = preferred ? 1.0 : 2.0;

    const evidenceItem = resumeSkills[item.name];
    const rawSim = localSimilarity(item.name, resumeText, resumeSet);
    let similarity = rawSim;
    let status = "missing";
    let matchValue = 0.0;
    let evidence: string | null = null;
    let explanation = "No direct or sufficiently related evidence was detected in the supplied resume text.";

    if (evidenceItem) {
      similarity = 1.0;
      status = "strong";
      matchValue = 1.0;
      evidence = evidenceItem.evidence;
      const mentionNote = evidenceItem.occurrences > 1 ? ` (${evidenceItem.occurrences} mentions)` : "";
      explanation = `Direct skill evidence found as '${evidenceItem.aliasFound}'${mentionNote}.`;
    } else if (rawSim >= 0.48) {
      status = "partial";
      matchValue = 0.5;
      explanation = "Related wording or skills were detected; verify that this experience demonstrates the requirement.";
    }

    totalWeight += weight;
    covered += weight * matchValue;
    semanticTotal += weight * similarity;

    const cat = catMap.get(item.category) || { total: 0, strong: 0, partial: 0, missing: 0, weight: 0, covered: 0 };
    cat.total += 1;
    if (status === "strong") cat.strong += 1;
    else if (status === "partial") cat.partial += 1;
    else cat.missing += 1;
    cat.weight += weight;
    cat.covered += weight * matchValue;
    catMap.set(item.category, cat);

    matches.push({
      skill: item.name,
      category: item.category,
      importance: preferred ? "preferred" : "required",
      weight,
      status,
      match_value: matchValue,
      similarity: Number(similarity.toFixed(4)),
      evidence,
      explanation,
      requirement_rationale: preferred ? "Classified as preferred requirement." : "Classified as required requirement.",
    });
  }

  const coverageScore = (100 * covered) / (totalWeight || 1);
  const semanticScore = (100 * semanticTotal) / (totalWeight || 1);
  const overall = (1 - semanticWeight) * coverageScore + semanticWeight * semanticScore;

  const strong = matches.filter((m) => m.status === "strong");
  const partial = matches.filter((m) => m.status === "partial");
  const missing = matches.filter((m) => m.status === "missing");

  const roadmap: LearningStep[] = [
    ...[...missing].sort((a, b) => b.weight - a.weight).map((m) => ({ skill: m.skill, priority: "High", reason: "Required or unverified skill not detected" })),
    ...[...partial].sort((a, b) => b.weight - a.weight).map((m) => ({ skill: m.skill, priority: "Medium", reason: "Related evidence detected, but direct evidence is limited" })),
  ]
    .slice(0, 12)
    .map(({ skill, priority, reason }) => {
      const [task, project_idea] = RESOURCE_MAP[skill] || [
        `Review the core concepts and practise ${skill} with small, measurable exercises.`,
        `Build a small end-to-end project that demonstrates ${skill} with tests and a README.`,
      ];
      return { skill, priority, reason, task, project_idea };
    });

  const requiredSet = new Set(matches.map((m) => m.skill));
  const category_breakdown: CategorySummary[] = [...catMap.entries()]
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([category, s]) => ({
      category,
      total_requirements: s.total,
      strong: s.strong,
      partial: s.partial,
      missing: s.missing,
      coverage_score: Number(((100 * s.covered) / (s.weight || 1)).toFixed(2)),
    }));

  const overallRounded = Number(overall.toFixed(2));
  return {
    overall_score: overallRounded,
    coverage_score: Number(coverageScore.toFixed(2)),
    semantic_score: Number(semanticScore.toFixed(2)),
    semantic_mode: "browser-demo-fallback",
    semantic_weight: semanticWeight,
    score_band: scoreBand(overallRounded),
    requirements_found: matches.length,
    strong_matches: strong.length,
    partial_matches: partial.length,
    missing_skills: missing.length,
    matched_skills: strong,
    partial_skills: partial,
    missing_skill_matches: missing,
    resume_skills_detected: [...resumeSet].sort(),
    extra_resume_skills: [...resumeSet].filter((s) => !requiredSet.has(s)).sort(),
    category_breakdown,
    learning_roadmap: roadmap,
    methodology_note:
      `Running in static browser demo mode (FastAPI server unreachable). Coverage uses strong=1.0, partial=0.5, missing=0.0 with required weight 2 and preferred weight 1 (${Math.round((1 - semanticWeight) * 100)}% coverage + ${Math.round(semanticWeight * 100)}% semantic alignment).`,
  };
}

export function compareLocal(resumeText: string, jobs: JobComparisonInput[], semanticWeight = 0.25): CompareResult {
  const resumeSkills = Object.keys(extractSkillsLocal(resumeText, true)).sort();
  const rankings = jobs
    .map((job) => {
      const res = analyzeLocal(resumeText, job.job_description, semanticWeight);
      return {
        title: job.title,
        overall_score: res.overall_score,
        coverage_score: res.coverage_score,
        semantic_score: res.semantic_score,
        score_band: res.score_band,
        requirements_found: res.requirements_found,
        strong_matches: res.strong_matches,
        partial_matches: res.partial_matches,
        missing_skills: res.missing_skills,
        top_strengths: res.matched_skills.slice(0, 5).map((m) => m.skill),
        top_gaps: res.missing_skill_matches.slice(0, 5).map((m) => m.skill),
      };
    })
    .sort((a, b) => b.overall_score - a.overall_score || b.strong_matches - a.strong_matches || a.missing_skills - b.missing_skills);

  return {
    semantic_mode: "browser-demo-fallback",
    semantic_weight: semanticWeight,
    resume_skills_detected: resumeSkills,
    rankings,
  };
}
