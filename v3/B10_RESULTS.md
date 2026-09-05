# B10 value-decomposition — results

## Verdict

**B10 VALUE DECOMPOSITION FAILS**

## Phase A (development discrimination)

- Set 1 (`b10_dev_cases.json`): B5 stable recall 4/4 → gate FAIL, too easy.
- Set 2 (`b10_dev2_cases.json`): B5 stable recall 4/4 → gate FAIL, too easy.
- Set 3 (`b10_dev3_cases.json`): B5 stable recall 3/4 (missed `devc3_token_chain`
  stably) → gate PASS. B10 prompt never tuned on any dev results.
- Held-out built only after set-3 PASS, with new сюжеты (no literal reuse).

## Held-out protocol

18 cases (8 VALUE_DEFECT + 4 anchors + 3 clean READY + 3 evidence-gap) ×
B5/B10 × 3 runs = 108 evaluator outputs. Evaluator `gemini-3.6-flash-high`,
judge `gemini-3.8-flash-high` with extended NC-classification rubric, gold
hidden, stable ≥ 2/3, same-model retry only. Freeze hashes
(`v3/B10_FREEZE_SHA256.txt`) verified OK after runs.

Verification: 108/108 outputs, 108/108 judgments, 0 evaluator errors,
0 judge errors after retry (3 empty judgments with error:null retried with
the same model), 0 unparseable, 0 missing status.

## Aggregate table

| system | recall | value recall | anchor recall | class | value class | unsup | NC rate | readiness | chars | latency med/p95 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| B5 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.148 | 0.815 | 0.22 | 89438 | 12.02 / 14.72 s |
| B10 | 0.93 | 1.00 | 1.00 | 0.93 | 1.00 | 0.148 | 0.556 | 0.28 | 94551 | 12.17 / 15.42 s |

## Gate evaluation

- VALUE-CROSSCUT recall B10 > B5 strictly → 1.00 vs 1.00 — FAIL (ceiling: B5
  solved all 8 value defects; dev-3 discrimination did not transfer).
- Overall recall ≥ B5 → 0.93 < 1.00 — FAIL (B10 missed gap finding `g01`).
- Anchor recall ≥ B5 → 1.00 = 1.00 — PASS.
- Overall class ≥ B5 → 0.93 < 1.00 — FAIL.
- Value class ≥ B5 — PASS (equal).
- Unsup confirmed ≤ B5 → 0.148 = 0.148 — PASS (equal, but both high — see below).
- NC rate ≤ B5 — PASS numerically, metric UNRELIABLE (see below).
- ZERO false FAIL on clean READY → B10 stable FAIL/BLOCKED on `c03` — FAIL.
- ZERO READY→NEEDS_EVIDENCE regression — PASS (no new; both systems already
  miscalibrate c01/c02 to NEEDS_EVIDENCE).
- Gaps stay PASS non-FAIL — PASS.
- Readiness ≥ B5 — PASS (0.28 ≥ 0.22; both weak — shared FAIL→READY bias).
- Cost: 1 call/run — PASS; chars 1.06× — PASS; latency med 1.01× — PASS.

## Diagnostic: B5-miss → B10-hit

None. There is no case B5 missed that B10 hit. The §14 causal-delta test
finds zero evidence for the hypothesis on this suite.

## False FAIL exhibit (c03, clean READY → B10 FAIL/BLOCKED)

B10 output lists as CONFIRMED: "Omission of Writer Payload Compatibility
Invariant" (artifact "omits the explicit operational requirement") and
"Ambiguous Reader-Writer Handoff Synchronization" ("lacks an explicit 100%
rollout completion gate"). Both satisfied requirements re-read as defective
for not being stated strictly enough. The value-necessity step amplified
suspicion instead of coverage.

## Metric caveat: NC rate is miscalibrated

The extended judge sets `unsupported_necessary_condition=true` nearly
everywhere — including B5 flat outputs with no NC section, anchors, gaps,
and clean controls (B5 NC rate 0.81). The rubric as written cannot
distinguish invented conditions from judge-invented attributions. The
numerical NC-gate PASS carries no evidential weight. Do not reuse this
rubric without a rewrite and a calibration set.

## Shared weaknesses (not B10-caused)

Both systems: FAIL→READY readiness bias (calibration 0.22/0.28), elevated
unsupported-confirmed flags on freshness/anonymization cases (v05/v07/v08),
READY→NEEDS_EVIDENCE downgrade on clean c01/c02.

## Conclusion

Per spec: result recorded, production unchanged, STOP. No B10.1, no B11/B12.

Honest summary: value decomposition added suspicion (false FAIL on a clean
control, missed gap finding) and zero coverage. The dev-3 gate success did
not predict held-out success — the held-out value cases were easier than
dev-3's hardest, and B5's ceiling left no room for a strict win.
