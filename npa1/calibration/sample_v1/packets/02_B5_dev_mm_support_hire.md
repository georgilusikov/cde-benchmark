# Packet 02 | B5 | dev_mm_support_hire | run 1
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
  "SUCCESS": "End-to-end ticket resolution consistently meets the 4h SLA by eliminating pre-assignment queue delays and maintaining post-assignment resolution efficiency without unnecessary headcount expansion.",
  "COMPONENTS_AND_INTERFACES": [
    {
      "component": "Pre-Assignment Stage (Intake, Triage & Queue Dispatch)",
      "local_contribution": "Ingest incoming requests, triage/classify priority, and route/assign tickets to an available support agent.",
      "coherent_quality_responsibility": "Ensure rapid transition from ticket creation to agent assignment (<30 minutes)."
    },
    {
      "component": "Post-Assignment Stage (Ticket Resolution Execution)",
      "local_contribution": "Investigate, troubleshoot, and resolve assigned customer tickets.",
      "coherent_quality_responsibility": "Execute ticket resolution accurately and efficiently (currently median 19 minutes)."
    },
    {
      "component": "Resource Capacity Management",
      "local_contribution": "Maintain agent staffing levels and active workload allocation.",
      "coherent_quality_responsibility": "Ensure effective headcount utilization without over-staffing or under-staffing (currently at 43% utilization)."
    },
    {
      "interface": "Queue-to-Agent Handoff Interface",
      "local_contribution": "Transfer queued unassigned tickets to idle/available support agents.",
      "coherent_quality_responsibility": "Ensure zero idle-agent queue accumulation (eliminate artificial dispatch bottlenecks)."
    }
  ],
  "CONFIRMED MATERIAL FAILURES": [
    "Misalignment of Intervention to Root Cause: The artifact proposes opening 8 new agent seats to solve a 4h SLA breach. However, current agent utilization is only 43% and 72% of total delay occurs pre-assignment. Adding agent seats does not reduce pre-assignment queue time and adds redundant underutilized capacity.",
    "Broken Queue-to-Agent Handoff Interface: Unassigned tickets sit in the queue (causing 72% of total SLA delay) even though agents are idle 57% of the time, indicating a breakdown in the assignment/dispatch mechanism."
  ],
  "EVIDENCE GAPS / ASSUMPTIONS": [
    "Assumption in Request/Plan: SLA breaches are caused by insufficient agent headcount.",
    "Evidence Gap: Specific root cause for pre-assignment queue delay (e.g., manual triage bottlenecks, flawed auto-assignment rules, notification failures, or shift schedule coverage mismatches).",
    "Evidence Gap: Tail latency (p90/p99) distribution for post-assignment resolution time beyond the median 19 minutes."
  ],
  "REQUIREMENTS + TESTS": [
    {
      "target": "Pre-Assignment Stage",
      "requirement": "Pre-assignment queue and triage latency must not exceed 30 minutes per ticket.",
      "test": "Measure timestamp delta from ticket creation to agent assignment across all incoming tickets."
    },
    {
      "target": "Post-Assignment Stage",
      "requirement": "Post-assignment resolution duration must maintain median <=20 minutes and p95 <=60 minutes.",
      "test": "Monitor timestamp delta from agent assignment to ticket resolution."
    },
    {
      "target": "Resource Capacity Management",
      "requirement": "Increase current agent utilization from 43% to target range (65-80%) before authorizing headcount expansion.",
      "test": "Audit active handle time against total logged/shift hours per agent."
    },
    {
      "target": "Queue-to-Agent Handoff Interface",
      "requirement": "Automated dispatch system must assign incoming tickets to available idle agents within 1 minute.",
      "test": "Simulate ticket arrival while agents are idle and verify handoff latency is <1 minute."
    }
  ],
  "NON-BLOCKING IMPROVEMENTS": [
    "Implement automated ticket tagging and skill-based auto-routing.",
    "Set up real-time queue notifications for unassigned tickets sitting >15 minutes.",
    "Realign agent shift rosters to match peak ticket submission windows."
  ],
  "WHAT NOT TO SPEND TIME ON": [
    "Opening 8 new agent seats, interviewing, hiring, or onboarding new support agents next month.",
    "Optimizing agent post-assignment resolution workflows (current post-assignment median of 19m is already well within limits)."
  ],
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