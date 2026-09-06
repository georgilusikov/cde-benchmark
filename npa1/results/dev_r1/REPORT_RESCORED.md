# NPA-1 dev_r1 (rescored)

24 cases × B5/NPA/Oracle × 1 run. Model gemini-3.6-flash-high. Deterministic layer only.

| system | route_acc | PROBLEM recall | TASK spec | PCR | URR | probe | lat med | chars |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| B5 | 0.500 | 0.0 | 1.0 | 0.9166666666666666 | 0.0 | 0.0 | 17.7 | 3841 |
| NPA-B5 | 1.000 | 1.0 | 1.0 | 0.0 | 0.0 | 0.6666666666666666 | 10.9 | 2008 |
| ORACLE-NPA-B5 | 1.000 | 1.0 | 1.0 | 0.0 | 0.0 | 0.8333333333333334 | 9.6 | 1746 |

## Gates

- A_problem_detection: PASS — PROBLEM recall=1.0
- B_pcr_reduction: PASS — PCR 0.0 <= 0.5499999999999999 (baseline 0.9166666666666666)
- C_paranoia_guard: PASS — URR=0.0
- D_b5_preservation: FAIL/PENDING — requires semantic requirement recall (not in deterministic layer)
- E_hallucination: FAIL/PENDING — requires semantic unsupported rate
- F_recovery: FAIL/PENDING — requires post-probe semantic recall
- cost_latency: PASS — lat 10.931610465049744 vs 17.71143341064453
- cost_chars: PASS — chars 2008.25 vs 3840.875
- deterministic_core_pass: True

## Notes
- Semantic gates D/E/F still pending (requirement recall judge not wired).
- Probe match  is deterministic alias overlap; remaining misses need alias expansion or judge.
- Single-run dev; for stable metrics re-run with --runs 3 before prompt freeze.
