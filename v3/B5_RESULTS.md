# B1 vs B5 (decomposition) — results

Protocol: 10 composite cases × 2 systems × 3 runs = 60 jobs. Evaluator
`gemini-3.6-flash-high`, judge `gemini-3.8-flash-high`, gold hidden, stable ≥2/3.
Evaluator errors: 0. Judge errors: 0. Status missing: 0.

Raw data: `results_b5/raw_outputs.jsonl`, `results_b5/raw_judgments.jsonl`,
aggregation: `results_b5/b5_report.json`.

## Aggregate

| system | recall | class acc | unsupported | readiness | chars | latency med/p95 |
|---|---|---:|---:|---:|---:|---|
| B1 | 0.57 | 0.57 | 0.148 | 0.50 | 19719 | 9.08 / 13.80 s |
| B5 | 0.86 | 0.86 | 0.138 | 0.50 | 46241 | 13.88 / 19.81 s |

## Case-by-case (stable)

| case | gold | B1 | B5 |
|---|---|---|---|
| etl_interface | CONFIRMED/FAIL | det/cls True, FAIL/READY | det/cls True, FAIL/READY |
| dose_handoff | CONFIRMED/FAIL | MISS (det False) | HIT (det/cls True) |
| edit_render_gap | CONFIRMED/FAIL | MISS (PASS/READY) | HIT (det/cls True) |
| phase_gate | CONFIRMED/FAIL | MISS | MISS (both) |
| report_chain | CONFIRMED/FAIL | HIT | HIT |
| screen_decide | CONFIRMED/FAIL | HIT | HIT |
| zoom_plan | CONFIRMED/FAIL | HIT | HIT |
| etl_clean | PASS/READY | PASS/READY | PASS/READY |
| dose_clean | PASS/READY | PASS/READY | PASS/READY |
| phases_clean | PASS/READY | PASS/READY | PASS/READY |

## Gate check

1. recall ≥ B1 → 0.86 ≥ 0.57 — PASS
2. class ≥ B1 → 0.86 ≥ 0.57 — PASS
3. unsupported ≤ B1 → 0.138 ≤ 0.148 — PASS (marginally)
4. readiness ≥ B1 → 0.50 ≥ 0.50 — PASS

## Verdict

**B5 PASSES.**

Decomposition fixed exactly the predicted failure type: two interface misses
(`dose_handoff`, `edit_render_gap`) that the flat pass lost, with zero new
false positives on clean composite controls. `phase_gate` was missed by both —
an honest miss, not a B5 regression. Shared weakness: both systems under-report
BLOCKED readiness on FAIL cases (0.50 each) — a separate issue, not caused by B5.

Cost: ~2.3× chars, ~1.5× latency, same 1-call structure (no agents).

Per preregistration this is held-out evidence for reopening FINAL_DECISION,
not a production change. Production skill untouched.
