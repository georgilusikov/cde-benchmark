# Packet 30 | ORACLE-NPA-B5 | dev_mm_more_moderators | run 1
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
  "intended_outcome": "Clear reports within SLA.",
  "route": "PROBLEM",
  "supra_goal": "Maintain report-resolution SLA reliably and efficiently, independent of specific headcount additions.",
  "model_gap": "Whether SLA failure is caused by insufficient moderator capacity or queue inflation from unclustered duplicate reports due to disabled auto-similarity tooling.",
  "competing_models": [
    "Model A (Capacity Deficit): SLA breach is caused by insufficient moderator throughput relative to total incoming report volume, requiring +20 moderators.",
    "Model B (Queue Inflation / Feature Disablement): SLA breach is caused by 70% duplicate report volume across 30 entities while the auto-similarity tool is off; existing moderator capacity is sufficient for unique items."
  ],
  "probe": "Turn on or simulate the auto-similarity tool against the 12k open queue to measure the net deduplicated volume and determine if existing moderators clear unique items within SLA.",
  "success": [],
  "parts": [],
  "material_failures": [],
  "requirements": [],
  "tests": [],
  "evidence_gaps": [
    "Net volume of unique report items after auto-similarity deduplication",
    "Throughput capacity of current moderator team against deduplicated queue"
  ],
  "decision_readiness": "NEEDS_EVIDENCE"
}

## EVIDENCE
(none)

## AGENT STAGE2
{}