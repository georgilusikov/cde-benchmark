# NPA-1 run (agy)

cases=8 systems=['B5', 'NPA-B5'] runs=1 jobs=16

| system | route_acc | PROBLEM recall | TASK spec | PCR | URR | probe | lat med |
|---|---:|---:|---:|---:|---:|---:|---:|
| B5 | 0.5 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 17.34267246723175 |
| NPA-B5 | 0.875 | 1.0 | 0.75 | 0.0 | 0.25 | 1.0 | 12.354955315589905 |

## Gates (deterministic core)

- A_problem_detection: PASS — PROBLEM recall=1.0
- B_pcr_reduction: PASS — PCR 0.0 <= 0.0 (baseline 0.0)
- C_paranoia_guard: FAIL/PENDING — URR=0.25
- D_b5_preservation: FAIL/PENDING — requires semantic requirement recall (not in deterministic layer)
- E_hallucination: FAIL/PENDING — requires semantic unsupported rate
- F_recovery: FAIL/PENDING — requires post-probe semantic recall
- cost_latency: PASS — lat 12.354955315589905 vs 17.34267246723175
- cost_chars: PASS — chars 2288.5 vs 4560.0
- deterministic_core_pass: False
