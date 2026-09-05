# B5 (decomposition) preregistration — FROZEN before first evaluator run

## Motivation

Observed production gap (montaj case): the flat Requirements Finder
(OBJECT → OUTCOME → FAILURES → REQUIREMENTS → TESTS) found the inter-skill
contract but did not systematically cover per-mechanism parameters (zoom
magnitude, timing, face size, cadence). The single global outcome is too far
from concrete mechanisms on composite objects.

## Hypothesis

An in-prompt decomposition step (one model, no extra agents, no fixed
taxonomy) improves coverage on composite objects without raising false
requirements: derive outcome-critical components/stages/interfaces from the
object itself, then apply failure-first reasoning per component and at
interfaces.

This tests a different factor than B4 (which tested more independent
critics). B5 adds no suspicion pressure — only object-space coverage.

## Comparison

- **B1**: `v3/prompts/b1.md`, unchanged, single flat pass.
- **B5**: B1 base + one frozen decomposition pre-step (`v3/prompts/b5.md`).
  Same output sections as B1, so judge rubric and status parser apply unchanged.

## Frozen files

- B5 prompt: `v3/prompts/b5.md`
- cases: `v3/b5_cases.json` (10 NEW composite cases, below)
- gold: inside `b5_cases.json` (`target_finding`, `target_class`, `status`,
  `readiness`), hidden from evaluator
- v3 `cases.json` / `gold.json` unmodified

## Cases (10 composite objects)

4 interface failures (each part locally correct, handoff broken):
- `etl_interface` (sql)
- `dose_handoff` (medical)
- `edit_render_gap` (render/edit plan)
- `phase_gate` (strategy)

3 component failures inside composite objects:
- `report_chain` (summary: Recommendation section reverses source)
- `screen_decide` (naming: selection precedes required gate)
- `zoom_plan` (render plan: four levels exceed two-level maximum)

4 clean composite controls:
- `etl_clean` (sql PASS/READY)
- `dose_clean` (medical PASS/READY)
- `phases_clean` (strategy PASS/READY)
- `zoom_clean` (render plan PASS/READY)

Every failure is provable from brief + artifact alone (confirmation-gate
compatible): no external facts, no hidden sources.

## Protocol

- 10 cases × 2 systems × 3 runs = 60 jobs, randomized system order per case/run
- evaluator model/settings identical to v3.1: `gemini-3.6-flash-high` via agy
- same blind judge model/rubric as v3.1: `gemini-3.8-flash-high`
- quota/error retry with the same judge model only; evaluator status-missing
  retry per v3.1 precedent
- stable case result = ≥2/3 runs; scorer = `v3/score.py` ≥2/3 logic

## Decision rule

Adopt decomposition into the production skill ONLY if ALL hold:

1. Target Finding Recall ≥ B1
2. Finding Class Accuracy ≥ B1
3. Unsupported Confirmed Defect Rate ≤ B1
4. Readiness Calibration ≥ B1

If any fail: **B5 FAILS** — no B5.1, no patching, finding recorded, freeze stands.
A pass here is held-out evidence for reopening FINAL_DECISION, not a production change.
