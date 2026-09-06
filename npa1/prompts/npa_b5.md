First identify the intended outcome.

Before solving, determine whether the supplied situation is a TASK
or a PROBLEM.

TASK:
The supplied model of the situation is sufficient to determine
what must be true for the intended outcome.

PROBLEM:
The requested solution depends on a materially uncertain or
inadequate model of the situation.

Classify as PROBLEM only when at least one of these is true:

1. Two or more materially different explanations remain consistent
   with the supplied evidence and would imply different actions;

2. A premise required by the requested solution is unsupported or
   contradicted by supplied facts;

3. Success cannot be operationally defined without first resolving
   a material ambiguity in the model.

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
PROBLEM merely because a better engineering alternative (compression,
incrementals, extra budget, etc.) can be imagined.

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
7. Reclassify TASK vs still-PROBLEM.
8. If TASK, run B5 and fill the B5 fields.
