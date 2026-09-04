# CDE benchmark v2 report — B1 vs B2

## Protocol

- 25 artifacts: 5 domains × (`CLEAN_READY`, `CLEAN_INCOMPLETE`, 3 mutations).
- 3 independent runs per system; 150 evaluator calls total.
- Evaluator: `agy CLI`, `gemini-3.6-flash-high`, 8 parallel processes.
- Judge: `agy CLI`, primarily `claude-sonnet-4-6`; 39 quota-failed judgments were retried with `gemini-3.8-flash-high`, and two timeout/empty responses were retried individually. Final judge records cover all 150 cells; 42 failed attempts are retained in raw history but are not counted as final records.
- Stable = correct in at least 2/3 runs.
- v1 remains frozen.

## Results

| Metric | B1 | B2 |
|---|---:|---:|
| Stable defect recall (15 mutations) | 9/15 | 11/15 |
| Stable false-defect controls (10 controls) | 2/10 | 4/10 |
| Stable readiness calibration (25 cases) | 11/25 | 14/25 |
| Evaluator calls | 75 | 75 |
| Mean evaluator latency | 9.46 s | 12.37 s |
| Total output characters (cost proxy) | 245,391 | 403,206 |

## Interpretation

B2 improved stable mutation recall by 2/15 and readiness calibration by 3/25, but doubled the number of controls judged as false defects (4/10 vs 2/10). It cost about 31% more latency and 64% more output characters. The result is a trade-off, not a clean win. The relational-failure pass may have helped defect recall, but this benchmark does not isolate which B2 addition caused the change.

The new two-axis verdict is more informative than v1's ACCEPT/REJECT: a no-defect case can still be `NEEDS_EVIDENCE`. The benchmark should retain this design.

## Recommendation

**B2 is the better research candidate, not a production winner.** Continue with one narrow revision: keep the relational-failure pass and explicitly distinguish demonstrated defects from evidence gaps, then rerun with a judge whose quota and output format are stable. Do not add the full CDE router/provenance taxonomy. The next gate should require B2 to retain the recall/readiness gains while reducing false-defect controls to B1 level or better.

## Limitations

Judge models changed because of quota exhaustion, and token usage was not exposed by agy; latency and characters are proxies. The final set is complete, but judge-model heterogeneity reduces confidence. No causal attribution between B2's two additions was attempted.
