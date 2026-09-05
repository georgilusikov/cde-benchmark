# CDE benchmark v3.1 results

Dataset: 25 cases (10 controls + 15 single-failure mutations), 3 systems × 3 runs = 225 outputs.
Judge errors after retry: 0. Status missing after two B2 retries: 0.

## Scoreboard

| System | Target Finding Recall | Finding Class Accuracy | Unsupported Confirmed Defect Rate | Readiness Calibration | Output chars | Latency median / p95 |
|---|---:|---:|---:|---:|---:|---|
| B1 | 0.95 | 0.95 | 0.081 | 0.52 | 48855 | 8.90 / 17.23 s |
| B2 | 1.00 | 1.00 | 0.123 | 0.56 | 91727 | 11.58 / 15.94 s |
| B3 | 0.90 | 0.80 | 0.028 | 0.68 | 56692 | 9.77 / 20.27 s |

## Preregistered B3 gate

B3 passes only if:

- recall ≥ B2 → 0.90 ≥ 1.00? no
- class accuracy > B2 → 0.80 > 1.00? no
- unsupported confirmed defects ≤ B1 → 0.028 ≤ 0.081? yes
- readiness ≥ B2 → 0.68 ≥ 0.56? yes
- output size < B2 → 56692 < 91727? yes

Verdict: B3 does not pass the preregistered gate.

## Fixes applied in v3.1

1. Scorer now uses ≥2/3 for target detection and class correctness.
2. Latency median and p95 are reported.
3. `med_m1` is a real frequency conflict instead of an ambiguous unit conversion.
4. `med_m2` explicitly states that the artifact is the complete patient instruction.
5. `name_m1` supplies an explicit linguistic screen fact instead of relying on external knowledge.
