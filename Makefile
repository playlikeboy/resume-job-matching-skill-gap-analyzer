.PHONY: backend-test backend-eval backend-run streamlit-install streamlit-run

backend-test:
	cd backend && pytest -q

backend-eval:
	cd backend && python scripts/evaluate.py

backend-run:
	cd backend && uvicorn app.main:app --reload --port 8000

streamlit-install:
	pip install -r requirements.txt

streamlit-run:
	streamlit run streamlit_app.py
