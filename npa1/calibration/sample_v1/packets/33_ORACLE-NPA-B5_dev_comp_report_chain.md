# Packet 33 | ORACLE-NPA-B5 | dev_comp_report_chain | run 1
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
  "intended_outcome": "Recommendation consistent with source constraints.",
  "route": "TASK",
  "supra_goal": null,
  "model_gap": null,
  "competing_models": [],
  "probe": null,
  "success": "The artifact's summary results accurately reflect pilot data (22% to 27%, n=41, NS) and the recommendation strictly complies with the source requirement (expand to n≈300 before full rollout).",
  "parts": [
    {
      "component": "Pilot Results Summary",
      "local_contribution": "Accurately state the quantitative findings (22%→27% retention, n=41, non-significant)."
    },
    {
      "component": "Rollout Recommendation",
      "local_contribution": "Preserve the source decision logic regarding deployment steps."
    },
    {
      "component": "Source-to-Artifact Alignment Interface",
      "local_contribution": "Ensure the recommended action logically follows from the pilot evaluation and source policy without skipping required pre-rollout expansion."
    }
  ],
  "material_failures": [
    "Direct policy contradiction: The artifact recommends immediate full rollout ('roll out to all users now'), violating the source constraint requiring expansion to n≈300 prior to rollout."
  ],
  "requirements": [
    "The recommendation in the artifact must state expanding the pilot to n≈300 before full rollout.",
    "The summary of results in the artifact must maintain accurate reporting of pilot metrics (22%→27% retention, n=41, NS)."
  ],
  "tests": [
    "Check if the artifact recommendation matches the source directive (expand sample to n≈300 before rollout vs immediate full rollout).",
    "Check if the artifact summary of results strictly matches the pilot findings (22%→27%, n=41, NS)."
  ],
  "evidence_gaps": [],
  "decision_readiness": "BLOCKED"
}

## EVIDENCE
(none)

## AGENT STAGE2
{}