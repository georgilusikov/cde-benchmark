# Packet 13 | NPA-B5 | dev_comp_report_chain | run 1
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
  "intended_outcome": "Produce a summary of results and a recommendation consistent with source constraints.",
  "route": "TASK",
  "supra_goal": null,
  "model_gap": null,
  "competing_models": [],
  "probe": null,
  "success": "The summary accurately reports pilot results (22%→27% retention, n=41, NS) and the recommendation strictly aligns with the source constraint to expand to n≈300 before rollout.",
  "parts": [
    {
      "component": "Results Summarization",
      "local_contribution": "Accurately preserve and present pilot metrics including retention delta, sample size, and statistical significance."
    },
    {
      "component": "Recommendation Synthesis",
      "local_contribution": "Formulate next-step actions adhering strictly to source policy constraints."
    },
    {
      "component": "Results-to-Recommendation Interface",
      "local_contribution": "Ensure the recommendation logically follows from pilot findings and complies with source governance."
    }
  ],
  "material_failures": [
    "Artifact recommendation ('roll out to all users now') directly contradicts the source mandate ('expand to n≈300 before rollout').",
    "Interface failure: Authorizing immediate full rollout based on a non-significant pilot outcome (n=41, NS) violates decision rules."
  ],
  "requirements": [
    "The summary of results must report retention 22%→27%, n=41, and NS status.",
    "The recommendation must specify expanding the pilot to n≈300 before any full rollout.",
    "The recommendation must not authorize immediate full rollout to all users."
  ],
  "tests": [
    "Check that summary results state retention change 22%→27%, n=41, and NS.",
    "Check that recommendation explicitly mandates expanding to n≈300 prior to rollout.",
    "Verify that any recommendation for immediate full rollout triggers a policy failure."
  ],
  "evidence_gaps": [],
  "decision_readiness": "BLOCKED"
}

## EVIDENCE
(none)

## AGENT STAGE2
{}