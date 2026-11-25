from pathlib import Path

from app.services.extractors import extract_resume_text
from scripts.evaluate import evaluate


def test_extract_resume_text_supports_txt():
    text = extract_resume_text("candidate.txt", b"Python and SQL experience.")
    assert "Python" in text


def test_evaluation_script_runs_on_synthetic_dataset():
    dataset = Path(__file__).resolve().parents[2] / "examples" / "evaluation_dataset.jsonl"
    metrics = evaluate(dataset)
    assert set(metrics) == {"B0", "B1", "H1"}
    assert metrics["H1"]["skill_f1"] >= metrics["B0"]["skill_f1"]
    assert metrics["H1"]["match_macro_f1"] >= metrics["B0"]["match_macro_f1"]
