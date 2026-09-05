# Final decision — Requirements Finder / What Matters v1

Status: **FROZEN FOR PRODUCTION**

Production implementation: `.claude/skills/requirements-finder/SKILL.md`

## Decision

Use a simple single-agent Requirements Finder based on the strongest simple B1 behavior.

Do **not** ship:
- CDE v0.4 routing/taxonomy as production core;
- B2 as production;
- B3/B3.1 confirmation-gate variants;
- mandatory relational-failure pass;
- multi-agent roles, debate, voting, or B4 DEEP lenses;
- broad subagent criticism by default.

Subagents/tools are allowed only for **targeted evidence acquisition** after the simple pass identifies one concrete decision-relevant evidence gap.

## Production model

`OUTCOME + EXPLICIT MUSTS + MATERIAL FAILURE MODES -> REQUIREMENTS -> TESTS`

Failure-first reasoning is a discovery mechanism, not a mandate to generate more suspicions.

## Empirical basis

### SPEC

Pre-artifact stable mutation coverage:
- B1: 13/15
- B1 enriched: 10/15
- CDE: 10/15

Adding structure did not improve requirement discovery.

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

Conclusion: no B3.2/B4-style prompt patching to repair the confirmation trade-off.

### B4 DEEP lenses

Branch/commit: `experiment/deep-lenses` / `ae842ecb`

25 cases, 3 runs/system:

| System | Recall | Class accuracy | Unsupported confirmed defects | Readiness | Calls |
|---|---:|---:|---:|---:|---:|
| B1 | 0.95 | 0.90 | 0.043 | 0.56 | 75 |
| B4 | 0.95 | 0.80 | 0.056 | 0.60 | 375 |

B4 used four independent discovery lenses plus a conservative synthesizer. It produced no stable recall gain, worse classification, more unsupported confirmed defects, and 5x model calls.

Conclusion: **no permanent DEEP mode**.

## What survived the research

1. Outcome first.
2. Explicit mandatory constraints matter without needing to be rediscovered.
3. Material failure modes are a useful way to discover hidden requirements.
4. A useful requirement should map to a falsifiable test/check.
5. Missing evidence is not a defect.
6. Remove criteria that do not support the outcome, satisfy an explicit must, or prevent a material failure.
7. Resolve uncertainty with narrow targeted evidence retrieval, not broad parallel criticism.

## Stop condition

The prompt/framework optimization phase is closed.

Reopen only with new held-out evidence showing a specific, repeated production failure that the current skill cannot handle—not merely because another plausible taxonomy, role, or reasoning layer can be imagined.
