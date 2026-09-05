# Requirements-axes experiments — results (B6 / B7 / B8 vs B5)

Protocol per experiment: 14 cases (6 axis + 4 shared anchors + 4 shared
controls) × 2 systems × 3 runs = 84 evaluator jobs. Evaluator
`gemini-3.6-flash-high`, judge `gemini-3.8-flash-high`, gold hidden, stable
≥2/3, same-model retry only. Prompts/cases frozen before first call
(`v3/AXES_FREEZE_SHA256.txt` verified OK after runs).

Verification after retries: 84/84 outputs and 84/84 judgments per experiment,
0 evaluator errors, 0 judge errors, 0 unparseable judgments, 0 empty
judgments, 0 missing status.

## Verdicts

B6 STAKEHOLDER FAILS
B7 SYSTEM LEVEL FAILS
B8 TEMPORAL FAILS

## Aggregate table

| exp | system | recall | axis recall | anchor recall | class | axis class | unsup | readiness | chars | latency med/p95 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| b6 | B5 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.000 | 0.29 | 66551 | 11.97 / 18.13 s |
| b6 | B6 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.000 | 0.43 | 63350 | 11.59 / 18.14 s |
| b7 | B5 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.000 | 0.14 | 66659 | 14.33 / 18.53 s |
| b7 | B7 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.024 | 0.29 | 60328 | 14.24 / 17.21 s |
| b8 | B5 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.000 | 0.29 | 63362 | 11.22 / 15.87 s |
| b8 | B8 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.024 | 0.29 | 60326 | 11.43 / 18.83 s |

## Gate evaluation

- B6: axis recall 1.00 vs B5 1.00 — NOT strictly greater → coverage FAIL.
  All other gates pass (overall recall/class equal, anchors equal, unsup 0,
  readiness 0.43 ≥ 0.29, controls clean, cost within 1.5×). Ceiling effect:
  B5 already solved all 6 stakeholder cases, leaving no room to demonstrate gain.
- B7: axis recall equal → coverage FAIL. Safety FAIL: unsup 0.024 > B5 0.000
  (one speculative CONFIRMED failure, see excerpt below).
- B8: axis recall equal → coverage FAIL. Safety FAIL: unsup 0.024 > B5 0.000
  (one invented requirement inside a correct finding, see excerpt below).

## Controls (all three experiments)

- ZERO stable false FAIL on C1–C4 for every candidate.
- ZERO READY → NEEDS_EVIDENCE downgrades by candidates; candidates instead
  fixed B5's own NEEDS_EVIDENCE miscalibration on C1/C2 clean READY cases.
- C3/C4 remain non-FAIL everywhere (PASS/NEEDS_EVIDENCE, evidence-gap framing kept).

## Unsupported confirmed defects (with excerpts)

1. b7 / future_contract_unknown r3 B7. Output lists under CONFIRMED MATERIAL
   FAILURES: "Interface Handoff Failure ... may experience a catastrophic
   handoff breakdown upon next-quarter deployment if the unpublished
   next-quarter API contract introduces breaking schema, authentication, or
   protocol changes." A future speculation promoted to CONFIRMED — the exact
   failure the control was designed to catch. Judge flag correct.
2. b8 / storage_lifecycle r1 B8. Output correctly confirms the 22°C storage
   violation, but adds "Interface Handoff Breakdown ... without a quality
   verification hold or rejection gate" — a hold/rejection-gate requirement
   invented beyond the brief. Judge flag targets the invented requirement.

## Case-by-case stable results

Full per-case tables: `results_b6/b6_report.json`, `results_b7/b7_report.json`,
`results_b8/b8_report.json`. Shared anchors detected and classified correctly
by B5 and all candidates (anchor recall 1.00 everywhere, no regression).

## Counts / cost

- Evaluator outputs: 84 + 84 + 84 = 252 (1 model call each — cost gate holds).
- Primary judge judgments: 252 + 5 same-model retries (1 judge timeout, 4 empty
  judgments returned with error:null).
- All candidates: 1 evaluator call/run, chars ≤ 1.5× B5, median latency ≤ 1.5× B5.
- Total model calls: 252 evaluator + 257 judge.

## Files

- prompts: `v3/prompts/b6.md`, `b7.md`, `b8.md` (B5 + one frozen block each)
- cases: `v3/b6_cases.json`, `v3/b7_cases.json`, `v3/b8_cases.json`
- harness: `v3/run_axes.py`, `v3/judge_axes.py`, `v3/score_axes.py`
- raw: `v3/results_b6/`, `v3/results_b7/`, `v3/results_b8/` (raw_outputs.jsonl,
  raw_judgments.jsonl, *_report.json, manifest.json)
- freeze hashes: `v3/AXES_FREEZE_SHA256.txt`

## Conclusion

No axis demonstrated strictly-better coverage than B5 (ceiling: B5 was already
perfect on all 18 axis cases), and B7/B8 each added one unsupported confirmed
defect. Per instructions: no B6.1/B7.1/B8.1, no combined B9, no production
change. Stop.
