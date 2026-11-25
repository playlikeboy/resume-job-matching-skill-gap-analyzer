# Experimental Protocol (Draft)

## Comparison systems

- **B0 — Keyword baseline:** exact canonical skill and alias detection, unweighted or transparently weighted as a baseline variant.
- **B1 — Weighted taxonomy:** normalized skills, required/preferred weights and evidence snippets.
- **H1 — Hybrid:** B1 plus sentence-embedding similarity for candidate evidence fragments.

## Annotation schema

Each annotation row should contain:

- pair_id (pseudonymous)
- role_family
- resume_source and job_source provenance
- job_skill_text
- canonical_skill
- importance (required / preferred / uncertain)
- resume_evidence_span (or empty)
- human_match_label (strong / partial / missing)
- reviewer_id (pseudonymous)
- adjudication_note

## Evaluation measures

- Precision, recall and F1 for canonical skill extraction.
- Macro-F1 for required/preferred/uncertain classification.
- Macro-F1 for strong/partial/missing matching.
- Score MAE or rank correlation against a human-reviewed rubric.
- Explanation relevance and actionability rubric.
- Median latency per pair.

## Experimental hygiene

1. Keep candidate-level splits disjoint between development and held-out testing.
2. Freeze the taxonomy and embedding model version before final test evaluation.
3. Tune thresholds only on the development set.
4. Run all comparison systems on the same examples.
5. Record random seeds, package versions, thresholds, weights and hardware.
6. Publish only aggregate results and synthetic examples unless explicit permission allows data sharing.
7. Keep a failure-case log, including alias errors, missing sections, false semantic matches and preferred/required misclassification.

## Results template

| System | Skill precision | Skill recall | Skill F1 | Match macro-F1 | Score MAE | Median latency |
|---|---:|---:|---:|---:|---:|---:|
| B0 — Keyword | TBD | TBD | TBD | TBD | TBD | TBD |
| B1 — Weighted taxonomy | TBD | TBD | TBD | TBD | TBD | TBD |
| H1 — Hybrid | TBD | TBD | TBD | TBD | TBD | TBD |

Do not fill TBD values until the experiment has been run and validated.
