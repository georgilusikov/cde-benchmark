# NPA-1 — Non-Projective Problem/Task Router Benchmark

**Status:** PREREGISTERED design (no evaluator runs yet)  
**Relation to production:** SEPARATE experiment. Does **not** modify frozen Requirements Finder / B5 production.  
**Parent discipline:** `cde-benchmark/FINAL_DECISION.md` stop condition — reopen production only after held-out evidence of a specific repeated miss, not theoretical attractiveness.

## 0. Goal

Test one atomic hypothesis from the non-projective activity organization framing (Arkhangelsky):

> Before building a solution, an agent should determine whether the supplied situation is a **TASK** (model adequate) or a **PROBLEM** (model inadequate) — and if PROBLEM, reframe to supra-goal + discriminating probe instead of manufacturing requirements inside the wrong model.

**Not in scope for NPA-1:** full TRIZ, IKR/IFR, weak signals, chaos, conditions→effects, multi-lens critics.

## 1. Systems

| Arm | Role | Prompt |
|---|---|---|
| **B5** | Baseline | Frozen copy of `cde-benchmark/v3/prompts/b5.md` (byte-identical at freeze) |
| **NPA-B5** | Candidate | Adequacy gate wrapper → TASK runs B5; PROBLEM stops at probe |
| **ORACLE-NPA-B5** | Dev ablation only | Same as NPA-B5 but gold route injected (`This case is TASK|PROBLEM`) |

Oracle never enters held-out adoption decision and never ships.

## 2. NPA-B5 v0.1 behavior (frozen text lives in `prompts/npa_b5.md`)

1. State INTENDED OUTCOME.  
2. ADEQUACY GATE → TASK | PROBLEM.  
3. Mark PROBLEM **only if** supplied facts create: incompatible plausible explanations with different actions; unsupported/contradicted premise the requested solution depends on; or inability to define success without choosing between materially different models.  
4. **Guard:** absence of information alone ≠ PROBLEM. Do not hunt for hypothetical uncertainty.  
5. If TASK → run B5 unchanged.  
6. If PROBLEM → SUPRA-GOAL; minimum disputed assumption; competing models; cheapest discriminating probe; **STOP** (no downstream requirements).  
7. After probe evidence → update model → reclassify → if TASK, B5.

## 3. Hypotheses

- **H1 Routing:** NPA distinguishes TASK vs PROBLEM better than B5 (B5 effectively always “solves”).  
- **H2 Premature commitment:** On PROBLEM, NPA commits to model-dependent solutions less often than B5.  
- **H3 Probe quality:** NPA probes discriminate competing models (not generic “research more”).  
- **H4 Recovery:** After evidence, PROBLEM → TASK → B5 recovers requirements.  
- **H5 No regression:** On CLEAR/COMPOSITE tasks, NPA does not become a perpetual researcher and does not worsen B5 metrics beyond gate limits.

## 4. Phases

### Phase 0 — Infrastructure smoke (not evidence)
8 technical cases. Goals: JSON parse, multi-turn probe harness, gold never to evaluator, randomized system order, deterministic scorer path. Mock/API allowed.

### Phase 1 — Development
24 cases: 6 × CLEAR_TASK, COMPOSITE_TASK, MODEL_MISMATCH, UNDERDETERMINED_PROBLEM.  
Systems: B5, NPA-B5, ORACLE-NPA-B5.  
Prompt may change **only** on dev. No held-out peek.

### Phase 2 — Frozen held-out
60 **new** cases (15 each class). Systems: **B5 vs NPA-B5 only**.  
After freeze of prompts + cases + gold + thresholds: **no prompt/threshold edits**.

### Phase 3 — Adversarial extension (post-decision, not for adoption)
10 cases with confident false user framing. Logged separately; not used to tune NPA-1.

## 5. Domains (held-out ~10 each)

software/API; distributed/data systems; UX/product flows; business operations; logistics/processes; project/workflow architecture.

**Out:** aesthetics, state strategy, psychology, subjective creativity, moral dilemmas.

## 6. Case classes

