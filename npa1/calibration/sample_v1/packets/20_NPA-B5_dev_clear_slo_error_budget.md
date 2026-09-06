# Packet 20 | NPA-B5 | dev_clear_slo_error_budget | run 1
class=CLEAR_TASK gold_route=TASK

## BRIEF
SLO: 99.9% monthly availability. Month has 30 days. Current downtime already 50 minutes. Propose whether a 45-minute maintenance window is allowed this month.

## ARTIFACT
Change ticket: schedule 45 minutes downtime Friday.

## GOLD (for labeler only — hide from naive second rater if testing pure blindness)
{
  "material_model_gap": null,
  "valid_models": [],
  "acceptable_probes": [],
  "forbidden_premature_commitments": [],
  "stage2_requirements": [
    "reject or defer maintenance that exceeds remaining error budget",
    "compute remaining budget before approve"
  ],
  "stage2_material_failures": [
    "monthly budget ~43.2 min at 99.9%; 50 already used; 45 more exceeds"
  ],
  "stage2_readiness": "BLOCKED",
  "unnecessary_probe": true
}

## AGENT STAGE1
{
  "intended_outcome": "Decide whether a proposed 45-minute maintenance window is allowed this month given a 99.9% availability SLO over 30 days and 50 minutes of prior downtime.",
  "route": "TASK",
  "supra_goal": null,
  "model_gap": null,
  "competing_models": [],
  "probe": null,
  "success": "Determine accurately that the 45-minute maintenance window is disallowed, as total prospective downtime (95 minutes) exceeds the maximum allowed monthly limit (43.2 minutes) for a 99.9% availability SLO.",
  "parts": [
    {
      "component": "Monthly Error Budget Calculator",
      "local_contribution": "Calculates total allowable monthly downtime based on timeframe (30 days = 43,200 minutes) and availability target (99.9% SLO -> 0.1% allowed downtime = 43.2 minutes)."
    },
    {
      "component": "Accumulated Downtime Tracker",
      "local_contribution": "Tracks and reports historical downtime consumed during the month (50 minutes)."
    },
    {
      "component": "Maintenance Decision Evaluator",
      "local_contribution": "Sums consumed downtime and proposed maintenance duration (50 + 45 = 95 minutes) and compares against maximum allowed error budget to decide change ticket approval."
    },
    {
      "component": "Tracker-to-Evaluator Interface",
      "local_contribution": "Ensures prior accumulated downtime figures are reliably passed to the evaluation stage without omission."
    }
  ],
  "material_failures": [
    {
      "failure_mode": "Existing Budget Exhaustion",
      "description": "Accumulated downtime of 50 minutes already exceeds the monthly error budget of 43.2 minutes by 6.8 minutes."
    },
    {
      "failure_mode": "SLO Breach via Maintenance Approval",
      "description": "Approving the 45-minute window would increase total monthly downtime to 95 minutes, dropping availability to ~99.78% and violating the 99.9% SLO."
    },
    {
      "failure_mode": "Interface Handoff Omission",
      "description": "Evaluating the 45-minute change ticket in isolation without incorporating the 50 minutes of prior downtime."
    }
  ],
  "requirements": [
    "Total downtime within the 30-day monthly period must not exceed 43.2 minutes.",
    "Maintenance evaluation logic must enforce the condition: (Current Downtime + Proposed Downtime) <= Allowed Error Budget.",
    "The Friday 45-minute maintenance change ticket must be rejected for the current monthly period."
  ],
  "tests": [
    "Verify error budget baseline: 30 days * 1440 min/day * (1 - 0.999) = 43.2 minutes maximum allowed downtime.",
    "Verify current budget status: 50 minutes recorded > 43.2 minutes allowed -> remaining budget is -6.8 minutes.",
    "Evaluate change ticket impact: 50 min + 45 min = 95 min > 43.2 min -> assert change ticket status == REJECTED."
  ],
  "evidence_gaps": [],
  "decision_readiness": "READY"
}

## EVIDENCE
(none)

## AGENT STAGE2
{}