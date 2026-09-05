# Final decision — Requirements Finder / What Matters v1.1

Status: **FROZEN FOR PRODUCTION, AMENDED BY HELD-OUT B5 EVIDENCE**

Production implementation lives in a separate project/repository: `requirements-finder` (standalone skill). This benchmark repository contains only research history, cases, results, and the decision record.

## Decision

Use a **single-agent Requirements Finder with conditional minimal decomposition**:

- for simple/atomic objects, keep the flat B1-style pass;
- for structurally composite objects (multiple outcome-critical components, stages, flows, sections, or handoffs), first identify the smallest set of outcome-critical parts and interfaces, state each part's local contribution, then derive failures → requirements → tests per part and at interfaces;
- decompose only until each retained part has one coherent quality responsibility; do not split further unless the distinction changes a material failure or test.

Do **not** ship:
- CDE v0.4 routing/taxonomy as production core;
- B2 as production;
- B3/B3.1 confirmation-gate variants;
- mandatory fixed relational-failure taxonomy;
- multi-agent roles, debate, voting, or B4 DEEP lenses;
- broad subagent criticism by default.

Subagents/tools are allowed only for **targeted evidence acquisition** after the single-agent pass identifies one concrete decision-relevant evidence gap.

## Production model

For atomic/simple objects:

`OUTCOME + EXPLICIT MUSTS + MATERIAL FAILURE MODES -> REQUIREMENTS -> TESTS`

For composite objects:

`OUTCOME -> OUTCOME-CRITICAL PARTS / STAGES / FLOWS + INTERFACES -> LOCAL OUTCOMES -> MATERIAL FAILURES -> REQUIREMENTS -> TESTS -> FINAL WHAT-MATTERS SET`

Failure-first reasoning is a discovery mechanism, not a mandate to generate more suspicions.

The decomposition is derived from the object itself, not from a fixed checklist of legal / UX / risk / timing / lifecycle categories.

## Empirical basis

### SPEC

Pre-artifact stable mutation coverage:
- B1: 13/15
- B1 enriched: 10/15
- CDE: 10/15

Adding generic structure did not improve requirement discovery.

### v3.1 audit benchmark

25 cases, 3 runs/system:

| System | Recall | Class accuracy | Unsupported confirmed defects | Readiness | Output chars | Median latency |
|---|---:|---:|---:|---:|---:|---:|
| B1 | 0.95 | 0.95 | 0.081 | 0.52 | 48,855 | 8.90 s |
| B2 | 1.00 | 1.00 | 0.123 | 0.56 | 91,727 | 11.58 s |
| B3 | 0.90 | 0.80 | 0.028 | 0.68 | 56,692 | 9.77 s |

B2 improved coverage/classification but increased unsupported confirmed defects and verbosity. B3 reduced false confirmation but lost real findings.

### B3.1 targeted regression

Branch/commit: `experiment/b3-1-omission-gate` / `320e1965`

B3.1 failed its preregistered gate:
- no improvement over B3 on target omissions;
- readiness regression on a clean SQL control;
- supplied naming defect still treated as evidence gap.

Conclusion: no B3.2-style confirmation prompt patching.

### B4 DEEP lenses

Branch/commit: `experiment/deep-lenses` / `ae842ecb`

25 cases, 3 runs/system:

| System | Recall | Class accuracy | Unsupported confirmed defects | Readiness | Calls |
|---|---:|---:|---:|---:|---:|
| B1 | 0.95 | 0.90 | 0.043 | 0.56 | 75 |
| B4 | 0.95 | 0.80 | 0.056 | 0.60 | 375 |

B4 used four independent discovery lenses plus a conservative synthesizer. It produced no stable recall gain, worse classification, more unsupported confirmed defects, and 5x model calls.

Conclusion: **no permanent DEEP / multi-agent discovery mode**.

### B5 composite decomposition

Branch/commit: `experiment/decomp-b5` / `ae412003`

Frozen experiment: 10 new composite cases, B1 vs B5, 3 runs/system, same evaluator/judge and stable >=2/3 scoring.

| System | Recall | Class accuracy | Unsupported confirmed defects | Readiness | Output chars | Median latency |
|---|---:|---:|---:|---:|---:|---:|
| B1 | 0.57 | 0.57 | 0.148 | 0.50 | 19,719 | 9.08 s |
| B5 | 0.86 | 0.86 | 0.138 | 0.50 | 46,241 | 13.88 s |

B5 passed all four preregistered adoption conditions. It recovered two predicted composite/interface misses (`dose_handoff`, `edit_render_gap`) without introducing a new stable false positive on the clean composite controls in the frozen dataset. Cost was ~2.3x output and ~1.5x latency, still one model call and no subagents.

Important audit notes:
- preregistration text contains an arithmetic/documentation typo: it says 10 cases but lists 4 interface + 3 component + 4 clean; the frozen dataset actually contains 10 cases = 7 defect + 3 clean (no `zoom_clean`);
- `phase_gate` gold is not a sound confirmed defect as written: the brief permits licence grant in M7 and the artifact starts revenue in M7, so ordering within the month is not proven. Both B1 and B5 missed it, so it does not create the comparative B5 gain. Excluding that ambiguous case, B5 detects all 6 valid planted defect targets while B1 detects 4/6.

Conclusion: B5 is held-out evidence that **object-space decomposition is useful on composite objects**, unlike generic taxonomy expansion or multi-agent criticism.

## What survived the research

1. Outcome first.
2. Explicit mandatory constraints matter without needing to be rediscovered.
3. For composite objects, identify the smallest set of outcome-critical components/stages/flows and their interfaces before deriving requirements.
4. Give each retained component one coherent local quality responsibility; stop decomposing when further splitting would not change a material failure or test.
5. Material failure modes are a useful way to discover hidden requirements.
6. A useful requirement should map to a falsifiable test/check.
7. Check interface failures where components can be locally correct but the handoff is wrong.
8. Missing evidence is not a defect.
9. Remove criteria that do not support the outcome, satisfy an explicit must, or prevent a material failure.
10. Resolve uncertainty with narrow targeted evidence retrieval, not broad parallel criticism.

## Production routing rule

Use decomposition only when the supplied object is structurally composite: multiple stages/components/sections/flows contribute different responsibilities or one part's output becomes another part's input.

Otherwise use the flat pass.

This is a complexity gate, not a taxonomy router.

## Stop condition

The prompt/framework optimization phase is closed again after adopting this single held-out structural correction.

Reopen only with new held-out evidence showing a specific, repeated production failure that the current conditional-decomposition skill cannot handle—not merely because another plausible taxonomy, role, or reasoning layer can be imagined.
