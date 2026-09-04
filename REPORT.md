# CDE Benchmark Report — agy run

## Run integrity

- Evaluator: `agy CLI`, `gemini-3.6-flash-high`, 8 parallel subprocesses.
- Judge: `agy CLI`, `claude-sonnet-4-6`, 8 parallel subprocesses.
- 20 artifacts × 4 systems × 3 runs = **240/240** evaluator outputs.
- 20 cases × 3 paired judgments = **60/60** blind judgments; 0 judge errors.
- Gold was hidden from evaluators and frozen before the run.
- This is a synthetic benchmark. The judge is an LLM, so results are evidence, not proof.

## Primary comparison: B1 vs CDE-STANDARD

| Metric (stable case-level criterion) | B1 | CDE-STANDARD |
|---|---:|---:|
| Defect recall | 14/15 | 14/15 |
| Verdict correctness | 13/20 | 16/20 |
| Stable unsafe critical/normative ignore | 0 | 0 |
| Clean-control false rejection | 4/5 | 3/5 |
| Evaluator calls | 60 | 60 |
| Mean latency per call | 9.01 s | 18.86 s |
| Total output characters (proxy, not tokens) | 150,656 | 649,914 |

Both systems caught the same 14/15 mutated defects at the preregistered 2/3 threshold. CDE-STANDARD had three case-level verdict wins over B1 and no verdict losses in the paired judge comparison, but neither system reliably passed clean-control rejection: B1 falsely rejected 4/5 controls and CDE 3/5.

## Secondary systems

- B0: 60 outputs; heuristic pre-score only.
- CDE-LIGHT: 60 outputs; heuristic pre-score only.
- Their raw outputs are preserved, but no primary blind-judge conclusion is claimed for them.

## Scope limitation: SPEC / requirements discovery

The preregistered SPEC coverage metric was **not run**. All 240 evaluator calls were artifact audits: 20 artifacts × 4 systems × 3 runs. The separate test in which systems generate requirements before seeing artifacts was absent from the executed benchmark.

Therefore this report supports a conclusion only for **AUDIT / checking an existing object**. It does not test the original hypothesis that CDE discovers decision-changing requirements before object creation.

## F ablation and block ablation

Not run. The preregistered trigger requires a demonstrated material CDE win. Equal defect recall and poor control behavior do not satisfy that gate.

## Decision

**AUDIT: COLLAPSE TO SIMPLE PROMPT / RETAIN SELECTED MODULES.** CDE-STANDARD did not materially improve defect recall over B1. It showed a modest verdict advantage in this sample and zero stable unsafe-ignore cases, but used about 2.1× mean latency and 4.3× output characters while still falsely rejecting 3/5 controls.

**REQUIREMENTS DISCOVERY / SPEC: NOT TESTED.** No conclusion is justified about whether CDE is needed for pre-creation requirement discovery. The next decisive experiment is smaller: 5 briefs, systems generate requirements without seeing artifacts, then score coverage of 15 hidden mutations; compare B1, B1+provenance/assumptions/reference, and CDE. Do not claim that CDE v0.4 is proven or disproven for this task.

## Caveat

The current scorer’s original string heuristic is not used for this conclusion; the primary numbers above come from the 60 blinded judge records. Token usage was not exposed by the agy CLI, so output characters and latency are reported as cost proxies.
