# B10 value-decomposition preregistration — FROZEN

## Research question

Does decomposing the OUTCOME into necessary conditions (before B5 object
decomposition) improve coverage of cross-cutting value failures?

Tests ONE variable: OUTCOME → NECESSARY CONDITIONS → B5 decomposition →
failures → requirements → tests. NOT stakeholder/system/temporal lenses,
subagents, TOC-as-whole, Five Focusing Steps, or any other addition.

## Files

- B10 prompt: `v3/prompts/b10.md` (= frozen B5 + one VALUE NECESSITY CHECK block)
- Phase A dev cases: `v3/b10_dev_cases.json` (6 cases, §6 of task spec)
- Held-out cases: `v3/b10_cases.json` (18 cases, ONLY if Phase A passes)
- This preregistration: `v3/B10_PREREGISTRATION.md`

## Phase A gate

B5 only, 6 cases × 3 runs. PASS iff B5 stable recall on the 4 defect cases
is in [0.25, 0.75]. Otherwise rebuild the dev set; never run held-out on a
failed gate; never tune the B10 prompt on dev results.

## Held-out design (18 cases: 8 value-crosscut defects, 4 B5 anchors,
3 clean READY, 3 evidence-gap) and full B10 gate

Per task spec §§9–13: VALUE-CROSSCUT recall B10 > B5 strictly, overall recall
≥ B5, anchors ≥ B5, overall + value class ≥ B5, both unsupported rates ≤ B5,
zero false FAIL / zero READY→NEEDS_EVIDENCE regression on clean READY,
gaps stay PASS non-FAIL, readiness ≥ B5, 1 call/run, chars ≤ 1.75× B5,
median latency ≤ 1.5× B5.

Models: evaluator `gemini-3.6-flash-high`, judge `gemini-3.8-flash-high`;
no silent substitution — STOP and report if unavailable. Stable ≥ 2/3.
SHA256 freeze before first held-out evaluator call.
