# Packet 21 | NPA-B5 | dev_comp_phase_gate | run 1
class=COMPOSITE_TASK gold_route=TASK

## BRIEF
Phase1: licence filed M1, grant takes 6-9 months. Phase2 regulated revenue legally requires grant first.

## ARTIFACT
Phase1 grant expected M7-M10. Phase2 first regulated revenue starts M7.

## GOLD (for labeler only — hide from naive second rater if testing pure blindness)
{
  "material_model_gap": null,
  "valid_models": [],
  "acceptable_probes": [],
  "forbidden_premature_commitments": [],
  "stage2_requirements": [
    "phase2 start >= actual grant",
    "cannot schedule revenue at M7 given grant window M7-M10"
  ],
  "stage2_material_failures": [
    "revenue starts at earliest grant boundary, can precede grant"
  ],
  "stage2_readiness": "BLOCKED",
  "unnecessary_probe": true
}

## AGENT STAGE1
{
  "intended_outcome": "Revenue generated only after licence grant is received.",
  "route": "TASK",
  "supra_goal": null,
  "model_gap": null,
  "competing_models": [],
  "probe": null,
  "success": "100% of Phase 2 regulated revenue is generated on or after the official date of Phase 1 licence grant.",
  "parts": [
    {
      "name": "Licence_Grant_Stage",
      "local_contribution": "Submits licence application at M1 and secures regulatory grant within expected 6-9 month window (M7-M10)."
    },
    {
      "name": "Regulated_Revenue_Stage",
      "local_contribution": "Initiates and processes Phase 2 regulated commercial transactions (scheduled for M7)."
    },
    {
      "name": "Grant_Revenue_Interface",
      "local_contribution": "Acts as a prerequisite gate ensuring Phase 2 regulated revenue start is locked until Phase 1 grant is confirmed."
    }
  ],
  "material_failures": [
    {
      "failure_mode": "Premature_Revenue_Execution",
      "description": "Regulated revenue starts at M7 according to schedule, but licence grant is delayed until M8-M10, creating illegal unlicenced revenue operations."
    },
    {
      "failure_mode": "Interface_Gating_Failure",
      "description": "Revenue stage triggers automatically on a static M7 calendar date rather than dynamically waiting for licence grant signal."
    }
  ],
  "requirements": [
    {
      "component": "Licence_Grant_Stage",
      "requirement": "Must obtain official licence grant documentation and issue verification signal prior to enabling revenue activities."
    },
    {
      "component": "Regulated_Revenue_Stage",
      "requirement": "Must maintain blocked state on regulated revenue operations until formal clearance from licence stage is received."
    },
    {
      "component": "Grant_Revenue_Interface",
      "requirement": "Must dynamically gate revenue launch to actual grant date (M7-M10) rather than fixed schedule assumption."
    }
  ],
  "tests": [
    {
      "component": "Licence_Grant_Stage",
      "test": "Verify official regulatory approval document and timestamp before releasing dependency lock."
    },
    {
      "component": "Regulated_Revenue_Stage",
      "test": "Audit financial transaction logs to confirm zero regulated revenue occurs prior to grant verification timestamp."
    },
    {
      "component": "Grant_Revenue_Interface",
      "test": "Simulate grant arrival at M10 and test that revenue trigger remains disarmed through M7-M9."
    }
  ],
  "evidence_gaps": [
    "Exact grant month within the M7-M10 window cannot be determined prior to regulatory processing."
  ],
  "decision_readiness": "BLOCKED"
}

## EVIDENCE
(none)

## AGENT STAGE2
{}