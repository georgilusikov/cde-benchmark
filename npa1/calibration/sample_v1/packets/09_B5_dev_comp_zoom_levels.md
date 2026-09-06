# Packet 09 | B5 | dev_comp_zoom_levels | run 1
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
  "SUCCESS": "1. Face height of 50% satisfies the brief requirement (40%–60%).\n2. Allowed zoom levels 1.08x and 1.16x from the brief are present in the artifact.",
  "CONFIRMED MATERIAL FAILURES": "1. Zoom level count violation: Artifact specifies 4 zoom levels (1.08, 1.10, 1.12, 1.16), violating the brief's constraint of 'at most 2 zoom levels'.\n2. Disallowed zoom levels: Artifact includes 1.10x and 1.12x, which fall outside the brief's explicit allowed set of {1.08x, 1.16x}.",
  "EVIDENCE GAPS / ASSUMPTIONS": "1. Assumption: 'Face 50%' indicates that subject face height occupies 50% of total render frame height.\n2. Assumption: Zoom values (1.08, 1.10, 1.12, 1.16) represent linear scale multipliers.\n3. Evidence Gap: No parameters provided regarding animation or transition rules between zoom levels.",
  "REQUIREMENTS + TESTS": {
    "Component 1: Zoom Level Selector": {
      "Local Contribution": "Restricts available zoom scale factors to approved discrete levels.",
      "Material Failure": "Configuring more than 2 zoom levels or including non-permitted scale factors (e.g. 1.10x, 1.12x).",
      "Requirement": "Must limit zoom options to at most 2 levels, restricted exclusively to 1.08x and 1.16x.",
      "Test": "Assert count(ZoomLevels) <= 2 AND set(ZoomLevels) ⊆ {1.08, 1.16}."
    },
    "Component 2: Face Height Framer": {
      "Local Contribution": "Scales and positions subject to maintain correct talking-head visual proportion.",
      "Material Failure": "Rendered subject face height falling outside the 40%–60% total frame height range.",
      "Requirement": "Subject face height MUST occupy between 40% and 60% of total frame height.",
      "Test": "Measure (face_height / frame_height); assert 0.40 <= ratio <= 0.60."
    },
    "Interface: Zoom-to-Framing Handoff": {
      "Local Contribution": "Applies zoom scale factor to baseline framing without exceeding face height limits or compromising visual distinctness.",
      "Material Failure": "Handoff failure where zoom selector and baseline framer are locally valid, but applied zoom pushes post-zoom face height out of [40%, 60%] or subtle intermediate steps erode visual distinctness.",
      "Requirement": "Combined zoom scale factor applied to face framing must maintain face height within [40%, 60%] dynamically across all allowed zoom states while ensuring distinct steps.",
      "Test": "Calculate post-zoom face height ratio across baseline range for zoom levels {1.08x, 1.16x}; assert all resulting ratios remain within [0.40, 0.60] and inter-level scale delta provides visual distinctness."
    }
  },
  "NON-BLOCKING IMPROVEMENTS": "1. Remove 1.10x and 1.12x zoom levels to restore compliance with brief limits.\n2. Explicitly specify transition style (e.g., hard cut vs ease) between 1.08x and 1.16x.",
  "WHAT NOT TO SPEND TIME ON": "1. Fine-tuning or calibrating 1.10x and 1.12x zoom settings.\n2. Re-adjusting base face height framing, as 50% is centered within the allowable 40%–60% range.",
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