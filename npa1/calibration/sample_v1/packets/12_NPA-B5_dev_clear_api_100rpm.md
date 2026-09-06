# Packet 12 | NPA-B5 | dev_clear_api_100rpm | run 1
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
  "intended_outcome": "Complete 500 jobs/hour without exceeding 100 req/min.",
  "route": "TASK",
  "supra_goal": null,
  "model_gap": null,
  "competing_models": [],
  "probe": null,
  "success": "Execute all 500 independent 1-request jobs within 60 minutes while ensuring HTTP request rate does not exceed 100 requests per minute in any rolling 60-second window.",
  "parts": [
    {
      "component": "Job Queue",
      "local_contribution": "Buffers incoming jobs up to 500 jobs/hour and yields them sequentially without loss."
    },
    {
      "component": "Rate Limiter",
      "local_contribution": "Enforces rate restriction of at most 100 requests per minute."
    },
    {
      "component": "HTTP Dispatcher",
      "local_contribution": "Executes 1 HTTP request per authorized job and captures response."
    },
    {
      "component": "Interface: Queue to Rate Limiter",
      "local_contribution": "Delivers queued job to rate governor upon request without duplication."
    },
    {
      "component": "Interface: Rate Limiter to Dispatcher",
      "local_contribution": "Triggers dispatcher execution only when rate capacity token is granted."
    }
  ],
  "material_failures": [
    "Rate Limiter Failure: Dispatches more than 100 requests in a rolling 60-second window, violating upstream limit.",
    "Throughput Underflow: Over-throttling causes job completion rate to fall below 500 jobs/hour (~8.33 jobs/min).",
    "Queue Loss: Incoming jobs drop or fail to persist during queueing.",
    "Queue-RateLimiter Handoff Failure: Queue dequeues a job but fails to transfer it to rate governor, dropping the job.",
    "RateLimiter-Dispatcher Handoff Failure: Token is granted but dispatcher fails to send request, wasting token quota without completing job."
  ],
  "requirements": [
    "The Rate Limiter MUST strictly enforce an upper bound of 100 requests per rolling 60-second window.",
    "The Job Queue MUST store and reliably process all 500 jobs per hour without message drop or duplication.",
    "The system MUST maintain an average throughput of at least 8.34 requests/minute to complete 500 jobs within 1 hour.",
    "The Queue to Rate Limiter interface MUST ensure atomic handoff of jobs.",
    "The Rate Limiter to Dispatcher interface MUST consume token quota only upon successful request dispatch initialization."
  ],
  "tests": [
    "Rate Limit Boundary Test: Benchmark request emission and verify request count over any 60-second window is strictly <= 100.",
    "Hourly Workload Completion Test: Submit 500 jobs into queue and verify all 500 complete in <= 3600 seconds.",
    "Queue Durability & Single-Delivery Test: Enqueue 500 distinct jobs and verify exactly 500 dispatches occur.",
    "Interface Handoff Exception Test: Inject failure at dispatcher start and verify rate token is restored or unconsumed."
  ],
  "evidence_gaps": [],
  "decision_readiness": "READY"
}

## EVIDENCE
(none)

## AGENT STAGE2
{}