# Packet 17 | NPA-B5 | dev_comp_zoom_levels | run 1
class=COMPOSITE_TASK gold_route=TASK

## BRIEF
Talking-head render: at most 2 zoom levels 1.08x and 1.16x; face height 40-60%.

## ARTIFACT
Zoom: 1.08, 1.10, 1.12, 1.16. Face 50%.

## GOLD (for labeler only — hide from naive second rater if testing pure blindness)
{
  "material_model_gap": null,
  "valid_models": [],
  "acceptable_probes": [],
  "forbidden_premature_commitments": [],
  "stage2_requirements": [
    "only 1.08 and 1.16"
  ],
  "stage2_material_failures": [
    "four zoom levels exceed two-level max"
  ],
  "stage2_readiness": "BLOCKED",
  "unnecessary_probe": true
}

## AGENT STAGE1
{
  "intended_outcome": "Visually distinct natural talking-head zooms adhering strictly to zoom level count, zoom values, and face framing rules.",
  "route": "TASK",
  "supra_goal": null,
  "model_gap": null,
  "competing_models": [],
  "probe": null,
  "success": "Render uses at most 2 zoom levels restricted to 1.08x and 1.16x, while keeping face height framing within 40%–60%.",
  "parts": [
    {
      "name": "Zoom Controller",
      "local_contribution": "Restricts zoom operations to at most 2 distinct levels, limited to 1.08x and 1.16x.",
      "interfaces": [
        "Render Compositor"
      ]
    },
    {
      "name": "Framing Controller",
      "local_contribution": "Maintains face height proportion within 40% to 60% of vertical frame height.",
      "interfaces": [
        "Render Compositor"
      ]
    },
    {
      "name": "Render Compositor",
      "local_contribution": "Combines zoom and framing parameters to output visually distinct natural talking-head video.",
      "interfaces": [
        "Zoom Controller",
        "Framing Controller"
      ]
    }
  ],
  "material_failures": [
    "Artifact uses 4 distinct zoom levels (1.08, 1.10, 1.12, 1.16), violating the brief constraint of at most 2 zoom levels.",
    "Artifact includes intermediate zoom levels (1.10, 1.12) that are disallowed by the brief."
  ],
  "requirements": [
    "Total distinct zoom levels in the sequence must not exceed 2.",
    "Zoom values must be strictly chosen from {1.08x, 1.16x}.",
    "Face height framing must remain within 40%–60% vertical height."
  ],
  "tests": [
    "Verify count of unique zoom levels in the artifact is <= 2.",
    "Confirm all active zoom values match only 1.08x or 1.16x.",
    "Measure face height relative to full frame height to ensure compliance with 40%–60% range."
  ],
  "evidence_gaps": [],
  "decision_readiness": "BLOCKED"
}

## EVIDENCE
(none)

## AGENT STAGE2
{}