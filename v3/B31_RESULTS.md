# B3 vs B3.1 targeted regression — results

Protocol: 8 cases × 2 systems × 3 runs = 48 outputs. Evaluator `gemini-3.6-flash-high`,
judge `gemini-3.8-flash-high`, gold hidden from evaluator, stable = ≥2/3.
Judge errors after same-model retry: 0. Status missing: 0.

Raw data: `results_b31/raw_outputs.jsonl`, `results_b31/raw_judgments.jsonl`,
case-by-case aggregation: `results_b31/b31_report.json`.

## Case-by-case (stable results)

| case | gold | B3 det/cls/status/read | B3.1 det/cls/status/read |
|---|---|---|---|
| sum_m1_omission | CONFIRMED/FAIL/BLOCKED | True/True/FAIL/BLOCKED | True/True/FAIL/BLOCKED |
| str_m1_omission | CONFIRMED/FAIL/BLOCKED | True/False/PASS/NEEDS_EVIDENCE | True/False/PASS/NEEDS_EVIDENCE |
| med_incomplete_evidence | GAP/PASS/NEEDS_EVIDENCE | True/True/PASS/NEEDS_EVIDENCE | True/True/PASS/NEEDS_EVIDENCE |
| sum_incomplete_evidence | GAP/PASS/NEEDS_EVIDENCE | True/True/PASS/NEEDS_EVIDENCE | True/True/PASS/NEEDS_EVIDENCE |
| str_incomplete_evidence | GAP/PASS/NEEDS_EVIDENCE | True/True/PASS/NEEDS_EVIDENCE | True/True/PASS/NEEDS_EVIDENCE |
| name_incomplete_evidence | GAP/PASS/NEEDS_EVIDENCE | True/True/PASS/NEEDS_EVIDENCE | True/True/PASS/NEEDS_EVIDENCE |
| sql_ready_corrected | NONE/PASS/READY | PASS/READY | PASS/NEEDS_EVIDENCE |
| name_m1_supplied_fact | CONFIRMED/FAIL/BLOCKED | True/False/PASS/NEEDS_EVIDENCE | True/False/PASS/NEEDS_EVIDENCE |

## Aggregate

| system | recall | class acc | unsupported | readiness | chars | latency med/p95 |
|---|---|---:|---:|---:|---:|---|
| B3 | 1.00 | 0.71 | 0.000 | 0.75 | 19526 | 10.03 / 16.76 s |
| B3.1 | 1.00 | 0.71 | 0.000 | 0.625 | 21898 | 13.55 / 41.70 s |

## Gate check

1. sum_m1_omission CONFIRMED ≥2/3 → B3.1 True/True — PASS
2. str_m1_omission CONFIRMED ≥2/3 → B3.1 detected but class False, stable PASS/NEEDS_EVIDENCE — FAIL
3. four EVIDENCE_GAP controls stay PASS/NEEDS_EVIDENCE — PASS
4. sql_ready_corrected PASS/READY — B3.1 stable PASS/NEEDS_EVIDENCE — FAIL (readiness regression vs B3)
5. name_m1_supplied_fact FAIL/BLOCKED + CONFIRMED — B3.1 PASS/NEEDS_EVIDENCE, class False — FAIL
6. unsupported B3.1 ≤ B3 — 0.000 ≤ 0.000 — PASS

## Verdict

**B3.1 FAILS TARGETED GATE**

B3.1 shows no improvement over B3 on the two target omissions (str_m1 fails
identically under both prompts; sum_m1 passes under both) and regresses
readiness on the clean sql_ready control. Per plan: no further framework
layers, no full 25-case rerun.
