# Packet 29 | ORACLE-NPA-B5 | dev_comp_dose_card | run 1
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
  "intended_outcome": "Patient schedule on patient card (Section B) matches safe prescriber max (Section A: 10mg BID, max 20mg/day).",
  "route": "TASK",
  "supra_goal": null,
  "model_gap": null,
  "competing_models": [],
  "probe": null,
  "success": "Section B patient card instructions strictly mirror Section A prescriber max limits, ensuring total daily dose does not exceed 20mg/day and schedule adheres to 10mg BID.",
  "parts": [
    {
      "name": "Section A Prescriber Specification",
      "contribution": "Establishes clinical safe maximum dosage of 10mg BID, max 20mg/day."
    },
    {
      "name": "Section B Patient Card",
      "contribution": "Provides direct administration instructions relied upon exclusively by the patient."
    },
    {
      "name": "Prescriber-to-Patient Interface",
      "contribution": "Translates prescriber limits into actionable patient schedule instructions without introducing overdosage risk."
    }
  ],
  "material_failures": [
    "Interface failure: Section B instruction ('10mg morning and 10mg whenever needed') introduces unconstrained PRN administration, allowing total daily intake to exceed 20mg/day and violating the 10mg BID requirement from Section A."
  ],
  "requirements": [
    "Section B patient card schedule must replace 'whenever needed' with a fixed BID interval matching Section A (10mg twice daily).",
    "Section B patient card must explicitly enforce a maximum daily cap of 20mg/day."
  ],
  "tests": [
    "Compare Section B schedule parameters against Section A maximum limits to verify zero probability of patient exceeding 20mg/day.",
    "Verify Section B eliminates unscheduled or PRN ('whenever needed') dosing language."
  ],
  "evidence_gaps": [],
  "decision_readiness": "BLOCKED"
}

## EVIDENCE
(none)

## AGENT STAGE2
{}