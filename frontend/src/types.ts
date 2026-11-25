export type SkillMatch = {
  skill: string;
  category: string;
  importance: string;
  weight: number;
  status: string;
  match_value: number;
  similarity: number;
  evidence?: string | null;
  explanation: string;
  requirement_rationale?: string;
};

export type LearningStep = {
  skill: string;
  priority: string;
  reason: string;
  task: string;
  project_idea: string;
};

export type CategorySummary = {
  category: string;
  total_requirements: number;
  strong: number;
  partial: number;
  missing: number;
  coverage_score: number;
};

export type Analysis = {
  overall_score: number;
  coverage_score: number;
  semantic_score: number;
  semantic_mode: string;
  semantic_weight: number;
  score_band: string;
  requirements_found: number;
  strong_matches: number;
  partial_matches: number;
  missing_skills: number;
  matched_skills: SkillMatch[];
  partial_skills: SkillMatch[];
  missing_skill_matches: SkillMatch[];
  resume_skills_detected: string[];
  extra_resume_skills: string[];
  category_breakdown: CategorySummary[];
  learning_roadmap: LearningStep[];
  methodology_note: string;
};

export type JobComparisonInput = {
  title: string;
  job_description: string;
};

export type JobComparisonItem = {
  title: string;
  overall_score: number;
  coverage_score: number;
  semantic_score: number;
  score_band: string;
  requirements_found: number;
  strong_matches: number;
  partial_matches: number;
  missing_skills: number;
  top_strengths: string[];
  top_gaps: string[];
};

export type CompareResult = {
  semantic_mode: string;
  semantic_weight: number;
  resume_skills_detected: string[];
  rankings: JobComparisonItem[];
};
