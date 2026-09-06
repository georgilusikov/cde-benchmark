# Model A/B — B5 suite (B1 vs B5 × 3.6 vs 3.8 Flash High)

**Scope:** frozen `b5_cases.json` (10), prompts B1/B5 unchanged. Evaluator arms: `gemini-3.6-flash-high` vs `gemini-3.8-flash-high` via agy. Judge fixed: `gemini-3.8-flash-high`. Runs: 3. Stable ≥2/3. Gold hidden.

**Not production change.** Separate from NPA-1. Results in `results_model_ab/`.

## Aggregate

| model | system | recall | class | unsup | readiness | chars | lat med/p95 |
|---|---|---:|---:|---:|---:|---:|---:|
| gemini-3.6-flash-high | B1 | 0.71 | 0.71 | 0.103 | 0.40 | 19410 | 8.29 / 10.92 |
| gemini-3.6-flash-high | B5 | 0.71 | 0.71 | 0.115 | 0.40 | 46623 | 12.24 / 17.81 |
| gemini-3.8-flash-high | B1 | 0.57 | 0.57 | 0.069 | 0.50 | 20570 | 11.79 / 17.79 |
| gemini-3.8-flash-high | B5 | 0.86 | 0.86 | 0.250 | 0.30 | 57518 | 32.64 / 79.56 |

## Paired deltas (3.8 − 3.6)

- **B1**: recall -0.14, class -0.14, unsup -0.034, readiness +0.10, chars×1.06
- **B5**: recall +0.14, class +0.14, unsup +0.135, readiness -0.10, chars×1.23

## Detection flips (stable)

- B5_36miss_38hit: ['dose_handoff']
- B5_36hit_38miss: —
- B1_36miss_38hit: —
- B1_36hit_38miss: ['dose_handoff']

## False FAIL on clean controls

- gemini-3.8-flash-high / B5 / `phases_clean` → FAIL/READY

## Verdict

### vs historical B5 held-out (3.6 eval, 3.8 judge)
- Historical B5: recall 0.86, class 0.86, unsup 0.138, readiness 0.50
- This rerun 3.6 B5: recall **0.71**, class 0.71, unsup 0.115, readiness 0.40 — **lower recall than published B5** (dose_handoff miss on 3.6 this time).
- This rerun 3.8 B5: recall **0.86**, class 0.86, unsup **0.250**, readiness 0.30 — recall matches historical B5; **unsupported up**; readiness worse; **false FAIL on `phases_clean`**.

### Model comparison (this run)
- **B5 recall:** 3.8 > 3.6 (+0.14) via `dose_handoff` flip 36miss→38hit.
- **B1 recall:** 3.8 < 3.6 (−0.14) via `dose_handoff` flip 36hit→38miss — same case, opposite direction: decomposition interacts with model.
- **Cost:** 3.8 B5 ~1.23× chars vs 3.6 B5; latency med ~similar order (see table).
- **Safety:** 3.8 B5 raises unsupported confirmed rate (+0.135) and produces a clean-control false FAIL — same failure mode family as B10 suspicion expansion.

### Recommendation
- **Do not switch production evaluator default to 3.8 solely on recall.** B5@3.8 recovers interface hit but buys false FAIL + higher unsup.
- **Keep published B5 numbers as historical**; this is a fresh model A/B, not a reopening of B5 prereg.
- If bulk cost matters, 3.6 remains acceptable for mass runs; use 3.8 only where interface sensitivity is worth the paranoia risk, with clean-control monitoring.
- NPA-1 stays separate; this model A/B does not change NPA gates.

## Errors

- gemini-3.6-flash-high: eval_err=0 judge_err=0 status_missing=0
- gemini-3.8-flash-high: eval_err=0 judge_err=0 status_missing=0
