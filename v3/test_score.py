import importlib.util
from pathlib import Path


SPEC = importlib.util.spec_from_file_location("v3_score", Path(__file__).with_name("score.py"))
assert SPEC is not None and SPEC.loader is not None
score = importlib.util.module_from_spec(SPEC)


def test_stable_true_requires_two_of_three():
    SPEC.loader.exec_module(score)
    assert score.stable_true([True, True, False]) is True
    assert score.stable_true([True, False, False]) is False
    assert score.stable_true([False, False, False]) is False


def test_latency_summary_reports_median_and_p95():
    SPEC.loader.exec_module(score)
    result = score.latency_summary([1.0, 2.0, 3.0, 4.0, 5.0])
    assert result["median_s"] == 3.0
    assert result["p95_s"] == 4.8


def test_v31_case_fixes_are_explicit():
    import json

    cases = {c["id"]: c for c in json.loads((Path(__file__).parent / "cases.json").read_text())}
    assert "twice daily" in cases["med_m1"]["artifact"]
    assert "once daily" in cases["med_m1"]["artifact"]
    assert "complete patient instruction" in cases["med_m2"]["brief"]
    assert "Supplied linguistic screen" in cases["name_m1"]["brief"]
