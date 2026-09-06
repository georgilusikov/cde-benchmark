# Packet 00 | B5 | dev_clear_disk_alert | run 1
class=CLEAR_TASK gold_route=TASK

## BRIEF
Alert rule: page on-call if disk used >=90% on any prod DB host. Hosts: db1 92%, db2 71%, db3 88%. Runbook: free space or page.

## ARTIFACT
Monitoring dashboard lists db1=92%, db2=71%, db3=88%.

## GOLD (for labeler only — hide from naive second rater if testing pure blindness)
{
  "material_model_gap": null,
  "valid_models": [],
  "acceptable_probes": [],
  "forbidden_premature_commitments": [],
  "stage2_requirements": [
    "page for any host >=90%",
    "db1 must trigger page"
  ],
  "stage2_material_failures": [
    "db1 is above 90% and must page"
  ],
  "stage2_readiness": "READY",
  "unnecessary_probe": true
}

## AGENT STAGE1
{
  "SUCCESS": "The monitoring dashboard accurately lists the disk usage metrics for all specified hosts (db1: 92%, db2: 71%, db3: 88%), matching the values in the brief.",
  "CONFIRMED MATERIAL FAILURES": [],
  "EVIDENCE GAPS / ASSUMPTIONS": [
    "EVIDENCE GAP: No evidence provided showing that the alert rule (disk used >= 90%) is actively configured in the monitoring/alerting engine.",
    "EVIDENCE GAP: No evidence that an alert was evaluated, triggered, or entered a FIRING state for db1 (92% usage).",
    "EVIDENCE GAP: No evidence of delivery logs or paging confirmation sent to on-call personnel.",
    "EVIDENCE GAP: No evidence that the runbook (free space or page) is accessible or linked within the paging notification.",
    "ASSUMPTION: Hosts db1, db2, and db3 are assumed to be production DB hosts as described in the brief.",
    "ASSUMPTION: The metric of 92% on db1 represents current, active disk usage requiring threshold evaluation."
  ],
  "REQUIREMENTS + TESTS": [
    {
      "component": "Host Telemetry & Dashboard Display",
      "local_contribution": "Ingests and displays current host disk usage percentages accurately.",
      "requirement": "Dashboard must accurately display real-time disk usage for all production DB hosts.",
      "failure_mode": "Stale metric caching or UI rounding error masking a disk threshold breach.",
      "test": "Verify dashboard metric values for db1, db2, and db3 against raw host OS telemetry (`df -h`)."
    },
    {
      "component": "Alert Rule Evaluator",
      "local_contribution": "Evaluates host metrics against the >= 90% threshold and transitions to FIRING state when breached.",
      "requirement": "Alert engine must continuously evaluate disk usage metrics and trigger an alert state whenever any prod DB host disk usage is >= 90% (specifically db1 at 92%).",
      "failure_mode": "Rule disabled, incorrect evaluation window, metric query mismatch, or wrong operator logic (> 90% instead of >= 90%).",
      "test": "Ingest test metric of 92% for db1 into alerting engine and verify state transitions to FIRING within expected evaluation interval."
    },
    {
      "component": "Paging & Notification Gateway",
      "local_contribution": "Routes triggered alert events to the active on-call engineer via notification channels.",
      "requirement": "Upon alert trigger for db1, paging gateway must immediately dispatch high-priority page to on-call responder.",
      "failure_mode": "Notification delivery failure, unmapped escalation policy, or silent payload drop.",
      "test": "Simulate alert trigger for db1 and confirm page delivery to on-call engineer endpoint with receipt confirmation."
    },
    {
      "component": "Runbook Integration",
      "local_contribution": "Provides actionable resolution procedure (free space or page/escalate) to the on-call responder.",
      "requirement": "Paged alert notification must include a valid link to the runbook specifying free space and escalation procedures.",
      "failure_mode": "Missing or broken runbook link in the alert payload.",
      "test": "Validate that the embedded runbook URL in the alert payload resolves to a valid document with current procedures."
    },
    {
      "interface": "Telemetry -> Alert Evaluator",
      "local_contribution": "Handoff of host disk metric telemetry from ingestion stream to alert rule engine.",
      "failure_mode": "Dashboard displays db1 at 92% (locally correct), but alert evaluator queries a stale cache or different metric scope evaluating db1 < 90%.",
      "requirement": "Alert evaluator must consume from the exact same live metric stream displayed on the dashboard.",
      "test": "Verify timestamp and value of telemetry data point consumed by evaluator match dashboard rendered value."
    },
    {
      "interface": "Alert Evaluator -> Paging System",
      "local_contribution": "Handoff of firing alert state to the paging notification engine.",
      "failure_mode": "Alert evaluator correctly fires for db1 (92%), but paging system rejects payload due to schema mismatch or missing metadata key.",
      "requirement": "Alert evaluator trigger payload format must strictly conform to paging gateway API contract.",
      "test": "Execute integration test sending evaluator trigger schema to paging endpoint and verify HTTP 200 response and incident creation."
    }
  ],
  "NON-BLOCKING IMPROVEMENTS": [
    "Configure a warning alert threshold (e.g., at 80% or 85%) to allow proactive disk cleanup prior to emergency paging.",
    "Display active alert firing state directly on the monitoring dashboard metric tiles.",
    "Automate initial non-destructive cleanup actions (such as log truncation) upon threshold breach."
  ],
  "WHAT NOT TO SPEND TIME ON": [
    "Redesigning dashboard UI styling or layout.",
    "Investigating non-breaching hosts (db2 at 71%, db3 at 88%) beyond confirming non-firing behavior.",
    "Modifying storage architecture for non-production environments."
  ],
  "DEFECT STATUS": "PASS",
  "DECISION READINESS": "NEEDS_EVIDENCE",
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