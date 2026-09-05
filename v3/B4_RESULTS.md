# B1 vs B4 (DEEP lenses) — results

Protocol: 25 cases × 2 systems × 3 runs = 150 jobs. Evaluator
`gemini-3.6-flash-high`, judge `gemini-3.8-flash-high`, gold hidden, stable ≥2/3.
B4 job = 4 independent lenses + 1 synthesizer (judged output = synth only).
Evaluator errors: 0. Judge errors after same-model retry: 0. Status missing
after one B1 evaluator retry (v3.1 precedent): 0.

Raw data: `results_b4/raw_outputs.jsonl`, `results_b4/raw_judgments.jsonl`,
`results_b4/lens_outputs.jsonl`, aggregation: `results_b4/b4_report.json`.

## Aggregate

| system | recall | class acc | unsupported | readiness | chars | latency med/p95 | calls |
|---|---|---:|---:|---:|---:|---|---:|
| B1 | 0.95 | 0.90 | 0.043 | 0.56 | 47357 | 8.45 / 11.14 s | 75 |
| B4 | 0.95 | 0.80 | 0.056 | 0.60 | 77846 | 24.36 / 34.35 s | 375 |

## Gate check (B4 earns DEEP mode only if ALL hold)

1. recall ≥ B1 → 0.95 ≥ 0.95 — PASS
2. class ≥ B1 → 0.80 ≥ 0.90 — FAIL
3. unsupported ≤ B1 → 0.056 ≤ 0.043 — FAIL
4. readiness ≥ B1 → 0.60 ≥ 0.56 — PASS

## Where B4 lost

- `sql_incomplete` (gold PASS/NEEDS_EVIDENCE): B4 stable FAIL/BLOCKED — false defect.
- `str_m3` (gold PASS/NEEDS_EVIDENCE): B4 stable FAIL/BLOCKED — false defect.
- `name_ready` (gold PASS/READY): B4 stable FAIL/BLOCKED — false defect on a clean control.
- `med_ready`, `sum_ready`, `str_ready` (gold PASS/READY): B4 stable PASS/NEEDS_EVIDENCE — readiness downgrade.
- `sum_m1`: B4 detected the target (B1 missed) but misclassified it — no net gain.

B4 is more suspicious everywhere, including where gold says PASS. The lenses
raised recall pressure that the synthesizer did not contain: same failure mode
as B2, at 5× calls, 1.6× chars, ~3× latency.

## Verdict

**B4 FAILS — no DEEP mode.**

Per preregistration: no B4.1, no prompt patching. The discovery→synthesis split
did not resolve the recall/precision trade-off; it reproduced B2's false-positive
pattern at higher cost.