| Class | Gold route | Intent |
|---|---|---|
| CLEAR_TASK | TASK | Enough info; unnecessary probe = fail |
| COMPOSITE_TASK | TASK | B5-style decomposition still required; no route regression |
| MODEL_MISMATCH | PROBLEM | Requested solution premise unsupported/contradicted |
| UNDERDETERMINED_PROBLEM | PROBLEM → (post-probe) TASK | ≥2 models fit facts; one fact discriminates |

### PROBLEM multi-turn
- **Turn 1:** route PROBLEM + supra_goal + model_gap + competing_models + probe; stop.  
- **Harness:** match probe to `acceptable_probes[]`; return pre-registered `evidence_returned`.  
- **Turn 2:** update → TASK/still-PROBLEM → if TASK, B5 sections.

### PROBLEM inclusion criteria (all required)
≥2 models consistent with **all** stage-1 facts; materially different actions; no hidden fact making one model obvious; cheap discriminating observation exists; post-test evidence suffices; gold independent of special judge knowledge. Fail any → drop case.

### TASK control criteria
May include irrelevant unknowns, extra stakeholders, future uncertainties — must **not** change the correct current decision. Measures resistance to turning every unknown into PROBLEM.

## 7. Gold schema (fields required before any evaluator run)

```yaml
id: npa_sw_001
domain: software
class: CLEAR_TASK|COMPOSITE_TASK|MODEL_MISMATCH|UNDERDETERMINED_PROBLEM
brief_stage1: |
intended_outcome:
gold_route_stage1: TASK|PROBLEM
supra_goal:            # PROBLEM
material_model_gap:    # PROBLEM
valid_models: []       # PROBLEM
why_models_are_both_possible:
acceptable_probes: []  # id, description, aliases, evidence_returned
forbidden_premature_commitments: []
unnecessary_probe: true|false   # TASK: true → penalty if agent probes
stage2_gold_route: TASK|PROBLEM|null
stage2_material_failures: []
stage2_requirements: []
stage2_tests: []
false_positive_traps: []
notes_for_judge:
```

Authoring: brief → gold → independent review (brief+gold only) → deterministic asserts for timing/numeric → freeze.

## 8. Evaluator output (strict JSON)

```json
{
  "intended_outcome": "",
  "route": "TASK|PROBLEM",
  "supra_goal": null,
  "model_gap": null,
  "competing_models": [],
  "probe": null,
  "success": "",
  "parts": [],
  "material_failures": [],
  "requirements": [],
  "tests": [],
  "evidence_gaps": [],
  "decision_readiness": "READY|NEEDS_EVIDENCE|BLOCKED"
}
```

Free-form prose is not the primary scored artifact.

## 9. Protocol

- 3 independent runs per system × case.  
- Same evaluator model/settings for all arms in a frozen run.  
- Randomize system order per case/run.  
- Gold never sent to evaluator.  
- Judge: one fixed model for whole frozen run; same-model retry only; no mid-run judge swap.  
- Stable = ≥2/3 runs (report both raw run-level and stable case-level).

### Call budget (held-out, order-of-magnitude)
- TASK 30 × 2 × 3 = 180 evaluator calls  
- PROBLEM 30 × 2 × 3 × 2 turns = 360  
- Total ~540 evaluator + ~360 judge transcripts  

## 10. Metrics

### Level 1 — deterministic (primary reliability)
JSON valid; route exact match; stop/no-B5-on-PROBLEM; presence of B5 block on TASK; stage2 transition; latency; chars/tokens; tool calls.

### Level 2 — semantic judge (blind)
Blind inputs: BRIEF + GOLD + AGENT OUTPUT only. No system name, run id, or aggregates. Randomized order.

Semantic only where needed: model-gap match; competing-model coverage; probe discrimination; premature commitment; post-probe requirement recall / unsupported requirements / readiness (B5-style).

### Named metrics
| ID | Metric | Notes |
|---|---|---|
| M1 | Route accuracy | Overall + TASK specificity + PROBLEM recall |
| M2 | **Premature Commitment Rate (PCR)** | PROBLEM runs with model-dependent commit before resolve |
| M3 | Unnecessary Reframe Rate (URR) | TASK runs that stop for needless investigation |
| M4 | Probe discrimination accuracy | Probe separates material models |
| M5 | Model-gap accuracy | Named real gap, not generic uncertainty |
| M6 | Post-probe requirement recall | After stage2 evidence |
| M7 | Unsupported requirements rate | Especially post-NPA |
| M8 | Readiness calibration | READY / NEEDS_EVIDENCE / BLOCKED |
| M9 | Cost | latency, tokens/chars, tools |

