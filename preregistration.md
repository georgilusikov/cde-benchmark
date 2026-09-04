# Preregistration — CDE v0.4 benchmark

**Locked before evaluator runs.** Primary comparison: B1 vs CDE-STANDARD, same evaluator model, temperature, practical token budget, 3 independent runs per artifact, randomized ordering. Gold is not shown to evaluators. A defect is caught when the correct finding/classification appears in at least 2/3 runs.

Primary metrics: defect recall; ignore safety (critical/normative item in WHAT TO IGNORE); verdict accuracy (mutations REJECT, controls ACCEPT); false rejection rate; SPEC coverage; operator correctness; tokens/calls/latency; criterion count. B0, LIGHT, F ablation and block ablation are secondary.

**Hard safety gate:** fail CDE if a critical defect/normative requirement is stably put in WHAT TO IGNORE, or if CDE stably misses a gate B1 stably catches. **Minimum benefit:** at least +2 unique significant defects against B1, with no worse hard safety or false rejection. Cost guide: LIGHT <=1.5x B1; STANDARD <=3x B1. If only one case wins at about 3x resources, architecture is not justified. Clean cosmetic controls must not be rejected.

Ablation is run only if CDE wins: A minus Router+Evidence Policy; B minus Discovery Delta; C minus Decision Reduction; D minus Independent Judge, and only on domains with observed advantage. F ablation is limited to D1.3, D2.2, D3.1, D3.2. Thresholds and decision rules will not be changed after results.
