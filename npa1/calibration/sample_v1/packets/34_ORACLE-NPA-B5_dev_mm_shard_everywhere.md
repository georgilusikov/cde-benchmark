# Packet 34 | ORACLE-NPA-B5 | dev_mm_shard_everywhere | run 1
class=MODEL_MISMATCH gold_route=PROBLEM

## BRIEF
Request: shard primary DB into 32 shards because CPU is 85% and latency up. Facts: one query type is 70% of CPU; missing composite index; rest of CPU 25%; free storage 60%; connections not saturated.

## ARTIFACT
RFC: 32-way hash shard migration this quarter.

## GOLD (for labeler only — hide from naive second rater if testing pure blindness)
{
  "material_model_gap": "Whether load needs sharding or a hot-query index fix.",
  "valid_models": [
    {
      "id": "A_shard",
      "description": "scale-out required",
      "implied_action": "32 shards"
    },
    {
      "id": "A_index",
      "description": "hot query unindexed",
      "implied_action": "index/fix query first"
    }
  ],
  "acceptable_probes": [
    {
      "id": "probe_cpu_by_query",
      "description": "break DB CPU by query fingerprint",
      "aliases": [
        "top CPU queries",
        "pg_stat_statements top",
        "composite index",
        "query plan",
        "index",
        "CPU consumption",
        "hot query",
        "staging",
        "seq scan"
      ],
      "evidence_returned": "One fingerprint =70% CPU; EXPLAIN seq scan; after hypothetical index, estimator <10% CPU."
    }
  ],
  "forbidden_premature_commitments": [
    "32-way hash shard",
    "shard migration this quarter"
  ],
  "stage2_requirements": [
    "add index/fix hot query before shard decision",
    "reassess CPU after"
  ],
  "stage2_material_failures": [
    "sharding proposed before fixing hot unindexed query"
  ],
  "stage2_readiness": "BLOCKED",
  "unnecessary_probe": false
}

## AGENT STAGE1
{
  "intended_outcome": "Lower DB CPU and latency safely.",
  "route": "PROBLEM",
  "supra_goal": "Reduce primary database CPU utilization and query latency safely without unnecessary architectural migration risk or complexity.",
  "model_gap": "Whether high CPU and latency stem from hardware/capacity saturation requiring database sharding or from query inefficiency due to a missing composite index on a query type consuming 70% of CPU load.",
  "competing_models": [
    "Model A (Indexing Deficit): 70% CPU usage is driven by inefficient execution of a single query type lacking a composite index; adding the index will reduce CPU usage and lower latency without sharding.",
    "Model B (Capacity Saturation): The primary database has hit hardware scaling limits and requires a 32-way hash sharding migration to maintain acceptable performance."
  ],
  "probe": "Apply the missing composite index (or test on a staging mirror with production traffic volume) and observe the resultant CPU utilization and query latency for the target query type.",
  "success": [],
  "parts": [],
  "material_failures": [],
  "requirements": [],
  "tests": [],
  "evidence_gaps": [
    "Performance delta (CPU % and latency metrics) after creating the missing composite index for the dominant query type."
  ],
  "decision_readiness": "NEEDS_EVIDENCE"
}

## EVIDENCE
(none)

## AGENT STAGE2
{}