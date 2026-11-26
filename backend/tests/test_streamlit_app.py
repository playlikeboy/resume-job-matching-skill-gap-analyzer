from pathlib import Path

import pytest

streamlit = pytest.importorskip("streamlit")
pytest.importorskip("plotly")

from streamlit.testing.v1 import AppTest  # noqa: E402

APP_PATH = str(Path(__file__).resolve().parents[2] / "streamlit_app.py")


def test_streamlit_single_role_analysis_runs():
    at = AppTest.from_file(APP_PATH, default_timeout=15)
    at.run()
    assert not at.exception

    analyze_btn = next(btn for btn in at.button if btn.key == "btn_analyze")
    analyze_btn.click().run()
    assert not at.exception
    assert at.session_state["analysis_result"] is not None
    assert at.session_state["analysis_result"].requirements_found > 0


def test_streamlit_compare_roles_runs():
    at = AppTest.from_file(APP_PATH, default_timeout=15)
    at.run()
    assert not at.exception

    mode_radio = next(r for r in at.radio if r.key == "mode")
    mode_radio.set_value("Compare Multiple Roles").run()
    assert not at.exception

    compare_btn = next(btn for btn in at.button if btn.key == "btn_compare")
    compare_btn.click().run()
    assert not at.exception
    assert at.session_state["compare_result"] is not None
    assert len(at.session_state["compare_result"].rankings) == 3


def test_streamlit_taxonomy_and_benchmark_runs():
    at = AppTest.from_file(APP_PATH, default_timeout=15)
    at.run()
    assert not at.exception

    mode_radio = next(r for r in at.radio if r.key == "mode")
    mode_radio.set_value("Skill Taxonomy & Benchmark").run()
    assert not at.exception

    bench_btn = next(btn for btn in at.button if btn.key == "run_benchmark")
    bench_btn.click().run()
    assert not at.exception
    assert set(at.session_state["benchmark_results"]) == {"B0", "B1", "H1"}
