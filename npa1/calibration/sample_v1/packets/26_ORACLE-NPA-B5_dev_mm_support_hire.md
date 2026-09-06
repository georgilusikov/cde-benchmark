# Packet 26 | ORACLE-NPA-B5 | dev_mm_support_hire | run 1
class=MODEL_MISMATCH gold_route=PROBLEM

## BRIEF
Request: hire more support agents because SLA 4h is missed. Facts: agent util 43%; 72% delay before assignment; post-assign median 19m.

## ARTIFACT
Plan: open 8 new agent seats next month.

## GOLD (for labeler only — hide from naive second rater if testing pure blindness)
{
  "material_model_gap": "Whether breach is agent capacity after assign or pre-assign queue.",
  "valid_models": [
    {
      "id": "A_capacity",
      "description": "agents bottleneck",
      "implied_action": "hire"
    },
    {
      "id": "A_preassign",
      "description": "pre-assign delay dominates",
      "implied_action": "fix routing/assignment"
    }
  ],
  "acceptable_probes": [
    {
      "id": "probe_wait_vs_handle",
      "description": "measure time-to-assign vs handle time on late tickets",
      "aliases": [
        "assignment wait vs handle time",
        "pre-assignment delay"
      ],
      "evidence_returned": "Late tickets: median time-to-assign 3h40m; handle 19m; daytime idle >50%."
    }
  ],
  "forbidden_premature_commitments": [
    "open 8 new agent seats",
    "hire more agents",
    "headcount expansion"
  ],
  "stage2_requirements": [
    "target assignment queue before headcount",
    "SLA must include time-to-assign"
  ],
  "stage2_material_failures": [
    "hiring assumes capacity shortage contradicted by util and post-assign speed"
  ],
  "stage2_readiness": "BLOCKED",
  "unnecessary_probe": false
}

## AGENT STAGE1
{
  "intended_outcome": "Meet 4h end-to-end SLA.",
  "route": "PROBLEM",
  "supra_goal": "Consistently meet the 4-hour end-to-end SLA for customer support requests.",
  "model_gap": "Unclear whether SLA breaches stem from capacity shortages during arrival spikes or upstream triage/routing bottlenecks prior to agent assignment, given low overall agent utilization (43%) and long pre-assignment delay (72% of total delay).",
  "competing_models": [
    "Capacity Shortage Model: SLA breaches occur during extreme arrival spikes where agent headcount is temporarily insufficient, causing pre-assignment queue buildup despite a low overall average utilization (43%).",
    "Routing/Dispatch Bottleneck Model: SLA breaches occur because triage, categorizing, or automated routing logic delays assigning tickets to agents who otherwise have available capacity (post-assign median is only 19m)."
  ],
  "probe": "Analyze time-series ticket arrival logs alongside triage/routing event timestamps to determine whether pre-assignment delays correlate with peak agent busyness or delays in ticket routing logic.",
  "success": null,
  "parts": [],
  "material_failures": [],
  "requirements": [],
  "tests": [],
  "evidence_gaps": [
    "Time-series breakdown of ticket arrival rates vs agent availability across peak and off-peak hours",
    "Duration breakdown within the pre-assignment stage (e.g., automated routing queue time vs manual triage delay)"
  ],
  "decision_readiness": "NEEDS_EVIDENCE"
}

## EVIDENCE
Late tickets: median time-to-assign 3h40m; handle 19m; daytime idle >50%.

## AGENT STAGE2
{
  "intended_outcome": "Meet 4h end-to-end SLA.",
  "route": "PROBLEM",
  "supra_goal": "Consistently meet the 4-hour end-to-end SLA for customer support requests.",
  "model_gap": "While daytime agent idle time >50% rules out general capacity shortage, it remains unclear whether the 3h40m median pre-assignment delay is caused by automated routing/skill-matching rule stalls or manual triage queue delays and notification gaps.",
  "competing_models": [
    "Automated Routing Rule Failure Model: Late tickets sit unassigned for 3h40m because automated dispatch algorithms, skill filters, or system event triggers fail to automatically route incoming tickets to available idle agents.",
    "Manual Triage & Queue Visibility Model: Late tickets sit unassigned for 3h40m because ticket assignment depends on manual triage or agent queue-pulling processes, and idle agents are either unnotified or not monitoring the unassigned queue."
  ],
  "probe": "Audit lifecycle event timestamps for late tickets to decompose the 3h40m pre-assignment interval into automated pipeline processing duration versus manual triage/queue waiting duration.",
  "success": null,
  "parts": [],
  "material_failures": [],
  "requirements": [],
  "tests": [],
  "evidence_gaps": [
    "Timestamp breakdown of automated dispatch processing time vs unassigned queue wait time",
    "Audit logs showing agent notification delivery and unassigned queue interactions during daytime idle periods"
  ],
  "decision_readiness": "NEEDS_EVIDENCE"
}