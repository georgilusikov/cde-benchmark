# NPA-1 run (mock)

cases=8 systems=['B5', 'NPA-B5', 'ORACLE-NPA-B5'] runs=1 jobs=24

| system | route_acc | PROBLEM recall | TASK spec | PCR | URR | probe | lat med |
|---|---:|---:|---:|---:|---:|---:|---:|
| B5 | 0.5 | 0.0 | 1.0 | 1.0 | 0.0 | 0.0 | 9.059906005859375e-06 |
| NPA-B5 | 1.0 | 1.0 | 1.0 | 0.0 | 0.0 | 1.0 | 1.1086463928222656e-05 |
| ORACLE-NPA-B5 | 1.0 | 1.0 | 1.0 | 0.0 | 0.0 | 1.0 | 8.463859558105469e-06 |

## Gates (deterministic core)

- A_problem_detection: PASS — PROBLEM recall=1.0
- B_pcr_reduction: PASS — PCR 0.0 <= 0.6 (baseline 1.0)
- C_paranoia_guard: PASS — URR=0.0
- D_b5_preservation: FAIL/PENDING — requires semantic requirement recall (not in deterministic layer)
- E_hallucination: FAIL/PENDING — requires semantic unsupported rate
- F_recovery: FAIL/PENDING — requires post-probe semantic recall
- cost_latency: PASS — lat 1.1086463928222656e-05 vs 9.059906005859375e-06
- cost_chars: PASS — chars 609.625 vs 553.625
- deterministic_core_pass: True
