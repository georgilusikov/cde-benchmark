# Packet 32 | ORACLE-NPA-B5 | dev_clear_api_100rpm | run 1
class=CLEAR_TASK gold_route=TASK

## BRIEF
Design an HTTP client. Upstream hard limit: 100 requests/min. Workload: 500 independent jobs/hour, 1 request each. Jobs may queue. No other constraints.

## ARTIFACT
(none)

## GOLD (for labeler only — hide from naive second rater if testing pure blindness)
{
  "material_model_gap": null,
  "valid_models": [],
  "acceptable_probes": [],
  "forbidden_premature_commitments": [],
  "stage2_requirements": [
    "avg rate <=100/min",
    "throughput >=500 jobs/h",
    "queue when needed"
  ],
  "stage2_material_failures": [],
  "stage2_readiness": null,
  "unnecessary_probe": true
}

## AGENT STAGE1
{
  "intended_outcome": "Complete 500 jobs/hour without exceeding 100 requests/minute.",
  "route": "TASK",
  "supra_goal": null,
  "model_gap": null,
  "competing_models": [],
  "probe": null,
  "success": "Process at least 500 independent HTTP jobs per hour while guaranteeing that total outgoing request frequency never exceeds 100 requests per rolling 60-second window.",
  "parts": [
    {
      "name": "Job Queue Manager",
      "local_contribution": "Buffers incoming job submissions (500 jobs/hour workload) and manages execution order without dropping jobs."
    },
    {
      "name": "Rate Limiter Controller",
      "local_contribution": "Throttles request permissions using a token/leaky bucket algorithm to enforce the <= 100 req/min upstream bound."
    },
    {
      "name": "HTTP Request Dispatcher",
      "local_contribution": "Receives rate-approved jobs, executes HTTP requests upstream, and captures completion responses."
    },
    {
      "name": "Queue-to-RateLimiter Interface",
      "local_contribution": "Transfers job context to rate controller state upon readiness without task duplication or leakage."
    },
    {
      "name": "RateLimiter-to-Dispatcher Interface",
      "local_contribution": "Signals token availability to trigger single HTTP dispatch, ensuring retries re-acquire rate tokens."
    }
  ],
  "material_failures": [
    "Rate Limiter Failure: Outbound rate exceeds 100 req/min in any rolling window, triggering upstream 429/throttling errors.",
    "Queue Exhaustion Failure: Buffer memory overflows or drops jobs during load bursts.",
    "Queue-RateLimiter Interface Failure: Concurrent dequeue race condition causing dropped or double-processed jobs.",
    "RateLimiter-Dispatcher Interface Failure: Internal network retry loop bypasses rate limiter tokens, violating the rate ceiling."
  ],
  "requirements": [
    "REQ-1 (Rate Boundary): Enforce a strict maximum limit of 100 HTTP requests per rolling 60-second interval.",
    "REQ-2 (Throughput Capacity): Maintain queue depth and execution speed to guarantee completion of 500 jobs/hour (~8.33 jobs/min).",
    "REQ-3 (Atomic Handoff): Queue dequeue and rate-token consumption must be atomic per job execution.",
    "REQ-4 (Retry Rate Budgeting): Any HTTP retry attempt must pass through the Rate Limiter Controller and consume a rate token."
  ],
  "tests": [
    "TEST-1 (Rate Ceiling Verification): Run 1000 jobs under maximum concurrency and verify outbound HTTP request rate never exceeds 100 req/min in any 60-second window.",
    "TEST-2 (Throughput Verification): Ingest 500 jobs over 1 hour and confirm all 500 jobs complete within 3600 seconds.",
    "TEST-3 (Retry Throttling Test): Mock upstream 500 errors to trigger retries; verify overall request count (initial + retries) stays strictly <= 100 req/min."
  ],
  "evidence_gaps": [],
  "decision_readiness": "READY"
}

## EVIDENCE
(none)

## AGENT STAGE2
{}