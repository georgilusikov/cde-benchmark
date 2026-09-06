# NPA-1 run (agy)

cases=8 systems=['B5', 'NPA-B5'] runs=1 jobs=16

| system | route_acc | PROBLEM recall | TASK spec | PCR | URR | probe | lat med |
|---|---:|---:|---:|---:|---:|---:|---:|
| B5 | 0.5 | 0.0 | 1.0 | 1.0 | 0.0 | 0.0 | 17.022626638412476 |
| NPA-B5 | 1.0 | 1.0 | 1.0 | 0.0 | 0.0 | 1.0 | 12.164121985435486 |

## Gates (deterministic core)

- A_problem_detection: PASS — PROBLEM recall=1.0
- B_pcr_reduction: PASS — PCR 0.0 <= 0.6 (baseline 1.0)
- C_paranoia_guard: PASS — URR=0.0
- D_b5_preservation: FAIL/PENDING — requires semantic requirement recall (not in deterministic layer)
- E_hallucination: FAIL/PENDING — requires semantic unsupported rate
- F_recovery: FAIL/PENDING — requires post-probe semantic recall
- cost_latency: PASS — lat 12.164121985435486 vs 17.022626638412476
- cost_chars: PASS — chars 1967.25 vs 4313.5
- deterministic_core_pass: True
