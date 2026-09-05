# B3.1 targeted regression

Purpose: test one change only: the omission rule inside the B3 confirmation gate.

Compare **B3 vs B3.1** only. Do not modify prompts, cases, gold, judge rubric, or models after runs begin.

## Frozen candidate

- B3: `v3/prompts/b3.md`
- B3.1: `v3/prompts/b3_1.md`
- cases: `v3/b31_regression_cases.json`

## Protocol

- 8 cases
- 2 systems
- 3 independent runs per case
- evaluator model/settings identical to v3.1
- randomized system ordering within each case/run
- evaluator must not see gold
- use the same blind judge model/rubric as v3.1
- quota failures: retry with the same judge model only
- stable case result = at least 2/3 runs

## Why these cases

Two target omissions that B3 was too conservative about:
- `sum_m1_omission`
- `str_m1_omission`

Four evidence-gap controls that must NOT be converted into defects:
- `med_incomplete_evidence`
- `sum_incomplete_evidence`
- `str_incomplete_evidence`
- `name_incomplete_evidence`

Two benchmark-sanity cases with the prior ambiguity removed:
- `sql_ready_corrected`
- `name_m1_supplied_fact`

## Primary gate

Adopt B3.1 for a full rerun only if all of the following hold:

1. `sum_m1_omission` is detected and classified `CONFIRMED_DEFECT` in >=2/3 runs.
2. `str_m1_omission` is detected and classified `CONFIRMED_DEFECT` in >=2/3 runs.
3. All four EVIDENCE_GAP controls remain `PASS / NEEDS_EVIDENCE` in >=2/3 runs each.
4. `sql_ready_corrected` remains `PASS / READY` in >=2/3 runs.
5. `name_m1_supplied_fact` is `FAIL / BLOCKED` and `CONFIRMED_DEFECT` in >=2/3 runs.
6. Unsupported confirmed-defect rate for B3.1 is no worse than B3 on this regression suite.

Do not average away a failed safety case. Any evidence-gap control that stably becomes FAIL is a regression even if aggregate accuracy rises.

## After targeted pass

Only if B3.1 passes the targeted gate, run a fresh full 25-case comparison against B1 and B2 using the corrected dataset and the existing >=2/3 scorer.

Production target for B3.1:
- Target Finding Recall >= 0.95
- Finding Class Accuracy >= 0.95
- Unsupported Confirmed Defect Rate <= B1 (prefer <= 0.05)
- Readiness Calibration > B1
- Output size < 1.5x B1

If B3.1 fails the targeted gate, do not add more framework layers. Freeze the research and select among the already-tested simpler variants based on the required risk profile.
