You are given an authoritative route label for this case. Obey it.

ROUTE LABEL: {{ROUTE}}

If ROUTE is TASK: treat the situation as TASK. Do not reframe into PROBLEM.
If ROUTE is PROBLEM: treat the situation as PROBLEM. Do not manufacture a full solution.

Then follow the NPA-B5 rules below exactly.

---

First identify the intended outcome.

Before solving, determine whether the supplied situation is a TASK
or a PROBLEM — but the ROUTE LABEL above is authoritative; your route
field MUST equal the ROUTE LABEL.

TASK:
The supplied model of the situation is sufficient to determine
what must be true for the intended outcome.

PROBLEM:
The requested solution depends on a materially uncertain or
inadequate model of the situation.

Missing information by itself is NOT sufficient to classify
the situation as PROBLEM. Do not search for hypothetical uncertainty.

Output strict JSON only with keys:
intended_outcome, route (TASK|PROBLEM),
supra_goal, model_gap, competing_models, probe,
success, parts, material_failures, requirements, tests, evidence_gaps,
decision_readiness (READY|NEEDS_EVIDENCE|BLOCKED).

If TASK:
The constraints already determine what must be true. Even if the only
feasible conclusion is FAIL/BLOCKED, that is still a TASK: state the
contradiction as a material failure and requirements/tests. Do NOT
reclassify a fully determined arithmetic or policy contradiction as
PROBLEM merely because a better engineering alternative can be imagined.

Run the normal B5 Requirements Finder and fill success, parts,
material_failures, requirements, tests, evidence_gaps, decision_readiness.
Set supra_goal, model_gap, competing_models, probe to null or [].

B5 rules: Before deriving requirements, identify the smallest set of
outcome-critical components, stages, or flows that produce the overall
outcome, plus the interfaces between them. For each component state its
local contribution to the overall outcome. Then derive material failure
modes, requirements and tests per component, including failures at
interfaces between components where each side is locally correct but the
handoff is broken. Decompose only until each retained component has one
coherent quality responsibility. Missing evidence is not a defect.
Do not invent facts.

If PROBLEM:
1. State the SUPRA-GOAL / intended outcome independent of the proposed solution.
2. State the minimum disputed assumption or model gap.
3. State the competing materially different models.
4. Identify the cheapest observation/test that would discriminate them.
5. Stop. Do not create downstream requirements based on an unresolved model.
   Leave success/parts/material_failures/requirements/tests empty or minimal;
   decision_readiness = NEEDS_EVIDENCE or BLOCKED as appropriate.

When new evidence is supplied in a follow-up message:
6. Update the model.
7. Reclassify TASK vs still-PROBLEM (still obey ROUTE LABEL if still given).
8. If TASK, run B5 and fill the B5 fields.
