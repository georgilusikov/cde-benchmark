# NPA-1 calibration — reviewer queue

Independent reviewer: `gpt-5.6-sol`

`assistant_labels.jsonl` is **model reviewer output, not human gold**. Human labels should be entered separately in `human_labels.jsonl`.

## P0 — fix or explicitly exclude before trusting calibration

### `dev_comp_phase_gate` / packet 21
The supplied gold is not entailed by the brief at month-level resolution. Grant may occur in M7 and regulated revenue may also start later in M7. Without intra-month ordering, `revenue starts M7` does not prove revenue precedes grant. This is the same phase-gate ambiguity seen in earlier CDE work.

Recommendation: repair the case (e.g. revenue starts M7 while earliest grant is M8, or give exact dates/order) or exclude it from calibration metrics.

## P1 — define `readiness_correct` semantics once

Several outputs correctly diagnose/reject an artifact but say `decision_readiness=READY`, while gold says `BLOCKED` (examples: packets 01, 05, 16, 20, 24).

Two plausible meanings are being mixed:

- `READY` = enough evidence exists to make the decision;
- `BLOCKED` = the artifact/action must not proceed.

The current gold appears to use the second meaning. Human raters should follow one explicit definition or agreement on `readiness_correct` will measure terminology rather than reasoning.

## P1 — post-probe over-reframing

Packets 26, 27, 31, 35 are important. Oracle correctly identifies the first model gap and receives discriminating evidence, then opens a finer second `PROBLEM` instead of converting to the gold `TASK` and producing requirements.

My labels: initial `model_gap_correct=1`, `probe_discriminating=1`, but `stage2_requirement_recall=0` and `readiness_correct=0`.

These cases test the NPA stop condition, not just routing.

## P1 — calibration packets with no returned stage2 evidence

Packets 22, 23, 30, 34 contain plausible probes that appear close to the expanded aliases, yet `EVIDENCE` is `(none)`. Confirm whether the calibration packets were generated before alias expansion / evidence-routing fixes.

If so, do not interpret absence of stage2 as an agent failure.

## P2 — binary labels worth human spot-checking

- Packet 02 `B5 / support_hire`: I marked model-gap=1, probe=1, premature=1. It recognizes the right distinction but then commits to queue/dispatch fixes.
- Packet 06 `B5 / more_moderators`: model-gap=1, probe=1, premature=1. It diagnoses dedup as cause before validating why the tool is disabled.
- Packet 10 `B5 / CDN`: model-gap=1, probe=1, premature=1. It identifies the correct alternatives but treats cache/origin as already settled.
- Packet 18 `NPA / support_hire`: model-gap=1. The wording shifts to finer pre-assignment submodels, so a very strict rater could mark the gold gap mismatch as 0.

## P2 — unsupported-confirmed counts are the least reliable manual field

Highest subjectivity is in packets 00, 02, 03, 06, 08-12, 14-16, 18-19, 32. The issue is whether an implementation-specific requirement (exact latency threshold, signed token, atomic handoff, retry architecture, mandatory redaction middleware) counts as unsupported or as a legitimate derived design requirement.

Use the rubric literally: count it unsupported when the brief/evidence does not require that specific mechanism or threshold.

## Reviewer summary

The binary route/model-gap/probe/premature labels are mostly high-confidence. The main human-review risks are:

1. ambiguous `phase_gate` gold;
2. `READY` vs `BLOCKED` semantics;
3. stage2 over-reframing;
4. exact unsupported-count/rate calibration.
