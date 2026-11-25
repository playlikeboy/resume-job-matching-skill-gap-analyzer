# Contributing

1. Create a focused branch for each feature or experiment.
2. Add or update tests for extraction, matching, scoring, and API changes.
3. Keep the explainability output in sync with the scoring logic.
4. Never commit real candidate resumes, personal data, secrets, or API tokens.
5. Document the dataset source, annotation protocol, and model version for every experiment.
6. Verify locally before opening a pull request:
   - Backend: `cd backend && pytest -v && python scripts/evaluate.py`
   - Frontend: `cd frontend && npm run build`

For research changes, include the baseline being compared, the metric, the evaluation split, and any threshold or model changes.
