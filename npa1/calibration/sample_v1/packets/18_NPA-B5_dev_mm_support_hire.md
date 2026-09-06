# Packet 18 | NPA-B5 | dev_mm_support_hire | run 1
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
  "intended_outcome": "Meet 4h end-to-end SLA",
  "route": "PROBLEM",
  "supra_goal": "Achieve end-to-end ticket resolution within 4 hours SLA.",
  "model_gap": "The premise that hiring agents will solve SLA breaches is contradicted by 43% agent utilization and 72% pre-assignment delay; the root cause of pre-assignment queue delay is undetermined.",
  "competing_models": [
    "Routing/System Bottleneck: Automated triage rules, dispatch workflows, or system notification delays stall ticket assignment despite available agent capacity.",
    "Skill/Queue Mismatch: Tickets accumulate in specific specialized queues due to agent skill misallocation despite low overall utilization across the pool."
  ],
  "probe": "Analyze timestamp logs of pre-assignment ticket stages to determine whether wait times stem from routing automation delays or queue-specific capacity imbalances.",
  "success": [],
  "parts": [],
  "material_failures": [],
  "requirements": [],
  "tests": [],
  "evidence_gaps": [
    "Ticket timestamp log breakdown detailing pre-assignment wait duration by queue type and routing rule status."
  ],
  "decision_readiness": "NEEDS_EVIDENCE"
}

## EVIDENCE
Late tickets: median time-to-assign 3h40m; handle 19m; daytime idle >50%.

## AGENT STAGE2
{
  "intended_outcome": "Meet 4h end-to-end SLA",
  "route": "TASK",
  "supra_goal": null,
  "model_gap": null,
  "competing_models": [],
  "probe": null,
  "success": [
    "End-to-end ticket resolution duration is maintained at or under the 4-hour (240-minute) SLA for incoming tickets.",
    "Ticket time-to-assign is reduced from the current median of 3h40m (220m) to a level that guarantees completion within SLA when combined with handle time."
  ],
  "parts": [
    "Ticket Assignment & Dispatch Stage: Local contribution is to triage and assign incoming tickets within the assignment SLA time budget (<= 221 minutes maximum, target <= 60 minutes).",
    "Agent Resolution Execution Stage: Local contribution is to process assigned tickets to resolution within the handle time budget (median 19 minutes).",
    "Assignment-to-Agent Handoff Interface: Local contribution is to immediately route unassigned tickets to idle agents, converting >50% daytime agent idle capacity into active queue throughput."
  ],
  "material_failures": [
    "Assignment Latency Failure: Time-to-assign consumes 3h40m of the 4h SLA window (91.7%), leaving only 20 minutes for ticket handling and causing SLA breaches whenever handle time or assign time fluctuates.",
    "Handoff Dispatch Stall: Unassigned tickets remain queued for 3h40m despite agents being idle >50% of the daytime, failing to trigger assignment or alert available agents.",
    "Resolution Overrun: Ticket handling time exceeds the remaining SLA budget post-assignment."
  ],
  "requirements": [
    "The Ticket Assignment & Dispatch Stage MUST reduce median time-to-assign from 3h40m (220m) to <= 221 minutes (and target <= 60 minutes) to keep total end-to-end time within the 240-minute SLA.",
    "The Assignment-to-Agent Handoff Interface MUST automatically push unassigned tickets to idle agents or notify idle agents immediately upon ticket entry while daytime agent idle time is >50%.",
    "The Agent Resolution Execution Stage MUST maintain handle time performance at or below the 19-minute median."
  ],
  "tests": [
    "Measure end-to-end ticket resolution duration and verify that 95%+ of tickets are resolved within 240 minutes.",
    "Measure time-to-assign metrics and verify median time-to-assign is <= 221 minutes (target < 60 minutes).",
    "Verify dispatch handoff latency by testing that an incoming ticket in queue is assigned to an idle agent within < 5 minutes when agent idle capacity > 50%."
  ],
  "evidence_gaps": [],
  "decision_readiness": "READY"
}