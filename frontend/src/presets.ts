import type { JobComparisonInput } from "./types";

export const SAMPLE_RESUME = `Alex Example
Computer Science student

Projects
- Built REST APIs using Python and FastAPI with pytest unit tests.
- Developed responsive interfaces with React, JavaScript and TypeScript.
- Used PostgreSQL and SQL for structured data storage.
- Worked with Git, Docker and Linux during team projects.
- Explored NLP, Machine Learning and sentence embeddings in an academic prototype.`;

export const ROLE_PRESETS: Record<string, { label: string; jobDescription: string }> = {
  swe: {
    label: "SWE Intern",
    jobDescription: `Software Engineering Intern

Required qualifications
- Strong Python and JavaScript fundamentals.
- Experience building REST APIs using FastAPI or Express.js.
- SQL and PostgreSQL knowledge.
- Git, Unit Testing and Docker familiarity.

Preferred qualifications
- React and TypeScript experience.
- Exposure to NLP or Machine Learning.`,
  },
  data: {
    label: "Data Analyst Intern",
    jobDescription: `Data Analyst Intern

Required qualifications
- Strong SQL and Python skills for querying and cleaning data.
- Experience with pandas, NumPy, and Data Analysis in Jupyter.
- Data Visualization using matplotlib or plotly.

Preferred qualifications
- Statistics and hypothesis testing.
- PostgreSQL or MySQL experience.`,
  },
  ml: {
    label: "ML / NLP Intern",
    jobDescription: `Machine Learning & NLP Intern

Required qualifications
- Python programming and scikit-learn or PyTorch experience.
- Foundations in Machine Learning, Deep Learning, and NLP.
- Git and Linux workflow familiarity.

Preferred qualifications
- Sentence Transformers or spaCy experience.
- Docker and FastAPI deployment basics.`,
  },
};

export const DEFAULT_COMPARE_JOBS: JobComparisonInput[] = [
  { title: "Software Engineering Intern", job_description: ROLE_PRESETS.swe.jobDescription },
  { title: "ML / NLP Intern", job_description: ROLE_PRESETS.ml.jobDescription },
  { title: "Data Analyst Intern", job_description: ROLE_PRESETS.data.jobDescription },
];
