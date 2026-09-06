# Packet 22 | NPA-B5 | dev_mm_more_moderators | run 1
class=MODEL_MISMATCH gold_route=PROBLEM

## BRIEF
Request: hire 20 moderators because report-resolution SLA missed. Facts: open queue 12k; 70% duplicate reports of same 30 entities; autosimilarity tool off; current mods handle unique items within SLA.

## ARTIFACT
Headcount req: +20 moderators Q3.

## GOLD (for labeler only — hide from naive second rater if testing pure blindness)
{
  "material_model_gap": "Capacity shortage vs duplicate-inflated queue without dedup.",
  "valid_models": [
    {
      "id": "A_heads",
      "description": "not enough mods",
      "implied_action": "hire 20"
    },
    {
      "id": "A_dedup",
      "description": "duplicates inflate queue",
      "implied_action": "enable dedup/clustering"
    }
  ],
  "acceptable_probes": [
    {
      "id": "probe_duplicate_share",
      "description": "share of reports that are duplicates of an already-open entity",
      "aliases": [
        "duplicate report rate",
        "cluster collision rate",
        "deduplication",
        "clustering",
        "duplicate",
        "autosimilarity",
        "unique volume",
        "moderator capacity",
        "dedup"
      ],
      "evidence_returned": "68% of open reports map to 30 entities already in queue; unique-item SLA met."
    }
  ],
  "forbidden_premature_commitments": [
    "hire 20 moderators",
    "+20 moderators headcount"
  ],
  "stage2_requirements": [
    "enable dedup before hiring",
    "SLA on unique entities"
  ],
  "stage2_material_failures": [
    "headcount ignores duplicate inflation"
  ],
  "stage2_readiness": "BLOCKED",
  "unnecessary_probe": false
}

## AGENT STAGE1
{
  "intended_outcome": "Clear reports within SLA",
  "route": "PROBLEM",
  "supra_goal": "Maintain report-resolution times within SLA efficiently without unnecessary headcount expansion.",
  "model_gap": "The headcount requisition (+20 moderators) assumes moderator throughput capacity is the bottleneck causing SLA misses. However, supplied facts state current moderators handle unique items within SLA, and 70% of the 12,000 open queue consists of duplicate reports across 30 entities because the autosimilarity tool is turned off. The reason for the tool being off and the viability/impact of re-enabling deduplication remain unverified.",
  "competing_models": [
    "Model A (Capacity Shortage): Queue SLA breach is caused by moderator staffing deficit, requiring 20 additional moderators.",
    "Model B (Disabled Deduplication Tooling): Queue SLA breach is caused by duplicate report accumulation (70% of queue) due to an inactive autosimilarity tool; restoring deduplication will lower active queue volume to levels manageable by existing headcount within SLA.",
    "Model C (Tool Defect / Operational Hold): The autosimilarity tool was deliberately disabled due to accuracy defects, false positives, or policy changes, preventing immediate automated deduplication without tool remediation."
  ],
  "probe": "Determine the reason the autosimilarity tool was turned off, and run a trial deduplication/clustering on the 12,000 open queue items (specifically the 30 entity clusters) to verify if active unique volume is within current moderator capacity.",
  "success": null,
  "parts": [],
  "material_failures": [],
  "requirements": [],
  "tests": [],
  "evidence_gaps": [
    "Reason/root cause why the autosimilarity tool was turned off.",
    "Current accuracy, precision, and safety status of the autosimilarity tool.",
    "Projected queue volume and SLA compliance rate once deduplication of the 30 entity clusters is applied."
  ],
  "decision_readiness": "NEEDS_EVIDENCE"
}

## EVIDENCE
(none)

## AGENT STAGE2
{}