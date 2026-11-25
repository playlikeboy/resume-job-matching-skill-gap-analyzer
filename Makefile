.PHONY: backend-test backend-eval backend-run frontend-install frontend-dev frontend-build

backend-test:
	cd backend && pytest -q

backend-eval:
	cd backend && python scripts/evaluate.py

backend-run:
	cd backend && uvicorn app.main:app --reload --port 8000

frontend-install:
	cd frontend && npm install

frontend-dev:
	cd frontend && npm run dev

frontend-build:
	cd frontend && npm run build
