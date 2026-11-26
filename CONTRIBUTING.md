# Contributing

1. Create a focused branch for each feature or experiment.
2. Add or update tests for extraction, matching, scoring, API, and Streamlit UI changes.
3. Keep the explainability output in sync with the scoring logic.
4. Never commit real candidate resumes, personal data, secrets, or API tokens.
5. Document the dataset source, annotation protocol, and model version for every experiment.
6. Verify locally before opening a pull request:
   - Backend & Streamlit tests: `cd backend && pytest -v && python scripts/evaluate.py`
   - Streamlit UI smoke run: `streamlit run streamlit_app.py`

For research changes, include the baseline being compared, the metric, the evaluation split, and any threshold or model changes.
