"""Reproducible comparison script for B0 (exact keyword), B1 (weighted taxonomy), and H1 (hybrid)."""

from __future__ import annotations

import json
import re
import statistics
import sys
import time
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = BACKEND_ROOT.parent
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.services.analysis import analyze_resume_job  # noqa: E402
from app.services.requirements import extract_job_requirements  # noqa: E402
from app.services.skill_extraction import extract_skills  # noqa: E402
from app.services.taxonomy import SKILLS  # noqa: E402


def _exact_canonical_skills(text: str) -> set[str]:
    """B0 baseline: match canonical skill names only (no aliases, no weighting/similarity)."""
    found: set[str] = set()
    for canonical in SKILLS:
        escaped = re.escape(canonical).replace(r"\ ", r"\s+")
        pattern = re.compile(rf"(?<![A-Za-z0-9]){escaped}(?![A-Za-z0-9])", re.IGNORECASE)
        if pattern.search(text):
            found.add(canonical)
    return found


def _prf(tp: int, fp: int, fn: int) -> tuple[float, float, float]:
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
    return precision, recall, f1


def _macro_f1(y_true: list[str], y_pred: list[str], labels: tuple[str, ...]) -> float:
    scores: list[float] = []
    for label in labels:
        tp = sum(1 for t, p in zip(y_true, y_pred) if t == label and p == label)
        fp = sum(1 for t, p in zip(y_true, y_pred) if t != label and p == label)
        fn = sum(1 for t, p in zip(y_true, y_pred) if t == label and p != label)
        _, _, f1 = _prf(tp, fp, fn)
        scores.append(f1)
    return sum(scores) / len(scores) if scores else 0.0


def evaluate(dataset_path: Path) -> dict[str, dict[str, float | str]]:
    rows = [
        json.loads(line)
        for line in dataset_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    # Accumulators for B0, B1, H1
    systems = ("B0", "B1", "H1")
    skill_counts = {s: {"tp": 0, "fp": 0, "fn": 0} for s in systems}
    match_true: list[str] = []
    match_preds: dict[str, list[str]] = {s: [] for s in systems}
    latencies_ms: dict[str, list[float]] = {s: [] for s in systems}
    importance_correct = 0
    importance_total = 0
    h1_mode = "rule-based-fallback"

    for row in rows:
        resume_text = row["resume_text"]
        job_desc = row["job_description"]
        expected_skills = set(row["expected_skills"])
        expected_imp = row["expected_importance"]
        expected_matches = row["expected_matches"]

        # B0: Exact canonical keyword matching only
        t0 = time.perf_counter()
        b0_jd = _exact_canonical_skills(job_desc)
        b0_resume = _exact_canonical_skills(resume_text)
        latencies_ms["B0"].append((time.perf_counter() - t0) * 1000.0)

        skill_counts["B0"]["tp"] += len(b0_jd & expected_skills)
        skill_counts["B0"]["fp"] += len(b0_jd - expected_skills)
        skill_counts["B0"]["fn"] += len(expected_skills - b0_jd)

        # B1: Weighted taxonomy + aliases (coverage-only, no partial semantic signal)
        t1 = time.perf_counter()
        b1_reqs = extract_job_requirements(job_desc)
        b1_resume = extract_skills(resume_text, ignore_negated=True)
        latencies_ms["B1"].append((time.perf_counter() - t1) * 1000.0)

        b1_jd_set = {r.skill for r in b1_reqs}
        skill_counts["B1"]["tp"] += len(b1_jd_set & expected_skills)
        skill_counts["B1"]["fp"] += len(b1_jd_set - expected_skills)
        skill_counts["B1"]["fn"] += len(expected_skills - b1_jd_set)

        for r in b1_reqs:
            if r.skill in expected_imp:
                importance_total += 1
                if r.importance == expected_imp[r.skill]:
                    importance_correct += 1

        # H1: Full hybrid pipeline
        t2 = time.perf_counter()
        h1_res = analyze_resume_job(resume_text, job_desc)
        latencies_ms["H1"].append((time.perf_counter() - t2) * 1000.0)
        h1_mode = h1_res.semantic_mode

        h1_by_skill = {
            item.skill: item.status
            for item in (*h1_res.matched_skills, *h1_res.partial_skills, *h1_res.missing_skill_matches)
        }
        h1_jd_set = set(h1_by_skill)
        skill_counts["H1"]["tp"] += len(h1_jd_set & expected_skills)
        skill_counts["H1"]["fp"] += len(h1_jd_set - expected_skills)
        skill_counts["H1"]["fn"] += len(expected_skills - h1_jd_set)

        for skill, expected_label in expected_matches.items():
            match_true.append(expected_label)
            match_preds["B0"].append("strong" if (skill in b0_jd and skill in b0_resume) else "missing")
            match_preds["B1"].append("strong" if (skill in b1_jd_set and skill in b1_resume) else "missing")
            match_preds["H1"].append(h1_by_skill.get(skill, "missing"))

    summary: dict[str, dict[str, float | str]] = {}
    for system in systems:
        c = skill_counts[system]
        p, r, f1 = _prf(c["tp"], c["fp"], c["fn"])
        macro_f1 = _macro_f1(match_true, match_preds[system], ("strong", "partial", "missing"))
        summary[system] = {
            "skill_precision": round(p, 4),
            "skill_recall": round(r, 4),
            "skill_f1": round(f1, 4),
            "match_macro_f1": round(macro_f1, 4),
            "median_latency_ms": round(statistics.median(latencies_ms[system]), 3),
            "importance_accuracy": round(importance_correct / importance_total, 4) if system != "B0" and importance_total else 0.0,
            "mode": "exact-canonical" if system == "B0" else ("taxonomy-aliases" if system == "B1" else h1_mode),
        }
    return summary


def main() -> None:
    dataset = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO_ROOT / "examples" / "evaluation_dataset.jsonl"
    results = evaluate(dataset)
    print(f"Dataset: {dataset} (synthetic starter benchmark)\n")
    print("| System | Mode | Skill P | Skill R | Skill F1 | Match Macro-F1 | Median Latency (ms) |")
    print("|---|---|---:|---:|---:|---:|---:|")
    for sys_name, metrics in results.items():
        print(
            f"| {sys_name} | {metrics['mode']} | "
            f"{metrics['skill_precision']:.3f} | {metrics['skill_recall']:.3f} | "
            f"{metrics['skill_f1']:.3f} | {metrics['match_macro_f1']:.3f} | "
            f"{metrics['median_latency_ms']:.3f} |"
        )


if __name__ == "__main__":
    main()
