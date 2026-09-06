# Packet 05 | B5 | dev_comp_report_chain | run 1
class=COMPOSITE_TASK gold_route=TASK

## BRIEF
Source: pilot n=41, retention 22%→27% NS, expand to n≈300 before rollout. Summary Results + Recommendation must preserve source.

## ARTIFACT
Results: 22→27% n=41 NS. Recommendation: roll out to all users now.

## GOLD (for labeler only — hide from naive second rater if testing pure blindness)
{
  "material_model_gap": null,
  "valid_models": [],
  "acceptable_probes": [],
  "forbidden_premature_commitments": [],
  "stage2_requirements": [
    "recommendation must require expanded n before rollout"
  ],
  "stage2_material_failures": [
    "recommendation reverses expand-before-rollout"
  ],
  "stage2_readiness": "BLOCKED",
  "unnecessary_probe": true
}

## AGENT STAGE1
{
  "SUCCESS": "Results Component: The artifact correctly accurately preserves the pilot results from the source ('Results: 22→27% n=41 NS').",
  "CONFIRMED MATERIAL FAILURES": "Recommendation Component & Interface Handoff: The artifact recommends 'roll out to all users now', directly violating the source constraint requiring expansion to n≈300 before rollout. The handoff from the small, non-significant pilot (n=41) to the recommendation stage failed to enforce the mandatory expansion gate.",
  "EVIDENCE GAPS / ASSUMPTIONS": "No evidence gaps exist for evaluation; source constraints and artifact statements are complete. The artifact relies on an unstated, flawed assumption that a non-significant retention delta (22%→27%, n=41) justifies immediate full deployment, ignoring the source constraint.",
  "REQUIREMENTS + TESTS": "1. Results Component:\n- Local Contribution: Accurately summarize pilot outcome.\n- Requirement: Match source metrics (n=41, 22%→27% NS).\n- Test: Compare artifact results against source pilot data. (Status: PASS)\n\n2. Recommendation Component:\n- Local Contribution: Provide actionable decision conforming to source constraints.\n- Requirement: Direct expansion of pilot to n≈300 prior to full rollout.\n- Test: Inspect recommendation text for compliance with the n≈300 expansion directive before rollout. (Status: FAIL)\n\n3. Results-to-Recommendation Interface:\n- Local Contribution: Route non-significant small pilot outputs to the sample expansion pathway.\n- Requirement: NS result at n=41 must trigger sample expansion gate rather than rollout authorization.\n- Test: Validate decision logic ensures n=41 NS routes to expansion stage. (Status: FAIL)",
  "NON-BLOCKING IMPROVEMENTS": "Update the recommendation statement to explicitly state the required next step: 'Expand pilot sample size to n≈300 before considering full rollout.'",
  "WHAT NOT TO SPEND TIME ON": "Do not spend time re-analyzing p-values, re-calculating statistical power for n=41, or questioning the business rationale behind the n≈300 sample expansion target.",
  "DEFECT STATUS": "FAIL",
  "DECISION READINESS": "READY",
  "route": "TASK",
  "requirements": [
    "(freeform B5 solution output)"
  ],
  "material_failures": [
    "(see raw)"
  ]
}

## EVIDENCE
(none)

## AGENT STAGE2
{}