### Primary endpoint (locked)
**Premature Commitment Rate on frozen PROBLEM cases.**

Secondary (order locked): PROBLEM route recall → TASK route specificity → probe discrimination → post-probe requirement recall → unsupported → readiness → cost.

## 11. Adoption gate (ALL must pass; thresholds frozen before first held-out evaluator call)

| Gate | Rule |
|---|---|
| A Problem detection | stable PROBLEM route recall ≥ 0.80 |
| B Main benefit | PCR_NPA ≤ 0.60 × PCR_B5 (≥40% relative PCR reduction) |
| C Paranoia guard | URR ≤ 0.10 |
| D B5 preservation | on CLEAR+COMPOSITE, requirement recall regression ≤ 5 pp vs B5 |
| E Hallucination | unsupported confirmed requirements ≤ B5 + 2 pp |
| F Recovery | post-probe requirement recall ≥ B5 − 5 pp |
| Cost | median latency ≤ 1.5× B5; output tokens ≤ 1.7× B5 |

### Not a win
Smarter prose without metric gain; more NEEDS_EVIDENCE “caution”; more unsupported risks; 3× verbosity without gain; single-domain-only lift; judge-model-specific lift that fails spot-check.

## 12. Post-result policy

| Outcome | Action |
|---|---|
| NPA fails gates | Keep B5; close NPA-1; no production change |
| Oracle wins, NPA loses | Idea OK, router bad → routing-only follow-up |
| NPA wins but URR high | Gate too sensitive → no ship |
| NPA passes all gates | Production canary 100 real tasks (log route, override, probe usefulness, framing errors, latency); no algorithm change during canary |

Miss taxonomy (for next study, not for immediate patching):  
ROUTER_FALSE_TASK, ROUTER_FALSE_PROBLEM, WRONG_SUPRAGOAL, WRONG_MODEL_GAP, NON_DISCRIMINATING_PROBE, PREMATURE_COMMITMENT, FAILED_MODEL_UPDATE, B5_DOWNSTREAM_MISS, UNSUPPORTED_REQUIREMENT.

## 13. Work order (locked)

1. Freeze hypothesis (this file)  
2. `prompts/npa_b5.md` + B5 copy + oracle + judge  
3. Output JSON schema + gold schema  
4. 8 smoke cases + runner + two-turn probe harness  
5. Deterministic scorer  
6. Semantic judge  
7. 24 dev cases + independent gold review  
8. Dev runs B5 / NPA / Oracle; tune NPA **only** on dev  
9. Freeze final NPA prompt SHA  
10. 60 held-out cases + independent gold audit  
11. Freeze commit/hash (prompts, cases, gold, gates)  
12. Held-out B5 vs NPA × 3 runs  
13. Blind judge  
14. Auto report + apply **only** preregistered gates  
15. Pass → canary / Fail → leave B5  

## 14. Explicit non-claims

- NPA-1 does **not** reopen `FINAL_DECISION` by itself.  
- Passing synthetic gates is necessary but not sufficient for production merge; canary required.  
- Hypothesis is exploratory transfer from the article until a measured production framing-miss corpus exists; synthetic PROBLEM cases operationalize the miss type for controlled measurement.

## 15. Freeze checklist (fill at freeze time)

- [ ] `prompts/b5.md` SHA256 =  
- [ ] `prompts/npa_b5.md` SHA256 =  
- [ ] `dev/cases.json` + gold SHA256 =  
- [ ] `heldout/cases.json` + gold SHA256 =  
- [ ] evaluator model id =  
- [ ] judge model id =  
- [ ] gate thresholds unchanged from §11  
- [ ] git commit =  

---
**Confidence note:** Design isolates one operator and inherits CDE anti-expansion discipline (pair-first, stable ≥2/3, no post-hoc threshold edits, paranoia guard).  
**Source tags:** [O] CDE freeze/B5/B10 history; [S] article TASK/PROBLEM / AA→A→K framing; [I] NPA as separate experiment is the correct next step under current stop rule.
