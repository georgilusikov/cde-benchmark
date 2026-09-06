# NPA-1 run (agy)

cases=24 systems=['B5', 'NPA-B5', 'ORACLE-NPA-B5'] runs=1 jobs=72

| system | route_acc | PROBLEM recall | TASK spec | PCR | URR | probe | lat med |
|---|---:|---:|---:|---:|---:|---:|---:|
| B5 | 0.5 | 0.0 | 1.0 | 0.9166666666666666 | 0.0 | 0.0 | 17.71143341064453 |
| NPA-B5 | 1.0 | 1.0 | 1.0 | 0.08333333333333333 | 0.0 | 0.5833333333333334 | 10.931610465049744 |
| ORACLE-NPA-B5 | 1.0 | 1.0 | 1.0 | 0.08333333333333333 | 0.0 | 0.8333333333333334 | 9.580702900886536 |

## Gates (deterministic core)

- A_problem_detection: PASS — PROBLEM recall=1.0
- B_pcr_reduction: PASS — PCR 0.08333333333333333 <= 0.5499999999999999 (baseline 0.9166666666666666)
- C_paranoia_guard: PASS — URR=0.0
- D_b5_preservation: FAIL/PENDING — requires semantic requirement recall (not in deterministic layer)
- E_hallucination: FAIL/PENDING — requires semantic unsupported rate
- F_recovery: FAIL/PENDING — requires post-probe semantic recall
- cost_latency: PASS — lat 10.931610465049744 vs 17.71143341064453
- cost_chars: PASS — chars 2008.25 vs 3840.875
- deterministic_core_pass: True
