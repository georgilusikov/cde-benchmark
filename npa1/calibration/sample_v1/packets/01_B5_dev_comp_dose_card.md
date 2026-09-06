# Packet 01 | B5 | dev_comp_dose_card | run 1
class=COMPOSITE_TASK gold_route=TASK

## BRIEF
Covelin fictional. Section A: 10mg BID max 20mg/day. Section B patient card must match; patient uses only B.

## ARTIFACT
A: 10mg BID max 20/day. B: 10mg morning and 10mg whenever needed.

## GOLD (for labeler only — hide from naive second rater if testing pure blindness)
{
  "material_model_gap": null,
  "valid_models": [],
  "acceptable_probes": [],
  "forbidden_premature_commitments": [],
  "stage2_requirements": [
    "B identical in meaning to A"
  ],
  "stage2_material_failures": [
    "PRN language can exceed max"
  ],
  "stage2_readiness": "BLOCKED",
  "unnecessary_probe": true
}

## AGENT STAGE1
{
  "SUCCESS": "Component identification completed: Prescriber Specification (Section A), Patient Card Instruction (Section B), and the Translation Interface (A -> B). Section A successfully specifies a clear prescriber maximum (10mg BID, max 20mg/day).",
  "CONFIRMED MATERIAL FAILURES": "Interface and Component Failure: Section B ('10mg morning and 10mg whenever needed') fails to match Section A ('10mg BID max 20/day'). Replacing a scheduled twice-daily regimen (BID) with PRN ('whenever needed') instruction creates an unsafe dosing ambiguity, risking inappropriate timing or potential overdose since the patient card relies solely on Section B.",
  "EVIDENCE GAPS / ASSUMPTIONS": "Assumed BID implies scheduled twice-daily administration (e.g., morning and evening ~12 hours apart). Brief explicitly states patient relies only on Section B, so no additional external evidence is missing.",
  "REQUIREMENTS + TESTS": "1. Prescriber Specification (Section A):\n   - Requirement: Must define explicit dose (10mg), frequency (BID), and daily maximum (20mg/day).\n   - Test: Inspect Section A for dose, frequency, and ceiling cap. [PASS]\n\n2. Patient Card Instruction (Section B):\n   - Requirement: Must provide clear, deterministic, scheduled dosing times matching BID without introducing PRN ('whenever needed') language.\n   - Test: Check Section B text for non-deterministic terms like 'whenever needed'. [FAIL]\n\n3. Interface (A -> B Alignment):\n   - Requirement: Section B instructions must be semantically equivalent to Section A prescription and guarantee compliance with safe max.\n   - Test: Perform semantic equivalence check between Section A and Section B dosing schedules. [FAIL]",
  "NON-BLOCKING IMPROVEMENTS": "Rephrase Section B to explicit timing (e.g., '10mg in the morning and 10mg in the evening') and explicitly state 'Maximum 20mg per day' on the patient card.",
  "WHAT NOT TO SPEND TIME ON": "Do not spend time evaluating clinical efficacy, pharmacokinetics of fictional drug Covelin, or downstream packaging redesigns.",
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